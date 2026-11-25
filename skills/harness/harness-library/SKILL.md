---
name: harness-library
description: Find, verify or change reusable Harness resources in an authorized scope. Use for scoped lookup, selection and lineage, library drafts, updates, exclusion, restoration or promotion. Consumer adoption is separate.
---

# Harness Library

Accept the requested operation, focused question or exact identity, consumer,
store/scope and relevant authority or expected revision. Setup and Evolve call
this skill internally when needed; Implement calls it before applying a
selection. Do not start the caller's workflow or ask the user to invoke a second
skill. Return only the information needed for the current step.

| Operation | Read only what is needed |
| --- | --- |
| Locate/store scope, search, inspect or verify current selection | [Read and verify](READ.md) |
| Author, save, disable or explicitly restore | [Write and reconcile](WRITE.md) |
| Reconcile an identifier change | [Lineage](READ.md#lineage) first; use [write guard](WRITE.md#write-guard) only for permitted recording |
| Compare origins, replace a parent or carry forward a customization | [Origin updates](UPDATE.md); [write guard](WRITE.md#write-guard) for any mutation |
| Shared promotion | [Promotion](PROMOTION.md); [write guard](WRITE.md#write-guard) for any mutation |
| Record maintenance | [Maintenance](../../../kit/MAINTENANCE.md); enforce the [write gate](../harness-implement/WORK.md#write-boundary-and-reconciliation) before any effect |

Resolve the real skill directory to find the adjacent `kit/` and helpers.
Keep CLI calls inside this skill. Load focused references, candidate details
or history only as needed, never the whole catalog or library bundle. Reuse
results only while question, store, scope, authority and relevant data/revision
remain current; always recheck before application and read back after writes.

For a verified selection read, return the [v1 selection handoff](READ.md#selection-handoff),
not an adoption decision or a grant. For other reads, return focused findings
and blockers; for writes, also return readback evidence or `Unknown`.
Reading, saving, applying and executing are different effects. The consumer
owns adoption and its evidence; do not apply a selection or record adoption
in Library. An unverified store or identity blocks only dependent use.

If work must continue in another session, use the
[continuation handoff](../../../kit/PERSISTENCE.md#continuation-handoff) to
point to authorized Library records without changing the selection handoff.
