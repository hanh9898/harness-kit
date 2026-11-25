# Reconcile design writeback

Use at completion of an applicable interview, including a resumed accepted interview whose writeback may be incomplete. This is the Q44 completion check, integrated into the selected method's completion rather than a second interview or approval stage. Unrelated work does not acquire an interview requirement.

1. Read the accepted design and relevant live artifacts. Distinguish settled terms and choices from unresolved proposals. Reuse an actual shared-understanding confirmation; preserve any still-required interaction in the original interview method. An asserted method name or old summary does not establish current artifact contents.
2. Load the selected original domain-modeling method when domain terms or choices need reconciliation. Follow its context discovery and referenced formats. Compare each settled domain term with its actual context's glossary, using an existing glossary map when present. Resolve real contradictions using source evidence or the owner; repair missing accepted definitions within the grant. Capture terms when resolved, keeping implementation choices outside the glossary.
3. Apply the original ADR criteria to actual choices: hard to reverse, surprising without context, and a real trade-off. All three must hold. Reuse a matching adequate ADR; write missing material when authorized, or preserve the original method's offer when authority is unresolved. A cosmetic or easily reversible choice needs no ADR. Required consequential-choice logging can still apply separately under the selected standard; link adequate records rather than copying them.
4. Read back the resulting glossary, decision artifacts and affected deliverables. Verify accepted meanings, material alternatives/reasons, context placement, links and unchanged scope. A path in a report or a promise to write later is insufficient. Reuse checks already performed during the method; do not add a duplicate pass.
5. In the existing authorized current record, distinguish completed artifacts, choices that did not meet ADR criteria, missing work and the exact next trigger. Link the authoritative design and artifact locations. Follow [UPDATE.md](UPDATE.md) for pre-action capture, serialization and continuation. Without a save grant, return findings and the missing grant; do not claim writeback completion or create a shadow record.

**Done:** every settled term and qualifying choice is accounted for by inspected adequate artifacts or an explicit dependent blocker. A fresh continuation can locate those artifacts and retain completed work without duplicate entries, repeated questions or renewed approval for already-granted effects.

## Hand off the current change

Use this for a requested Harness change, whether or not it needed an interview.
Reopen the original decision ID/revision and basis, affected and protected scope,
acceptance and dependencies. Check the actual spec and ticket for compatibility
with those inputs, their links and the intended Harness target. Reuse compatible
references, including manually authored artifacts and legacy records that pass
the same checks. If both are compatible, skip preparation; reuse the canonical
ticket rather than publishing again. Do not convert obsolete or conflicting
references into authority, or silently downgrade an invalid v1 handoff to legacy.

If another session must pick up the change, use the
[continuation handoff](../../../kit/PERSISTENCE.md#continuation-handoff) to
point to the existing record and next step. Keep stage payloads separate.

At `DesignReady`, send [`prepare`](../../../kit/STAGE-CONTRACTS.md#setup-or-evolve--implement-prepare)
only for missing artifacts. Include only the needed route evidence and any
compatible `spec_ref` or canonical `ticket_ref`; if both artifacts are missing,
resolve `to-spec` before `to-tickets`. For example, when only the ticket is missing:

```json
{
  "version": 1,
  "operation": "prepare",
  "request_ref": "request:handoff-check",
  "scope_ref": "scope:harness",
  "decision_ref": "decision:handoff-check@2",
  "acceptance": ["A revoked claim cannot dispatch the change"],
  "dependency_refs": [],
  "needed_route_refs": ["route:ticket-draft@1"],
  "spec_ref": "spec:handoff-check@2"
}
```

Drafting does not publish, claim or authorize execution. Without permission to
persist the draft, return it inline as `DraftOnly`; do not invent a durable ref.
Send [`publish`](../../../kit/STAGE-CONTRACTS.md#setup-or-evolve--implement-publish)
separately only for an exact draft revision, satisfied prerequisites, a verified
Harness namespace and a live grant for that create or update. A missing, wrong,
ambiguous or shared namespace blocks publication; never substitute Product, an
orchestration board, or an unchosen local record. Small work may use a durable
local Harness record only when explicitly selected and authorized. Use the existing
[publish and readback gate](../harness-implement/WORK.md#publish-or-update) to
deduplicate by stable work ID and logical work, then read back the canonical
ticket. For example, a separately granted publication:

```json
{
  "version": 1,
  "operation": "publish",
  "draft_ref": "draft:handoff-check@1",
  "target": {
    "instance": "tracker:workspace",
    "namespace": "tracker:harness",
    "role": "harness"
  },
  "work_id": "work:handoff-check",
  "grant_ref": "authorization:publish-handoff-check@1"
}
```

If a prior send is `Unknown`, do not re-publish; reconcile at the original
destination using the existing `work_id` and [checkpoint](UPDATE.md#reconcile-an-uncertain-effect).
Keep payloads to one operation, reference existing records rather than copying
contents, and never pass live credentials. Shape validation is not authorization.
