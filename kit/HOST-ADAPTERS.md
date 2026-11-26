# Host adapters

Use this runbook to select an existing route, not a shared host API. An
`AdapterBinding` identifies the host, scope and actual caller. In its
[route binding](M2-CONFIG.md#route-binding), select at most one `BoundRoute`
per capability. Record its mode, status, target, exact ID, source, revision
or digest, and evidence. For writes, record grantor and configuration
precedence. Verify reads, supervised writes and unattended writes separately.
A tool the owner can use may still be unavailable to the Bot or worker.

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
| `work-workers` | Tasks board via `devin_ticket_manage` or a pinned Harness tracker. Human assignee is not session claim. Read back the canonical claim and ACL; a Bot-managed board is not necessarily private. Use authorized dispatch or `devin_session_create`; inspect via `devin_session_events` or `devin_session_interact`. | Run a separate Pi session in an isolated worktree from the canonical ticket, or use a qualified runner. | Use a project agent or separate `claude` session; reopen the claim in the canonical tracker. | Run a Codex session in an approved worktree; use a child or runner only for the bound caller and capability. | One authorized operator holds the existing claim. No reassignment or background execution without proven exclusivity and a fence against the old worker. Do not create a default board. |
| `inbox` | Prefer native `bot-inbox` and `devin_inbox_manage` (**Needs you**) when the caller has access. Verify native PR settlement; send only on the approved route with separate send authority. | Opt in with `--skill`; ask in the TUI or use an existing qualified Inbox. | Opt in project-locally; ask in-session or use an existing qualified Inbox. Native confirmation gates only its own effect. | Opt in project-locally; ask in-session or use an existing qualified Inbox. Sandbox approval does not grant the target effect. | Leave an authorized inline draft or ask the user in-session. Without qualified Inbox and dedupe, do not create cards, schedule sends, promise auto-settlement or build a queue. See [Inbox HOST](../skills/bot/bot-inbox/HOST.md). |
| `memory` | Prefer native `bot-memory` and `memory_sync` when qualified. Verify the correct Bot's **Memory**, caller ACL and fresh-worker readback. | Opt in with `--skill`; read the scoped snapshot and resume manually from the approved checkpoint. | Opt in project-locally and read the approved store. Auto-memory is not an M2 store without qualified ACL and revision checks. | Opt in project-locally and open the approved store/checkpoint, not chat history or personal instructions. | Use session context or an authorized published snapshot. No background write or sync, cross-session promise or substitute store. See [Memory HOST](../skills/bot/bot-memory/HOST.md). |
| `domain-targets` | Use the bound integration, MCP, tracker, Git or CLI for the exact target. `devin_mcp_server_manage` installs an integration; it does not grant business operations. | Use a qualified project tool, MCP or CLI with access to the target. | Use the actual project's permitted tools, MCP or CLI under its policy. | Use a qualified tool, MCP or CLI under sandbox policy and target permissions. | Read only if the caller has access, or use an authorized operator if policy permits. Otherwise stop. Never fall back to the Product namespace or transfer secrets between hosts. |
| `wake` | Use the right Bot's **Automations** or authorized `devin_automation_manage`. Distinguish a Bot event, new worker and session reminder; verify trigger ID, state, occurrence key and checkpoint. | Use an external runner/scheduler only after qualifying the actual Pi caller. Package loading does not schedule work. | Qualify the caller, time window, CLI and non-interactive policy before using a runner or native trigger. Plugin loading is not a wake. | Qualify the automation or runner's runtime, sandbox and checkpoint. The plugin or app does not establish a wake route. | Keep the trigger off and resume manually from the approved checkpoint. Do not substitute polling or a session reminder. |
| `evidence-write-gate` | Use `git_view_pr` or `git_pr_checks` for readback; use `upload_attachment` only for the authorized audience. The target enforces the grant and fence (for example, Library SQLite). Commit, push, PR creation, merge and deploy need separate authority. | Keep evidence in the approved destination, not a volatile local path. Verify the revision and grant at the target. | Put evidence in an authorized PR/tracker. A tool prompt cannot replace the target's claim and revision checks. | Use the approved provider for PR/check evidence. A workspace sandbox does not verify the App or PR actor. | Select another authorized evidence ref if the recipient cannot reopen it, or report `Blocked`. Stop without a required fence; only use a separately qualified, supervised non-atomic route if policy permits and each send is confirmed. |

Keep Tasks, Inbox and Git provider state separate. An Inbox reply or settled
card does not claim a task, grant an effect, close a PR or wake a Bot. Read
the canonical PR from its provider and use the Inbox of the bound Bot.

Use [Bot lifecycle gates](../skills/harness/harness-setup/ACTIVATION.md#configure-and-qualify-a-bot)
for configuration, rebind and activation. Fixture checks do not qualify
native invocation, caller ACL, durability or unattended operation.

## Select one entry route

Use a full checkout pinned to an approved revision. Require authority for
registration before changing configuration. Invoke the exact ID in the
intended project and caller, check the returned source and its content, and
exercise the required behavior. A list or matching digest alone is not
enough. If source is hidden and verified exclusive loading cannot establish
it, report `ambiguous` and block the dependent step.

| Host | Harness entries | Optional Inbox and Memory |
| --- | --- | --- |
| Devin | Use [project-local links](#devin-project-links). If Devin returns another project's Source, open a target-only session and recheck. Qualify persistence with a fresh worker from the correct Bot. | Prefer the qualified native exact IDs. Do not register same-ID skills to shadow them. If native is unqualified, explicitly select a collision-free external or operator route per the HOST references, or keep the capability off. |
| Pi | Choose the [local package or one-session skill directory](../README.md#pi--package); invoke `/skill:harness-setup` and the other entries. Use `/reload` or a clean session after a source change. Choose trust explicitly; `pi list --approve` applies to that command only. Package loading does not apply a role. | Add `--skill "$KIT/skills/bot/<id>"` for each selected skill and invoke `/skill:<id>` after checking for conflicts. |
| Claude Code | Choose the [plugin route](../README.md#claude-code--plugin); use `claude --plugin-dir "$KIT"` for one session. For installation, verify marketplace and settings scope; user scope is the default. Reload or start a new session, then invoke `/harness-kit:harness-setup` and the other qualified names. | Link the selected directory to project-local `.claude/skills/<id>` and invoke `/<id>` only after checking for conflicts. |
| Codex | Choose the [plugin or project-local links](../README.md#codex--plugin), not both. In a new session, check `/plugins` for the plugin and `/skills` or the `$` picker, then invoke `$harness-setup` and the other entries. Verify runner discovery separately. | Link the selected directory to project-local `.agents/skills/<id>` and invoke `$<id>` only after checking for conflicts. |

For opt-in routes, follow [Inbox HOST](../skills/bot/bot-inbox/HOST.md) and
[Memory HOST](../skills/bot/bot-memory/HOST.md). Do not change default package
registration. Follow [Setup activation](../skills/harness/harness-setup/ACTIVATION.md)
for upstream prerequisites and invocation restrictions.

## Load internal routes on demand

Pin the host version, manifest, source and exact caller. Keep only
`harness-setup`, `harness-evolve`, `harness-implement` and `harness-library`
in the default inventory. Do not add `skills/discovery/` or `skills/overrides/`
as a directory. Follow the parent skill's dispatch and
[override contracts](../skills/harness/harness-implement/ROUTES.md); loading
an override does not authorize invocation of a user-only original.

| Host | Load one selected internal ID |
| --- | --- |
| Devin | Use exact invocation in the approved project binding and verify Source. |
| Pi | Use one approved session route, `--skill "$KIT/skills/<group>/<id>"`. |
| Claude Code | Use a verified project binding or read the exact pinned file when policy allows. |
| Codex | Use a verified project binding or read the exact pinned file when policy allows. |

Compare the default inventory and injected prompt before and after loading
the selected ID. A read of one source file is not native invocation; record it
as `pinned-instruction-read` under [the topic route contract](../skills/harness/harness-setup/DISCOVERY.md#topic-route-and-result).
Do not register all discovery topics as public commands to avoid that distinction.
If the host requires changing default registration, report the gap and leave the
route off.

## Devin project links

Use a clean, complete checkout. A copied skill directory cannot find
`kit/scripts/library` from its real path. Save the shell block below and
run it with `sh <script> inspect`, using absolute `KIT` and `PROJECT` paths
and the approved full `KIT_COMMIT`. Keep the consumer outside the checkout.
Inspect makes no project writes, checks every destination and runs the pinned
helper without writing bytecode. Any preflight rejection exits 2.

Run `sh <script> apply` with the same inputs only after a live project link
grant. Serialize changes to the approved paths through preflight, Apply and
readback. If another writer cannot be excluded, stop; if a write's outcome is
uncertain, reconcile the original paths before retry. Do not delete partial
links, replace conflicts, register globally or commit absolute links.

```sh
blocked() { printf 'Blocked: %s\n' "$*" >&2; exit 2; }
case "${1:-}" in inspect|apply) phase=$1;; *) blocked 'choose inspect or apply';; esac
case "${KIT:-}" in /*) ;; *) blocked 'KIT must be an absolute checkout path';; esac
case "${PROJECT:-}" in /*) ;; *) blocked 'PROJECT must be an absolute project path';; esac
for tool in git realpath mkdir ln python3; do
  command -v "$tool" >/dev/null || blocked "required executable not found: $tool"
done
test -d "$PROJECT" || blocked "project not found: $PROJECT"
kit_root=$(realpath "$KIT") || blocked "cannot resolve checkout: $KIT"
project_root=$(realpath "$PROJECT") || blocked "cannot resolve project: $PROJECT"
case "$project_root" in
  "$kit_root"|"$kit_root"/*) blocked "PROJECT must be outside the pinned kit checkout: $project_root";;
esac
top=$(git -C "$kit_root" rev-parse --show-toplevel) || blocked "cannot read checkout: $kit_root"
test "$top" = "$kit_root" || blocked "KIT must be the checkout root: $kit_root"
head=$(git -C "$kit_root" rev-parse --verify HEAD) || blocked "cannot read checkout: $kit_root"
test "$head" = "${KIT_COMMIT:-}" || blocked "checkout is not at the approved commit: $kit_root"
state=$(git --no-optional-locks -C "$kit_root" status --porcelain --untracked-files=normal) ||
  blocked "cannot inspect checkout: $kit_root"
test -z "$state" || blocked "checkout is not clean: $kit_root"
helper="$kit_root/kit/scripts/library"
test -x "$helper" || blocked "Library helper is missing or not executable: $helper"

skills="$project_root/.devin/skills"
for dir in "$project_root/.devin" "$skills"; do
  if [ -L "$dir" ] || { [ -e "$dir" ] && [ ! -d "$dir" ]; }; then
    blocked "not a project-local directory: $dir"
  fi
done
set -- harness-setup harness-evolve harness-implement harness-library
missing=
for id; do
  src="$kit_root/skills/harness/$id"
  dst="$skills/$id"
  test -r "$src/SKILL.md" || blocked "cannot read the pinned $id/SKILL.md"
  expected=$(realpath "$src") || blocked "cannot resolve $src"
  test "$expected" = "$src" || blocked "source is not at its pinned location: $src"
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    test -L "$dst" && actual=$(realpath "$dst") && test "$actual" = "$expected" ||
      blocked "existing entry does not resolve to $src: $dst"
  else
    missing="$missing $id"
  fi
done
PYTHONDONTWRITEBYTECODE=1 "$helper" --help >/dev/null ||
  blocked "cannot run the pinned Library helper with python3: $kit_root"
if [ "$phase" = inspect ]; then
  printf 'Ready for link grant: %s at %s; missing:%s\n' "$project_root" "$head" "$missing"
  exit 0
fi
if [ -n "$missing" ]; then
  mkdir -p "$skills" || blocked "cannot create $skills"
  for id in $missing; do
    ln -s "$kit_root/skills/harness/$id" "$skills/" ||
      blocked "link outcome needs reconciliation: $skills/$id"
  done
fi
actual=$(realpath "$skills/harness-library") || blocked "cannot resolve the linked Library skill"
test "$actual" = "$kit_root/skills/harness/harness-library" || blocked "Library link changed: $actual"
PYTHONDONTWRITEBYTECODE=1 "$actual/../../../kit/scripts/library" --help ||
  blocked "cannot run the linked Library helper: $actual"
```

Then invoke `skill_invoke({"skill":"harness-setup"})` and each of the other
three exact IDs in the intended Devin project and caller. Check the returned
Source exists under that project, resolves to the pinned file, and matches
the approved commit and content. Reject a foreign project even when its
digest matches. A skill list or a successful local helper probe is not native
evidence. Mark an unprovable source `ambiguous` and block only that route.

## Bind automation to one Bot

In the existing configuration, use `bots[]` with unique, stable `bot_id`s.
Each entry binds one current instance, scope and binding revision, independent
role/contract selections, Inbox/Memory, grants, receipts and checkpoint.
Only the pinned Library backing store may be shared; reopen each selection
under the exact Bot's scope. A legacy single `bot_ref` cannot receive wake.

Bind each unique `automation_id` and host trigger to one `target_bot_id` with
the exact schedule or integration `source_id`, scope and binding revision.
Do not retarget an existing ID to a different Bot. Read back the exact active
trigger before accepting authenticated automation ingress. Do not derive the
target from role, thread, chat payload or array position. Reject missing,
multiple, stale or wrong targets before claim, positive ACK or dispatch.

Use [automation wake](PERSISTENCE.md#automation-wake) for claim, dedupe and
the instance fence. Rebind the same logical Bot only through the lifecycle
gates; old delivery cannot cross the new instance fence. Admit no conflicting
writes to another Bot's state.
