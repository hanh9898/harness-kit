# Selected provider activation

## Install required upstream skills

1. On the host that will use them, check the original `grilling` and
   `domain-modeling` before discovery. Before authoring overrides, check
   `writing-for-agents` (unless a qualified replacement is selected), the
   originals for the needed `to-spec`, `to-tickets`, `implement` or
   `implement-spec` routes, and any methods those routes actually require.
   Check exact IDs, source and invocation policy; reuse verified originals.
   An ambiguous or disallowed route is not a missing installation.
2. For missing originals, choose one install path for the actual host from
   [upstream's installation guide](https://github.com/mattpocock/skills#installation-30-second-setup).
   Prefer the documented managed route where supported and in scope. For Devin
   use the project root and an explicit `--skill` list of missing, required
   IDs. For example, when both discovery methods are missing:

   ```sh
   npx skills@latest add mattpocock/skills -a devin --skill grilling domain-modeling
   ```

   Do not use `--global` for the Devin pilot. Check all destinations and side
   effects, including bundled skills and installer metadata (on Devin, check
   `.devin/skills/` and `skills-lock.json`). Do not install the same skill via
   two routes or replace an existing source without authorization.
3. Before running the installer, require explicit, current authority for
   that host, command, scope and effects. If missing, present the exact plan
   and request approval; selecting or invoking Setup is not permission.
   Apply the [write gate](../harness-implement/WORK.md#write-boundary-and-reconciliation),
   including real-time confirmation for a permitted non-atomic send.
   Run only within the grant; otherwise leave configuration unchanged and
   record the blocked methods and next action. If the host requires the user
   or an admin to install, hand them the exact approved route. Include
   `setup-matt-pocock-skills` as upstream directs when per-repo configuration
   is needed and covered by the install grant; it does not gate discovery.
   The user runs that helper, with separate authorization for its writes.
4. After installation, read back the installed IDs and check their resolved
   source/path and revision or digest in the intended project. For
   agent-callable methods, verify loading through the permitted host route;
   for user-only originals, inspect their source and policy without invoking
   them. If native loading requires a reload or new session, or the install
   fails or is uncertain, hold dependent work until verified and continue
   independent authorized work. Reconcile uncertain effects before retrying.
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
