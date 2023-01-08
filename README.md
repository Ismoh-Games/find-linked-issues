# find-linked-issues *and more*

[![test `pull_request`](https://img.shields.io/github/actions/workflow/status/ismoh-games/find-linked-issues/test.yml?event=pull_request&label=test%20%60pull_request%60&style=for-the-badge)](https://github.com/Ismoh-Games/find-linked-issues/actions/workflows/test.yml)
[![test `pull_request_target`](https://img.shields.io/github/actions/workflow/status/ismoh-games/find-linked-issues/test.yml?event=pull_request_target&label=test%20%60pull_request_target%60&style=for-the-badge)](https://github.com/Ismoh-Games/find-linked-issues/actions/workflows/test.yml)

Marketplace action for finding the linked issues of a pull request. 

## Usage

Make use of GitHub's [keywords](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword) to link issues to a pull request by default.\
You can also do this [manually](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#manually-linking-a-pull-request-or-branch-to-an-issue-using-the-issue-sidebar) in the 'development' section of the pull request sidebar on the right.


### Inputs and outputs

| Name INPUTS                        | Description                                                          |                          | Default                                   |
|------------------------------------|----------------------------------------------------------------------|--------------------------|-------------------------------------------|
| `token`                            | The GitHub token to use for authentication.                          | **required**             | `${{ secrets.GITHUB_TOKEN }}`             |
| `repository`                       | The repository to use. If linked issue is on a different repository. | **required**             | `${{ github.repository }}`                |
| `pull-request-number`              | The pull request number to use. If pull requests are linked.         | **required**             | `${{ github.event.pull_request.number }}` |
| `pull-request-body`                | The pull request body to search for keywords like `Resolves #48`.    | **required**             | `${{ github.event.pull_request.body }}`   |
| `copy-issues-labels`               | Copy the labels of the linked issues to the pull request.            | optional                 | `false`                                   |
| **Name OUTPUTS**                   | **Description**                                                      | **Values**               | **Defaults**                              |
| `is-pull-request-linked-to-issues` | Whether the pull request is linked to issues or not.                 | `'True'` or `'False'`    | `'False'`                                 |
| `linked-issues`                    | List of issues that are linked to the pull request.                  | `[1, 2, 4, 82, 124]`     | `[]`                                      |   
| `pull-request-labels`              | List of labels assigned to this pull request.                        | `[bug, enhancement, ..]` | `[]`                                      |

Example workflow:

```yaml
    - name: Find linked issues
      id: find-linked-issues
      uses: Ismoh-Games/find-linked-issues@v0.0.1
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        repository: ${{ github.repository }}
        pull-request-number: ${{ github.event.pull_request.number }}
        pull-request-body: ${{ github.event.pull_request.body }}
        copy-issues-labels: true # optional
    
    # Use the output from the `find-linked-issues` step
    - name: Use the output
      run: |
        echo "is-pull-request-linked-to-issues: ${{ steps.find-linked-issues.outputs.is-pull-request-linked-to-issues }}"
        echo "linked-issues: ${{ steps.find-linked-issues.outputs.linked-issues }}"
        echo "pull-request-labels: ${{ steps.find-linked-issues.outputs.pull-request-labels }}"

    - name: Conditional step
      if: ${{ steps.find-linked-issues.outputs.is-pull-request-linked-to-issues == 'True' }}
      run: |
        echo "Pull request is linked to issues"

    - name: Another conditional step
      if: ${{ steps.find-linked-issues.outputs.is-pull-request-linked-to-issues == 'False' }}
      run: |
        exit 1
```

This action will only work on pull request events:
- [pull_request](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request)
    - opened
    - edited
    - synchronize
- [pull_request_target](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request_target)
    - opened
    - edited
    - synchronize

#### Further reading
There is a pattern used to find the linked issues in the pull request body.\
To get insights on how this pattern works, check out the [regex101.com](https://regex101.com/r/f60fNx/4)!\
When having problems with the pattern, you can test it out on [pythex.org](https://pythex.org).