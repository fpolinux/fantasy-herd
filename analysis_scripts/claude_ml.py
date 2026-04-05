import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import sys
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from config import NEXT_ACTION_ID, COOKIE, DATA_FILE_PATH

# ── 1. LOAD ───────────────────────────────────────────────────────────────────
df_full = pd.read_csv(DATA_FILE_PATH)
df_full = df_full.sort_values(['ID', 'Week']).reset_index(drop=True)

last_week = df_full['Week'].max()
df_train  = df_full[df_full['Week'] < last_week]   # features built from these
df_target = df_full[df_full['Week'] == last_week]   # what we're trying to predict

# ── 2. FEATURE ENGINEERING ────────────────────────────────────────────────────
def calc_slope(series):
    """Linear trend — positive means improving, negative means declining."""
    if len(series) < 2:
        return 0.0
    weeks = np.arange(len(series))
    return np.polyfit(weeks, series, 1)[0]

herd_features = df_train.groupby(['ID', 'Name', 'Tag']).agg(
    Avg_Pts        = ('Total Pts',   'mean'),
    Pts_Volatility = ('Total Pts',   'std'),
    Peak_Pts       = ('Total Pts',   'max'),
    Median_Pts     = ('Total Pts',   'median'),
    Pts_Slope      = ('Total Pts',    calc_slope),  # trending up or down?
    Avg_Volume     = ('Milk Volume', 'mean'),
    Avg_FCE        = ('FCE',         'mean'),
    FCE_Slope      = ('FCE',          calc_slope),  # getting more efficient?
    Avg_KGMS       = ('KGMS',        'mean'),
    KGMS_Slope     = ('KGMS',         calc_slope),  # production trajectory
    Avg_Move_Pts   = ('Move Pts',    'mean'),
    Rest_Count     = ('Resting',     lambda x: (x == 'YES').sum()),
    Weeks_Recorded = ('Week',        'count'),       # how reliable are these stats?
).reset_index()

# Rookie flag — cows with few weeks have unreliable stats
herd_features['Is_Rookie'] = (herd_features['Weeks_Recorded'] < 3).astype(int)

# Merge in the true last-week score as the target
target = df_target[['ID', 'Total Pts']].rename(columns={'Total Pts': 'True_Pts'})
herd_features = herd_features.merge(target, on='ID', how='inner')

# ── 3. MODEL INPUTS ───────────────────────────────────────────────────────────
features = [
    'Avg_Pts', 'Pts_Volatility', 'Peak_Pts', 'Median_Pts', 'Pts_Slope',
    'Avg_Volume', 'Avg_FCE', 'FCE_Slope', 'Avg_KGMS', 'KGMS_Slope',
    'Avg_Move_Pts', 'Rest_Count', 'Is_Rookie'
]

X = herd_features[features].fillna(0)  # std=0 for single-week cows
y = herd_features['True_Pts']          # genuine future value — no leakage

# ── 4. TRAIN ──────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=500, random_state=42)
model.fit(X_train, y_train)

# ── 5. EVALUATE ───────────────────────────────────────────────────────────────
test_predictions = model.predict(X_test)

print("─── MODEL REPORT CARD ───────────────────────────────")
print(f"  Avg Error  : {mean_absolute_error(y_test, test_predictions):.2f} pts")
print(f"  R² Score   : {r2_score(y_test, test_predictions):.2f}")

importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
print("\n─── WHAT THE MODEL CARES ABOUT ──────────────────────")
print(importances.round(3).to_string())

# ── 6. RANK & ASSIGN ROLES ────────────────────────────────────────────────────
herd_features['Predicted_Pts'] = model.predict(X)
ranked = herd_features.sort_values('Predicted_Pts', ascending=False).reset_index(drop=True)
ranked['Rank'] = range(1, len(ranked) + 1)
ranked['Role'] = ranked['Rank'].apply(
    lambda r: 'STARTER' if r <= 5 else ('INSURANCE' if r == 6 else 'BENCH')
)

# ── 7. RESULTS ────────────────────────────────────────────────────────────────
cols = ['Rank', 'Tag', 'Name', 'Role', 'Predicted_Pts', 'True_Pts', 'Avg_Pts', 'Pts_Volatility', 'Pts_Slope']
print("\n─── OPTIMISED LINEUP (Top 10) ───────────────────────")
print(ranked[cols].head(10).to_string(index=False))

# ── 8. CURRENT SQUAD ANALYSIS (uncomment to use) ─────────────────────────────
# current_tags = [713, 534, 133, 390, 405, 626, 542, 132, 91, 233]
# print("\n─── CURRENT SQUAD ───────────────────────────────────")
# print(ranked[ranked['Tag'].isin(current_tags)][cols].to_string(index=False))