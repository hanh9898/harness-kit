# harness-kit

A lightweight harness plugin for Matt Pocock skills. Spec: /Users/hanhnt2/Desktop/hbu-1976-control/.scratch/harness-kit/spec.md

## Installation

The `harness-setup` and `harness-evolve` skills require explicit invocation (`disable-model-invocation: true`). The kit root is both a Claude Code plugin (`.claude-plugin/plugin.json`) and a local marketplace (`.claude-plugin/marketplace.json`).

```
claude plugin marketplace add <absolute-path-to-harness-kit>
claude plugin install harness-kit@harness-kit
```

Restart Claude Code and invoke `/harness-setup` or `/harness-evolve`. Validate the manifest with `claude plugin validate <harness-kit-directory>`. Installation on other platforms (Codex, Copilot, VS Code, Gemini CLI, `npx skills`) has not been tested.
