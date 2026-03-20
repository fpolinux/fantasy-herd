# Fantasy Herd Analysis
A collection of all the code used to run my drafting on Meadow Fresh's fantasy herd. 

## Setup
1. Create and activate a virtual environment
2. Install dependencies:
   pip install -r requirements.txt

## Run locally
python *\
Where * is the name of the analysis script you would like to run. 

## Features and Functions
Current week's data is conveniently placed in data/herd_stats_all.csv. If you would like to run the data extraction yourself, feel free to run analysis_scripts/round_n_download.py. 

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
