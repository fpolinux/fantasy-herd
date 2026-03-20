# Fantasy Herd Analysis
A collection of all the code used to run my drafting on Meadow Fresh's fantasy herd. 

## Setup
1. Create and activate a virtual environment
2. Install dependencies:
   pip install -r requirements.txt

## Run locally
To download the most up to date data for yourself. Open up fantasyherd.co.nz and find your session's respective Next-Action-ID and Cookie and add these into config.py. These both can be found through: inspect element -> network -> requests -> headers. The below code showcases storing these variables in a .env file but you can also just replace the RHS with your respective codes if running them for yourself.

```bash
NEXT_ACTION_ID = os.getenv("YOUR_NEXT_ACTION_ID") 
COOKIE = os.getenv("YOUR_COOKIE")
DATA_FILE_PATH = Path(os.getenv("LOCATION_FOR_DATA_FILE"))
```

Then once that is done, you can run to download the entire cow database so far. 
```bash
python data/run_n_download.py
```

## Features and Functions
Current week's data is conveniently placed in data/herd_stats_all.csv. If you would like to run the data extraction yourself, feel free to run analysis_scripts/round_n_download.py as above. 

The code in gemini_ml.py is a vibe-coded optimiser to pick the best herd based on the fantasy cow universse. This model selects based on the following features:
1. Total Pts
2. FCE
3. KGMS
4. Move Points
5. Resting

For continuous data, the mean is used wherever possible and for total pts, the model also accounts for the volatility (std deviation) of a cow's ability to earn points. 

## Notes
In the Data/ folder you will find individual cow cards, my csv extracts from web-scrapes, and some basic EDA done in excel.

When going through the individual data points, note that the draft round is coded as game week 1, while the other rounds are indexed from 6. So for the scoring weeks, it looks like week 1: '6', week 2: '7' and so on. 
