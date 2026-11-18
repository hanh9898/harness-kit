# harness-kit

Composable harness skills for Codex, Claude Code and Pi, using Matt Pocock methods.
The supplied catalog, rules and references support project onboarding, harness
improvement and reusable resources. Original methods need their own available
provider; this kit does not bundle an autonomous execution service.

## Installation

Keep a complete checkout in a stable location: skill references and helpers depend
on the adjacent `kit/` tree. Register the original methods you intend to use through
the same host; they are separate dependencies. Choose your host below.

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
marketplace. The plugin keeps all three skills, references and kit helpers together.
See [OpenAI's plugin packaging and compatibility documentation](https://developers.openai.com/plugins/build/plugins)
and [plugin usage](https://learn.chatgpt.com/docs/plugins).

#### Alternative: project-local skill links

Use this route when you want direct skill discovery instead of a plugin install.
Choose one registration route for a given project to avoid duplicate skill entries.

Codex discovers `.agents/skills/` and follows symlinked skill directories. Link
these three entries from the consuming project to the full kit checkout
(macOS/Linux shell):

```sh
harness_kit="/absolute/path/to/harness-kit"
project="/absolute/path/to/your-project"
mkdir -p "$project/.agents/skills"
for skill in harness-setup harness-evolve harness-library; do
  link="$project/.agents/skills/$skill"
  if [ -e "$link" ] || [ -L "$link" ]; then
    printf 'Already exists; inspect its target: %s\n' "$link"
  else
    ln -s "$harness_kit/skills/harness/$skill" "$link"
  fi
done
```

Start Codex in the consuming project. Use `/skills` or mention `$harness-setup`,
`$harness-evolve` or `$harness-library` in your prompt. Restart Codex if the new
entries do not appear. Existing entries are left untouched by the commands above;
inspect any reported conflict. Resolve supporting paths from the symlink's real
target directory, as the skills specify. For personal scope, Codex also discovers
`~/.agents/skills/`; choose that scope explicitly instead of changing it as part
of project setup. See the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

### Claude Code — plugin

The repository includes a Claude Code plugin manifest and local marketplace:

```sh
claude plugin marketplace add <absolute-path-to-harness-kit>
claude plugin install harness-kit@harness-kit
```

Restart Claude Code and invoke `/harness-kit:harness-setup`,
`/harness-kit:harness-evolve` or `/harness-kit:harness-library`.
For session-only use, pass `claude --plugin-dir <absolute-path-to-harness-kit>`.
The `.claude-plugin/` manifest is also accepted by Codex through its compatibility
route above. Pi loads the same skill source through its native skill interface.

### Pi — explicit skill directory

From the consuming project, start the already installed Pi with the full skills
root:

```sh
pi --skill /absolute/path/to/harness-kit/skills/harness
```

Invoke `/skill:harness-setup`, `/skill:harness-evolve` or
`/skill:harness-library`. Add another `--skill` for each required original-method
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
