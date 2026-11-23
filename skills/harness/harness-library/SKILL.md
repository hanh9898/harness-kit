---
name: harness-library
description: Find and manage reusable harness-kit resources and personal customizations. Use to research gaps, save unfinished pieces, rules or workflows, revise, disable or restore library material, maintain history, archive or preview cleanup, or promote guidance for shared reuse. Applying resources to a project belongs to setup or evolve.
---

# Harness Library

Return attributable material or a durable library change. Library-only work ends with a handoff or save; consumer adoption belongs to setup/evolve. Ordinary product fixes and today's report remain ordinary work.

Resolve `<skill-dir>` to this file's real directory. The supplied catalog is at `<skill-dir>/../../../kit`. Read its [library operation contract](../../../kit/LIBRARY.md) before saving, editing, disabling or restoring. For origin updates, whole-parent replacement or requested carry-forward, follow [update and comparison](UPDATE.md). The existing `kit/scripts/kit` remains the focused catalog retrieval interface.

## 1. Find the material and its boundary

Use the requested result and existing context to identify the resource, owner and scope. Editing project A's reusable guidance stays project-scoped. Reuse across projects is personal scope. Reuse actual grants and suitable accessible stores; resolve only consequential ambiguity. Personal intent does not authorize writes to arbitrary user-wide locations or host installation. Keep shared distribution edits and consumer adoption outside a personal save.

Inspect relevant current records and known consumers within authorized scope. A known-use list is partial unless the inspected records establish otherwise. For resumed work, read live content, selection and their histories before retrying an uncertain write. Retain completed work.

Use an owner identity or responsible role supplied for the resource. Keep incidental host/account metadata out of saved resources and reports; it does not establish resource ownership or provenance.

Search existing personal/project stores and the supplied catalog before authoring. Use `library --store <selected-path> search <focused-term>` for pieces/rules and saved resources; use `kit list`, `kit list <group>`, `kit list rules <topic>` or `kit list P` to narrow other references. Retrieve selected IDs in full with `kit show <id>` or `library --store <path> show <id>`. Before using directly retrieved material, check `"<skill-dir>/../../../kit/scripts/library" --store <selected-path> selection <id> --source supplied` for catalog material, or use `--source saved` for saved material. Raw catalog retrieval retains excluded resources for inspection. Follow relevant source pointers instead of loading whole CSVs. This step ends with selected references, actual uncovered needs and the authorized destination, or the precise unresolved boundary.

For shared promotion, read [promotion guidance](PROMOTION.md) after retrieval and before effects. It handles overlap, private source details, shared authority, maintenance acceptance and proposal-only outcomes. Then use the authoring and save steps below for the selected result.

For history corrections, competing contributions, archival or cleanup, read [record maintenance](../../../kit/MAINTENANCE.md). Reuse native store operations; preview against actual ownership/references and preserve required history and evidence. Archive and deletion are separate effects.

## 2. Return or author

For retrieval, return identity, sources and certainty, applicability, dependencies, customization/origin and material gaps. State unknown ownership or provenance as unknown. Source-backed advice is not execution evidence. Stop here when the requested result is reusable-resource discovery. When the result is context reachable during a particular task, compose evolve's [context route](../harness-evolve/CONTEXT.md); material retrieval alone does not establish task use and requires no library edit.

For authoring, reuse adequate material. Research only unresolved factual gaps against primary sources, preserving exact references and stated/inferred/open/partial certainty. Load the current original `research` method when research is needed and `writing-for-agents` for agent-read guidance (including its skill mechanics when authoring a skill); preserve applicable interaction and completion requirements. Use relevant kit rules in construction and review, and the consumer's selected standards. English agent instructions use clear STE-inspired structure; Vietnamese uses structural habits only. No certification is implied.

If a required method/source is unavailable or restricted, report that dependency and continuation. Do not invent execution or silently replay a missing provider. Independent retrieval or an authorized incomplete save can continue with the gap visible. An authorized user override of a method's process remains explicit in evidence.

Support pieces, rules and workflows. Give a piece its use/inputs/results/dependencies, a rule its applicability/check, and a workflow its roles, inputs, outputs, handoffs and failure continuation as applicable. Missing sources, incomplete detail, uncertain references or untested use produce specific warnings and repair suggestions; they do not impose an approval lifecycle. A draft can be saved while dependent consumption remains blocked by its unmet conditions.

For exclusion or restoration, follow the selection operation in the library contract. Inspect source identity, live selection/history and current material. Reuse the grant for the requested library effect. Disable keeps the resource out of effective selection across supplied updates; restore requires an explicit request and selects current material. Preserve decision/provenance and independent content edits. Check known consumers without changing them. Use original writing-for-agents if authoring agent-read guidance; a selection-only operation can record that no authoring method applies.

## 3. Save and reconcile

Use an adequate existing store's safe operation if available. Otherwise use the local `library` operation contract. It stores content and history together with origin, decision references, evidence and continuation. Establish authority and recoverable rationale before effects under the selected logging standard; adequate existing references can satisfy this. The operation's JSON is a concrete machine consumer, not a new format requirement for other stores.

Save with the inspected revision, then read back the result. A conflict requires reconciliation against live state, not an automatic overwrite. Missing authority, ambiguous target or persistence failure blocks the invalid operation. Use only an authorized, qualified durable alternative; otherwise report the blocker and next action. Never call an uncertain write successful; inspect `show` and `history` before retry.

Finish with what was found/saved, the durable identity/path/revision, material warnings and repairs, known impacts and their coverage, and the next useful action. Name only methods/resources that materially determined the result and what was actually checked. Keep saved, applied and improved separate. Point future work to the authoritative store and its continuation; record remaining grants/providers/evidence without claiming readiness.

This route implements retrieval, research, add, edit, checked origin updates, durable exclusion, explicit restoration and scoped promotion through adequate native stores. Report a precise limitation for unavailable operations rather than treating a content edit as those effects.
