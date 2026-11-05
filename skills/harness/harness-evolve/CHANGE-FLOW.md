# Change flow (step 3)

The skills are Matt's engineering skills, registered by `setup-matt-pocock-skills` in the `## Agent skills` block. Run them in this order and hand each the change sentence from step 1 and the approved gate evidence from step 2.

1. `to-spec`: turns the change into a spec in the project tracker.
2. `to-tickets`: breaks the spec into tickets in the tracker. Every ticket carries one check, a command that proves it. A ticket without a check is not done being written.
3. `implement`: builds the tickets.

`implement` may tell you to commit; let it, unless the user says otherwise. `to-tickets` may prefer tickets without file paths; a check may still name harness paths. Where files land is the tracker's business (`docs/agents/issue-tracker.md`). Harness files go under `harness/`, never into the product's folders.

Matt's skills may be hand-typed only, or missing in this project. Try them through the Skill tool. If one cannot be called, say which one and why, then produce the same output by hand (a spec file, ticket files, the change) in the shape the tracker file describes, and tell the user the flow ran by hand. Never skip a stage silently.

Log `work` once the tickets are implemented, with `tickets=` and the check commands.
