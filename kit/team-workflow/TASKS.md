# Task contracts and workflows

Use for task definitions, review timing, transitions, handoffs or workflow readiness through setup/evolve. Deliver a workflow-only result using existing actors; team setup and factory adoption are optional. For reviewer identity, context, authority or independence changes, use [TEAM.md](TEAM.md). The calling workflow owns original-method composition, grants, required pre-action records and final assessment; this reference supplies capability content only.

This is inferred guidance under the [accepted task contract and source map](SOURCES.md). Reuse adequate definitions, native facilities and project conventions before adding a gap.

## 1. Locate the authoritative definition

Inspect existing task and policy homes and the selected consumers' read/write access. Offer these alternatives when choosing a home:

| Organization | Fit and required discovery |
| --- | --- |
| Central definitions at the harness location | Recommended when no adequate organization exists; callers need a pointer and target access |
| Definitions beside each target | Fit local ownership; harness guidance points to each authoritative definition |
| Existing management tool | Fit established work management; retain access instructions and authoritative-source references |

Recommend Markdown for initially human-reviewed material. Markdown plus metadata, YAML/JSON and native tool records are alternatives for actual consumers. A structured consumer validates its required contract; an export identifies its authority and revision rather than becoming another master. No universal schema, directory or file count follows.

**Done:** intended actors can find and read the definition and required references at the point of need. For disposable runners, demonstrate the selected storage's survival path; an uncommitted file inside the runner is insufficient. Missing access blocks dependent execution, not authorized independent design.

## 2. Make the task usable

Populate these meanings directly or by accessible reference. Explain deliberate non-use instead of filling empty boilerplate.

| Contract part | Required useful meaning |
| --- | --- |
| Start | Trigger; input/source identities and freshness; entry conditions, including grants, required access and readiness |
| Execution | Steps or selected original methods; consuming target; services read/written; allowed effects and authority references |
| Completion | Outputs and consumer; testable done criteria; self-check; evidence and known limits |
| Continuation | Handoff state and recipient; next trigger or termination; unresolved work; human re-entry conditions and responsible role |
| Controls | Applicable duplicate-work, effect reconciliation, run/review limits, stop and give-up policies |

Workflow supplies review timing, exact inputs/revisions, output meaning and correction/handoff path. Team supplies the reviewer's identity, competence/context, authority and independence. For example, “review after draft” is incomplete without naming which draft and criteria, what findings authorize, and what happens on failure; none of these timing facts establishes a qualified independent reviewer.

For committed work, define a work item with source key, intended value, scope/target, acceptance evidence, dependencies, current owner/claim, state, remaining work and next trigger. Keep these in or referenced from the selected [tracker](TRACKERS.md). Define the commitment point before treating an incoming source item as accepted work; incomplete proposals can remain uncommitted. A brief interactive task may end in a conversation without a work tracker.

**Done:** a new actor can start the task, recognize completion and continue a partial result without reconstructing the original chat. An output artifact alone is not completion if a selected review or effect remains unverified.

## 3. Resolve policy and reuse

Offer self-contained task policy, shared policy references with explicit task exceptions (recommended), or layered policy. Identify the actual selected precedence; do not invent an order from file proximity. Resolve each applicable limit, source, scope and exception to an effective value with its authority and rationale before dependent execution. Unresolved conflicts block that action. An exception can customize selected policy only within grants and applicable obligations; a task's input or declared cap is neither a grant nor evidence of enforcement.

Share task definitions when steps and done criteria match, with run-specific target/inputs and authorized exceptions. Split definitions when differences obscure obligations. Each run identifies its task, target and effective authority; record contract/policy versions when needed for traceability. Stable definitions during a run do not delay revocation or stop commands.

Workflow owns composition and project-chosen per-task limits/rationale. Context supplies locations/targets. Team supplies role and decision-authority references. Standards supplies brake, reversibility and applicable limit requirements. Tools supplies and verifies actual mechanisms. Selected factory guidance supplies stage meaning. Keep references to the owner of each fact rather than competing copies.

When selecting a flow assembly or task automation, read [FLOW.md](FLOW.md) and account for every applicable function. A direct manual contract need not invent a scheduler or factory.

**Done:** the effective policy is unambiguous and useful reuse preserves target-specific scope and evidence.

## 4. Check readiness and continue

Use a supervised walkthrough, an agent check with inspected evidence, or a validator/native check according to the real consumer. Check definition/reference accessibility, inputs, actual grants, effective policy, reviewer route and selected controls before dependent effects. Inspect target results and unchanged scope. Keep design, authorized application and observed operation distinct. A cap written in a task is a declaration until its mechanism is verified; manual checks establish supervised readiness only.

If a prerequisite fails, preserve completed work, exact blocker and next trigger in the existing authorized durable record. On resume, reopen live state and inspect uncertain effects before retry. A completed run does not append another completion or repeat adoption. Report the task's actual stage if a stage ladder is selected; an observer-like stage never authorizes merging.

**Done:** requested contracts/transitions are accessible and assessed for the actual target, with precise continuation and no unsupported execution or improvement claim.
