# Delegation framework

How much an agent may decide on a person's behalf. It has four axes and one seven-step scale. Setting delegation on or off is moving along the scale; nothing else needs to be rebuilt.

**Certainty.** Every row below is `partial`. The sources were read only in part: several came through a summarizing tool, one came as a substitute text rather than the original, and others could not be opened at all (listed at the end). Treat the rows as a starting design to confirm, not as a finished standard.

## The four axes

| # | Axis | Question to ask | Guidance | Certainty | Sources |
|---|---|---|---|---|---|
| 1 | Reversibility | Can the outcome be undone cheaply? | Identify the consequences, restoration path, and cost of reversing the action. Assign consequential or hard-to-reverse choices to a person unless the granted scope explicitly delegates them; allow reversible work within the authority already granted. | partial | Type 1 / Type 2 framing; agent autonomy measurement; Claude Code permission modes; auto mode write-up; Codex approvals page |
| 2 | Information level | Does the agent know enough to decide? | Identify missing evidence that could change the chosen action. Ask when that evidence or a required criterion is unavailable; otherwise proceed within scope and state any material assumption. A fixed information percentage does not establish readiness. | partial | Shareholder-letter rule on 70 percent; autonomy measurement; AI-approvals FAQ; Cynefin domain definitions (inferred as a related axis) |
| 3 | Delegation scale (seven steps) | How is the choice shared between agent and person? | See the scale below. A matching ladder of five human roles exists (operator, collaborator, consultant, approver, observer), and a ten-step automation scale split by function type exists only as a substitute text. | partial | Delegation Poker; autonomy-levels paper; Sheridan-Verplank scale (substitute text) |
| 4 | Permitted zone and escalation threshold | Where may the agent act alone, and when must it stop and ask? | Define authorized actions, accessible resources, and the conditions that require escalation. Technical access does not grant authority; an existing authorization remains valid within its scope. Stop the affected operation when required authority is missing, including in unattended runs. Choose escalation thresholds for the task rather than inheriting a product default. | partial | Codex sandbox and approval policy; auto mode write-up; Claude Code permission modes |

Also cited across axes: one accountable approver per choice (DACI), a record of each choice with its reason (decision records), and an audit log at the highest autonomy levels.

## The seven-step scale

Steps are named from the Delegation Poker levels; the "typical use" column is inferred, not stated by the source.

| Step | Name | Meaning (source wording) | Typical use | Certainty |
|---|---|---|---|---|
| 1 | Tell | "I will tell them" | Hard-to-reverse work where the person decides and the agent only executes | partial |
| 2 | Sell | "I will try and sell it to them" | The agent proposes with reasons; the person still decides | partial |
| 3 | Consult | "I will consult and then decide" | The agent asks for input, then the person decides; a good floor for one-way doors | partial |
| 4 | Agree | "We will agree together" | Joint choice; the agent waits for agreement | partial |
| 5 | Advise | "I will advise but they decide" | The agent decides after the person has given advice | partial |
| 6 | Inquire | "I will inquire after they decide" | The agent decides first; the person reviews afterwards. Fits reversible choices | partial |
| 7 | Delegate | "I will fully delegate" | The agent decides and carries on; use only inside a bounded zone with logging | partial |

## How the axes combine (inferred)

1. Start from axis 1: choose the authority needed for the consequences and reversibility of the action, honoring scope already granted.
2. Apply axis 2: escalate missing information that could change the action; otherwise keep working within the chosen scope and record material assumptions.
3. Set axis 4: name the authorized scope and conditions that trigger escalation; cap how far up the scale an agent may go by task type.
4. Raise a step only after the agent has a record of correct choices for that type of work (situational-leadership reading: ability and willingness for a specific task).
5. Turning delegation off returns the affected choices to the person; granting it selects the scope and reporting behavior for that task. Tool availability alone does not determine the level.

## Not read

These could not be opened or were seen only as second-hand mentions, so nothing here relies on them: original Sheridan-Verplank / PSW table, SAE J3016, Tannenbaum-Schmidt, RAPID, RACI, the army doctrine on commander's intent, OODA, Decision Quality, and the autonomy frameworks of some large vendors. Sources reached through a summarizing tool may differ from the original wording; re-open the original before using any quote as a hard rule. The two defaults conflict: one source favors quick action on reversible choices, another asks before any change to code or systems unless permission was granted for good. No source settles which applies.
