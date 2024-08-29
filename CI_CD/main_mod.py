import requests
import json
import csv

# Constants for API endpoint, API key, and the collection GUID
BASE_URL = "https://app.snapattack.com"
API_KEY = ""  # API key for authentication
COLLECTION_GUID = "0101267a-80df-43b8-894e-90363fc2a256"  # Unique identifier for the collection

# ... [Previous functions remain unchanged] ...

def process_guids(guids, base_url, api_key, csv_filename):
    """
    Process a list of GUIDs through the supplemental data endpoint and write to CSV.
    
    Parameters:
        guids (list): List of GUIDs to process.
        base_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        csv_filename (str): Name of the CSV file to write the data to.
    """
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['GUID', 'Name', 'Description', 'DetectionType', 'ThreatScore']  # Add or modify fields as needed
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for guid in guids:
            supplemental_data = get_supplemental_data(base_url, api_key, guid)
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
    
    print(f"Supplemental data has been written to {csv_filename}")

def main():
    """
    Main function to fetch and process collection and deployment data, 
    get supplemental data for each GUID in two separate lists, and output to CSV files.
    """
    data = get_collection(BASE_URL, API_KEY, COLLECTION_GUID)
    
    if data is None:
        print("Failed to retrieve collection data.")
        return
    
    if 'analytic_filter' not in data:
        print("No 'analytic_filter' found in the collection data.")
        return
    
    analytics = extract_values(data['analytic_filter'])
    
    deployed = get_deployed(BASE_URL, API_KEY)
    
    if deployed is None:
        print("Failed to retrieve deployed data.")
        return
    
    deployed_guids = [item.get('guid') for item in deployed.get('items', [])]
    matches = [x for x in deployed_guids if x in analytics]
    diff = [x for x in analytics if x not in deployed_guids]
    
    # Process matches list
    process_guids(matches, BASE_URL, API_KEY, 'matches_supplemental_data.csv')
    
    # Process diff list
    process_guids(diff, BASE_URL, API_KEY, 'diff_supplemental_data.csv')

if __name__ == "__main__":
    main()