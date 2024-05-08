import argparse
import json
from google.auth.transport import requests
from google.oauth2 import service_account
from common import chronicle_auth
from common import regions

CHRONICLE_API_BASE_URL = "https://backstory.googleapis.com"

def list_rules(http_session, page_size=0, page_token="", archive_state=""):
    url = f"{CHRONICLE_API_BASE_URL}/v2/detect/rules"
    params = {k: v for k, v in [("page_size", page_size), ("page_token", page_token), ("state", archive_state)] if v}
    
    try:
        response = http_session.request("GET", url, params=params)
        response.raise_for_status()
        rules_data = response.json()
        return rules_data.get("rules", []), rules_data.get("nextPageToken", "")
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return [], None
    except json.JSONDecodeError:
        print("Failed to decode JSON from response.")
        return [], None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List detection rules from the Chronicle API.")
    chronicle_auth.add_argument_credentials_file(parser)
    regions.add_argument_region(parser)
    parser.add_argument("-s", "--page_size", type=int, help="Maximum number of rules to return.")
    parser.add_argument("-t", "--page_token", type=str, help="Page token for pagination.")
    parser.add_argument("-as", "--archive_state", type=str, help="Archive state ('ACTIVE', 'ARCHIVED', 'ALL').")
    args = parser.parse_args()

    credentials = service_account.Credentials.from_service_account_file(
        args.credentials_file, scopes=['https://www.googleapis.com/auth/cloud-platform'])

    try:
        session = requests.AuthorizedSession(credentials)
        rules, next_page_token = list_rules(session, args.page_size, args.page_token, args.archive_state)
        print(json.dumps({"rules": rules, "nextPageToken": next_page_token}, indent=2))
    except Exception as e:
        print(f"Error during authentication or request: {e}")
