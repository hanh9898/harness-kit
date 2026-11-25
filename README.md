# harness-kit

Composable Harness skills using Matt Pocock methods. Devin is the first v1 pilot
host; the suite also packages for Codex, Claude Code and Pi. Registration does
not establish end-to-end support on any host. Original methods are separate
dependencies. The kit does not bundle an execution service.

## Installation

Keep a complete checkout in a stable location: skill references and helpers depend
on the adjacent `kit/` tree. Original methods are separate dependencies.
Harness Setup checks them and can [install missing prerequisites with explicit
permission](skills/harness/harness-setup/ACTIVATION.md#install-required-upstream-skills).
Choose your host below.

### Devin — project scope (v1 pilot)

In an approved project, expose the four skill directories from the full checkout
as project-local skills under `.devin/skills/` using Devin's supported mechanism.
Keep each `SKILL.md` with its references and preserve the adjacent kit paths.
Verify by invoking the exact skill ID in the project and checking the resolved
source and revision or digest; listing/search alone is not proof. Do not register
globally by default.

Setup registers project-scoped, agent-callable preparation and execution
overrides only when authorized. The original user-only methods keep their own
routes. See [activation](skills/harness/harness-setup/ACTIVATION.md) for the
override contracts and verification, and [qualification](docs/harness-v1.md) for
what to test before relying on a route.

### Codex — plugin

Codex accepts this repository's existing Claude-compatible plugin manifest and
marketplace. Register the full checkout and install the plugin with Codex CLI:

```sh
codex plugin marketplace add /absolute/path/to/harness-kit
codex plugin add harness-kit@harness-kit
```

Start a new Codex session after installation. Use `/plugins` to inspect installed
plugins and `/skills` or the `$` skill picker to select a bundled harness skill.
In supported desktop clients, use the plugin browser after registering the local
marketplace. The plugin keeps all four skills, references and kit helpers together.
See [OpenAI's plugin packaging and compatibility documentation](https://developers.openai.com/plugins/build/plugins)
and [plugin usage](https://learn.chatgpt.com/docs/plugins).

#### Alternative: project-local skill links

Use this route when you want direct skill discovery instead of a plugin install.
Choose one registration route for a given project to avoid duplicate skill entries.

Codex discovers `.agents/skills/` and follows symlinked skill directories. Link
these four entries from the consuming project to the full kit checkout
(macOS/Linux shell):

```sh
harness_kit="/absolute/path/to/harness-kit"
project="/absolute/path/to/your-project"
mkdir -p "$project/.agents/skills"
for skill in harness-setup harness-evolve harness-implement harness-library; do
  link="$project/.agents/skills/$skill"
  if [ -e "$link" ] || [ -L "$link" ]; then
    printf 'Already exists; inspect its target: %s\n' "$link"
  else
    ln -s "$harness_kit/skills/harness/$skill" "$link"
  fi
done
```

Start Codex in the consuming project. Use `/skills` or mention the relevant
skill, such as `$harness-setup`, in your prompt. Restart Codex if the new
entries do not appear. Existing entries are left untouched by the commands above;
inspect any reported conflict. Resolve supporting paths from the symlink's real
target directory, as the skills specify. For personal scope, Codex also discovers
`$HOME/.agents/skills/`; choose that scope explicitly instead of changing it as part
of project setup. See the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

### Claude Code — plugin

The repository includes a Claude Code plugin manifest and local marketplace:

```sh
claude plugin marketplace add <absolute-path-to-harness-kit>
claude plugin install harness-kit@harness-kit
```

Restart Claude Code and invoke the relevant skill by its plugin-qualified name,
such as `/harness-kit:harness-setup`.
For session-only use, pass `claude --plugin-dir <absolute-path-to-harness-kit>`.
The `.claude-plugin/` manifest is also accepted by Codex through its compatibility
route above. Pi loads the same skill source through its native skill interface.

### Pi — package

Pi's package mechanism bundles skills and other resources. This repository's
`package.json` declares the same four skill directories as the compatible
Codex/Claude plugin; the shared `kit/` remains alongside them.

From the consuming project, register a local checkout in that project's settings:

```sh
pi install --local /absolute/path/to/harness-kit
```

Or install the repository from Git:

```sh
pi install --local git:github.com/hanh9898/harness-kit@main
```

Use a reviewed commit or tag instead of the branch name when you need a fixed
revision. `--local` writes the package declaration to `.pi/settings.json`; Pi loads
project packages after project trust is granted. Omitting `--local` selects personal
scope.

`pi list` can report `No packages installed.` after a successful local install if
Pi does not yet trust the project. After reviewing the project's Pi configuration
and package sources, run `pi list --approve` from that project if you choose to
trust it for this command. The flag does not save a trust decision.

This repository is not published to npm.
See [Pi packages](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).

#### Alternative: one-session skill directory

For one session without registering a package, start Pi from the consuming project:

```sh
pi --skill /absolute/path/to/harness-kit/skills/harness
```

Invoke the relevant entry, such as `/skill:harness-setup`. Add another
`--skill` for each required original-method
file or directory. Pi also discovers project/user `.agents/skills/` directories;
use `/reload` after changing skill content in an active session. See Pi's
[skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md)
and [CLI resource options](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/cli.md#resource-options).

These are registration and invocation instructions. Each host, configuration and
selected task retains its own access grants and behavioral qualification; loading
a skill does not establish all-host support or authorize its effects.

## Skills

| Skill | Purpose |
| --- | --- |
| [harness-setup](skills/harness/harness-setup/SKILL.md) | Settle a minimum design in two discovery passes and verify initial use. |
| [harness-evolve](skills/harness/harness-evolve/SKILL.md) | Diagnose or improve an existing Harness without replaying onboarding. |
| [harness-implement](skills/harness/harness-implement/SKILL.md) | Prepare, publish or execute approved Harness work through separate gates. |
| [harness-library](skills/harness/harness-library/SKILL.md) | Discover, author and maintain reusable resources with attributable sources and explicit storage scope. |

Setup and Evolve invoke Implement and Library internally where needed. A draft
does not require tracker permission; publishing requires a verified Harness
destination and its own grant; execution requires a canonical ticket, a
verified route and authority at the effect target. Product issues are read-only
references in this workflow, not a fallback tracker. A non-atomic write needs
direct authorized supervision if policy allows it; otherwise it stops. Narrow
advice can finish without a saved record, and saving is not consumer adoption.

## Building blocks

See the [architecture diagram](docs/architecture/harness-kit.png)
([PlantUML source](docs/architecture/harness-kit.puml)) for the package, helper
and consumer-state boundaries.

Start with the [catalog and retrieval interface](kit/README.md). Capability
references include [context](skills/harness/harness-evolve/CONTEXT.md),
[instruction design](kit/instruction-response/DESIGN.md),
[standards](kit/standards/SELECT.md), [team and task contracts](kit/team-workflow/TASKS.md),
[authority](kit/authority/DESIGN.md), [tool operations](kit/TOOL-OPERATIONS.md),
[recovery](kit/RECOVERY.md), [persistence](kit/PERSISTENCE.md),
[maintenance](kit/MAINTENANCE.md), [Bot role templates](kit/README.md#bot-role-templates),
and explicitly selected [factory design](kit/FACTORY.md).

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
