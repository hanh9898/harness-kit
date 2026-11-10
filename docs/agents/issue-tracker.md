# Issue tracker: GitHub

Specs and tickets for this repo are GitHub Issues in `hanh9898/harness-kit`. Use the `gh` CLI.

## Verify the target

Read the Git remote and run `gh repo view --json nameWithOwner` before creating the first issue in a session. The target must be `hanh9898/harness-kit`; resolve any mismatch before writing. File issues only in the user's repo.

## Operations

- Create: `gh issue create --title "..." --body-file <body-file>`. Write multiline content to a file before invoking the command.
- Read the complete issue and discussion: `gh issue view <number> --json number,title,body,labels,comments`.
- List: `gh issue list --state open --limit <N> --json number,title,labels`; filter with `--label` as needed and read relevant issues in full.
- Comment: `gh issue comment <number> --body-file <body-file>`.
- Change labels: `gh issue edit <number> --remove-label <old-label> --add-label <new-label>`; see the mapping in `triage-labels.md`.
- Close: post the result or explanation as a comment, then run `gh issue close <number>`. This preserves the explanation even if the issue was already closed.

## Child tickets and dependencies

Use native GitHub sub-issues and dependencies when available. If the CLI lacks the corresponding flags, use the GitHub API:

- Get a database ID: `gh api repos/hanh9898/harness-kit/issues/<number> --jq .id`.
- Add a child ticket: `gh api --method POST repos/hanh9898/harness-kit/issues/<parent>/sub_issues -F sub_issue_id=<child-database-id>`.
- Add a dependency: `gh api --method POST repos/hanh9898/harness-kit/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-database-id>`.

Database IDs differ from issue numbers and `node_id`. If these features are unavailable, put `Part of #<parent>` and `Blocked by: #<number>, #<number>` at the top of the child body and list child tickets in the parent. A ticket is unblocked only when every blocker is closed.

## When a skill requests publish or fetch

- Publish a spec or ticket: create a GitHub issue.
- Fetch a ticket: read the complete issue and comments using its number or URL.

## Pull requests as a triage surface

**PRs as a request surface: no.**

## Wayfinding operations

For `wayfinder`, the map is an issue labelled `wayfinder:map`; children are sub-issues or linked checklist entries as above. Ticket types use `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task`; create needed labels if absent.

- Frontier: open child tickets with no open blockers and no assignee; select in map order.
- Claim: assign the ticket to the person doing the work with `gh issue edit <number> --add-assignee @me` before starting.
- Resolve: comment with the answer, close the ticket, then update the map's Decisions-so-far with a brief conclusion and a link to the answer.
