import requests
import json
import pandas as pd

def test_with_real_data():
    """Test with actual processed data sample"""
    try:
        # Load processed data
        df = pd.read_csv('../../data/processed/telco_churn_final_processed.csv')
        
        # Get first customer (excluding target)
        sample_customer = df.drop('Churn_binary', axis=1).iloc[0].to_dict()
        
        print("Testing with real customer data...")
        print(f"Features in sample: {len(sample_customer)}")
        
        # Test API
        url = "http://localhost:5000/predict"
        response = requests.post(url, json=sample_customer)
        
        if response.status_code == 200:
            print("✅ API Test Successful!")
            print(json.dumps(response.json(), indent=2))
        else:
            print("❌ API Test Failed:")
            print(response.json())
            
    except Exception as e:
        print(f"Error: {e}")

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get("http://localhost:5000/")
        print("Health Check:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Health check failed: {e}")

if __name__ == "__main__":
    print("Testing API...")
    test_health()
    print("\n" + "="*50 + "\n")
    test_with_real_data()