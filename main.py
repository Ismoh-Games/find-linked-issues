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
    pattern = re.compile(r"(((.lose|.ix|.esolve)(\S*|\s*))(.|)\#\d+)", re.VERBOSE)
    matches = re.findall(pattern, pull_request_body)
    print(f"Matches: {matches}")
    if not matches:
        raise RuntimeError("No regex matches found in the body!")

    issue_numbers = []
    for match in matches:
        for entry in match:
            print(f"entry: {entry}")
            if "#" not in entry:
                print(f"Skipping {entry}")
            else:
                print(f"Found {entry}")
                index = entry.index("#")
                issue_number = entry[index + 1:]
                issue_numbers.append(issue_number)
                print(f"Found issue number: {issue_number}")
    if not issue_numbers:
        raise RuntimeError("No issue found in the regex matches!")
    print(f"Issue numbers: {issue_numbers}")

    # Find issues with GitHub API
    print("Fetching issues...")
    url = f"https://api.github.com/search/issues?q=repo:{repository} is:issue is:open linked:pr " \
          + " ".join(str(i) for i in issue_numbers)
    print(f"Request url: {url}")
    headers = {
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"is-pull-request-linked-to-issues=false >> $GITHUB_OUTPUT")
        raise RuntimeError(f"Error fetching issues: {response.text}")

    response_json = response.json()
    if response_json["total_count"] == 0:
        print(f"is-pull-request-linked-to-issues=false >> $GITHUB_OUTPUT")

        raise RuntimeError("Error fetching issues, 'total_response' = 0")
        
    if response_json["number"] not in issue_numbers:
        print(f"is-pull-request-linked-to-issues=false >> $GITHUB_OUTPUT")

        raise RuntimeError(f"Error fetching issues, didn't find issue number in response: {response_json}")
        
    else:
        print(f"Issues fetched successfully: {response_json['number']}")
        print(f"is-pull-request-linked-to-issues=true >> $GITHUB_OUTPUT")
        print(f"linked-issues={response_json['number']} >> $GITHUB_OUTPUT")


if __name__ == "__main__":
    main()
