# Record format

## Current stage handoffs

Use [the v1 contract](../../../kit/STAGE-CONTRACTS.md) for a single operation
at a time. Pass minimal stable references the recipient can reopen. Use a host
structure in-session or an authorized existing record for continuation; do
not invent a durable reference or write path. With no approved write
destination, return an inline draft and its blocker, not a promised resume.
Use the [M2 contract](../../../kit/M2-CONFIG.md) in the owning decision and
configuration records, not as extra v1 fields.

| Operation | Setup boundary |
| --- | --- |
| `prepare` | After `DesignReady`, send the original request or immutable request ref, scoped decision/revision and basis, acceptance, dependencies and only still-needed drafting routes. Carry compatible spec/ticket refs; leave unavailable artifacts out. Reuse drafts without publishing them. |
| `publish` | With a live grant for the exact draft revision and verified Harness destination, send that draft, the destination's exact instance/namespace/role, stable work ID and grant reference. A selected durable local record uses its own verified binding, not a placeholder tracker. Keep the same work ID on timeout and reconcile at the destination before continuing; no Product fallback. |
| `execute` | The coordinator constructs it, not discovery. Require a canonical ticket, live `DispatchReady` evidence and current exclusive claim/epoch; use the verified route, expected target revision, exact effect and applicable selection. Publish does not authorize execution. |
| `result` | Validate shape and reopen the assignment, effect, target state and recipient-readable evidence. For `Unknown`, keep the checkpoint and reconcile without retry, rollback or reassigning the dependent work. Check an `Applied` result against acceptance before `Verified`; closure requires separate permission. |
| `bot-setup` | Emit to the operator only after reading back an authorized Bot-target configuration, the actual instance and capabilities still disabled. Include the pinned role template and contract, adapter and observed configuration refs, scope and evidence. Neither the handoff nor readback activates a trigger. |

When exchanging a JSON file, run the bundled read-only shape check on the
authorized file, passing the exact intended operation. Nonzero means stop the
dependent handoff and retain the draft/evidence; success does not establish
reference validity or authority.

```sh
<skill-dir>/../../../kit/scripts/check-stage-handoff --expect-operation <operation> <file>
```

These illustrative payloads show shape, not live records, grants or receipts.
A repo-only Setup can emit this `prepare` without Bot data:

```json
{
  "version": 1,
  "operation": "prepare",
  "request": "Set up guidance for the docs repository.",
  "scope_ref": "scope:docs",
  "decision_ref": "decision:docs-guidance@2",
  "acceptance": ["The selected reader can locate the documentation guidance."],
  "dependency_refs": [],
  "needed_route_refs": ["route:to-spec@1", "route:to-tickets@1"]
}
```

An independently granted publication to a selected local work record
that already has a verified Harness binding:

```json
{
  "version": 1,
  "operation": "publish",
  "draft_ref": "draft:docs-guidance@3",
  "target": {"instance": "local:docs-work-records", "namespace": "harness:docs", "role": "harness"},
  "work_id": "work:docs-guidance",
  "grant_ref": "grant-ref:docs-guidance-publish"
}
```

A coordinator dispatch after current `DispatchReady` readback:

```json
{
  "version": 1,
  "operation": "execute",
  "request_ref": "request:docs-guidance@1",
  "scope_ref": "scope:docs",
  "decision_ref": "decision:docs-guidance@2",
  "ticket_ref": {"instance": "local:docs-work-records", "namespace": "harness:docs", "id": "ticket:docs-guidance", "revision": 1},
  "assignment_ref": "assignment:docs-guidance@1",
  "route_ref": "route:harness-project-implement@1",
  "effect_ref": "effect:write-docs-guidance@1",
  "expected_target_revision": 4
}
```

A separate Bot-only workspace after configuration readback:

```json
{
  "version": 1,
  "operation": "bot-setup",
  "instance_id": "instance:editorial-assistant",
  "template_ref": "kit:role/editorial@4",
  "contract_ref": "kit:bot-contract@4",
  "scope_ref": "scope:editorial",
  "adapter_ref": "binding:editorial-worker@1",
  "configuration_ref": "host:editorial-config@2",
  "evidence_refs": ["evidence:editorial-config-readback"],
  "disabled_capabilities": ["wake"]
}
```

