# Host adapters

Use this runbook to select an existing route, not a shared host API. Record the
actual caller, scope, exact ID, source, revision or digest, configuration
precedence, grantor and observed evidence in the
[route binding](M2-CONFIG.md#route-binding). Verify reads, supervised writes
and unattended writes separately. A tool named below may be unavailable to
the Bot or worker even when the owner can use it.

| Operation | Result boundary |
| --- | --- |
| `resolve(route, caller, scope)` | Return verified evidence or `Blocked`. An unresolved ID or source conflict is `ambiguous`; a missing primitive or caller access is `unavailable`. Name the exact missing requirement. |
| `inspect(ref)` | Return an observation or `Blocked`. Do not create a record, grant, registration, subscription or wake to satisfy a read. |
| `apply(effect, grant, expectedRevision)` | Submit only through the selected, qualified route and its target gate. Return `Applied`, `Denied` or `Unknown`. Never fall back to another route for the effect. |
| `reconcile(effectId, target)` | Inspect the original target at the same effect identity. Return an authoritative observation or keep `Unknown`; a timeout, failed read or absent record does not rule out late application. Follow [recovery](PERSISTENCE.md#3-continue-from-live-effects). |

## Capability map

Use only capabilities the role needs. A fallback is a separate, explicitly
selected and verified route, not an automatic retry. If its requirements also
fail, leave that capability off and continue independent work.

| Capability | Devin | Pi | Claude Code | Codex | Fallback when the required primitive is absent |
| --- | --- | --- | --- | --- | --- |
| `work-workers` | Boards via `devin_ticket_manage` or a pinned Harness tracker. Use an authorized dispatch or `devin_session_create`; inspect via `devin_session_events` or `devin_session_interact` when permitted. | Run a separate Pi session in an isolated worktree from the canonical ticket, or use a qualified runner. | Use a project agent or separate `claude` session; reopen the claim in the canonical tracker. | Run a Codex session in an approved worktree; use a child or runner only for the bound caller and capability. | One authorized operator holds the existing claim. No reassignment or background execution without proven exclusivity and a fence against the old worker. Do not create a default board. |
| `inbox` | Prefer native `bot-inbox` and `devin_inbox_manage` (**Needs you**) when the caller has access. Verify native PR settlement; send only on the approved route with separate send authority. | Opt in with `--skill`; ask in the TUI or use an existing qualified Inbox. | Opt in project-locally; ask in-session or use an existing qualified Inbox. Native confirmation gates only its own effect. | Opt in project-locally; ask in-session or use an existing qualified Inbox. Sandbox approval does not grant the target effect. | Leave an authorized inline draft or ask the user in-session. Without qualified Inbox and dedupe, do not create cards, schedule sends, promise auto-settlement or build a queue. See [Inbox HOST](../skills/bot/bot-inbox/HOST.md). |
| `memory` | Prefer native `bot-memory` and `memory_sync` when qualified. Verify the correct Bot's **Memory**, caller ACL and fresh-worker readback. | Opt in with `--skill`; read the scoped snapshot and resume manually from the approved checkpoint. | Opt in project-locally and read the approved store. Auto-memory is not an M2 store without qualified ACL and revision checks. | Opt in project-locally and open the approved store/checkpoint, not chat history or personal instructions. | Use session context or an authorized published snapshot. No background write or sync, cross-session promise or substitute store. See [Memory HOST](../skills/bot/bot-memory/HOST.md). |
| `domain-targets` | Use the bound integration, MCP, tracker, Git or CLI for the exact target. `devin_mcp_server_manage` installs an integration; it does not grant business operations. | Use a qualified project tool, MCP or CLI with access to the target. | Use the actual project's permitted tools, MCP or CLI under its policy. | Use a qualified tool, MCP or CLI under sandbox policy and target permissions. | Read only if the caller has access, or use an authorized operator if policy permits. Otherwise stop. Never fall back to the Product namespace or transfer secrets between hosts. |
| `wake` | Use the right Bot's **Automations** or authorized `devin_automation_manage`. Distinguish a Bot event, new worker and session reminder; verify trigger ID, state, occurrence key and checkpoint. | Use an external runner/scheduler only after qualifying the actual Pi caller. Package loading does not schedule work. | Qualify the caller, time window, CLI and non-interactive policy before using a runner or native trigger. Plugin loading is not a wake. | Qualify the automation or runner's runtime, sandbox and checkpoint. The plugin or app does not establish a wake route. | Keep the trigger off and resume manually from the approved checkpoint. Do not substitute polling or a session reminder. |
| `evidence-write-gate` | Use `git_view_pr` or `git_pr_checks` for readback; use `upload_attachment` only for the authorized audience. The target enforces the grant and fence (for example, Library SQLite). Commit, push, PR creation, merge and deploy need separate authority. | Keep evidence in the approved destination, not a volatile local path. Verify the revision and grant at the target. | Put evidence in an authorized PR/tracker. A tool prompt cannot replace the target's claim and revision checks. | Use the approved provider for PR/check evidence. A workspace sandbox does not verify the App or PR actor. | Select another authorized evidence ref if the recipient cannot reopen it, or report `Blocked`. Stop without a required fence; only use a separately qualified, supervised non-atomic route if policy permits and each send is confirmed. |

Use the [configured activation gates](M2-CONFIG.md#readiness-and-authority-gates)
for wake, target fencing and host changes. Package and local fixture checks do
not qualify native invocation, caller ACL, durability or unattended operation.

## Select one entry route

Use a full checkout pinned to an approved revision. Require authority for
registration before changing configuration. Invoke the exact ID in the
intended project and caller, check the returned source and its content, and
exercise the required behavior. A list or matching digest alone is not
enough. If source is hidden and verified exclusive loading cannot establish
it, report `ambiguous` and block the dependent step.

| Host | Harness entries | Optional Inbox and Memory |
| --- | --- | --- |
| Devin | Use the [project-local link quickstart](../README.md#devin--project-scope-v1-pilot). Invoke with `skill_invoke({"skill":"harness-setup"})` and the other three exact IDs. If Devin returns another project's source, open a target-only session and recheck. Qualify persistence with a fresh worker from the correct Bot. | Prefer the qualified native exact IDs. Do not register same-ID skills to shadow them. If native is unqualified, explicitly select a collision-free external or operator route per the HOST references, or keep the capability off. |
| Pi | Choose the [local package or one-session skill directory](../README.md#pi--package); invoke `/skill:harness-setup` and the other entries. Use `/reload` or a clean session after a source change. Choose trust explicitly; `pi list --approve` applies to that command only. Package loading does not apply a role. | Add `--skill "$KIT/skills/bot/<id>"` for each selected skill and invoke `/skill:<id>` after checking for conflicts. |
| Claude Code | Choose the [plugin route](../README.md#claude-code--plugin); use `claude --plugin-dir "$KIT"` for one session. For installation, verify marketplace and settings scope; user scope is the default. Reload or start a new session, then invoke `/harness-kit:harness-setup` and the other qualified names. | Link the selected directory to project-local `.claude/skills/<id>` and invoke `/<id>` only after checking for conflicts. |
| Codex | Choose the [plugin or project-local links](../README.md#codex--plugin), not both. In a new session, check `/plugins` for the plugin and `/skills` or the `$` picker, then invoke `$harness-setup` and the other entries. Verify runner discovery separately. | Link the selected directory to project-local `.agents/skills/<id>` and invoke `$<id>` only after checking for conflicts. |

For opt-in routes, follow [Inbox HOST](../skills/bot/bot-inbox/HOST.md) and
[Memory HOST](../skills/bot/bot-memory/HOST.md). Do not change default package
registration. Follow [Setup activation](../skills/harness/harness-setup/ACTIVATION.md)
for upstream prerequisites and invocation restrictions.
