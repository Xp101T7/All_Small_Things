import requests
import json
from datetime import datetime, timedelta
import os

# API endpoint and headers
url = "https://app.snapattack.com/api/org/audit/"
api_key = "your_api_key_here"  # Replace with your actual API key
headers = {
    "accept": "application/json",
    "X-API-KEY": api_key,
    "Content-Type": "application/json"
}

# Path to store the last lookback timestamp (uses Windows path format)
LOOKBACK_FILE = os.path.join(os.path.dirname(__file__), "lookback_timestamp.json")

# Function to fetch logs based on the lookback timestamp
def fetch_logs(lookback):
    data = {
        "lookback": lookback
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Logs retrieved successfully.")
        return response.json()  # Return logs data if needed
    else:
        print(f"Error: {response.status_code}")
        return None

# Load the last lookback timestamp from a JSON file
def load_last_lookback():
    if os.path.exists(LOOKBACK_FILE):
        with open(LOOKBACK_FILE, "r") as f:
            data = json.load(f)
            return data.get("lookback")
    else:
        # If the file doesn't exist, return a time 10 minutes ago from now
        return (datetime.utcnow() - timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'z'

# Save the new lookback timestamp to a JSON file
def save_lookback(lookback):
    with open(LOOKBACK_FILE, "w") as f:
        json.dump({"lookback": lookback}, f)

# Main function to fetch logs and manage lookback
def retrieve_logs():
    # Load the last lookback timestamp
    last_lookback = load_last_lookback()

    # Fetch logs starting from the last lookback timestamp
    logs = fetch_logs(last_lookback)

    # Process logs as needed (e.g., save, analyze, etc.)
    
    # Set the current time as the new lookback timestamp
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'z'
    
    # Save the new lookback timestamp for the next run
    save_lookback(current_time)

# Run the function
retrieve_logs()
