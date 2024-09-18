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

# Path to store the last lookback timestamp and logs
LOOKBACK_FILE = os.path.join(os.path.dirname(__file__), "lookback_timestamp.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "logs.json")  # File to store the logs

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

# Append logs to a file in JSON format
def save_logs(logs):
    # Check if the log file exists
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            existing_logs = json.load(f)
    else:
        existing_logs = []
    
    # Append the new logs to the existing logs
    existing_logs.append({
        "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'z',
        "logs": logs
    })
    
    # Write the updated logs back to the file
    with open(LOG_FILE, "w") as f:
        json.dump(existing_logs, f, indent=4)

# Main function to fetch logs and manage lookback
def retrieve_logs():
    # Load the last lookback timestamp
    last_lookback = load_last_lookback()

    # Fetch logs starting from the last lookback timestamp
    logs = fetch_logs(last_lookback)

    if logs:
        # Save logs to the file
        save_logs(logs)

    # Set the current time as the new lookback timestamp
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'z'
    
    # Save the new lookback timestamp for the next run
    save_lookback(current_time)

# Run the function
retrieve_logs()
