import requests

def update_github_issue(token, owner, repo, issue_number, new_body):
    url = f"https://api.github.com/repos/owner/repo/issues/{issue_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "body": new_body
    }
    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Issue updated:", response.json()["html_url"])
    else:
        print("Error updating issue:", response.text)

if __name__ == "__main__":
    github_token = "YOUR_TOKEN_HERE"

    issue_number_to_update = input("Enter the issue number to update: ")

    body_text = """\
# Updated Issue Body

- Some details here
- More info here
"""

    update_github_issue(
        token=github_token,
        issue_number=issue_number_to_update,
        new_body=body_text
    )