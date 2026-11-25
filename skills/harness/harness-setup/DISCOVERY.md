# Discover by Harness tree node

Setup covers the whole tree in two passes. Evolve uses the same method for
relevant nodes without replaying onboarding. Use tree paths, not kit group or
skill IDs, as node identifiers. A node is one working context, not necessarily
a separate chat, delegate or user turn. Parent nodes set direction; children
make choices inside that direction. A topic checklist can serve several nodes
without opening another session.

| Branch in pass order | Domains (second pass) | Branch outcome |
| --- | --- | --- |
| 1. Environment & authority | Context isolation; Runtime environment; Execution authority | Work, host and control boundaries, autonomy, records and Harness Glossary/ADR area. |
| 2. Guidance & knowledge | Host entry points; Authoritative sources | Effective guidance and source ownership; instruction entry points do not enforce permissions. |
| 3. Capabilities | Skills; CLI; MCP; Other tools | Necessary capabilities; native tools and scripts belong under Other tools. |
| 4. Agent configuration & roles | Model profiles; Roles and subagents | Fit profiles to work and cost; workflows reference rather than own them. |
| 5. Coordination | Workflows; On demand | Combine capabilities and roles. Consider hooks, automation and a factory only when needed. |
| 6. Verification & feedback | Product verification; Harness verification; Evidence | Separate the criteria and evidence for each. |
| 7. State & continuation | Decision records; Handoff and resume | Preserve current choices, execution status and evidence through a readable source. |

The library serves all branches. Its groups classify resources, not nodes;
there are no required pairings. Use [topic checks](TOPICS.md) only for the
current question. Large eval, tracing, language servers and packaging are
extensions, not prerequisites.

## One discovery context per node

1. Read the node's question, parent direction, relevant settled choices and
   Glossary/ADR pointers, scope, active repo and host defaults. Keep drafts
   distinct. Use existing facts first; no runtime or incident data is needed
   for initial setup.
2. Use [grilling][grilling] and [domain-modeling][domain] directly via the
   approved host mechanism before asking the first question. Default to
   invoking both for every node. Reuse a load only in the same context and
   scope/revision if qualification shows unchanged outputs, isolation and
   node-specific questions. Never call the user-only `grill-with-docs`,
   `wayfinder` or `/handoff` on the user's behalf. If a required route is
   blocked, name it, point to the [upstream installation guide][install] and
   hold dependent discovery. Do not install, copy or emulate it.
3. Call `harness-library` internally with the current question, destination,
   store and scope. Search a few terms based on need, not translated node
   names. Open details and verify state only for viable candidates; reuse
   still-current scoped results. Compare the repo, effective host defaults
   and relevant enabled resources. A default or library entry is not an
   applied choice. An unreadable store or source is unknown, not empty.
4. Offer only applicable intent: if none of the three sources has a relevant
   component, **add** or **defer**; otherwise also consider **keep**,
   **improve**, **move layer or replace**, and **remove** on the exact piece
   and scope. Offer **connect** only once both endpoints are confirmed keep/add
   and their data, meaning, consumers and grants warrant it. Trace consumers
   and recovery before removal; removal from a project is not library disable.
5. Return node path, choice/options, reasoning, source references, missing
   facts, dependencies, scope and proposed checks. Send clear recommendations
   for batch design review; ask only material, actionable unanswered
   questions with a recommendation and consequence. Route answers back to
   the node and reopen only affected questions. Silence and missing authority
   are not deferral; record an approved deferral's reason and revisit trigger.

Use the agreed Harness context for Glossary terms and qualifying ADRs
(hard to reverse, surprising without context, real trade-off). Reuse adequate
documents and follow an existing glossary map. The decision record links the
ADR rather than repeating reasoning. Keep these artifacts as drafts until an
authorized implementation writes them to the selected Harness area. Product
Glossary/ADRs stay read-only unless a separately selected and authorized change
explicitly covers that destination.

[grilling]: https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/productivity/grilling/SKILL.md
[domain]: https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/domain-modeling/SKILL.md
[install]: https://github.com/mattpocock/skills/blob/abeeaf95660ba9e8b7c753eb38f441ca707a8823/.agents/install-block.md
