import requests

def update_github_issue(
    token,
    issue_number,
    new_body=None,
    new_assignees=None,
    new_milestone=None,
    new_labels=None
):
    """
    Updates an existing GitHub issue with new content, assignees, milestone, or labels.
    Reference: https://docs.github.com/en/rest/issues/issues#update-an-issue
    """
    url = f"https://api.github.com/repos/owner/repo/issues/{issue_number}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {}

    if new_body is not None:
        payload["body"] = new_body
    if new_assignees is not None:
        payload["assignees"] = new_assignees
    if new_milestone is not None:
        payload["milestone"] = new_milestone
    if new_labels is not None:
        payload["labels"] = new_labels

    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Issue updated:", response.json()["html_url"])
    else:
        print("Error updating issue:", response.text)

def add_comment_to_issue(
    token,
    issue_number,
    comment_body
):
    """
    Adds a comment to an existing GitHub issue.
    Reference: https://docs.github.com/en/rest/issues/comments#create-an-issue-comment
    """
    url = f"https://api.github.com/repos/owner/repo/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"body": comment_body}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Comment added:", response.json()["html_url"])
    else:
        print("Error adding comment:", response.text)

if __name__ == "__main__":
    github_token = "YOUR_TOKEN"

    issue_number_input = input("Enter the issue number to update: ")
    new_body_text = "Updated issue body here"
    assignees_list = ["octocat"]
    milestone_number = 1
    labels_list = ["bug", "help wanted"]

    # Update issue
    update_github_issue(
        token=github_token,
        issue_number=issue_number_input,
        new_body=new_body_text,
        new_assignees=assignees_list,
        new_milestone=milestone_number,
        new_labels=labels_list
    )

    # Add a comment
    comment_body = """\
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
    add_comment_to_issue(
        token=github_token,
        issue_number=issue_number_input,
        comment_body=comment_body
    )



