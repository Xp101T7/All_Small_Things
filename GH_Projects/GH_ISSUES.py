import requests

def create_github_issue(
    title,
    body,
    token,
    owner,
    repo,
    assignees=None,
    milestone=None,
    labels=None
):
    """
    Create a new GitHub issue on the specified repository.

    :param title: The title of the issue.
    :param body: The body/content of the issue (Markdown supported).
    :param token: Your GitHub Personal Access Token.
    :param owner: The owner (username or organization) of the repo.
    :param repo: The name of the repository.
    :param assignees: Optional list of GitHub usernames to assign to the issue.
    :param milestone: Optional integer representing the milestone number.
    :param labels: Optional list of label names.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "title": title,
        "body": body
    }
    if assignees is not None:
        payload["assignees"] = assignees
    if milestone is not None:
        payload["milestone"] = milestone
    if labels is not None:
        payload["labels"] = labels

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Issue created:", response.json()["html_url"])
    else:
        print("Error creating issue:", response.text)


# Example usage in a Jupyter cell:
if __name__ == "__main__":
    # Prompt user for the issue title
    issue_title = input("Enter the issue title: ")

    body_text = """\
# Bug Report

I found a bug in our application:

- **Steps to reproduce**:
  1. Step one
  2. Step two

- **Expected behavior**:
  The app should not crash.

- **Additional context**:
  This includes environment info, logs, etc.
"""

    github_token = "YOUR_TOKEN_HERE"
    repo_owner = "owner"
    repo_name = "repo"
    assignees_list = ["octocat"]
    milestone_number = 1
    labels_list = ["bug"]

    create_github_issue(
        title=issue_title,
        body=body_text,
        token=github_token,
        owner=repo_owner,
        repo=repo_name,
        assignees=assignees_list,
        milestone=milestone_number,
        labels=labels_list
    )
