import joblib
import pandas as pd

# Load the model
model = joblib.load('../../models/best_model_logistic_regression.joblib')

# Check if model has feature names
if hasattr(model, 'feature_names_in_'):
    print("Model expects these features:")
    for i, feature in enumerate(model.feature_names_in_):
        print(f"{i+1:2d}. {feature}")
    print(f"\nTotal features: {len(model.feature_names_in_)}")
else:
    print("Model doesn't have feature names stored")

# Let's also check the processed data structure
try:
    df = pd.read_csv('../../data/processed/telco_churn_final_processed.csv')
    X_features = [col for col in df.columns if col != 'Churn_binary']
    print(f"\nProcessed data has {len(X_features)} features:")
    for i, feature in enumerate(X_features):
        print(f"{i+1:2d}. {feature}")
except Exception as e:
    print(f"Error loading processed data: {e}")