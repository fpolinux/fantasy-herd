import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load and Clean (As before)
df = pd.read_excel(r"C:\Users\nansh\Documents\Python\fantasy_herd\round_1_model_data.xlsx")
df.columns = df.columns.str.strip()

# 2. Scaling (Whole Herd)
static_cols = ['BreedWorth', 'ProdWorth', 'MilkHistory', 'ProteinHistory']
dynamic_cols = ['FCE_Pts', 'Move_Pts', 'Vol_Pts', 'KGMS_Pts']

df['Static_Potential'] = df[static_cols].apply(stats.zscore).sum(axis=1)
df['Dynamic_Performance'] = df[dynamic_cols].sum(axis=1)
df['Success_Score'] = df['Static_Potential'] + df['Dynamic_Performance']

# 3. Create the Insurance Flag (instead of -999)
# This keeps the math clean but identifies who is "Active"
df['Is_Fit'] = df['Move_Pts'] >= 3

# 4. Train-Test Split (300/200)
test_df = df.iloc[300:].copy()

# 5. THE FIX: Filter for Healthy Cows only for the Correlation/Plot
# We only want to see if we can rank healthy cows correctly
healthy_test = test_df[test_df['Is_Fit'] == True].copy()
sidelined_test = test_df[test_df['Is_Fit'] == False].copy()

corr, p_value = spearmanr(healthy_test['Success_Score'], healthy_test['Total_Pts'])

# 6. Improved Visualization
plt.figure(figsize=(10, 6))
sns.regplot(x='Success_Score', y='Total_Pts', data=healthy_test, 
            scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title(f"Healthy Cow Validation (Correlation: {corr:.2f})")
plt.xlabel("Theoretical Success Score")
plt.ylabel("Real-World Total Points")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# 7. Final Ranking Logic (Starting 5 + Insurance)
# We sort by Fitness first, then Score
final_rank = test_df.sort_values(by=['Is_Fit', 'Success_Score'], ascending=False)

print(f"Validated Ranking Accuracy: {corr:.2f}")
print("\n--- FINAL RECOMMENDED STARTING 5 ---")
print(final_rank.head(5)[['ID', 'Success_Score', 'Total_Pts', 'Is_Fit']])

print("\n--- NEXT IN LINE (6TH COW INSURANCE) ---")
print(final_rank.iloc[5:6][['ID', 'Success_Score', 'Total_Pts', 'Is_Fit']])