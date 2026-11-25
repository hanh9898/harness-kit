---
name: harness-project-to-spec
description: Draft a missing Harness spec from a settled project decision. Return a draft, not approval.
---

# Draft a Harness spec

Accept only a verified project binding and caller for this route. Require
`DesignReady`, the pinned decision and basis, affected and protected scope,
and acceptance checks. Return a blocker if the binding or inputs do not match.

Reuse a compatible spec. Otherwise draft the missing spec: problem, target
behavior, design choices, protected scope and checks at agreed interfaces.
Return material choices to the caller instead of changing the decision.

Return the draft inline unless a separate grant allows storing it at the
selected destination. Return the exact draft revision or reference and open
questions. The caller owns spec approval (H5); do not approve, publish,
invoke ticket drafting or apply changes.
