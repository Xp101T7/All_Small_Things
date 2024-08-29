import requests
import json

# Constants for API endpoint, API key, and the collection GUID
BASE_URL = "https://app.snapattack.com"
API_KEY = ""  # API key for authentication
COLLECTION_GUID = "0101267a-80df-43b8-894e-90363fc2a256"  # Unique identifier for the collection

def extract_values(filter_dict):
    """
    Recursively extract values from a nested dictionary structure where the 'field' is 'guid'.
    """
    for item in filter_dict['items']:
        if isinstance(item, dict):
            if 'field' in item and item['field'] == 'guid':
                return extract_values(item)
            return item.get('value', [])
    return []

def get_collection(base_url, api_key, collection_id):
    """
    Fetch collection data from the API using the collection GUID.
    """
    headers = {"X-API-Key": f"{api_key}"}
    try:
        response = requests.get(f"{base_url}/api/collections/{collection_id}/", headers=headers, timeout=90)
        
        if response.status_code == 204:
            print("No content available for this request (204 No Content).")
            return None
        
        if not response.text:
            print("Received an empty response.")
            return None
        
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except json.JSONDecodeError as json_error:
        print(f"Error decoding JSON: {json_error}")
        print(f"Response content: {response.text}")
        return None

def get_deployed(base_url, api_key):
    """
    Fetch data from the API related to deployed signatures.
    """
    headers = {"X-API-Key": f"{api_key}"}
    payload = json.dumps({
        "field": "deployment_integration_filter.success",
        "op": "not_equals",
        "value": "true"
    })
    try:
        response = requests.get(f"{base_url}/api/search/signatures/query/cached/v2/?page=0&size=5000", data=payload, headers=headers, timeout=90)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def get_supplemental_info(base_url, api_key, guid):
    """
    Fetch supplemental data for a specific GUID from the API.
    """
    headers = {"X-API-Key": f"{api_key}"}
    try:
        response = requests.get(f"{base_url}/api/search/signatures/query/cached/v2/{guid}/supplemental/", headers=headers, timeout=90)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching supplemental data for GUID {guid}: {e}")
        return None

def search_by_guid_list(base_url, api_key, guid_list):
    """
    Search the API using a list of GUIDs by passing them to the bas/script endpoint.
    """
    headers = {"X-API-Key": f"{api_key}", "Content-Type": "application/json"}
    
    # JSON payload as shown in your image, with the actual GUID list inserted
    payload = {
        "field": "sessions.analytics.guid",
        "op": "in",
        "value": guid_list  # Insert the list of GUIDs here
    }
    
    try:
        print("Sending payload to bas/script endpoint...")
        print(json.dumps(payload, indent=2))  # Print the payload for debugging
        
        # POST the JSON payload to the bas/script endpoint
        response = requests.post(f"{base_url}/api/search/bas/script/?page=0&size=1000", json=payload, headers=headers, timeout=90)
        
        print(f"Response Status Code: {response.status_code}")  # Print the status code
        print(f"Response Text: {response.text[:500]}")  # Print the first 500 characters of the response for debugging
        
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()  # Return the response as a JSON object
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data with GUID list: {e}")
        return None
    except json.JSONDecodeError as json_error:
        print(f"Error decoding JSON: {json_error}")
        print(f"Response content: {response.text}")
        return None

def main():
    """
    Main function to fetch and process collection and deployment data, then process each GUID
    through supplemental and bas/script endpoints, and combine all the information.
    """
    data = get_collection(BASE_URL, API_KEY, COLLECTION_GUID)  # Fetch collection data
    
    if data is None:
        print("Failed to retrieve collection data.")
        return
    
    if 'analytic_filter' not in data:
        print("No 'analytic_filter' found in the collection data.")
        return
    
    analytics = extract_values(data['analytic_filter'])  # Extract 'analytic_filter' GUIDs
    
    deployed = get_deployed(BASE_URL, API_KEY)  # Fetch deployed signatures data
    
    if deployed is None:
        print("Failed to retrieve deployed data.")
        return
    
    deployed_guids = [item.get('guid') for item in deployed.get('items', [])]  # Extract GUIDs from deployed data
    
    combined_data = {}  # Initialize a dictionary to store combined information
    
    # Search using the list of GUIDs
    bas_script_info = search_by_guid_list(BASE_URL, API_KEY, analytics)  # Pass the entire analytics list
    
    for guid in deployed_guids:
        supplemental_info = get_supplemental_info(BASE_URL, API_KEY, guid)  # Get supplemental info for each GUID
        if supplemental_info is None:
            continue
        
        name = supplemental_info.get('name', f"Unnamed-{guid}")  # Use the GUID as a fallback name
        
        # Combine the information
        combined_data[name] = {
            "guid": guid,
            "supplemental_info": supplemental_info,
            "bas_script_info": bas_script_info
        }
    
    # Print or save the combined data
    print(json.dumps(combined_data, indent=2))

if __name__ == "__main__":
    main()
