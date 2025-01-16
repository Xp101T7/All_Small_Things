import requests
import os

def create_github_issue(owner, repo):
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GitHub token not found in environment variables.")

    title = input("Enter the issue title: ")
    body = "Default Body"
    labels = ["default-label"]

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "title": title,
        "body": body,
        "labels": labels
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Issue created:", response.json().get("html_url"))
    else:
        print("Error creating issue:", response.text)

if __name__ == "__main__":
    create_github_issue("your-username", "your-repo")
