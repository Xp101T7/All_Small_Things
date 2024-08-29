import requests
import json
import csv

# Constants for API endpoint, API key, and the collection GUID
BASE_URL = "https://app.snapattack.com"
API_KEY = ""  # API key for authentication
COLLECTION_GUID = "0101267a-80df-43b8-894e-90363fc2a256"  # Unique identifier for the collection

# ... [Previous functions remain unchanged] ...

def get_supplemental_data(base_url, api_key, guid):
    """
    Fetch supplemental data for a specific GUID from the API.
    
    Parameters:
        base_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        guid (str): The GUID to fetch supplemental data for.
    
    Returns:
        dict or None: The JSON response from the API as a dictionary, or None if the request fails.
    """
    headers = {"X-API-Key": f"{api_key}"}
    try:
        response = requests.get(f"{base_url}/api/search/signatures/query/cached/v2/{guid}/supplemental", headers=headers, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching supplemental data for GUID {guid}: {e}")
        return None

def main():
    """
    Main function to fetch and process collection and deployment data, 
    get supplemental data for each GUID, and output to a CSV file.
    """
    data = get_collection(BASE_URL, API_KEY, COLLECTION_GUID)
    
    if data is None:
        print("Failed to retrieve collection data.")
        return
    
    if 'analytic_filter' not in data:
        print("No 'analytic_filter' found in the collection data.")
        return
    
    analytics = extract_values(data['analytic_filter'])
    attacks = extract_values(data['bsscript_filter'])
    threatevents = extract_values(data['sessions'])
    
    deployed = get_deployed(BASE_URL, API_KEY)
    
    if deployed is None:
        print("Failed to retrieve deployed data.")
        return
    
    deployed_guids = [item.get('guid') for item in deployed.get('items', [])]
    matches = [x for x in deployed_guids if x in analytics]
    diff = [x for x in analytics if x not in deployed_guids]
    
    # Combine all GUIDs
    all_guids = list(set(matches + diff))
    
    # Fetch supplemental data for each GUID and write to CSV
    with open('supplemental_data.csv', 'w', newline='') as csvfile:
        fieldnames = ['GUID', 'Name', 'Description', 'DetectionType', 'ThreatScore']  # Add or modify fields as needed
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for guid in all_guids:
            supplemental_data = get_supplemental_data(BASE_URL, API_KEY, guid)
            if supplemental_data:
                writer.writerow({
                    'GUID': guid,
                    'Name': supplemental_data.get('name', ''),
                    'Description': supplemental_data.get('description', ''),
                    'DetectionType': supplemental_data.get('detectionType', ''),
                    'ThreatScore': supplemental_data.get('threatScore', '')
                })
            else:
                writer.writerow({'GUID': guid, 'Name': 'Error fetching data'})
    
    print("Supplemental data has been written to supplemental_data.csv")

if __name__ == "__main__":
    main()