## Setup scope selection records

Use one UTF-8 JSON object for the user-visible target scope before recording a
target profile. Validate it locally:

```sh
<skill-dir>/../../../kit/scripts/check-setup-scope <scope.json>
```

The object has integer `version: 1` and exactly these fields:

| Field | Contract |
| --- | --- |
| `request` | The user request text, empty for a bare invocation. |
| `intent` | `repo-only`, `bot-only`, `repo-and-bot` or `unclear`. |
| `basis` | Fact labels or refs. `user-request` or `user-selection` is required for a decided scope. `git-directory` and `agent-host` never decide an unclear scope. |
| `user_view` | `text`, `shown_profile`, `options` and `bot_question_asked`: what the user saw and whether Bot questions opened. |
| `recorded_profile` | The same profile shown, or `undecided`. |
| `bot_identity` | `verified`, `missing` or `not-applicable`. Bot intent may be recorded while missing. |
| `effects` | Must be empty: selecting scope grants no effect. |

An undecided scope shows exactly three plain-language options with IDs
`repo-only`, `bot-only` and `repo-and-bot`. A clear repo-only request may name
`repo-only` briefly and continue without Bot questions. A nonzero check blocks
use of the scope and writes nothing.

## Setup transition records

Use one UTF-8 JSON object when a state change needs local validation. The
checker validates structure and cross-references, not live authority:

```sh
<skill-dir>/../../../kit/scripts/check-setup-transition <transition.json>
```

Required common fields are integer `version: 1`, `transition`, `scope_ref`,
`decision_ref`, `branch_outcomes` and `confirmations`. `transition` is
`design-ready`, `prepare` or `verified`.

Each confirmation has `ref` and `covered_paths`. Each branch outcome has the
exact Harness tree `path`, `status` (`settled`, `deferred` or
`not-applicable`), `decision_ref`, `confirmation_ref` and `checkpoint_ref`.
A deferral also has `deferral_ref` and `revisit_ref`. The checker requires all
seven main branches and verifies that the referenced confirmation explicitly
covers each branch path. Child branches are required only when applicable and
cannot be settled under an unsettled parent.

Embed handoffs under `handoffs` by operation. `prepare` requires
`handoffs.prepare`. `verified` requires `prepare`, `publish`, `execute` and
`result`, plus non-empty `acceptance_evidence` entries with `acceptance_ref`
and `evidence_ref`, and separate `close_authority_ref`. `result` must be
`Applied` and carry non-empty verification and evidence refs. Scope, decision
and assignment references must agree across the chain.

A failed check blocks the state claim. It does not change records, target
files, tickets or grants.

## Historical formats

Use the following only to interpret existing setup artifacts under `harness/`.
Current onboarding follows [SKILL.md](SKILL.md) and [RESUME.md](RESUME.md);
the historical sequence and prerequisites are not requirements.

### `record/<entry>.md`

`<entry>` is a short kebab-case slug of the need.

```
---
kind: tool            # tool | folder | team | delegation | role-profile | standard | isolation
choice: <kit id and name, or "outside the kit">
reason: <why this piece, one or two lines>
check: <the exact command; for a generated file, its path>
status: unverified    # unverified | passing | failing | adopted | needs-change
verified_on:          # date; empty until the check ran
check_scope:          # optional; "structural" on team entries
verified_platform:    # optional; hook entries: platform, event, matcher, date, or "not verified on <platform>"
gate_lighter_rung: <next lighter rung, or "none">
gate_why_not_enough: <one or two lines>
gate_source: <url, or the exact `--help` command>
gate_read_on: <date the source was read>
gate_answer: <what the source said>
gate_approved: user   # always "user"; an entry without it is not written
---

## Check result

<command, exit code, pasted output; empty until run>
```

Entries of `kind: delegation` (one per role) and `kind: role-profile` (one per role, named `role-<role>`) use the same keys. Their body is set out in [DELEGATION.md](DELEGATION.md) and [ROLES.md](ROLES.md); the `check` of a role profile tests that every pointer exists.

`check_scope: structural` on a `kind: team` entry means the check proves the pattern exists in the kit and the folders exist; it does not prove the team works. `passing` on such an entry is never read as "the team runs".

