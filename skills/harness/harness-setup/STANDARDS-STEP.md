# Standards (step 9)

The harness has its own standard, separate from the product's. It holds only rules a machine can check, and it applies only to changes under `harness/`.

## Choose

1. List what the project chose: the entries in `record/` and the kit pieces behind them (the `choice` of each).
2. Look up rules with the `kit` command (path as in step 2), never `rules.csv` whole:

```
kit list rules              # gate rules only: id, topic, how it is checked, text
kit list rules all          # the topics
kit list rules <topic>      # every rule of one topic; * marks gate rules
kit show <rule id>          # one rule in full, with its verified quote if it is a gate rule
```

3. Offer gate rules first, then other rules whose check is `machine`, and only those that fit a chosen piece. Find the topic by reading the topic list against the piece's `summary` (`kit show <piece id>`); a guessed topic name that errors is not a reason to guess again, run `kit list rules all`. Show each with its id and the sentence it rests on. The user picks; a rule the user does not pick is not written. No fitting rule: say so, write no standard, log `outcome=none`.

## Write `harness/STANDARDS.md`

Line 1, in the user's language: this file applies only to changes under `harness/`. Then one section per chosen rule: kit rule id, the rule in one line, the command that checks it. Existing sections are updated in place, not repeated.

## Record

One entry per standard, `standard-<slug>`, `kind: standard`. `choice` names the section of `STANDARDS.md` (path and heading) and the kit rule id. Do not copy the rule into the entry. `check` is the command from that section, run against the real files. The `gate_*` keys follow the delegation entry: `gate_lighter_rung: none`, `gate_source` the `kit show` command you ran, `gate_approved: user`. Run the check, paste the output, set `status` only after it ran. Add the entry to `record/index.md`. `check` may hold a multi-line command in the section of `STANDARDS.md`; the entry holds the same command. A check that can only inspect the file because the piece is not wired yet (step 11) says so in the section; step 11 supplies the behavioural proof. Log `standards` once, after the last entry, with the entry names comma-separated in `entry=`.
