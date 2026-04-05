import requests
import json
import time
import csv
from tqdm import tqdm
import sys
from pathlib import Path

# Adding the parent directory to path for environment variables
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from config import NEXT_ACTION_ID, COOKIE, DATA_FILE_PATH

## Begin main code

def get_complete_herd_history(start_id, end_id):
    url = "https://fantasyherd.co.nz/results"
    
    # Update these directly from browser or through .env and config pipeline
    next_action_id = NEXT_ACTION_ID
    cookie = COOKIE
    data_path = DATA_FILE_PATH
    
    # Define headers for web-scrape
    headers = {
        "Next-Action": next_action_id,
        "Content-Type": "text/plain;charset=UTF-8",
        "User-Agent": "Mozilla/5.0",
        "Cookie" : cookie
    }

    master_stats = []

    print(f"Scanning history for IDs {start_id} to {end_id}...")

    for cow_id in tqdm(range(start_id, end_id + 1), desc="Fetching Cow History", unit="cow", dynamic_ncols=True):
        try:
            response = requests.post(url, headers=headers, data=json.dumps([cow_id]))
            
            if response.status_code == 200:
                lines = response.text.split('\n')
                data_line = next((line for line in lines if line.startswith('1:')), None)
                
                if data_line:
                    json_data = json.loads(data_line[2:])
                    cow = json_data.get('data', {})
                    perf_list = cow.get('performances', [])

                    # 2. NESTED LOOP: Create a row for every week found
                    for week in perf_list:
                        master_stats.append({
                            "ID": cow.get('id'),
                            "Tag": cow.get('earTag'),
                            "Name": cow.get('name'),
                            "Week": week.get('gameWeekId'),
                            "Milk Volume": week.get("totalMilkVolume"),
                            "KGMS": week.get('kgms', 0),
                            "FCE": round(week.get('feedConversionEfficiency', 0), 2) if week.get('feedConversionEfficiency') else 0,
                            "Volume Pts": week.get('totalMilkVolumePoint'),
                            "Move Pts": week.get('movementPoint'),
                            "FCE Pts": week.get('feedConversionEfficiencyPoint'),
                            "KGMS Pts": week.get('kgmsPoint'),
                            "Total Pts": week.get('totalPoints'),
                            "Resting": "YES" if week.get('isResting') else "No"
                        })
            
            time.sleep(0.1) # Respect the server

        except Exception as e:
            tqdm.write(f"Error on ID {cow_id}: {e}")

    # 3. SAVE TO CSV
    if master_stats:
        with open(data_path, 'w', newline='', encoding='utf-8') as f:
            # Dynamically get headers from the first entry
            fieldnames = master_stats[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(master_stats)
        print(f"Saved {len(master_stats)} rows to f'{data_path}.csv")
    else:
        print("\nNo data collected. Check your Next-Action ID and Cookie.")

# Run for your full range
get_complete_herd_history(231, 730)