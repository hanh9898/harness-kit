# Simplicity gate

Run for every item before it is recorded: a tool, a folder, a team shape.

Ladder, lightest first: **instruction-file**, **skill**, **script-cli**, **mcp**. An item at the lightest rung has nothing lighter; write `none` and say why it is the lightest. For a folder item the lighter option is "no new folder, a line in an instruction file". For a team item it is the next simpler pattern in the kit.

For each item:

1. Name the next lighter rung that could do the job.
2. Find out why it is not enough. Do not argue from memory. Open the platform's documentation page, or run the platform's own `--help`, in this turn. A claim about what a platform can or cannot do needs this reading.
3. Write down: the url or the exact command, today's date (`date -u +%F`), and what the page or output said in one or two lines.
4. If the lighter rung is enough, the item moves to that rung and the gate runs again for it.

Keep one block per item for yourself and for `harness/gate.md` (English keys, for machines and agents):

```
<item> (<proposed rung>)
  lighter rung: <rung>
  why not enough: <your reading>
  source: <url or command>  read on: <date>
  answer: <what the source said>
```

Do not paste that block at the user. Say it in the **evidence block** of [ASKING.md](ASKING.md): in the user's language, conclusion first, needs in plain words (never a piece id), the reliability of each source in one line, and one decision sentence last. Show the full block (id, url, date, exact answer) only if the user asks to see it. The approval covers the whole list; the user may still edit or reject single items.

The user approves, edits or rejects each block. A rejected item, or one the source does not support, is dropped; say so and record nothing for it. After approval write the approved blocks to `harness/gate.md` (temp file, then rename; one `## <item>` section per block with the same five fields). Step 5 copies them into the entries.

## Question sheets (step 3)

### [S09] Approve the evidence list

- Stage: 2/6 Pick one thing to improve and the lightest way to do it
- Helps: nothing heavier than needed is set up; you see why a simpler way would not do
- If skipped: items without your approval are dropped and nothing is recorded or installed for them
- Why: for each item I read the documentation today and compared simpler ways; only you may approve what I found
- Ask: Do you approve what I found for "<needs in plain words>"? (shown in the evidence block form)
- Terms: simpler way = a lighter way to do the same job (a rule in a text file, a reusable instruction, a small script, an outside service, from lightest to heaviest); evidence = the page or command output I read today, with its date
- Enough: ok, or name the items to edit or reject
- Unsure: say "not sure"; I treat those items as not approved
- Suggest: ok for items whose source clearly says what I claim; point out any item whose source only gave a summary
