import requests
import json
import csv

# Constants for API endpoint, API key, and the collection GUID
BASE_URL = "https://app.snapattack.com"
API_KEY = ""  # API key for authentication
COLLECTION_GUID = "0101267a-80df-43b8-894e-90363fc2a256"  # Unique identifier for the collection

def extract_values(filter_dict):
    """
    Recursively extract values from a nested dictionary structure where the 'field' is 'guid'.
    
    Parameters:
        filter_dict (dict): Dictionary from which to extract values.
    
    Returns:
        list: List of values corresponding to the 'guid' field.
    """
    for item in filter_dict['items']:
        if isinstance(item, dict):  # Check if the item is a dictionary
            if 'field' in item and item['field'] == 'guid':  # Look for 'guid' field
                return extract_values(item)  # Recurse if 'guid' is found
            return item.get('value', [])  # Return the value if present
    return []

def get_collection(base_url, api_key, collection_id):
    """
    Fetch collection data from the API using the collection GUID.
    
    Parameters:
        base_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        collection_id (str): The GUID of the collection.
    
    Returns:
        dict or None: The JSON response from the API as a dictionary, or None if the request fails.
    """
    headers = {"X-API-Key": f"{api_key}"}  # Set up headers with API key
    try:
        # Send GET request to the API endpoint for the collection
        response = requests.get(f"{base_url}/api/collections/{collection_id}/", headers=headers, timeout=90)
        response.raise_for_status()  # Raise an exception for any non-200 status code
        return response.json()  # Return the JSON response as a dictionary
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, invalid API key)
        print(f"Error fetching data: {e}")
        return None  # Return None if the request fails

def get_deployed(base_url, api_key):
    """
    Fetch data from the API related to deployed signatures.
    
    Parameters:
        base_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
    
    Returns:
        dict or None: The JSON response from the API as a dictionary, or None if the request fails.
    """
    headers = {"X-API-Key": f"{api_key}"}  # Set up headers with API key
    payload = json.dumps({
        "field": "deployment_integration_filter.success",
        "op": "not_equals",
        "value": "true"
    })  # Payload to filter deployed signatures where 'success' is not equal to 'true'
    try:
        # Send GET request to the API endpoint for deployed signatures with the specified payload
        response = requests.get(f"{base_url}/api/search/signatures/query/cached/v2/?page=0&size=5000", data=payload, headers=headers, timeout=90)
        response.raise_for_status()  # Raise an exception for any non-200 status code
        return response.json()  # Return the JSON response as a dictionary
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, invalid API key)
        print(f"Error fetching data: {e}")
        return None  # Return None if the request fails

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