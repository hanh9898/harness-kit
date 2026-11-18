# Team and workflow provenance

Maintainer: harness-kit maintainers. Checked 2026-11-13. These resources are **inferred project synthesis**, not copied methods, formal Kanban certification, universal factory policy or runtime qualification. Original selected methods remain with their providers. Read the relevant source again when its current facts materially affect a decision; inaccessible required material blocks that dependent claim.

## Accepted design authority

| Source | What it determines |
| --- | --- |
| [Spec 15 choices 17, 34, 41–43](https://github.com/hanh9898/harness-kit/issues/15) | Independent team/workflow results, responsibility boundaries, selected controls and tracker applicability |
| [Original task-contract resolution](https://github.com/hanh9898/harness-kit/issues/2#issuecomment-6767291458) | Contract content, location/format alternatives, effective policy, reuse and readiness |
| [Original flow resolution](https://github.com/hanh9898/harness-kit/issues/5#issuecomment-6766748029) | Ten flow functions, four conditional requirements, reuse map and project-chosen values |
| [Recovered selected controls](https://github.com/hanh9898/harness-kit/issues/5#issuecomment-6817464457) | Work-item/brake/andon/adoption families; selected iterative-review, reversibility and stage obligations |
| [Recovered tracker decision](https://github.com/hanh9898/harness-kit/issues/5#issuecomment-6819871633) | Four tracker alternatives, actual source permissions and commitment-point scope |
| [Document review recovery](https://github.com/hanh9898/harness-kit/issues/13#issuecomment-6816002303) | Human accuracy review for human-only sources; editorial review remains distinct |
| [Q113 amendment](https://github.com/hanh9898/harness-kit/issues/12#issuecomment-6769572260) | Selected standards bind until competent authorized replacement with rationale and impact |

These original accepted comments were retrieved through GitHub's API, with URL and revision timestamps retained in the implementation evidence. Their source-recovery accounts are accepted design evidence, not a claim that this implementation re-read the original archived sessions. The historical untracked research files cited in the flow resolution are unavailable in this checkout and checked local history. No claims about their unseen contents or historical source versions follow.

## Primary-source corroboration and adaptation limits

| Retrieved primary source | Narrow finding used here | Adaptation |
| --- | --- | --- |
| [Kanban Guide, May 2025](https://kanbanguides.org/the-kanban-guide/2025.5/) | A workflow defines work items, start/finish, states, explicit flow policy and WIP control; active management includes item age. | Work-item and capacity guidance; values and commitment policy are project choices. Waiting-backlog age differs from the guide's started-item age. This kit does not impose every Kanban practice. |
| [AWS: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) | A caller request identifier distinguishes retries; ambiguous effects need reconciliation; atomic service behavior matters. | Inspect existing effects and identify logical actions before retry. A label, local file or instruction alone is not an atomic remote idempotency guarantee. |
| [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents) | Evaluation loops need criteria; environment feedback and stopping conditions support bounded work. | Reuse P9/rule 5.33, retaining the stronger selected review-stop policy from the accepted design. No source-imposed retry number. |
| [Google SRE: Example error-budget policy](https://sre.google/workbook/error-budget-policy/) | An explicit policy can halt changes for reliability and name escalation. | Evidence-based brake and re-entry guidance. Its example thresholds and service-specific policy are not kit defaults. |
| [Toyota Production System](https://global.toyota/en/company/vision-and-philosophy/production-system/) | Jidoka detects abnormalities and stops; andon makes a problem visible to people who can respond. | An agent-work handoff should identify the abnormality and responsible human. This analogy does not supply a waiting/notification service or force automatic stage lowering. |
| [IHI: Model for Improvement](https://www.ihi.org/library/model-for-improvement) | Aims, measures and testing/adapting changes support improvement. | Compare observed results and regressions before recommending broader adoption; ordinary corrections remain proportional. |
| [OpenAI Symphony specification](https://github.com/openai/symphony/blob/main/SPEC.md) | A repository-owned workflow can coexist with tracker reads, separate agent writes and a human-review handoff. | Reference existing execution facilities and separate tracker authority. This kit does not adopt Symphony's scheduler, schema or tracker product. Moving main was read; version-sensitive integration must be checked again. |

This corroboration is fresh research, not a reconstruction of the missing scratch notes. TOC, DORA and OpenAI governance are named in that historical resolution but are not used here to support uninspected specific claims. Project policy above supplies authority; research supplies rationale, never grants.

## Existing material reused

Retrieve only applicable details through `kit/scripts/kit show <id>`: A04/A05 for briefs and completion; C07 and P8 for roles and review; K01/H07 for effective configuration; E06 for claims; L04 for shared-resource exclusion; D15/D22 for concurrency/caps; J09 for recovery; P9/5.33 for bounded iteration; 6.25 for stopping; A02 for triage; N06/E07/E08 for writing and records. Read each resource's certainty and platform conditions. A script-shaped resource does not require a new script if an adequate manual/native mechanism exists.

The gaps filled here are coherent independently consumable responsibility/task guidance, source/tracker separation, commitment, idempotency/reconciliation, backlog age, trigger-loop prevention and scoped stop/adoption guidance. Existing sources retain their provenance and narrower host claims.
