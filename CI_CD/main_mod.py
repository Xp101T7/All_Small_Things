import requests
import json

# Constants for API endpoint, API key, and the collection GUID
BASE_URL = "https://app.snapattack.com"
API_KEY = ""  # API key for authentication
COLLECTION_GUID = "0101267a-80df-43b8-894e-90363fc2a256"  # Unique identifier for the collection

def api_request(endpoint, method="GET", params=None, data=None):
    """Generic function to make API requests"""
    headers = {"X-API-Key": API_KEY}
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=90)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in API request to {url}: {e}")
        return None

def extract_values(filter_dict):
    """
    Recursively extract values from a nested dictionary structure where the 'field' is 'guid'.
    """
    for item in filter_dict['items']:
        if isinstance(item, dict):  # Check if the item is a dictionary
            if 'field' in item and item['field'] == 'guid':  # Look for 'guid' field
                return extract_values(item)  # Recurse if 'guid' is found
            return item.get('value', [])  # Return the value if present
    return []

def get_collection(collection_id):
    """Fetch collection data from the API using the collection GUID."""
    return api_request(f"/api/collections/{collection_id}/")

def get_deployed():
    """Fetch data from the API related to deployed signatures."""
    payload = {
        "field": "deployment_integration_filter.success",
        "op": "not_equals",
        "value": "true"
    }
    return api_request("/api/search/signatures/query/cached/v2/?page=0&size=5000", method="POST", data=payload)

def get_signature_supplemental(guid):
    """Fetch supplemental data for a specific signature GUID."""
    return api_request(f"/api/search/signatures/query/cached/v2/{guid}/supplemental/")

def get_bas_scripts(guids):
    """Fetch BAS scripts for the given GUIDs."""
    payload = {
        "field": "sessions.analytics.guid",
        "op": "in",
        "value": guids
    }
    return api_request("/api/search/bas/script/?page=0&size=1000", method="POST", data=payload)

def main():
    # Fetch collection data
    collection_data = get_collection(COLLECTION_GUID)
    if not collection_data:
        print("Failed to retrieve collection data.")
        return

    # Print the collections list
    print("Collections List:")
    print(json.dumps(collection_data, indent=2))
    print("\n" + "="*50 + "\n")

    # Extract GUIDs from collection data
    analytics_guids = extract_values(collection_data['analytic_filter'])
    
    # Fetch deployed signatures data
    deployed_data = get_deployed()
    if not deployed_data:
        print("Failed to retrieve deployed data.")
        return

    # Extract GUIDs from deployed data
    deployed_guids = [item.get('guid') for item in deployed_data.get('items', [])]
    
    # Find matching GUIDs
    matching_guids = [guid for guid in analytics_guids if guid in deployed_guids]

    # Fetch BAS scripts for matching GUIDs
    bas_scripts = get_bas_scripts(matching_guids)
    if not bas_scripts:
        print("Failed to retrieve BAS scripts.")
        return

    # Create a dictionary of BAS scripts keyed by GUID
    bas_dict = {script['guid']: script for script in bas_scripts.get('items', [])}

    # Process matching GUIDs
    result_dict = {}
    for guid in matching_guids:
        supplemental_data = get_signature_supplemental(guid)
        if supplemental_data:
            name = supplemental_data.get('name', 'Unknown')
            result_dict[name] = {
                'guid': guid,
                'supplemental_data': supplemental_data,
                'bas_script': bas_dict.get(guid, {})
            }

    # Output the results
    print("Processed Results:")
    print(json.dumps(result_dict, indent=2))

if __name__ == "__main__":
    main()