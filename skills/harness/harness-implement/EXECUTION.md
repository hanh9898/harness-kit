# Execution methods

Read after dispatch preflight. For the new workflow, require
[all three verified bindings](ROUTES.md#route-readiness) and resolve only the
execution override for the assigned ticket. Reuse current preparation evidence
without loading drafting routes again. A draft pair, coordinator or H4 grant
cannot stand in for an execution binding or authority.

Before sending, apply the [write boundary](WORK.md#write-boundary-and-reconciliation)
to the one proposed effect. Stop if the current route, assignment, revision,
applicable selection or grant cannot be verified. The override returns the
effect outcome and evidence; Harness Implement handles the result, and the
caller retains verification and closure.

Choose supplemental methods only when needed and confirm their own routes
and prerequisites.

| Work | Method and evidence |
| --- | --- |
| Fix a Harness bug | Reuse Evolve's reproduction or use `diagnosing-bugs` if bounded diagnosis is still needed. Demonstrate the original failure, minimal fix and passing regression. Use `tdd` when test-first is suitable and the public seam is confirmed. |
| Add or change behavior | Deliver a checkable slice. Use `tdd` for testable code and `writing-for-agents` for agent instructions, including its skill mechanics when authoring a skill. For configurations test a case that must activate and a case that must not, on the authorized consuming host. |
| Refactor without changing behavior | Record a baseline on the same public contract, then verify parity, including invocation and permissions. Use `codebase-design` for module/interface changes and `writing-for-agents` for reshaping instructions. Return behavior changes to the decision owner. |
| Integrate dependent tickets | Choose one of the other methods per ticket. Run in dependency order; parallelize only independent writes. Keep one owner per ticket and one integration owner. Verify the combined result on the same integrated revision before reporting it. |

Do not spawn agents or worktrees for a single ticket by default. For adoption, migration, replacement or removal, inspect each target independently. For performance work, Evolve owns the comparable baseline, quality floor and improvement judgment. A valid config or successful test invocation is not proof of activation in other consumers.

If using the upstream `code-review` method, require an established base, a nonempty diff at `HEAD`, the spec/criteria and the repo's standards. If it needs a tracker, the verified Harness destination must be explicit and any write separately authorized. Report standards conformance and spec conformance separately. If prerequisites are missing, report the upstream review as not run; do not commit or create a tracker to satisfy the method without authority.
