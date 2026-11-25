# Resolve only the route the step needs

Select a skill by the missing, verifiable output, not by title or trigger. Reuse a spec, ticket, reproduction or check that still matches the decision, revision and target. Use this reference for Setup's route catalog, Evolve's direct resolution and Implement's preflight.

| Route | Required output and exclusions |
| --- | --- |
| `to-spec` | Draft spec and open questions from a settled decision. No posting, labeling or target effects. |
| `to-tickets` | Draft slices and dependency graph from a valid spec. No posting, labeling or target effects. |
| `implement` | Execute one eligible ticket and return assignment, effects and evidence. No implicit Git, tracker or host side effects. |
| `implement-spec` | Coordinate a dependency graph when selected. Do not load a second coordinator over the same scope; a child may need the independent-ticket route in its own context. |

Use the project-scoped Harness override when the upstream method is user-only; do not call the upstream route on behalf of the user. Originals that are already agent-callable and compatible may be reused when verified. See [upstream invocation rules](https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/.agents/invocation.md). Host or admin restrictions still apply. Do not turn source reading into simulated invocation.

## Evidence and minimal handoff

Inspect the actual project, host, effective configuration/manifest and invocation policy in the intended caller context. On Devin, probe by **exact skill ID** using the native skill tool and target project context, not by absolute file path as the name. Cross-check the resolved source/path and immutable revision or file digest. Listing/search can miss project-local routes; neither an empty list nor a frontmatter flag proves a route's availability. Check for collisions and test a separate child context only if this workflow uses it. A same-name project override needs proof of precedence and no change outside scope.

Record only ID, source and override revision/digest, host, scope, caller context, expected output, selection/exclusion conditions, dependencies, allowed effects, status and evidence pointer. Status is `verified` for a current exact resolution with pertinent invocation/output evidence (use a no-write probe where possible); `ambiguous` for competing resolutions; `unavailable` for missing permission, route or evidence. Do not probe a route if the probe could write without authority. Keep independent work available when one route is blocked.

Setup can pass the relevant entry from its verified catalog. Evolve can inspect and verify the needed step itself if no catalog exists or an entry is stale; do not rerun Setup or register a provider as part of resolution. Implement invokes the exact verified ID in the assigned context, checks what actually loaded and validates its output before continuing. A manual or existing artifact can eliminate the need for a preparation route, not the need to verify execution. Do not fall back to an unverifiable, colliding or user-only route.

Record selected/reused/skipped step, ID/revision and reason, actual load status and result reference. Load only necessary instructions and data, not a bundle. Reuse a load only in the same context when scope/revision remains valid. Recheck affected routes after changes to host, configuration, scope, revision or authority. Do not infer token savings from number of calls.
