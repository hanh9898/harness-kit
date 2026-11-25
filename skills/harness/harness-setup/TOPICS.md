# Discovery topic checks

Use only the rows relevant to the current node. These checks are not sessions
or an interview script. The [node contract](DISCOVERY.md) governs questions,
Library calls and write boundaries.

| Topic | Inspect | Return |
| --- | --- | --- |
| Context isolation | Repo, host and shared/personal sources, load order and disclosure. Separate Harness and product issue spaces and Glossary/ADR areas. Context separation does not sandbox execution. | Boundaries, scoped inputs, tracker identities or unresolved destinations, and one routing check. |
| Autonomy | Existing grant/revocation routes, who may choose or approve exact effects, stop conditions and external or irreversible actions. | What can proceed, wait or stop, plus a negative gate check. |
| Standards & guidance | Repo/package guidance, CI, stack and consumers. Eliminate duplication; distinguish instruction precedence and enforced gates. | Authoritative entry point, effective precedence and an important check. |
| Model & roles | Real model/profile availability, output quality, budget, role handoff, scope and fallback. | Rationale per override and an actual consumer-session check. |
| Skills | Installed capabilities, actual calls, overlaps, inputs/outputs and callers; compare with a shorter instruction or a native tool. | Reuse/change/add/remove choice, trigger and check; scope and proposed execution overrides if needed. |
| Tools | Compare native, CLI, scripts and MCP against exact effect, minimum access, credentials, maintenance and independent verification. | An available tool/operation with a check or a specific blocker. |
| Hooks | Real host event and payload, overlapping CI/checks, blocking, latency, double trigger and rollback. | Positive and negative event cases and a stop/restore path, or no hook. |
| Workflow | Existing ownership, gaps, handoff contracts and a simple manual option; use real producer/consumer outputs. | Entry, owner, handoff, completion and a recovery check. |
| Automation | Concrete event/schedule need, manual baseline, overlap, deduplication, effects and failure owner. | Limited experiment, success/stop criteria and separate activation decision, or defer. |
| Software factory | Intake, claims, human controls, integration, costs, failure/recovery and off-limits targets. | Need or no need; small supervised test and evidence needed before wider use. |
| Runtime environment | Clean checkout bootstrap, dependencies, readiness/cleanup and actual file/network/secret/runner boundaries. Worktrees are not sandboxes. | Bootstrap/check steps, per-surface boundaries and unknowns. Never record secrets. |
| Verification | Existing product tests and meaningful Harness behaviors, expected/non-trigger cases when relevant, environment/evidence/cleanup. Do not add telemetry by default. | Distinct product and Harness checks; identify unrun cases and conditions. |
| Continuity | Authoritative records, ownership, readback in a fresh session, safe pointers and unresolved work. Do not rely on transcript. | Checkpoint location, access, next action and any continuity limit. |
