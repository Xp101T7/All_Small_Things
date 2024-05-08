import argparse
import json
from google.auth.transport import requests
from common import chronicle_auth
from common import regions

CHRONICLE_API_BASE_URL = "https://backstory.googleapis.com"

def list_rules(http_session, page_size=0, page_token="", archive_state=""):
    url = f"{CHRONICLE_API_BASE_URL}/v2/detect/rules"
    params = {k: v for k, v in [("page_size", page_size), ("page_token", page_token), ("state", archive_state)] if v}
    response = http_session.request("GET", url, params=params)
    response.raise_for_status()
    rules_data = response.json()

    # Extracting alert names and MITRE related metadata
    filtered_rules = []
    for rule in rules_data.get("rules", []):
        alert_name = rule.get("ruleName")
        metadata = rule.get("metadata", {})
        mitre_metadata = {key: value for key, value in metadata.items() if key.startswith("MITRE_")}
        
        filtered_rules.append({
            "alertName": alert_name,
            "MITRE_metadata": mitre_metadata
        })
    return filtered_rules, rules_data.get("nextPageToken", "")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    chronicle_auth.add_argument_credentials_file(parser)
    regions.add_argument_region(parser)
    parser.add_argument("-s", "--page_size", type=int, help="maximum number of rules to return")
    parser.add_argument("-t", "--page_token", type=str, help="page token for pagination")
    parser.add_argument("-as", "--archive_state", type=str, help="archive state ('ACTIVE', 'ARCHIVED', 'ALL')")
    args = parser.parse_args()

    session = chronicle_auth.initialize_http_session(args.credentials_file)
    rules, next_page_token = list_rules(session, args.page_size, args.page_token, args.archive_state)
    
    # Writing results to a JSON file
    with open('rules_output.json', 'w') as outfile:
        json.dump({
            "rules": rules,
            "nextPageToken": next_page_token
        }, outfile, indent=2)

    print("Output has been written to 'rules_output.json'")
