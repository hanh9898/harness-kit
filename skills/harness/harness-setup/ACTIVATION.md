# Selected provider activation

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
load is blocked, not missing. If a required method cannot be verified, name it,
hold dependent work and continue independent authorized work. For Setup, follow
the [install route](#install-required-upstream-skills) only in Apply and only for
confirmed missing originals. Inspect and Advice report blockers without installing.

## Install required upstream skills

1. Confirm Setup is in Apply before entering this route. Present one scoped
   install plan from the [upstream installation guide](https://github.com/mattpocock/skills#installation-30-second-setup).
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

During discovery, plan only the needed `to-spec`, `to-tickets` and execution
routes. Follow the [route contracts](../harness-implement/ROUTES.md). At
authorized bootstrap, use the narrowest host-supported project scope. On Devin,
create project-local skill entries (the pilot used `.devin/skills/<id>/SKILL.md`)
with distinct IDs, matching frontmatter names and narrow descriptions. Use the
host's permitted project-skill mechanism; confirm loadability for this project
before relying on it. Keep global installed skills unchanged.

Before authoring or changing an override, use the
[agent-read guidance contract](../harness-evolve/CHANGE-FLOW.md#authoring-an-override-in-a-new-project).
If a required source or method cannot be used, leave the dependent override
unchanged and report what would unblock it.

For each selected override record the source revision/license and the limited
contract changes. Preserve upstream notices when adapting material. Implement
the required inputs, outputs, use and non-use conditions, dependencies and
effect limits from the route contract; merely changing invocation metadata is
not an override. Preparation routes return drafts; a ticket route checks the
assignment and target gate. Remove implicit tracker and Git effects. Do not
change an upstream skill or try to bypass invocation policy.

Treat registration as its own granted write, using the
[late-write gate](../harness-implement/WORK.md#write-boundary-and-reconciliation).
Read back the configuration and probe by exact ID through the native tool in
the intended Devin context. Verify the resolved path and revision/digest,
real output and denial without permission. Confirm no route collision or
change to upstream manual invocation outside scope. Verify a fresh or a child
session only when needed for the route; do not claim either without evidence.
Return the lightweight verified catalog; an unverified entry blocks only its
dependent step. Evolve can verify its own route without this bootstrap.

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
