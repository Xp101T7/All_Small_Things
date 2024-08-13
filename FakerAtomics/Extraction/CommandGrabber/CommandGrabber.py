import requests
import yaml
from pathlib import Path

GITHUB_API_URL = "https://api.github.com"
REPO_OWNER = "redcanaryco"
REPO_NAME = "atomic-red-team"
ATOMICS_PATH = "atomics"
OUTPUT_FILE = "commands.json"

# GitHub API token for authentication
# This is optional but recommended if you encounter rate limits
GITHUB_TOKEN = None  # Replace with your token or set it to None

def get_github_headers():
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return headers

def get_repo_tree_recursive():
    url = f"{GITHUB_API_URL}/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/master?recursive=1"
    response = requests.get(url, headers=get_github_headers())
    response.raise_for_status()
    return response.json()["tree"]

def get_file_content(file_path):
    url = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/master/{file_path}"
    response = requests.get(url, headers=get_github_headers())
    response.raise_for_status()
    return response.text

def extract_commands_from_yaml(yaml_content):
    commands = []
    try:
        data = yaml.safe_load(yaml_content)
        for test in data.get("atomic_tests", []):
            if "executor" in test and "command" in test["executor"]:
                commands.append(test["executor"]["command"])
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
    return commands

def main():
    repo_tree = get_repo_tree_recursive()
    commands = []

    for item in repo_tree:
        if item["path"].startswith(ATOMICS_PATH) and item["path"].endswith(".yaml"):
            file_content = get_file_content(item["path"])
            commands.extend(extract_commands_from_yaml(file_content))

    with open(OUTPUT_FILE, "w") as output_file:
        json.dump(commands, output_file, indent=4)

    print(f"Extracted {len(commands)} commands and saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
