# Minimum usable foundation

Read when selecting or checking onboarding completion. These are semantic outcomes,
not required files or a new schema. Existing guidance, a native store and references
can satisfy several outcomes together. Fill only actual gaps under the grant.

## Target profile and caller mode

Use the [M2 profile and mode contract](../../../kit/M2-CONFIG.md). Keep these
values in existing authorized records, not mandatory new files. Reuse known
owner, scope and bindings; ask only when a material input is missing. Show the
chosen target scope in plain language before recording it. Do not infer it from
the current Git directory or the selected agent host. If intent is unclear,
keep the profile undecided and let the user choose only this repository, only a
Bot, or both before recording a profile.

| Profile | Foundation in scope |
| --- | --- |
| `repo-only` | Use for a clear repo-only request or user selection. State the scope briefly and continue. Do not open Bot discovery, load Inbox/Memory, add a store write, or emit `bot-setup`. |
| `bot-only` | Use the real workspace, owner and scope. Bot intent may be recorded before a durable Bot identity exists; verify the exact Bot and grant before configuration. Skip repo and Product tracker inputs and Product verification. Keep a Harness work destination only where the work needs one; do not fabricate a repo or tracker. |
| `repo-and-bot` | Select both targets only when both are to change. Keep separate bindings, revisions, grants, effects and results. If Bot work depends on unfinished Repo work, hold only that Bot branch; Bot denial does not roll back independent Repo work. |

Use `interactive` for ordinary sessions and interactive Bot design or trials.
`persistent-bot` describes the caller, not permission to change a Bot target.
Record it as effective only after verifying the durable instance and adapter
and that a worker with the correct ACL can open its checkpoint.

For an in-scope Bot change, pin and read both the selected role template and
its linked contract at the same distribution revision; if using Library
selections, verify both are effective before applying. Selection is not
configuration authority. If applying configuration, read back the actual
instance ID, configuration and disabled capabilities. To qualify persistence,
run the authorized manual route and prove a fresh worker can resume and
deduplicate. Leave each trigger disabled until the operator obtains a
separate grant and reads back activation.

## Foundation outcomes

| Required outcome | Evidence of adequacy |
| --- | --- |
| Recoverable project/environment/scope context | Work and source locations, harness/control-plane roles, consuming targets and effect boundary can be found by the next consumer; unknowns are explicit. |
| Applicable working criteria and authority | Relevant content/language/output criteria, actual grants, prior change procedure, timing and stop/revocation limits are usable for the initial work. A stage or policy declaration is not native enforcement. |
| Effective resource/provider selection | Selected material has source/identity, applicability, prerequisites and limits; adequate personal material is retained even with unknown provenance. Required original methods actually load under the selected host policy. |
| Initial-use and evolve routes | The selected consumer can reach effective guidance and perform one useful initial task; later authorized improvement has a reachable public route. Explicit or source-read use may be qualified more narrowly than automatic selection. |
| Durable state, evidence and continuation | One discoverable authoritative current view references sources and live effects, preserves logically separate choice/review history and captures actual per-target results, conditions, remaining work and next trigger. |
| Revisitable discovery | The [Harness tree](DISCOVERY.md) and authorized decision map are reachable without replaying setup or activating unused capabilities. |

For applicable requirements, conflicts and document-quality checks, use [standards selection](../../../kit/standards/SELECT.md). Reuse consumer criteria and distinguish selected requirements, performed checks and satisfaction.

Choose a small actual use from the selected repo or workspace: create one attributable report,
answer one context question from selected sources, or perform one authorized
operation with observable output. Reuse supplied selection and check criteria.
If the use is unresolved, recommend one with a concrete benefit and explain only
consequential alternatives. Check actual effects and protected scope afterward.
A synthetic example can qualify its bounded use; describe its conditions honestly.

For an adequate foundation, preserve its location, wording and ownership. Verify
its pointers and exercise its use; record new evidence only where missing. An
unverified broader target remains partial even if the invoking host succeeds.
Selected standards, performed checks, satisfied criteria, decision review,
application and measured improvement remain independently reportable.

Use [UPDATE.md](../harness-evolve/UPDATE.md) for capture, serialization and resume.
A reference to an external authoritative store requires actual future accessibility;
a pointer to a disposable path cannot supply durable continuity after disposal.
