import os
import re
import requests
import json
from github import Github


class MissingEnvironmentVariable(Exception):
    pass


def main():
    """ Main function """

    """ Get environment variables """
    print("Fetching environment variables...")

    token = os.environ['INPUT_TOKEN']
    if not token:
        raise MissingEnvironmentVariable("`token` environment variable not found")

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

    """ Get pull request """
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

    """ Find issues with GitHub API """
    print("Fetching issues...")
    url = "https://api.github.com/search/issues?q=" \
          + f"repo:{repository} is:issue is:open linked:pr pr:{pull_request_number}" \
          + " ".join(str(i) for i in issue_numbers)
    print(f"Request url: {url}")
    headers = {
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f"is-pull-request-linked-to-issues={False}", file=fh)
        raise RuntimeError(f"Error fetching issues: {json.dumps(response.json(), indent=2)}")

    response_json = response.json()
    print(json.dumps(response_json, indent=2))

    if response_json["total_count"] == 0:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f"is-pull-request-linked-to-issues={False}", file=fh)
        raise RuntimeError("Error fetching issues, 'total_response' = 0")

    response_json_issue_numbers = []
    response_json_issues_labels = []
    for item in response_json["items"]:
        print(f"item: {json.dumps(item, indent=2)}")
        print(f"item['number']: {item['number']}")
        if str(item["number"]) in issue_numbers:
            response_json_issue_numbers.append(item["number"])
            print(f"Found issue number: {item['number']}")
            if copy_issues_labels:
                for label in item["labels"]:
                    if label["name"] and label["name"] not in response_json_issues_labels:
                        response_json_issues_labels.append(label["name"])
                        print(f"Found and added issue label: {label['name']}")

    if not response_json_issue_numbers:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f"is-pull-request-linked-to-issues={False}", file=fh)
        raise RuntimeError(f"Error fetching issues, didn't find issue number in response: {response_json}")

    print(f"Issues fetched successfully: {response_json_issue_numbers}")
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f"is-pull-request-linked-to-issues={True}", file=fh)
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f"linked-issues={response_json_issue_numbers}", file=fh)

    """ Copy labels from issues to pull request """
    if copy_issues_labels:
        print("Copying labels from issues to pull request...")
        github = Github(token)
        if response_json_issues_labels:
            github.get_repo(repository).get_pull(int(pull_request_number)).add_to_labels(
                " ".join(str(label) for label in response_json_issues_labels))
            print("Labels copied successfully")


if __name__ == "__main__":
    main()
