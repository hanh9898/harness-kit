# harness-kit

A lightweight harness plugin for Matt Pocock skills.

Repository source, documentation, examples, commits, issues, and pull requests use English.
Enable local checks after cloning with `git config core.hooksPath .githooks`.
Run `python3 tools/check_english.py --commits --history` to check source and history.
CI also checks pull-request titles and bodies. The automated language check detects
accented text; reviewers also verify that unaccented prose is English.

## Installation

The `harness-setup` and `harness-evolve` skills require explicit invocation (`disable-model-invocation: true`). The kit root is both a Claude Code plugin (`.claude-plugin/plugin.json`) and a local marketplace (`.claude-plugin/marketplace.json`).

```
claude plugin marketplace add <absolute-path-to-harness-kit>
claude plugin install harness-kit@harness-kit
```

Restart Claude Code and invoke `/harness-setup` or `/harness-evolve`. Validate the manifest with `claude plugin validate <harness-kit-directory>`. Installation on other platforms (Codex, Copilot, VS Code, Gemini CLI, `npx skills`) has not been tested.
