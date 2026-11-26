# Discover by Harness tree node

Use the [proposal entry guard](../../../kit/PROPOSAL-ENTRY.md) before
discovery. A concrete node question from Setup is Direct. Setup owns the two
passes, decision map, checkpoints and synthesis; a topic returns input for
one node. Use tree paths as decision identities, not skill IDs or Library
groups. Evolve can reference the map without calling Setup's routes.

| Order | Exact route | Parent route | Tree path | Areas handled by this branch |
| --- | --- | --- | --- | --- |
| 1.1 | [`environment-discovery`](../../discovery/environment-discovery/SKILL.md) | — | Environment & authority | Context isolation; Runtime environment; Execution authority |
| 1.2 | [`guidance-discovery`](../../discovery/guidance-discovery/SKILL.md) | — | Guidance & knowledge | Host entry points; Authoritative sources |
| 1.3 | [`capabilities-discovery`](../../discovery/capabilities-discovery/SKILL.md) | — | Capabilities | CLI; MCP; Other tools |
| 1.4 | [`agent-role-discovery`](../../discovery/agent-role-discovery/SKILL.md) | — | Agent configuration & roles | Model profiles; Roles and subagents |
| 1.5 | [`coordination-discovery`](../../discovery/coordination-discovery/SKILL.md) | — | Coordination | On demand; Software Factory fit |
| 1.6 | [`verification-discovery`](../../discovery/verification-discovery/SKILL.md) | — | Verification & feedback | Product verification; Harness verification; Evidence |
| 1.7 | [`state-continuation-discovery`](../../discovery/state-continuation-discovery/SKILL.md) | — | State & continuation | Decision records; Handoff and resume |
| 2.1 | [`skill-discovery`](../../discovery/skill-discovery/SKILL.md) | `capabilities-discovery` | Capabilities / Skills | — |
| 2.2 | [`workflow-discovery`](../../discovery/workflow-discovery/SKILL.md) | `coordination-discovery` | Coordination / Workflows | — |
| 2.3 | [`hooks-discovery`](../../discovery/hooks-discovery/SKILL.md) | `coordination-discovery` | Coordination / On demand / Hooks | — |
| 2.4 | [`automation-discovery`](../../discovery/automation-discovery/SKILL.md) | `coordination-discovery` | Coordination / On demand / Automation | — |

Pass one visits all seven branches in order, with no child load. Areas in the
last column use their branch's route, not a separate skill ID. The topic labels
each material choice or open question with its tree path under that branch.
Setup records each result at that path for H2, even when it batches questions.
Review all seven before batching actionable questions, authority first.
Include clear recommendations in the synthesis.

Pass two opens all applicable children, one working context at a time. Take the
earliest eligible route in table order unless a recorded dependency requires another order. A deferred parent
skips its children; lack of direction or a blocked dependency holds only
affected nodes. Continue independent work. Checkpoint through the
[decision map](DECISION-MAP.md); do not checkpoint in a topic.

## Topic route and result

Before entering a topic, resolve its exact ID, pinned source and revision or
digest, current scope, authorized caller and host invocation policy.
`harness-setup` is the only internal caller. A permitted user invocation can
use the topic for inline discovery, not take over Setup's map. Topics are not default entries,
and Setup must not register all eleven topics as public commands to make them
reachable.

Choose one route mode for each topic and record it in the node outcome:

| Route mode | Use when | Required evidence |
| --- | --- | --- |
| `native-invocation` | The host can invoke the exact internal ID in this caller and project. | Exact ID, resolved Source, revision or digest, caller and invocation policy. |
| `pinned-instruction-read` | The topic is not registered and the host policy lets Setup read one exact file from the same pinned plugin checkout. | Exact file path, pinned revision or digest, caller and read result. |

`pinned-instruction-read` loads the topic instructions inside Setup's working
context. It is not a skill invocation, does not prove host registration, and
must not be reported as one. It is valid only for the exact internal topic in
the pinned distribution. Do not use another file, caller or installation as a
fallback. If neither route mode is available, or the route, wrong caller,
source or access is ambiguous, return a blocker and hold dependent discovery.

Then run the node in one working context:

1. Pass the node and question, parent direction, mode and scope, relevant
   static facts, Library pin and prior decision/Glossary/ADR refs. Use the
   same working context for both methods. [Verify the originals](ACTIVATION.md#verify-upstream-prerequisites),
   then call original [grilling][grilling] and [domain-modeling][domain]
   directly via the approved read-only route. If either cannot run without
   effects, return a blocker. Don't invoke user-only wrappers or copy the
   methods. Reuse a load only in the same context and scope/revision with
   evidence that reuse preserves the node-specific result.
2. Ask `harness-library` directly for the scoped need, not the whole
   catalog. Compare static repo facts, effective host defaults and relevant
   enabled Library resources at the pin; verify only viable candidates.
   Do not substitute a raw catalog or CLI. A default or Library entry is
   not an applied choice; an unreadable source is unknown, not empty.
3. Return findings and applicable intents with source refs, route mode,
   route evidence, scope, dependencies, proposed checks and any links or
   Glossary/ADR refs. An empty node gets add or defer. Otherwise consider
   keep, improve, move layer or replace, and remove. Link only after both
   endpoints are confirmed keep/add; record their actual tree paths. Trace
   consumers and recovery before removal; project removal is not Library
   disable. Return material unresolved H2 questions with a recommendation
   and consequence, explicit deferrals with reasons and revisit triggers,
   or blockers. Route answers to their originating node.

Use the Harness Glossary for terms and ADRs for qualifying choices. Reuse
adequate documents and follow an existing glossary map. Point to the ADR
instead of duplicating it in the decision record. Return new text inline;
only the authorized apply path may persist it. Product Glossary and ADRs
are read-only unless a separately authorized request covers that destination.

[grilling]: https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/productivity/grilling/SKILL.md
[domain]: https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/domain-modeling/SKILL.md
