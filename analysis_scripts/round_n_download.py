import requests
import json
import time
import csv
from tqdm import tqdm

def get_complete_herd_history(start_id, end_id):
    url = "https://fantasyherd.co.nz/results"
    
    # 1. UPDATE THESE TWO FROM YOUR BROWSER
    next_action_id = "7f25cd7f274b40f654d530bda994dbbabc4b2c6c8d" 
    cookie = "_ga=GA1.1.1506113303.1770801640; accessToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjI0MzU1IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvc2lkIjoiMGZmZDc2YzUtYmNkMy00MjI3LThkYjEtN2U4NjA4NzRkNTg5IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZ2l2ZW5uYW1lIjoiTmFyYXlhbiIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3N1cm5hbWUiOiJTaGFzdHJpIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZW1haWxhZGRyZXNzIjoiZnBvZHVuZWRpbjgzQGdtYWlsLmNvbSIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL2NvdW50cnkiOiIxNTgiLCJpcGFkZHIiOiIxMzkuODAuMjM5LjY1IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiVXNlciIsImV4cCI6MTc3MzAwNzMxNywiaXNzIjoiZmFudGFzeS1oZXJkIiwiYXVkIjoiZmFudGFzeS1oZXJkLXVzZXJzIn0.M10QEWh10RAH-q_-cKVenfW43uTNaHCemeu3eUkKdA4; accessTokenExpiresAt=2026-03-08T22%3A01%3A57.368Z; refreshToken=xyZnm6bmLuMqis760xjJVOAbUH9Ct30CoibW2PeR%2Fs%2BNKsVJnPMecvqw%2BxIuqqmY%2FpUqsfXS%2Fct1iL3xj4qM2g%3D%3D; refreshTokenExpiresAt=2026-03-15T21%3A01%3A57.368Z; _ga_4VSVNMX6C1=GS2.1.s1773003707$o16$g1$t1773004455$j56$l0$h0; lastActivity=2026-03-08T21%3A17%3A08.569Z"

    headers = {
        "Next-Action": next_action_id,
        "Content-Type": "text/plain;charset=UTF-8",
        "User-Agent": "Mozilla/5.0",
        "Cookie" : cookie
    }

    master_stats = []

    print(f"🚀 Scanning history for IDs {start_id} to {end_id}...")

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
                            "KGMS": week.get('kgms', 0),
                            "FCE": round(week.get('feedConversionEfficiency', 0), 2) if week.get('feedConversionEfficiency') else 0,
                            "Move Pts": week.get('movementPoint'),
                            "FCE Pts": week.get('feedConversionEfficiencyPoint'),
                            "KGMS Pts": week.get('kgmsPoint'),
                            "Total Pts": week.get('totalPoints'),
                            "Resting": "YES" if week.get('isResting') else "No"
                        })
            
            time.sleep(0.1) # Respect the server

        except Exception as e:
            tqdm.write(f"❌ Error on ID {cow_id}: {e}")

    # 3. SAVE TO CSV
    if master_stats:
        with open(r'C:\Users\nansh\Documents\Python\fantasy_herd\herd_stats_all.csv', 'w', newline='', encoding='utf-8') as f:
            # Dynamically get headers from the first entry
            fieldnames = master_stats[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(master_stats)
        print(f"\n✅ Success! Saved {len(master_stats)} rows to 'complete_herd_history.csv'")
    else:
        print("\n⚠️ No data collected. Check your Next-Action ID and Cookie.")

# Run for your full range
get_complete_herd_history(231, 731)