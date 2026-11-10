# Assemble every harness, factory and harness-kit included, from kit pieces

Harness-kit designs every capability as kit pieces that a project assembles, and this includes software-factory capabilities such as flow control, brakes, and orchestration. Each function offers alternative pieces. A project fills each function with a piece, or records it as deliberately unused with a reason. The kit fixes only mandatory requirements, and each one applies under a stated condition. Values such as limits and counts are the project's recorded choice: a piece explains how to choose a value, not which value to use. Different assemblies are therefore valid, at the cost of each project recording and justifying its own choices.

The rule also covers harness-kit's own behavior: evolve routing, setup order, the list of unlocked Matt skills, result presentation, and the review chain form a recommended assembly in the kit, which users override through personal customization (ADR 0002). Only a small core stays fixed:

- the mechanisms: the evolve entry point, library management, and reading an assembly;
- the product's own conditional mandatory requirements: `writing-for-agents` for any change to a file an agent reads; distinct proposed, applied, and verified states; no upgrade of a state or of source certainty; write scope granted by the user; and the Matt restriction check before routing.

## Considered Options

- Ship one prescribed factory or harness shape with default mechanisms and values. Rejected on 2026-11-10 while resolving hanh9898/harness-kit#5: projects differ in trackers, permissions, review capacity, and hosts, and a fixed shape would fit some projects and force workarounds on others.
- Apply the rule only to project harnesses and keep harness-kit's own behavior fixed. Rejected because it would need a second customization mechanism and would stop harness-kit from building itself the way it teaches. The cost accepted: per-host verification tests the recommended assembly, and a user's own assembly relies on its self-checks.
