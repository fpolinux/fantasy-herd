import requests
from tqdm import tqdm

start_id = 230
end_id = 730

for id in tqdm(range(start_id, end_id), desc="Downloading cows", unit="cow"):
    url = f"https://www.fantasyherd.co.nz/images/cows/card?id={id}"
    
    response = requests.get(url)

    if response.status_code == 200:
        with open(fr"C:\Users\nansh\Documents\Python\fantasy_herd\cow_{id}.png", "wb") as f:
            f.write(response.content)
