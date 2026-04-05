import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import sys
from pathlib import Path

# Adding the parent directory to path for environment variables
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from config import NEXT_ACTION_ID, COOKIE, DATA_FILE_PATH
data_path = DATA_FILE_PATH
    
# 1. LOAD THE SCRAPED HISTORY
# This is the long-format data with multiple weeks per cow
df_history = pd.read_csv(data_path)

# 2. FEATURE ENGINEERING (The "Multi-Week" Logic)
# Compress the history into a single row per cow, but keep the statistical 'flavor'
herd_features = df_history.groupby(['ID', 'Name', 'Tag']).agg({
    'Total Pts': ['mean', 'std', 'max', 'last'], # How they do on avg, volatility, peak, and most recent
    'Milk Volume': ['mean', 'last'],
    'FCE': ['mean', 'last'],
    'KGMS': ['mean', 'last'],
    'Move Pts': 'mean',
    'Resting': lambda x: (x == 'YES').sum()
})

# Flatten column names
herd_features.columns = [
    'Avg_Pts', 'Pts_Volatility', 'Peak_Pts', 'Recent_Pts',
    'Avg_Volume', 'Recent_Volume', 'Avg_FCE', 'Recent_FCE', 'Avg_KGMS', 'Recent_KGMS', 
    'Avg_Move_Pts', 'Rest_Count'
]
herd_features = herd_features.reset_index()

# 3. DEFINE THE MODEL INPUTS
# Model to predict the 'Recent_Pts' based on their historical averages and volatility
features = ['Avg_Pts', 'Pts_Volatility', 'Peak_Pts', 'Avg_Volume', 'Avg_FCE', 'Avg_KGMS', 'Avg_Move_Pts', 'Rest_Count']
X = herd_features[features].fillna(0) # Fill volatility for cows with only 1 week of data
y = herd_features['Recent_Pts']

# 4. TRAINING (The "Study" Phase)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# 5. EVALUATION
test_predictions = model.predict(X_test)
print("--- MODEL REPORT CARD ---")
print(f"Avg Error: {mean_absolute_error(y_test, test_predictions):.2f} pts")
print(f"Confidence (R2): {r2_score(y_test, test_predictions):.2f}")

# 6. RANKING & ROLE ASSIGNMENT
herd_features['Predicted_Next_Week_Pts'] = model.predict(X)
ranked_herd = herd_features.sort_values(by='Predicted_Next_Week_Pts', ascending=False).reset_index(drop=True)

def assign_role(row):
    if row.name < 5: return 'STARTER'
    if row.name == 5: return 'INSURANCE (6th Cow)'
    return 'BENCH'

ranked_herd['Role'] = ranked_herd.apply(assign_role, axis=1)

# 7. RESULTS
print("\n--- OPTIMIZED LINEUP ---")
cols_to_show = ['ID', 'Tag', 'Name', 'Role', 'Predicted_Next_Week_Pts', 'Avg_Pts', 'Pts_Volatility']
print(ranked_herd[cols_to_show].head(10))

##Analyse current squad
# current_herd_tags = [713, 534, 133, 390, 405, 626, 542, 132, 91, 233]
# for tag in current_herd_tags:
#     print(ranked_herd[ranked_herd['Tag'] == tag])