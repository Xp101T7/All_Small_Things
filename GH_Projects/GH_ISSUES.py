import requests
import sys

def create_github_issue():
    url = "https://api.github.com/repos/owner/repo/issues"
    title = input("Enter the issue title: ")
    print("Enter the issue body (multi-line, markdown supported). Press Ctrl+D (or Ctrl+Z) when done:")
    body = sys.stdin.read()  # Read multi-line input from stdin

    headers = {
        "Authorization": "Bearer YOUR_TOKEN_HERE",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "title": title,
        "body": body,
        "assignees": ["octocat"],
        "milestone": 1,
        "labels": ["bug"]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Issue created:", response.json().get("html_url"))
    else:
        print("Error creating issue:", response.text)

if __name__ == "__main__":
    create_github_issue()
