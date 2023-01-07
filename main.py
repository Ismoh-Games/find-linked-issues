import os
import re
import requests
import urllib.parse


class MissingEnvironmentVariable(Exception):
    pass


def main():
    """ Main function """

    # Get environment variables
    print("Fetching environment variables...")

    # token = os.environ['INPUT_TOKEN']
    # if not token:
    #     raise MissingEnvironmentVariable("`token` environment variable not found")

    try:
        repository = os.environ['INPUT_REPOSITORY']
    except KeyError:
        raise MissingEnvironmentVariable("`repository` environment variable not found")

    try:
        pull_request_number = os.environ['INPUT_PULL-REQUEST-NUMBER']
    except KeyError:
        raise MissingEnvironmentVariable("`pull-request-number` environment variable not found")

    try:
        pull_request_body = os.environ['INPUT_PULL-REQUEST-BODY']
    except KeyError:
        raise MissingEnvironmentVariable("`pull-request-body` environment variable not found")

    try:
        copy_issues_labels = os.environ['INPUT_COPY-ISSUES-LABELS']
    except KeyError:
        copy_issues_labels = False

    print("Environment variables fetched successfully")

    # Get pull request
    print("Finding issue numbers in pull requests body..")
    print(f"Pull request body: {pull_request_body}")
    pattern = re.compile(r"((.lose|.ix|.esolve)(\S*|\s*))(.|)#\d+")
    matches = re.findall(pattern, pull_request_body)
    matches2 = re.finditer(pattern, pull_request_body)
    print(f"Matches: {matches}")
    print(f"Matches2: {matches2}")
    if not matches:
        raise RuntimeError("No issue found in the body")

    issue_numbers = []
    for match in matches:
        length = len(match)
        index = match.index('#')
        issue_number = match[index:length - index]
        issue_numbers.append(issue_number)
    print(f"Issue numbers: {issue_numbers}")

    # Find issues with GitHub API
    print("Fetching issues...")
    url = 'https://api.github.com/search/issues?'
    params = {
        "is": "issue",
        "repo": repository,
        "linked": "pr",
        "": " ".join(str(i) for i in issue_numbers)
    }
    headers = {
        "Accept": "application/vnd.github+json"
    }
    url = url + urllib.parse.urlencode(params)
    print(f"Request url: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"is-pull-request-linked-to-issues=false >> $GITHUB_OUTPUT")
        raise RuntimeError(f"Error fetching issues: {response.text}")

    issues = response.json()

    print(f"Issues fetched successfully: {issues}")
    print(f"is-pull-request-linked-to-issues=true >> $GITHUB_OUTPUT")
    print(f"linked-issues={issues} >> $GITHUB_OUTPUT")


if __name__ == "__main__":
    main()
