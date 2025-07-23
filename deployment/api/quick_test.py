import requests
import json

# Test the prediction endpoint with minimal data
def test_prediction():
    url = "http://localhost:5000/predict"
    
    # Send empty dict - API will fill missing features with 0
    test_data = {}
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_prediction()