# Fantasy Herd Analysis
A collection of all the code used to run my drafting on Meadow Fresh's fantasy herd. 

## The updated weekly database is provided 
Current week's data is conveniently placed in data/herd_stats_all.csv. If you would like to run the data extraction yourself, feel free to run analysis_scripts/round_n_download.py as below.

# To Run Locally

## Setup
1. Create and activate a virtual environment
2. Install dependencies:
```bash
pip install -r requirements.txt
```

To download the most up to date data for yourself, open up [fantasyherd](https://fantasyherd.co.nz) and find your session's respective Next-Action-ID and Cookie and add these into config.py. **NEXT_ACTION_ID** and **COOKIE** can both can be found through: **inspect element -> network -> requests -> headers**. Choose **DATA_FILE_PATH** as an appropriate location to store your csv of cow data. 

I encourage the usage of .env wherever possible but for personal usage you can also just **replace the environment variable code in round_n_download.py** to your own variables. 

```bash
NEXT_ACTION_ID = "YOUR_NEXT_ACTION_ID"
COOKIE = "YOUR_COOKIE"
DATA_FILE_PATH = "LOCATION_FOR_DATA_FILE"
```

Then **once that is done**, you can download round-by-round the entire cow database so far. 
```bash
python analysis_scripts/round_n_download.py
```
 
## Other Code Snippets and Applications
The code in gemini_ml.py is a vibe-coded optimiser to pick the best herd based on the fantasy cow universse. This model selects based on the following features:
1. Total Pts
2. FCE
3. KGMS
4. Move Points
5. Resting (Binary yes/no)

For continuous data, the mean is used wherever possible and for total pts, the model also accounts for the volatility (std deviation) of a cow's ability to earn points. 

## Notes
In the Data/ folder you will find individual cow cards, my csv extracts from web-scrapes, and some basic EDA done in excel.

When going through the individual data points, note that the draft round is coded as game week 1, while the other rounds are indexed from 6. So for the scoring weeks, it looks like week 1: '6', week 2: '7' and so on. 
