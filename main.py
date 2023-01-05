import os
import re
import requests


class MissingEnvironmentVariable(Exception):
    pass


def main():
    """ Main function """

    # Get environment variables
    print("Fetching environment variables...")

    token = os.environ.get("INPUT_TOKEN")
    if not token:
        raise MissingEnvironmentVariable("`token` environment variable not found")

    repository = os.environ.get("INPUT_REPOSITORY")
    if not repository:
        raise MissingEnvironmentVariable("`repository` environment variable not found")

    pull_request_number = os.environ.get("INPUT_PULL_REQUEST_NUMBER")
    if not pull_request_number:
        raise MissingEnvironmentVariable("`pull-request-number` environment variable not found")

    copy_issues_labels = os.environ.get("INPUT_COPY_ISSUES_LABELS")
    if not copy_issues_labels:
        raise MissingEnvironmentVariable("`copy-issues-labels` environment variable not found")

    body = os.environ.get("BODY")
    if not body:
        raise MissingEnvironmentVariable("BODY environment variable not found")

    print("Environment variables fetched successfully")

    # Get pull request
    print("Fetching pull request...")

    pattern = r'(.lose|.ix|.esolve)(\S*|\s*).#\d+'

    matches = re.findall(pattern, body, re.MULTILINE)
    print(f"Matches: {matches}")

    issue_numbers = re.search(pattern, body)
    if not issue_numbers:
        raise RuntimeError("No issue found in the body")

    print(f"Issue number: {issue_numbers}")

    # Find issues
    print("Fetching issues...")

    params = {
        "is": "issue",
        "repo": repository,
        "linked": "pr",
        "": " ".join(str(i) for i in issue_numbers)
    }
    response = requests.get("https://api.github.com/search/issues?q=", params=params)

    if response.status_code != 200:
        print(f"is-pull-request-linked-to-issues=false >> $GITHUB_OUTPUT")
        raise RuntimeError(f"Error fetching issues: {response.text}")

    issues = response.json()

    print(f"Issues fetched successfully: {issues}")
    print(f"is-pull-request-linked-to-issues=true >> $GITHUB_OUTPUT")
    print(f"linked-issues={issues} >> $GITHUB_OUTPUT")


if __name__ == "__main__":
    main()
