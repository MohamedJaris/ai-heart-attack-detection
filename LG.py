import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import pickle

# Paths
save_dir = r'C:\Jaris\College\Projects\AI Heart Attack Detection\path_to_save'
model_path = os.path.join(save_dir, 'heart_model.pkl')
scaler_path = os.path.join(save_dir, 'heart_scaler.pkl')

# Load dataset
file_path = r'C:\Jaris\College\Projects\AI Heart Attack Detection\heart_attack_dataset_1000.csv'
data = pd.read_csv(file_path)

# Show columns for verification (optional)
print("Available columns:", data.columns)

# Correct label column
label_column = 'Heart Attack (0=No, 1=Yes)'

# Features and labels
X = data.drop(label_column, axis=1)
y = data[label_column]

# Preprocessing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# Save model and scaler
os.makedirs(save_dir, exist_ok=True)
with open(model_path, 'wb') as f:
    pickle.dump(model, f)
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

print("✅ Heart attack model and scaler saved successfully.")

