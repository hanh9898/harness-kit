# Selected flow, brakes and adoption

Read when choosing a flow assembly or task automation. These are inferred recommendations with [source provenance](SOURCES.md). Values, stage ladders and mechanisms are project choices; this kit provides neither a scheduler nor a consumer waiting system. Manual and single-agent operation remain valid.

## Account for the selected flow

For each function below, select an adequate existing piece/provider or record a deliberate non-use reason. State the relevant condition, project value and rationale, actual mechanism, and verification evidence or gap. Preserve existing authority. Prefer capacity/effect evidence to arbitrary numeric defaults.

| Function and condition | Alternatives and selection guidance |
| --- | --- |
| Commitment/replenishment: incoming work needs acceptance | Human label/move, triage notes for a human, or an authorized source-signal rule. Matt triage is an optional explicit-use piece; this reference does not unlock model invocation. Admit work against downstream capacity; identify the commitment point and tracker. Reuse request-triage. |
| WIP: accepted unfinished work can outgrow capacity | Existing board limit or supervised selection. Choose a limit from review/finish capacity and explain its exceptions; count unfinished blocked work under the chosen definition. |
| Concurrency: simultaneous runs contend or consume resources | Existing orchestrator group, sequential human dispatch or bounded workers. Choose against available resources and integration ownership; reuse no-nested-subagents/hard-run-caps/per-task-resources where applicable. WIP and concurrent execution are different limits. |
| Claim: actors can take the same item | **Required for competing actors.** Reuse an atomic tracker claim, common lock/lease or orchestrator exclusion. Name owner/release/recovery rules; a label without exclusion is not demonstrated race safety. task-dependencies-and-claims is a candidate. |
| Idempotent effects: retries or duplicate events can repeat actions | Use a provider's request identity/transaction, or reconcile and serialize a logical action. Identify item, target, action and prior outcome. Uncertain remote success must be inspected before retry; a local marker alone does not guarantee exactly-once effects. |
| Retry/give-up: failure can recur | Distinguish transient failure from missing authority or bad inputs. Select a finite attempt/time/cost bound and rationale; name human escalation and visible handoff. Reuse P9, 5.33, hard-run-caps. An exhausted review loop ends rather than resetting its counter. |
| Reconciliation: live state can change or effects are uncertain | Compare tracker, active claim, target and recorded outcome before continuation. Preserve completed effects and finish missing records. run-recovery supports recovery, subject to its source limits. |
| Waiting-backlog age: waiting work can become stale | Human review at replenishment or an existing age report. Choose revisit/escalation criteria from work urgency and observed delay. Preserve arrival/commitment/start times separately; backlog age is not started-item age. |
| Off switch: execution may continue without a human | **Required for unattended tasks**, with a stop bound and visible give-up/handoff. Use an existing native stop/disable route and verify it at the correct scope. Distinguish stopping active work from preventing new runs; preserve state for re-entry. Reuse 6.25 when applicable. |
| Trigger-loop guard: outputs can start runs | **Required when outputs can trigger runs.** Use causal IDs/deduplication, origin filters or a bounded generation chain through existing facilities. Verify the guard using a representative self-generated output. A cap limits damage but does not itself deduplicate. |

A read-only ticket source remains unwritten regardless of tracker choice. [TRACKERS.md](TRACKERS.md) separates read/comment/create authority and the four storage alternatives. These four conditional requirements apply only in their stated situations; ordinary requests do not inherit unattended operation.

## Selected brakes and human re-entry

When the accepted standards are selected, preserve these obligations until competent authority changes them with rationale and impact under the prior procedure:

- Iterative review has a project-chosen stop bound and human escalation path. Record what is counted, when it is exhausted, who receives the finding/evidence and what decision can resume work.
- Apply the project's selected reversibility model. At levels declared irreversible, obtain human approval before the effect; existing applicable approval can suffice. A locally reversible edit does not make a downstream publication reversible.
- Each applicable task records its stage on the selected ladder. A stage describes adoption, not a permission ceiling. Raising it requires user approval. An observer-like stage is unsuitable for merging.
- Repeated brake failure raises visible **andon**: show the failure, affected task/target, evidence, stopped/uncertain effects, responsible human, safe independent work and re-entry condition. Let the selected response lower a stage, pause or otherwise handle the failure; no automatic lowering rule or universal failure count is imposed.

Use existing visible task/record/human handoff facilities; establish their actual access and delivery limits. A stored message is not proof anyone received it. End an unattended run with a visible handoff when human input is needed; the next authorized trigger resumes from inspected state. Do not create a waiting service or continue an exhausted loop.

For a concrete project, “two failed correction rounds, then hand to the report owner because another pass needs the private source” can be a justified choice. It is an example, not a default. Missing chosen values or actual control mechanisms remain dependent readiness gaps, not silent waivers.

## Adoption and improvement

Use the existing setup/evolve assessment to compare intended outcome, observed evidence, regressions and uncertainty. A drafted contract, applied configuration and useful operational improvement are separate claims. Inspect a small authorized representative task before recommending broader use; preserve negative or inconclusive findings and the next useful evidence step.

Adopt only for granted targets and timing, ordinarily future runs unless a reconciliation boundary or qualified live migration was selected. Stage raising needs the selected user approval; successful tests do not provide it. Repeated brake failure uses the selected andon response. Changes to selected policy follow the prior procedure, not the replacement's self-authorization. Permission withdrawal and stop commands remain immediately relevant to continuing work.

**Done:** the selected functions and controls are usable with project choices and evidence, or design completion is reported alongside specific deployment/readiness gaps. No fixed runtime, automatic workload or formal safety certification follows.
