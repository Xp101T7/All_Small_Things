import requests
import json
from typing import List, Dict, Any

BASE_URL = "https://app.snapattack.com"
API_KEY = ""  # Replace with your actual API key
COLLECTION_GUID = "0101267a-80df-43b8-894e-90363fc2a256"

def api_request(endpoint: str, method: str = "GET", data: Dict[str, Any] = None) -> Dict[str, Any]:
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=90)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=90)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error in API request to {url}: {e}")
        return {}

def get_collection_guids(collection_id: str) -> List[str]:
    data = api_request(f"/api/collections/{collection_id}/")
    if not data or 'analytic_filter' not in data:
        print("Failed to retrieve collection data or no 'analytic_filter' found.")
        return []
    
    def extract_guids(filter_dict):
        if isinstance(filter_dict, dict) and 'items' in filter_dict:
            for item in filter_dict['items']:
                if isinstance(item, dict):
                    if item.get('field') == 'guid':
                        return item.get('value', [])
                    elif 'items' in item:
                        result = extract_guids(item)
                        if result:
                            return result
        return []
    
    return extract_guids(data['analytic_filter'])

def get_deployed_guids() -> List[str]:
    payload = {
        "field": "deployment_integration_filter.success",
        "op": "not_equals",
        "value": "true"
    }
    data = api_request("/api/search/signatures/query/cached/v2/?page=0&size=5000", method="POST", data=payload)
    return [item['guid'] for item in data.get('items', []) if 'guid' in item]

def get_supplemental_info(guid: str) -> Dict[str, Any]:
    return api_request(f"/api/search/signatures/query/cached/v2/{guid}/supplemental/")

def get_bas_script_info(guids: List[str]) -> Dict[str, Any]:
    payload = {
        "field": "sessions.analytics.guid",
        "op": "in",
        "value": guids
    }
    return api_request("/api/search/bas/script/?page=0&size=1000", method="POST", data=payload)

def main():
    collection_guids = get_collection_guids(COLLECTION_GUID)
    deployed_guids = get_deployed_guids()
    
    # Find common GUIDs between collection and deployed
    common_guids = list(set(collection_guids) & set(deployed_guids))
    
    bas_script_info = get_bas_script_info(common_guids)
    
    combined_data = {}
    for guid in common_guids:
        supplemental_info = get_supplemental_info(guid)
        name = supplemental_info.get('name', f"Unnamed-{guid}")
        
        combined_data[name] = {
            "guid": guid,
            "supplemental_info": supplemental_info,
            "bas_script_info": next((item for item in bas_script_info.get('items', []) if item.get('guid') == guid), {})
        }
    
    # Output the combined data (you can modify this part to suit your needs)
    for name, data in combined_data.items():
        print(f"Name: {name}")
        print(f"GUID: {data['guid']}")
        print("Supplemental Info:", json.dumps(data['supplemental_info'], indent=2))
        print("BAS Script Info:", json.dumps(data['bas_script_info'], indent=2))
        print("-" * 50)

if __name__ == "__main__":
    main()