import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_excel(r"C:\Users\nansh\Documents\Python\fantasy_herd\round_1_model_data.xlsx", sheet_name="Sheet1")
df.columns = df.columns.str.strip()
#print(df.columns)

base_stats = ['BreedWorth', 'ProdWorth', 'MilkHistory', 'ProteinHistory']
dynamic_stats = ['FCE', 'Movement', 'Milk_Vol', 'KGMS', 'FCE_Pts', 'Move_Pts', 'Vol_Pts','KGMS_Pts']
features = base_stats + dynamic_stats
raw_features = base_stats + ['FCE', 'Movement', 'Milk_Vol', 'KGMS']
complex_features = base_stats + ['FCE_Pts', 'Move_Pts', 'Vol_Pts','KGMS_Pts']

df['Base_Stats'] = df[base_stats].apply(stats.zscore).sum(axis=1)
df['Dynamic_Performance'] = df[dynamic_stats].sum(axis=1)
df['Success_Score'] = df['Dynamic_Performance'] + df['Base_Stats']

# Input vars
x = df[complex_features]
# Target
y = df['Total_Pts']
# Split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
# Initialise and fit
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

# Forecasting
predictions = model.predict(x_test)
# Evaluation
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"Average Point Error: {mae:.2f}")
print(f"Model Explained Variance (R2): {r2:.2f}")

# Create a quick summary of what the model learned
importance = pd.Series(model.feature_importances_, index=complex_features).sort_values(ascending=False)

print("--- Feature Importance ---")
print(importance)