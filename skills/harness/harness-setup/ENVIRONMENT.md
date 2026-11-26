# Roles, scope and readiness

Read during discovery and whenever the intended consumer or target scope changes.
Inspect relevant supplied paths and accessible facts; do not sweep adjacent projects
or enumerate a user's home merely because a layout could include them.

A **harness** supplies the guidance, context, methods and tools around an agent.
A **control plane** coordinates work or agent sessions. Record their actual roles;
one product can serve both, and a project can have no control plane. Identify the
invoking host separately from hosts expected to consume the foundation later.

For each relevant target, retain its role, location, owner/authority, allowed reads
and writes, selected use and observed readiness. Distinguish:

- **Installed:** executable, plugin or source is present at an inspected location.
- **Configured:** relevant settings/registration exist; validity may still be unknown.
- **Active:** this use actually runs there, with observed host/model/provider conditions.
- **Intended:** requested future consumer; not evidence of current readiness.

These facts can overlap. Record evidence, date and uncertainty rather than force a
single status. An available CLI and valid manifest do not prove authentication,
loading, invocation or behavior. Intended Claude Code, Codex and Pi routes remain
explicitly unverified until exercised under their actual grants.

## Target preflight before effects

Before any Apply write, install, registration or activation, run the read-only
preflight through the real skill directory:

```sh
<skill-dir>/../../../kit/scripts/check-setup-preflight --target <target> --mode apply --effect <effect>=<grant-ref> --json
```

Repeat `--effect` for each exact effect. Add `--requires-tool node` and
`--requires-tool npx` when the selected route needs them. The command inspects
the target, accessible scheduler entries, deployment indicators and required
executables. It writes nothing. A nonzero exit is a stop: report the missing
tool, grant, target-role evidence or writer evidence exactly as reported.

Detached HEAD, no remote or a one-commit/shallow checkout is a review signal,
not a conclusion that the target is a deploy copy. For Apply, resolve the signal
with evidence that the target is the intended writable work location. Check
cron, scheduler entries, CI or deploy configuration that can write the target.
If an overwrite writer is possible and cannot be ruled out, stop before the
effect. Do not scan unrelated projects or the user's whole home to clear the
check.

## Layouts to distinguish

| Layout | Discover and preserve |
| --- | --- |
| Same repository | Distinguish product/source artifacts from harness guidance and records. Current-repo scope still needs concrete write authority. |
| Separate control repository | Identify the coordination/harness repository and consuming repository separately. A record edit in control does not apply guidance to the consumer; its writes and demonstration need their own grant. |
| Monorepo package scopes | Resolve root and package guidance precedence. Record which packages inherit or override it and verify only selected package effects; a package grant does not cover siblings. |
| User-level harness across repositories | Separate reusable personal guidance/configuration from each consumer's selection and application. Explicit user-level and repository grants are needed for their respective effects. Changing reusable material alone does not adopt it everywhere. |
| Non-Git documents/process folders | Use existing source, document and process conventions; Git, code and a tracker are not prerequisites. Establish an accessible durable record and actual content/accuracy criteria within the folder grant. Human-only source facts retain required human review. |
| Shared team harness repository | Separate shared definitions/maintenance authority, team responsibilities and each consumer's adoption. Establish a common integration writer or suitable native concurrency facility before shared effects; local checkout isolation is not race safety. |

A physical path alone does not establish its semantic role or permission. Reuse
known assignments. Ask only for missing material scope, target identity or access.
Keep blocked target work separate from independent authorized initial use. Reference
current team/workflow and observation capabilities when selected; their presence
in discovery does not certify a deployed team, telemetry system or factory.
