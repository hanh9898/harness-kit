# harness-kit

A lightweight plugin of composable harness guidance for Matt Pocock skills.
The supplied catalog, rules and references support project onboarding, harness
improvement and reusable resources. Original methods need their own available
provider; this kit does not bundle an autonomous execution service.

## Installation

The repository is both a Claude Code plugin and a local marketplace:

```sh
claude plugin marketplace add <absolute-path-to-harness-kit>
claude plugin install harness-kit@harness-kit
```

Restart Claude Code and invoke `/harness-kit:harness-setup`,
`/harness-kit:harness-evolve` or `/harness-kit:harness-library`.
For session-only use, pass `claude --plugin-dir <absolute-path-to-harness-kit>`.
Keep the full kit tree intact so relative references and helpers resolve.

Other hosts need their own skill registration and original-method access.
Registration and model-selection eligibility do not establish correct execution,
write authority or support for every host and installation route.

## Skills

| Skill | Purpose |
| --- | --- |
| [harness-setup](skills/harness/harness-setup/SKILL.md) | Reuse adequate foundations, fill onboarding gaps and demonstrate selected initial use. |
| [harness-evolve](skills/harness/harness-evolve/SKILL.md) | Diagnose or improve the selected harness capability; ordinary application work keeps its own route. |
| [harness-library](skills/harness/harness-library/SKILL.md) | Discover, author and maintain reusable resources with attributable sources and explicit storage scope. |

Each entry supports explicit invocation and is eligible for model selection on
its stated intent. Narrow advice can finish without onboarding or a saved record.
Saved material is separate from adoption into a consumer.

## Building blocks

Start with the [catalog and retrieval interface](kit/README.md). Capability
references include [context](skills/harness/harness-evolve/CONTEXT.md),
[instruction design](kit/instruction-response/DESIGN.md),
[standards](kit/standards/SELECT.md), [team and task contracts](kit/team-workflow/TASKS.md),
[authority](kit/authority/DESIGN.md), [tool operations](kit/TOOL-OPERATIONS.md),
[recovery](kit/RECOVERY.md), [persistence](kit/PERSISTENCE.md),
[maintenance](kit/MAINTENANCE.md), and explicitly selected [factory design](kit/FACTORY.md).

Use [observation](skills/harness/harness-evolve/OBSERVE.md) and
[assessment](skills/harness/harness-evolve/ASSESS.md) for operating questions;
[bounded experiments](skills/harness/harness-evolve/EXPERIMENT.md) for measured
changes; [adoption](skills/harness/harness-evolve/ADOPTION.md) for consumer updates;
and [library operations](kit/LIBRARY.md) for saved resources and selection.

## Source checks

Run the local source regressions with `python3 -m pytest -q`. They cover catalog
retrieval, library operations, packaged references and validation tools. Generator
checks that require original research reports are conditional on those inputs;
see [generation notes](docs/generation-notes.md). The
[description budget tool](docs/skill-budget.md) measures skill discovery overhead.

These checks do not qualify native host behavior, production reliability or
unattended operation. For an explicitly authorized behavioral assessment, use the
[setup checklist](skills/harness/harness-setup/CHECKLIST.md) or
[evolve checklist](skills/harness/harness-evolve/CHECKLIST.md), choose the relevant
cases and bound the work. Historical execution logs, review dispatches and trial
runners are maintained separately from source.
