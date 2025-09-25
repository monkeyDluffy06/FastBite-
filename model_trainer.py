import pandas as pd
import numpy as np
import random
import joblib
import os

# --- GET THE DIRECTORY OF THE CURRENT SCRIPT ---
# This ensures the model file is saved in the same directory as the script.
basedir = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(basedir, 'time_predictor.pkl')


# --- 1. DEFINE MENU AND CONSTANTS ---
# CORRECTED: The item names are now comments, fixing the SyntaxError.
MENU_STATS = {
    # id: base_prep_time_minutes
    201: 18, # Chicken Biriyani
    202: 15, # Veg Biriyani
    203: 12, # Chicken Schezwan Fried Rice
    204: 10, # Veg Schezwan Fried Rice
    205: 5,  # Plain Dosa
    206: 7,  # Masala Dosa
    207: 14, # Chilly Chicken
    208: 12, # Panner Butter Masala
    209: 14, # Butter Chicken
    210: 10, # Chicken Kothu Parotta
    211: 3,  # Butter Naan
}
ITEM_IDS = list(MENU_STATS.keys())


# --- 2. GENERATE SYNTHETIC DATA ---
print("Step 1: Generating realistic training data...")
NUM_ORDERS = 1000
data = []
current_queue_length = 0

# Simulates 1000 past orders to create a dataset
for _ in range(NUM_ORDERS):
    num_items_in_order = random.randint(1, 5)
    item_ids = random.choices(ITEM_IDS, k=num_items_in_order)
    prep_times = [MENU_STATS[id] for id in item_ids]
    
    # Feature Engineering
    max_item_time = max(prep_times)
    avg_item_time = np.mean(prep_times)
    time_of_day = random.randint(9, 21) # 9 AM to 9 PM
    is_peak = 1 if time_of_day in [12, 13, 14, 19, 20] else 0
    queue_length_at_order = max(0, current_queue_length + random.randint(-2, 2))
    
    
    # Target Variable Calculation 

    # 1. Calculate the core cooking time based on the most complex item.
    base_time = max_item_time 

    # 2. Add time for each additional item in the order.
    complexity_impact = (num_items_in_order - 1) * (avg_item_time * 0.4) 

    # 3. The queue and peak hours are still important, but less dominant.
    queue_impact = queue_length_at_order * 0.5
    peak_hour_impact = 7 if is_peak else 0
    random_noise = random.uniform(-1, 1)

    final_prep_time = round(base_time + complexity_impact + queue_impact + peak_hour_impact + random_noise)

    
    data.append([
        num_items_in_order, max_item_time, avg_item_time, 
        time_of_day, is_peak, queue_length_at_order, final_prep_time
    ])
    current_queue_length = queue_length_at_order + 1

# Create a DataFrame
columns = [
    'num_items', 'max_item_time', 'avg_item_time', 'time_of_day',
    'is_peak', 'queue_length', 'prep_time_minutes'
]
df = pd.DataFrame(data, columns=columns)


# --- 3. TRAIN THE REGRESSION MODEL ---
print("Step 2: Training the Random Forest Regressor model...")
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

features = ['num_items', 'max_item_time', 'avg_item_time', 'time_of_day', 'is_peak', 'queue_length']
target = 'prep_time_minutes'

X = df[features]
y = df[target]

# We train on the entire dataset to capture all patterns for the final model
model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=3)
model.fit(X, y)


# --- 4. SAVE THE TRAINED MODEL ---
# The model is saved to a file using the absolute path
joblib.dump(model, MODEL_PATH)
print(f"✅ Step 3: Model saved successfully to '{MODEL_PATH}'")

