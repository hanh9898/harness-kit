# Harness Kit

Harness Kit gives agents four skills for setting up, maintaining, and retrieving
resources for a project's development workflow. It includes a
[read-only catalog CLI](kit/README.md#look-something-up). The kit does not
include an execution service or a tracker.

## Try it without an agent host

From the root of a complete checkout, run this command with Python 3:

```sh
python3 -IB kit/scripts/kit show project-instructions
```

The command prints the supplied project-instructions piece. It does not install
skills, open a Library store, or write to the checkout. For more local exercises,
see [draft a spec and tickets](examples/devin-prepare/README.md) and
[inspect two disabled Bot setups](examples/bot-first-run/README.md).

## Register skills in one project

Pin a complete checkout to a reviewed commit. Keep each skill next to its
references and the shared `kit/`; copying a skill directory alone can break its
helper paths. Get approval for the project registration before applying it.
Choose one route per host. None of these routes is native-qualified by B8.

### Devin: project-local links

Use [Devin project links](kit/HOST-ADAPTERS.md#devin-project-links). Run the
read-only inspection first. Apply the links only after the project owner
approves the change. Check exact-ID invocation and Source in that project.
A list of skills does not prove which copy Devin loaded.

<a id="codex--plugin"></a>

### Codex: plugin

Register the full checkout as a local marketplace, or use project-local links
under `.agents/skills/`. Use one route, not both. Verify the source in a new
project session. See the [adapter guide](kit/HOST-ADAPTERS.md#select-one-entry-route)
and the Codex guides for [local plugins](https://developers.openai.com/plugins/build/plugins)
and [skill locations](https://developers.openai.com/codex/skills).

<a id="claude-code--plugin"></a>

### Claude Code: plugin

Register the local marketplace at project scope, or load the checkout for one
session through the plugin directory option. Verify the plugin-qualified skill
name and source. See the [adapter guide](kit/HOST-ADAPTERS.md#select-one-entry-route)
and [Claude Code plugin guide](https://code.claude.com/docs/en/plugins).

<a id="pi--package"></a>

### Pi: package

Use a project-local package or load the skill directory for one session. Confirm
the package source and review the project's trust settings before loading it.
See the [adapter guide](kit/HOST-ADAPTERS.md#select-one-entry-route) and
[Pi package guide](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md).

## Choose a skill

For a repository request, start with the `repo-only` profile in an
interactive session unless the current mode is already known. Use
`bot-only` for work bound to a Bot without a repository, or `repo-and-bot`
when both targets are in scope. See the [profile and mode examples](kit/M2-CONFIG.md#target-profile-examples).

| Default entry | Use it to |
| --- | --- |
| [harness-setup](skills/harness/harness-setup/SKILL.md) | Design an initial project workflow and verify an approved setup. |
| [harness-evolve](skills/harness/harness-evolve/SKILL.md) | Diagnose or change an existing workflow without repeating setup. |
| [harness-implement](skills/harness/harness-implement/SKILL.md) | Draft work, publish to a verified Harness tracker, or execute a canonical ticket. Each action has its own gates. |
| [harness-library](skills/harness/harness-library/SKILL.md) | Find supplied pieces or work with saved resources in an approved store. |

Setup checks for the [required upstream skills](skills/harness/harness-setup/ACTIVATION.md#install-required-upstream-skills).
It installs a missing prerequisite only with permission. Inbox and Memory are
[opt-in](kit/HOST-ADAPTERS.md#select-one-entry-route). Setup loads discovery
skills as needed. Use a project override only after its route is verified;
do not add discovery or override directories to the default inventory.

A draft needs no tracker write. Publishing needs a separate grant at the
Harness destination; never use a product tracker as a fallback. Execution
needs a canonical ticket, a verified route, and authority at the effect target.

## Check the source

Run these checks from the root of the checkout. Install pytest in your
Python environment first.

```sh
python3 -I tools/check_boundary.py --strict
python3 tools/check_kit.py --dir kit
python3 tools/skill_budget.py
python3 -m pytest -q -p no:cacheprovider
```

The [B8 evidence and pilot runbook](docs/harness-v1.md) separate local and
fixture results from unqualified native routes. The
[architecture package](docs/architecture/harness-v1-stage-2a-index.md)
links the locked design and diagrams.
