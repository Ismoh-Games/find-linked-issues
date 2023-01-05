# find-linked-issues

[![Build Status]()]
[![Coverage Status]()]

Marketplace action for finding the linked issues of a pull request. 

## Usage

Make use of GitHub's [keywords](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword) to link issues to a pull request by default.\
You can also do this [manually](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue#manually-linking-a-pull-request-or-branch-to-an-issue-using-the-issue-sidebar) in the 'development' section of the pull request sidebar on the right.


### Inputs
| Name                  | Description                                                          |          | Default                                   |
|-----------------------|----------------------------------------------------------------------|----------|-------------------------------------------|
| `token`               | The GitHub token to use for authentication.                          | required | `${{ secrets.GITHUB_TOKEN }}`             |
| `repository`          | The repository to use. If linked issue is on a different repository. | optional | `${{ github.repository }}`                |
| `pull-request-number` | The pull request number to use. If pull requests are linked.         | optional | `${{ github.event.pull_request.number }}` |
| `copy-issues-labels`  | Copy the labels of the linked issues to the pull request.            | optional | `false`                                   |

Example workflow:

```yaml
    - name: Find linked issues
      id: find-linked-issues
      uses: Ismoh-Games/find-linked-issues@v0.0.1
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        repo: ${{ github.repository }} # optional
        pull-request-number: ${{ github.event.pull_request.number }} # optional
        copy-issues-labels: true # optional
```

This action will only work on pull request events:
- [pull_request](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request)
- [pull_request_target](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request_target)

### Output
| Name                               | Description                                          | Value                         |
|------------------------------------|------------------------------------------------------|-------------------------------|
| `is-pull-request-linked-to-issues` | Whether the pull request is linked to issues or not. | `true` or `false`             |
| `linked-issues`                    | List of issues that are linked to the pull request.  | `["1", "2", "4", "82", "12"]` |

#### Further reading
There is a pattern used to find the linked issues in the pull request body.\
To get insights on how this pattern works, check out the [regex101 example](https://regex101.com/r/f60fNx/3)!