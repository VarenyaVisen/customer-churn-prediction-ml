# Flask API for Customer Churn Prediction
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os

# Initialize Flask app
app = Flask(__name__)

# Load the trained model (adjust path as needed)
model_path = '../../models/best_model_logistic_regression.joblib'
try:
    model = joblib.load(model_path)
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Get expected features from the model or processed data
def get_expected_features():
    """Get the exact feature names the model expects"""
    try:
        # First try to get from model
        if hasattr(model, 'feature_names_in_'):
            return model.feature_names_in_.tolist()
        
        # Fallback: get from processed data
        df = pd.read_csv('../../data/processed/telco_churn_final_processed.csv')
        return [col for col in df.columns if col != 'Churn_binary']
    except Exception as e:
        print(f"Error getting features: {e}")
        return []

# Get expected features dynamically
EXPECTED_FEATURES = get_expected_features()

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "message": "Churn Prediction API is running",
        "status": "healthy",
        "model_loaded": model is not None,
        "expected_features_count": len(EXPECTED_FEATURES),
        "sample_features": EXPECTED_FEATURES[:5] if EXPECTED_FEATURES else []
    })

@app.route('/predict', methods=['POST'])
def predict_churn():
    """Main prediction endpoint"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Handle case where no data is provided - use defaults
        if not data:
            data = {}  # Empty dict will be filled with defaults
        
        # Check if model is loaded
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500
        
        # Convert to DataFrame with expected features
        input_df = pd.DataFrame([data])
        
        # Ensure all expected features are present
        for feature in EXPECTED_FEATURES:
            if feature not in input_df.columns:
                input_df[feature] = 0  # Default value for missing features
        
        # Select features in correct order
        input_df = input_df[EXPECTED_FEATURES]
        
        # Make prediction
        prediction_proba = model.predict_proba(input_df)[0]
        churn_probability = prediction_proba[1]  # Probability of churn
        
        # Business interpretation
        if churn_probability >= 0.7:
            risk_level = "High Risk"
            recommendation = "Immediate retention action needed"
        elif churn_probability >= 0.4:
            risk_level = "Medium Risk"
            recommendation = "Monitor closely and consider retention offer"
        else:
            risk_level = "Low Risk"
            recommendation = "Customer likely to stay"
        
        # Return prediction
        return jsonify({
            "churn_probability": round(float(churn_probability), 3),
            "risk_level": risk_level,
            "recommendation": recommendation,
            "prediction": "Will Churn" if churn_probability > 0.5 else "Will Stay"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """Batch prediction for multiple customers"""
    try:
        data = request.get_json()
        
        if not data or 'customers' not in data:
            return jsonify({"error": "No customer data provided"}), 400
        
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500
        
        customers = data['customers']
        results = []
        
        for i, customer in enumerate(customers):
            # Convert to DataFrame
            input_df = pd.DataFrame([customer])
            
            # Ensure all expected features are present
            for feature in EXPECTED_FEATURES:
                if feature not in input_df.columns:
                    input_df[feature] = 0
            
            # Select features in correct order
            input_df = input_df[EXPECTED_FEATURES]
            
            # Make prediction
            prediction_proba = model.predict_proba(input_df)[0]
            churn_probability = prediction_proba[1]
            
            results.append({
                "customer_id": i + 1,
                "churn_probability": round(float(churn_probability), 3),
                "prediction": "Will Churn" if churn_probability > 0.5 else "Will Stay"
            })
        
        return jsonify({"predictions": results})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("Starting Churn Prediction API...")
    print(f"Model loaded: {model is not None}")
    app.run(debug=False, host='0.0.0.0', port=port)