Entries of `kind: standard` and `kind: isolation` point at a section of `harness/STANDARDS.md` (see [STANDARDS-STEP.md](STANDARDS-STEP.md) and [ISOLATION.md](ISOLATION.md)); they never copy the rule text. An entry whose piece is a hook names the platform config file it was wired into in `check` and records `verified_platform` (see [WIRING.md](WIRING.md)).

`adopted` and `needs-change` are for a `kind: folder` entry of a part that already existed (card: `prior_harness`): `adopted` meets the standard and stays; `needs-change` does not, gap in `reason`. Setup moves nothing; `harness-evolve` reconciles relevant `needs-change` entries within the requested scope.

### `situation.md`

Step 1 writes nine lines, `field: value`, facts only, no prose; `python3 tools/check_kit.py --situation harness/situation.md` checks them.

| Field | Value |
|---|---|
| `matt_config` | `present`, `partial` or `absent`: the `## Agent skills` block and `docs/agents/` |
| `work_source` | `git`, `tracker:<name>`, `doc:<path>` or `none`: where finished work is found |
| `code_home` | `.` or paths of the repos the flow writes product files to (code or product documents), comma separated |
| `flow_source` | `doc:<path>`, `sample` (one recent piece of work) or `asked` |
| `prior_harness` | `none`, or paths of harness parts that already exist, comma separated |
| `history` | `yes`, or `none` when no finished work can be named |
| `tree_relation` | `shared`: harness files and product code in one tree; `apart`: the harness repo holds no product code |
| `platform` | the agent app, or `<app>@<host>` when it runs through a host (schedules depend on it); `unknown` until S01 is answered |
| `confirmed` | `no` while drafting, `yes` once the user says the card is right |

### `gate.md`

Hand-off from step 3 to step 5, so an interrupted run keeps the approved evidence. One `## <item>` section per approved item with the five evidence fields (`lighter_rung`, `why_not_enough`, `source`, `read_on`, `answer`). The entry holds the lasting copy; later runs read the entry.

### `record/index.md`

Read first. One line per entry, no detail:

```
# Harness record

- [<entry>](<entry>.md): <kind>, <status>
```

### `progress.log`

Append only; one line per finished step, never edited:

```
<UTC timestamp from `date -u +%FT%TZ`> step=<observe|need-to-piece|gate|proposal|record|check|delegation-draft|delegation|roles|standards|isolation|wiring|final> <key=value ...>
```

`observe` carries `platform=`, `work=` (the piece of work of S02 turn 1), `flow=`, `labels=` (`shared=a,b;project=c,d`, an empty side left out, or `none`) and, once S07 is asked, `pain=`; `need-to-piece` carries `need=`, `piece=` and `groups=` (letters of every kit group looked at, comma separated); `gate` carries `items=` (approved) and `dropped=`; `proposal` carries `part=` (tools, folders or team) and `outcome=`; `record` and `check` carry `entry=` (`check` also `result=`); `standards` and `isolation` carry `entry=` (or `outcome=none`) and `result=`; `wiring` carries `map=`, `block=` and `hooks=`; `final` carries `entries=` and `result=`; `delegation-draft` is the one line written in the middle of step 7, after each answer that settles a field of a table row: `role=`, `kind=` and the fields settled so far (`undo=`, `info=`, `level=`, `zone=`, `stop=`); it lets a later run continue inside a stage without asking again; `delegation` and `roles` carry `entry=` and `result=`, and the first `delegation` line also `roles=` (all role names). A value with spaces goes in double quotes (`flow="ticket, code, review"`). Always take the timestamp from running `date -u`, never from memory. Before logging a step, read the last line: a line for the same step and the same entry (or, for `need-to-piece`, the same need) already there is not logged again.

**Revising a decision.** The log is never edited. When the user changes a decision already logged, append a new line with the same `step=` (and the same `part=` or `entry=`) and `revised=<timestamp of the old line>`; leave the old line alone. For each (step, part) the line in force is the last one. `python3 tools/check_kit.py --log harness/progress.log` checks that every `revised=` points to the timestamp of an earlier line with the same step, and lists the line in force for each (step, part) by the same rule.

### Writing safely

Write each file to `<name>.tmp` in the same folder, then rename over the target; remove no other file. An entry or index line already present is updated in place, never appended twice.
