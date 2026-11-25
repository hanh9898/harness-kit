---
name: harness-project-implement
description: Apply one authorized Harness effect for an assigned ticket. Return its receipt or blocker without closing work.
---

# Apply one Harness effect

Accept only a current execution binding that matches readback and the assigned
caller. Require
`DispatchReady` from Harness Implement, the exact effect and target, current
assignment ID and epoch, expected target revision, applicable selection and
live effect grant (H8). Registration or a draft is not authority.

Use the caller's write boundary. Send only if the destination enforces the
current grant, assignment and revision, or policy permits a non-atomic send
and an authorized supervisor confirms this exact send in real time (H9).
Stop before sending if the route, prerequisites or authority cannot be
verified. Do not substitute a different effect.

Send at most once for the authorized attempt. Return `Blocked` before send
if a prerequisite is missing; otherwise report `Denied`, `Applied` or
`Unknown` as observed, with the effect ID and any receipt or reconciliation
reference. Do not replay an uncertain send, coordinate other tickets, merge
or close work. The caller reconciles `Unknown` and escalates unresolved
outcomes at H13. The caller verifies the result and owns closure at H17.
