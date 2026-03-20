import pandas as pd
import numpy as np
from scipy import stats

# 1. Load and Clean
df = pd.read_excel(r"C:\Users\nansh\Documents\Python\fantasy_herd\round_1_model_data.xlsx")
df.columns = df.columns.str.strip()

# 2. Calculate the "Theoretical Success Statistic"
static_cols = ['BreedWorth', 'ProdWorth', 'MilkHistory', 'ProteinHistory']
dynamic_cols = ['FCE_Pts', 'Move_Pts', 'Vol_Pts', 'KGMS_Pts']

# Use the Z-score logic you've validated
df['Static_Potential'] = df[static_cols].apply(stats.zscore).sum(axis=1)
df['Dynamic_Performance'] = df[dynamic_cols].sum(axis=1)
df['Success_Score'] = df['Static_Potential'] + df['Dynamic_Performance']

# 3. Apply the Insurance Logic (Binary Filter)
# We keep the Move_Pts < 3 check, but as a "Fitness Flag"
df['Is_Fit'] = df['Move_Pts'] >= 3

# 4. Rank: Healthy Cows first, then by Score
# This ensures your 6th cow is the top of the 'backup' list if she's sick,
# or the next-in-line if she's healthy.
df_ranked = df
df_ranked = df.sort_values(by=['Is_Fit', 'Success_Score'], ascending=False)

# 5. Output the Roster
print("--- STARTING 5 ---")
print(df_ranked[df_ranked['Is_Fit']].head(5)[['ID', 'Success_Score', 'Move_Pts']])

print("\n--- 6TH COW INSURANCE ---")
# If the 6th cow is fit, she is your immediate backup
print(df_ranked[df_ranked['Is_Fit']].iloc[5:6][['ID', 'Success_Score', 'Move_Pts']])