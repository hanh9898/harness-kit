# Resolve only the route the step needs

Select a skill by the missing, verifiable output, not by title or trigger. Reuse a spec, ticket, reproduction or check that still matches the decision, revision and target. Use this reference for Setup's route catalog, Evolve's direct resolution and Implement's preflight.

## Project override routes

| Original | Project override ID | Contract |
| --- | --- | --- |
| `to-spec` | `harness-project-to-spec` | [Draft a missing spec](../../overrides/harness-project-to-spec/SKILL.md). |
| `to-tickets` | `harness-project-to-tickets` | [Draft missing tickets from an approved spec](../../overrides/harness-project-to-tickets/SKILL.md). |
| `implement` | `harness-project-implement` | [Apply one authorized effect](../../overrides/harness-project-implement/SKILL.md). |

Use the verified project binding for the new Harness workflow. Do not
substitute an upstream method for a missing binding, invoke a user-only original
on behalf of the user, or count source inspection as invocation. Keep original
manual routes intact. `implement-spec` remains supplemental coordination for a
selected graph, not a substitute for the execution override. Do not load a
second coordinator for the same scope.

## Route readiness

Require all three distinct, unshadowed project bindings to be verified in
their intended caller contexts before reporting the new workflow execution-ready.
Missing binding, duplicate ID, wrong caller, wrong resolved source (even
with the same digest), revision mismatch or user-only policy blocks that
route. Do not use precedence to accept a shadow.

Two verified preparation bindings can return drafts under the existing
preparation gates. The pair alone is not execution-ready. Registration
readback alone does not qualify native routes. Even with all three routes
qualified, spec approval and the [dispatch gates](WORK.md#dispatch-and-integrate)
still apply.

## Prepare only missing artifacts

Use compatibility checks in [Prepare](WORK.md#prepare) before probing or invoking routes.

| Compatible artifacts | Drafting routes, in order |
| --- | --- |
| Spec and ticket | None |
| Spec only | `harness-project-to-tickets` |
| Ticket only | `harness-project-to-spec` |
| Neither | `harness-project-to-spec`, await spec approval, then `harness-project-to-tickets` |

Check approval on the exact spec revision and basis before resolving the ticket
drafting route. With a reusable ticket, keep it and check it against the new
spec and approval instead of drafting a replacement. Resolve only needed routes
at their step. Preparation routes cannot publish or apply effects. Accept a
user-invoked route's artifact only after checking authority and compatibility.

## Evidence and minimal handoff

Inspect the actual project, host, effective configuration and invocation
policy in the intended caller context. On Devin, probe by **exact skill ID**
with the native skill tool in the target project, not by absolute file path.
Check resolved source, immutable revision or file digest, caller and policy.
Neither a listing nor a frontmatter flag proves the effective binding.
Test a separate child context only if the workflow uses it.

Record ID, source and override revision/digest, host, scope, caller, effective
invocation policy, expected output, selection/exclusion conditions, dependencies,
allowed effects, status and evidence pointer. Use `verified` for a current
exact resolution with pertinent invocation/output evidence, `ambiguous` for
competing resolutions or `unavailable` for missing or mismatched evidence.
Do not probe a route if the probe could write without authority. Keep
independent work available when one route is blocked.

Setup can pass the relevant entry from its verified catalog. Evolve can inspect and verify the needed step itself if no catalog exists or an entry is stale; do not rerun Setup or register a provider as part of resolution. Implement invokes the exact verified ID in the assigned context, checks what actually loaded and validates its output before continuing. A manual or existing artifact can eliminate the need for a preparation route, not the need to verify execution. Do not fall back to an unverifiable, colliding or user-only route.

For the new workflow's `execute`, resolve `route_ref` against
`harness-project-implement` and the current binding in the assigned context.
Preparation evidence or a load in another context is not execution evidence.
Stop the dependent effect if the actual resolution differs or cannot be proved.

Record selected/reused/skipped step, ID/revision and reason, actual load status and result reference. Load only necessary instructions and data, not a bundle. Reuse a load only in the same context when scope/revision remains valid. Recheck affected routes after changes to host, configuration, scope, revision or authority. Do not infer token savings from number of calls.
