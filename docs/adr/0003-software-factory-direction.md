# Grow harnesses toward a software factory

The product direction is a software factory: tasks that triggers start and that run without a human attending. The first release still runs interactively on the user's machine, but it defines each unit of harness work as a task with its trigger, actions, next trigger, human re-entry point, and duplicate-work guard, with the user's request as the first trigger. Later releases attach real triggers, so the first release's work carries forward instead of being rewritten.

## Considered Options

- Build factories directly for target projects. Rejected for the first release because remote infrastructure and unattended runs need proven brakes first.
- Keep harness-kit interactive and treat factories as a separate product. Rejected because harness work would then need redesign to run unattended.
