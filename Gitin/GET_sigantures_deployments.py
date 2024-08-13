import requests

# Set your API key here
api_key = "YOUR_API_KEY"

# Set the SnapAttack API endpoint
url = "https://api.snapattack.com/api/signatures/deployments/"

# Define query parameters
params = {
    "include_sigma": True,           # Boolean parameter
    "last_updated": "1970-01-01T00:00:00",  # Date-time parameter
    "include_confidence": True,      # Boolean parameter
    "include_metadata": True,        # Boolean parameter
    "include_severity": True,        # Boolean parameter
    "include_validation": True       # Boolean parameter
}

# Define headers for the request
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Make the API call with query parameters
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print("Deployments data:")
    print(data)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    print(f"Error message: {response.text}")

#