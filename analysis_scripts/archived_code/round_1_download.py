import requests
import json
import time
import csv
from tqdm import tqdm

def get_herd_stats(start_id, end_id):
    # The URL of the site
    url = "https://fantasyherd.co.nz/results"
    
    # Your confirmed Next-Action ID
    next_action_id = "7f863ccfbbeba6d369450496051065a063c060de37"
    
    headers = {
        "Next-Action": next_action_id,
        "Content-Type": "text/plain;charset=UTF-8",
        "User-Agent": "Mozilla/5.0",# Mimics a real browser
    }

    master_stats = []
    
    print(f"🚀 Starting scan for IDs {start_id} to {end_id}...")

    for cow_id in tqdm(range(start_id, end_id + 1), desc="Scanning herd", unit="cow"):
        try:
            # Send the request just like the browser does
            # The payload must be a list containing the ID: [id]
            response = requests.post(url, headers=headers, data=json.dumps([cow_id]))
            
            if response.status_code == 200:
                # Handle the Next.js stream (splitting the '1:' prefix)
                lines = response.text.split('\n')
                data_line = next((line for line in lines if line.startswith('1:')), None)
                
                if data_line:
                    # Clean the line and parse JSON
                    json_data = json.loads(data_line[2:]) # Skip the '1:'
                    cow = json_data.get('data', {})
                    perf = cow.get('performanceSummaries', [{}])[0]
                    
                    master_stats.append({
                        "ID": cow.get('id'),
                        "Tag": cow.get('earTag'),
                        "Name": cow.get('name'),
                        "FCE": round(perf.get('feedConversionEfficiency', 0), 2),
                        "Movement": perf.get('movement'),
                        "Milk Vol": perf.get('totalMilkVolume'),
                        "KGMS": perf.get('kgms', 0),
                        'FCE Pts': perf.get('feedConversionEfficiencyPoint'),
                        'Move Pts': perf.get('movementPoint'),
                        'Milk Vol Pts': perf.get('totalMilkVolumePoint'),
                        'KGMS Pts': perf.get('kgmsPoint'),
                        'Total Pts': perf.get('totalPoints'),
                        "Resting": "YES" if perf.get('isResting') else "No"
                    })
            
            # Pause to avoid rate limiting
            time.sleep(0.1)

        except Exception as e:
            print(f"\nError on ID {cow_id}: {e}")

    # Save to CSV
    with open(r'C:\Users\nansh\Documents\Python\fantasy_herd\herd_stats.csv', 'w', newline='', encoding='utf-8') as f:
        # Make sure your fieldnames list matches the keys in master_stats.append
        fieldnames = master_stats[0].keys()
        dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(master_stats)

    print(f"\nFinished! Data saved to 'herd_statistics.csv'")

# Run the script
get_herd_stats(231, 232)