import requests

def create_github_issue():
    token = "YOUR_PERSONAL_ACCESS_TOKEN"
    owner = "YOUR_USERNAME"
    repo = "YOUR_REPO"

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
    create_github_issue()
