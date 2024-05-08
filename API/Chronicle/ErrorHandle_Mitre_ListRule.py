import argparse
import json
from google.auth.exceptions import RefreshError
from requests.exceptions import RequestException
from common import chronicle_auth
from common import regions

# Set the base URL for the Chronicle API
CHRONICLE_API_BASE_URL = "https://backstory.googleapis.com"

def list_rules(http_session, page_size=0, page_token="", archive_state=""):
    # Build the API URL
    url = f"{CHRONICLE_API_BASE_URL}/v2/detect/rules"
    # Construct parameters for pagination and filtering by state
    params = {k: v for k, v in [("page_size", page_size), ("page_token", page_token), ("state", archive_state)] if v}

    # Make an HTTP GET request to the Chronicle API
    response = http_session.request("GET", url, params=params)

    # Check for HTTP errors and raise an exception if found
    response.raise_for_status()

    # Parse the JSON response
    rules_data = response.json()

    # Extract and filter rule details for alert names and MITRE-related metadata
    filtered_rules = []
    for rule in rules_data.get("rules", []):
        alert_name = rule.get("ruleName")
        metadata = rule.get("metadata", {})
        mitre_metadata = {key: value for key, value in metadata.items() if key.startswith("MITRE_")}
        filtered_rules.append({
            "alertName": alert_name,
            "MITRE_metadata": mitre_metadata
        })

    # Return the filtered rules and the next page token
    return filtered_rules, rules_data.get("nextPageToken", "")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser()
    # Add arguments for credentials and region selection
    chronicle_auth.add_argument_credentials_file(parser)
    regions.add_argument_region(parser)
    # Add optional arguments for controlling the API query
    parser.add_argument("-s", "--page_size", type=int, help="maximum number of rules to return")
    parser.add_argument("-t", "--page_token", type=str, help="page token for pagination")
    parser.add_argument("-as", "--archive_state", type=str, help="archive state ('ACTIVE', 'ARCHIVED', 'ALL')")
    args = parser.parse_args()

    try:
        # Initialize HTTP session with provided credentials
        session = chronicle_auth.initialize_http_session(args.credentials_file)

        # Call the list_rules function with parsed arguments
        rules, next_page_token = list_rules(session, args.page_size, args.page_token, args.archive_state)

        # Output the filtered results to a JSON file
        with open('rules_output.json', 'w') as outfile:
            json.dump({
                "rules": rules,
                "nextPageToken": next_page_token
            }, outfile, indent=2)
        print("Output has been written to 'rules_output.json'")

    except RefreshError as e:
        print(f"Authentication error: {str(e)}")
        print("Please check your credentials and ensure they are valid.")

    except RequestException as e:
        print(f"Error occurred while making the API request: {str(e)}")
        print("Please check your network connection and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print("Please check the error details and try again.")