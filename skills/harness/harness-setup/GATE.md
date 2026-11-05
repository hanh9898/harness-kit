# Simplicity gate

Run for every item before it is recorded: a tool, a folder, a team shape.

Ladder, lightest first: **instruction-file**, **skill**, **script-cli**, **mcp**. An item at the lightest rung has nothing lighter; write `none` and say why it is the lightest. For a folder item the lighter option is "no new folder, a line in an instruction file". For a team item it is the next simpler pattern in the kit.

For each item:

1. Name the next lighter rung that could do the job.
2. Find out why it is not enough. Do not argue from memory. Open the platform's documentation page, or run the platform's own `--help`, in this turn. A claim about what a platform can or cannot do needs this reading.
3. Write down: the url or the exact command, today's date (`date -u +%F`), and what the page or output said in one or two lines.
4. If the lighter rung is enough, the item moves to that rung and the gate runs again for it.

Show the user one list, one block per item:

```
<item> (<proposed rung>)
  lighter rung: <rung>
  why not enough: <your reading>
  source: <url or command>  read on: <date>
  answer: <what the source said>
```

The user approves, edits or rejects each block. A rejected item, or one the source does not support, is dropped; say so and record nothing for it. After approval write the approved blocks to `harness/gate.md` (temp file, then rename; one `## <item>` section per block with the same five fields). Step 5 copies them into the entries.
