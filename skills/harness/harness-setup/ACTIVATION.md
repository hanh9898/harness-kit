# Selected provider activation

## Bootstrap Harness on Devin

Use the [adapter runbook](../../../kit/HOST-ADAPTERS.md#devin-project-links)
to inspect the four Harness entries without writing, then link only in Apply
with a grant for the exact project and paths. Verify the returned project
Source, caller and pin before use. Missing access or unproven source blocks
the route; do not reinstall to clear it. Resolve
[internal routes on demand](../../../kit/HOST-ADAPTERS.md#load-internal-routes-on-demand);
do not register the discovery or override directories by default.

## Verify upstream prerequisites

Verify the originals `grilling` and `domain-modeling` before dependent discovery.
Before authoring a selected override, verify `writing-for-agents` and that
override's original: `to-spec`, `to-tickets` or `implement`. Skip originals
for unselected overrides. Check extra methods only where used.
Use the upstream originals, not vendored copies.

Check exact ID, source, revision, caller and invocation policy on the consuming
host and project. Probe each required route once per unchanged scope and reuse
the result until the host, project, caller, source, revision or policy changes.
Do not confuse a route probe with a node's use of the method. For user-only
originals, inspect source and policy if permitted. Never invoke them on the
user's behalf or count source inspection as invocation.

An ambiguous result, wrong source or wrong caller, denied invocation or pending
load is blocked, not missing. Re-probe a pending load only after the host's
skill discovery refreshes. If a required method cannot be verified, name it,
hold dependent work and continue independent authorized work. For Setup, follow
the [install route](#install-required-upstream-skills) only in Apply and only for
confirmed missing originals. Inspect and Advice report blockers without installing.

## Install required upstream skills

1. Confirm Setup is in Apply before entering this route. The
   [entry gate](../../../kit/PROPOSAL-ENTRY.md#selection-h1) does not grant installation.
   Present a scoped plan from the [upstream installation guide](https://github.com/mattpocock/skills#installation-30-second-setup).
   Require a fresh, explicit project administrator grant (H3) for this Apply.
   Bind the grant to the caller, host, project, exact missing IDs, installer
   version and upstream revision, command, destinations and lockfile effects.
   Without a matching grant, leave configuration unchanged and report the
   blocked methods and next action. Apply the [write gate](../harness-implement/WORK.md#write-boundary-and-reconciliation),
   including real-time confirmation for a permitted non-atomic send.
2. Check bundled skills and all proposed writes before running the installer.
   In Devin, use the target project root, `.devin/skills/` and `skills-lock.json`.
   Never install globally, use two install routes, or replace an existing source
   through this gate. With the approved installer version and upstream source
   pinned to its approved revision, run this only if both IDs are missing:

   ```sh
   npx "skills@$INSTALLER_VERSION" add "$MATT_REPO_AT_PIN" -a devin --skill grilling domain-modeling
   ```

   Pass only the confirmed missing IDs in scope. If the host requires a user or
   admin to install, give them the exact plan. The user runs
   `setup-matt-pocock-skills` only if per-repo configuration is needed and
   separately authorized. It is not a discovery prerequisite.
3. Read back the lockfile, installed IDs, resolved source/path, revision or
   digest, caller and invocation policy in the intended project. Verify host loading
   for agent-callable methods. If loading is pending or the install fails or
   is uncertain, hold dependent work until verified. Reconcile before retrying.
   Installation alone does not verify an override.

## Register the v1 implementation overrides on Devin

Plan only the needed [project override routes](../harness-implement/ROUTES.md#project-override-routes).
The three source templates under `skills/overrides/` are not default entries. On
Devin, register them at `.devin/skills/<id>/SKILL.md` in the intended project
using the host's supported mechanism. Do not register them globally, reuse an
original ID or change an upstream skill or its invocation policy.

Before authoring or changing an override, use the
[agent-read guidance contract](../harness-evolve/CHANGE-FLOW.md#authoring-an-override-in-a-new-project).
If a required source or method cannot be used, leave the dependent override
unchanged and report what would unblock it.

Record the template revision, any adaptations and the upstream source revision
and license. Preserve upstream notices if adapting material. Changing only
invocation metadata is not an override.

Only in Apply, require a separate project administrator grant (H4) for the
exact template IDs, source revisions, project, destination writes, intended
caller and invocation policy. H3 does not authorize registration. Use the
[late-write gate](../harness-implement/WORK.md#write-boundary-and-reconciliation)
and verify that every destination resolves inside the project and the grant
before writing. H4 does not authorize execution.

First read back the effective configuration in the intended caller and project.
Match exact ID, Source (resolved path), revision or digest, caller and effective
invocation policy. Check that each ID has a single binding and that the
originals retain their sources and manual invocation policy. Do not invoke a
user-only original to check it.

After matching the binding, resolve the exact ID with the native tool and
recheck what loaded. Use a permitted no-write probe to collect output or denial
evidence. Do not require prior output evidence for the first probe. Test a fresh
or child context only when the route uses it.

Record the verified binding and evidence for each route independently. A
verified preparation pair without verified execution is draft-only. Apply the
[route readiness checks](../harness-implement/ROUTES.md#route-readiness) before
reporting execution readiness; registration and fixture readback alone do not
qualify native routes. Evolve verifies its needed bindings without reinstalling.

### Opt in to the Devin prepare fixture

Use the [prepare fixture](../../../examples/devin-prepare/prepare.json) only
in a separate Devin project. Pin the full `hanh9898/harness-kit` checkout to an
approved commit and use the [fixture's upstream pin](../../../examples/devin-prepare/decision.json)
for provenance only. Do not load or change the original user-only skills.

With a grant for exact project-local registration, expose only the needed
example ID under `.devin/skills/<id>/SKILL.md` from the pinned example
directory. Record the registration path, resolved source and digest, project,
intended caller and effective agent-callable policy. Keep both IDs out of
default registration and the workflow override inventory. Follow the
[fixture route](../harness-implement/ROUTES.md#devin-prepare-fixture) for
invocation and evidence. This does not establish execution readiness.

## Configure and qualify a Bot

### Add a disabled Bot

Match the proposed `bot_id`, host, workspace, owner and scope to the recorded
intent. The intent is not an effective binding or a wake target. Use the
[adapter runbook](../../../kit/HOST-ADAPTERS.md) for the intended host and caller.

For the Library-backed quickstart, pin the approved distribution and read
[`software-factory`](../../../kit/BOT-ROLES.md#software-factory) and
[`bot-portable-template`](../../../kit/BOT-TEMPLATE.md) separately in the new
Bot's scope. Resolve the
[configured store](../../../kit/LIBRARY.md#configured-store-reads) first. In
these commands, `library` and `kit` stand for the absolute helpers from the
verified skill distribution. Disable Python bytecode writes:

```sh
for id in software-factory bot-portable-template; do
  library --store "$BOT_STORE" --require-existing-store selection "$id" --source supplied --kit-dir "$PINNED_KIT_DIR" || exit
  PYTHONDONTWRITEBYTECODE=1 kit --dir "$PINNED_KIT_DIR" show "$id" || exit
done
```

Keep two independent [selection handoffs](../harness-library/READ.md#selection-handoff).
For each, verify exact Bot, store, owner/scope, source, ID, revision and
effective state. Verify the supplied row digest and separately compare the
digest of the linked file to the approved distribution revision. Open the
selected role section and portable contract from that pin, not another checkout.
Neither a shared store nor the same role ID lets one Bot reuse another's evidence.

Only a confirmed unconfigured store permits catalog-only preview, using
the same pinned `kit show` command without claiming an effective selection.
A bound store that is missing, wrong-identity or unreadable is **Blocked**; do
not create a store, retry at a different path or fall back to catalog selections. Missing
permission, pin or linked digest, effective selection, or host role/tool
evidence keeps the Add in preview. Preview makes no writes, schedules nothing
and sends no notification.

Only in Apply, require H19 for the exact new Bot, binding and disabled
configuration effect. Submit only that effect. Read back the actual instance,
binding, configuration revision and every trigger as disabled (or absent);
then make that binding effective and emit one
[`bot-setup` v1](../../../kit/STAGE-CONTRACTS.md#setup-or-evolve--bot-operator-bot-setup)
for that instance. Incomplete or inconsistent readback is blocked, not a
receipt; reconcile at the original target before retrying. Adding or denying
this Bot never changes another Bot's binding, grant, revision, receipt or
triggers.

### Read-only smoke

Time the readback from the first pinned selection read through the last
verified readback. Report what was read and whether anything was written,
scheduled or sent. This smoke is not H15 qualification or authority to wake.

- **Devin:** Check the exact instance and caller, observed Instructions and
  Memory, and the read-only route. Read the approved fixture and observe
  **Needs you** without creating an ask. Never substitute another Bot.
- **Pi:** Use an isolated project and HOME. Check the installed version's
  flags and verify the effective tool list is read-only and the selected role
  is in the actual prompt. A package load does not inject the role. Render a
  role draft outside the target only with separate draft-write authority;
  otherwise keep it inline. Without real role and tool evidence, stop in
  preview.

A local fixture replay does not prove native caller ACLs or role loading.
Do not commit, create a PR or ticket, notify, or schedule from the smoke.

### Rebind or qualify an existing Bot

Before H14 rebind, disable and read back every trigger on the old binding,
drain or fence its work, and reconcile all `Unknown` effects at their original
targets. If reconciliation stalls, H13 is for an operator decision, not a
retry or reassignment. Require the owner's approval of the exact new binding,
read it back disabled and verify continuity of authorized records and occurrence
dedupe. Never keep two active bindings for the same Bot.

On either the initial or rebound binding, require its disabled readback and H15
for the manual and fresh-worker pilot. Check authority, scope, checkpoints,
fencing and the [automation wake contract](../../../kit/PERSISTENCE.md#automation-wake).
Only after both pilot checks pass on that binding may H16 authorize enabling
the exact trigger for that Bot. Read back that trigger before reporting it active.
H19, H14 and H15 do not authorize activation.

## Other selected activation

Read only when the selected initial use needs a provider installation,
registration, invocation-policy change or provider update. First inspect actual
availability and current host-specific documentation/help. Reuse adequate native
facilities; no universal manifest syntax or setup-provider prerequisite applies.

Identify the concrete target host/configuration, current effective settings,
selected original method and intended invocation route. Follow the provider
contract in [CHANGE-FLOW.md](../harness-evolve/CHANGE-FLOW.md), including nested
prerequisites and explicit-only restrictions. Reading a restricted source is not
an invocation unlock. A required missing source blocks dependent authoring.

Resolve the exact installation/configuration effect against actual grants and
prior adoption procedure. An outer setup call does not itself invoke an
explicit-only child, and selection is not a settings-write grant. If scope is
missing, preserve configuration and record the exact grant/source/access needed;
continue independent discovery. Do not ask again when sufficient authority exists.

Before granted effects, capture/read back the choice, target, rationale,
authority, expected change, timing and reversible recovery reference using
[UPDATE.md](../harness-evolve/UPDATE.md). Preserve unrelated configuration and
customization. Prefer a minimal semantic edit; retain the old effective state
for review/recovery under the same scope, without leaking credentials into records.

After the change or provider update, inspect effective settings and recheck
eligibility/loading and an actual invocation through the affected route. Exercise
the selected method's useful result, not an echo of its name. If the host requires
a restart or fresh session, that verification remains pending until actually run.
Do not launch another agent without authority; hand over a precise invocation
and evidence requirement when the needed session or access is unavailable.

Compare protected settings and affected target behavior; keep existing unrelated
providers working within the observed checks. A failed activation is partial,
not ready. Restore only within actual authority and after inspecting uncertain
effects; preserve the failure and recovery scope. Retain per-target host/version,
model, provider/resource revision, configuration/grant conditions, observed use,
missing conditions and next action. Material changes invalidate affected evidence,
not unrelated qualified uses.

```v1-gates
[
  {"id": "authority.bot-config", "requires": []},
  {"id": "authority.install", "requires": []},
  {"id": "authority.pilot", "requires": []},
  {"id": "authority.rebind", "requires": []},
  {"id": "authority.trigger", "requires": []},
  {"id": "bot.configure-disabled", "requires": ["bot.exact-target", "bot.disabled-config", "authority.bot-config"]},
  {"id": "bot.disabled-config", "requires": []},
  {"id": "bot.disabled-readback", "requires": []},
  {"id": "bot.drain-fence", "requires": []},
  {"id": "bot.exact-target", "requires": []},
  {"id": "bot.old-disabled-readback", "requires": []},
  {"id": "bot.pilot.initial", "requires": ["bot.configure-disabled", "bot.disabled-readback", "authority.pilot"]},
  {"id": "bot.pilot.rebound", "requires": ["bot.rebind", "bot.disabled-readback", "authority.pilot"]},
  {"id": "bot.rebind", "requires": ["bot.exact-target", "bot.old-disabled-readback", "bot.drain-fence", "bot.reconciled", "authority.rebind"]},
  {"id": "bot.reconciled", "requires": []},
  {"id": "method.domain-modeling", "requires": []},
  {"id": "method.grilling", "requires": []},
  {"id": "method.handoff", "requires": []},
  {"id": "method.writing-for-agents", "requires": []},
  {"id": "original.implement", "requires": []},
  {"id": "original.to-spec", "requires": []},
  {"id": "original.to-tickets", "requires": []},
  {"id": "override.implement", "requires": []},
  {"id": "override.to-spec", "requires": []},
  {"id": "override.to-tickets", "requires": []},
  {"id": "pilot.manual-fresh-worker", "requires": []},
  {"id": "setup.author-overrides", "requires": ["method.writing-for-agents", "original.to-spec", "original.to-tickets", "original.implement"]},
  {"id": "setup.discovery", "requires": ["method.grilling", "method.domain-modeling"]},
  {"id": "setup.execution-ready", "requires": ["override.to-spec", "override.to-tickets", "override.implement"]},
  {"id": "setup.install", "requires": ["entry.explicit-apply", "authority.install"]},
  {"id": "trigger.enable.initial", "requires": ["bot.pilot.initial", "bot.exact-target", "trigger.exact-id", "pilot.manual-fresh-worker", "authority.trigger"]},
  {"id": "trigger.enable.rebound", "requires": ["bot.pilot.rebound", "bot.exact-target", "trigger.exact-id", "pilot.manual-fresh-worker", "authority.trigger"]},
  {"id": "trigger.exact-id", "requires": []}
]
```
