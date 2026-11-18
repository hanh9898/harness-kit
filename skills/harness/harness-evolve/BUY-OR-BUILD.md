# Buy before build: human decision

Use this shared checkpoint when setup or evolve selects a new or replacement
harness capability, tool, service, integration or custom component. Read `E09`
through the kit CLI. Prefer an adequate existing solution over custom construction;
"buy" includes adopting free/open-source tools, plugins and managed services.

## Establish whether the choice is open

Identify the needed outcome, target, constraints and acceptance criteria. Reuse a
specific applicable human choice already in the request or authoritative record;
name its scope and check that its material assumptions still hold. Routine repairs
within that choice and unchanged reconciliation do not reopen it. A broad request
such as "set up monitoring" or "fix the harness" does not choose buy versus build.

## Prepare a concrete comparison

1. Inspect what the project and host already provide, then search relevant external
   tool/plugin catalogs and primary sources for suitable available alternatives.
   An uninstalled solution is still a candidate. Use the applicable original
   research method when research is needed; keep the search bounded to this need.
   If access or evidence is missing, state the gap rather than claiming nothing
   suitable exists or silently choosing to build.
   Stop when the shortlist supports a decision or a named evidence gap blocks it;
   an exhaustive market survey is not required.
2. Present a small shortlist of named viable options. Cover reuse/configuration,
   adoption of an existing solution, and custom build where justified; allow
   deferral. Do not invent a candidate or fill a quota. For build, state the unmet
   requirement or explicitly requested learning objective and the smallest custom
   part; an adapter may suffice.
3. Compare requirement fit, setup/integration effort, license or service cost,
   permissions/data exposure, maintenance and exit cost. Cite checked sources and
   relevant versions/dates; label estimates and unknowns. Prefer reuse/adoption
   when it meets the criteria at lower total burden. A cheaper fee alone does not
   establish the better fit. Recommend one route and explain the trade-off.

Read-only investigation may proceed within its grants. Purchasing, installing,
starting a trial, provisioning or implementing a candidate requires the applicable
choice and effect authority; comparison alone supplies neither.

## Ask and wait before dependent implementation

Use the available user-input tool, or ask directly if none exists. Give the
concrete options, recommendation, material trade-offs and the decision required.
Ask the human to select or amend the route. Group related choices when that makes
one coherent decision; avoid a question per file or tool call.

Keep the choice pending until the human answers. An agent's recommendation,
another agent's approval, silence or a timeout is not human selection. Continue
only independent authorized work while waiting; do not start the custom build or
adoption whose choice is pending. If the user defers, retain the useful comparison
and name the prerequisite for continuation. Advice-only work can finish with the
comparison explicitly unadopted, without forcing a deployment decision.

Reuse the existing decision record under [UPDATE.md](UPDATE.md), or the
conversation when no save was authorized. Preserve the human's answer, selected
route/target, reason, assumptions and remaining prerequisites. A solution choice
is distinct from permission to spend money, install, access data or change another
consumer; reuse sufficient existing grants and resolve only missing ones. Reopen
the human decision only when a material requirement, cost, access or chosen route
changes, not on every continuation.

**Done to proceed:** an applicable explicit human choice is recoverable and the
dependent effects are authorized. Pending or deferred choices remain blocked for
implementation. Only the chosen scope enters the owning workflow's capture and
execution step.

## Boundary examples

- "Install plugin X for this project" already selects an existing solution; verify
  its identity, fit and actual installation scope without asking the same choice.
- "Add unattended PR monitoring" leaves the solution open: compare the host's
  existing monitoring, suitable external packages and any justified custom gap;
  ask before implementing. No answer means pending, even if build looks simple.
- An unchanged accepted setup needs no new comparison. A new service or custom
  scheduler for that setup does: the adequate foundation does not select it.
