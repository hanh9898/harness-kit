# Inspect two disabled Bot setups

Use the local fixtures to check role and contract selection for two Bots
without creating an automation or contacting an agent host.

1. From the root of a complete checkout with Python 3 and pytest, read the
   supplied role and portable contract:

   ```sh
   python3 -IB kit/scripts/kit show software-factory
   python3 -IB kit/scripts/kit show bot-portable-template
   ```

   These commands read catalog pieces. They do not create Bot configuration
   or grant access to a Library store.
2. Run the Devin and Pi fixture cases:

   ```sh
   python3 -m pytest -q -s -p no:cacheprovider tests/test_m2_quickstarts.py -k disabled_bot_quickstart
   ```

   The fixtures create temporary configurations with all triggers disabled.
   They check that adding the second Bot leaves the first unchanged and that
   preview and smoke readback write no files. The printed times measure
   fixture readback, not native host latency.

In an approved project, H19 authorizes configuration for one exact Bot with
its triggers off. H15 covers a separately approved pilot. H16 covers enabling
one exact trigger after manual and fresh-worker qualification. Leave the
trigger disabled if the route is unqualified. See the [Bot lifecycle gates](../../skills/harness/harness-setup/ACTIVATION.md#configure-and-qualify-a-bot)
and [B8 evidence](../../docs/harness-v1.md#b8-qualification-evidence).

## Devin Setup readback and read smoke

This is a planned native check, separate from the local fixtures above. Run
it only after separate approval for an isolated Devin org or workspace and
synthetic data. Use a consuming project outside the Kit checkout. Stop if
you cannot isolate inherited access, including
[org secrets](https://docs.devin.ai/work-with-devin/bots/connections#secrets).
Identify who can create and configure the Bot, who can perform the read,
who can grant or revoke access at the target, and who can open the evidence.
Agree on the timeout and stop conditions before starting.

1. **Create the test Bot manually.** After approval for host creation, use
   [Create a Bot](https://docs.devin.ai/work-with-devin/bots#create-a-bot)
   and select **Start from scratch**. Do not send a first task or create or
   enable a trigger. Record the host-issued `bot_id` and conversation ref.
   Reopen that exact Bot. Record the owner, workspace, access, current
   **General / Instructions**, **Memory**, **Needs you**, and full trigger
   inventory. Stop if you cannot verify the ID or inventory from the host.
   A name, generic session URL, or Bot self-report is not identity proof.
2. **Verify the Setup route.** Set `KIT` to the checkout pinned at the
   approved SHA. Run `inspect` in
   [Devin project links](../../kit/HOST-ADAPTERS.md#devin-project-links).
   Run the `apply` block only when links are missing and project-local
   registration is separately approved. In the consuming project as the
   intended caller, invoke `skill_invoke({"skill":"harness-setup"})`. Verify
   the exact skill ID, Source, resolved path, SHA, and digest. A matching
   digest in another project is not a match. Select `bot-only/interactive`;
   the consuming project loads the skill, but is not the setup target.
   Resolve missing prerequisites under H3 or stop the dependent step.
3. **Verify two independent selections.** Select
   [Data Analyst](../../kit/BOT-ROLES.md#data-analyst) and the
   [portable Bot contract](../../kit/BOT-TEMPLATE.md) separately. Read each
   selection from the store bound to the exact Bot, scope, and owner.
   Use a separately approved fixture store if one is needed. Set
   `BOT_STORE` to its verified path. Run these pinned, read-only helpers:

   ```sh
   export PYTHONDONTWRITEBYTECODE=1
   for id in data-analyst bot-portable-template; do
     "$KIT/kit/scripts/library" --store "$BOT_STORE" --require-existing-store selection "$id" --source supplied --kit-dir "$KIT/kit" || exit
     "$KIT/kit/scripts/kit" --dir "$KIT/kit" show "$id" || exit
   done
   ```

   The CLI returns snapshots. Build one v1
   [`selection` handoff](../../skills/harness/harness-library/READ.md#selection-handoff)
   per snapshot. Use the verified store and scope refs, the pinned catalog
   SHA as `distribution_revision`, and evidence refs for the readback
   and provenance. Map `revision` to `selection_revision` and
   `current_snapshot.sha256` to `digest`.

   Verify each handoff has the expected canonical ID and supplied source
   and is enabled and available. Match its selection revision, distribution
   SHA, and catalog-row digest to the approved selection. Open the two
   linked sources and verify their digests separately. A configured store
   that is missing, mismatched, unreadable, or not qualified for no-write
   reads blocks apply. If you confirm no store is configured, stop at
   catalog preview.
4. **Apply the disabled configuration once.** Use H2 to confirm the exact
   target, read-only test scope, and design revision. Verify the test tool
   route for the caller without granting data access yet. Obtain H19 for
   the exact Bot, owner, workspace, binding, expected revision, and config.
   Have the authorized operator apply only that configuration through the
   verified host route, such as **General / Instructions**, and record its
   receipt. Do not grant read access, write memory, or send work in this
   step. If apply is uncertain, reconcile at the exact Bot instead of
   applying again.
5. **Read back the effective setup.** Reopen the Bot with an authorized
   caller. Read the exact `bot_id`, binding, effective role and contract
   in **Instructions**, and observed configuration revision. Use the host
   revision or a revision from a canonical configuration source verified
   on the host. A Git SHA, handwritten timestamp, or local draft hash is
   not that revision. Match the observed configuration, role and contract
   IDs, and pinned digest to the approved configuration. Inspect every
   trigger source that can target this Bot, including sources outside
   **Automations**. Each trigger must be disabled or the complete inventory
   must confirm no triggers exist. Confirm **Memory** does not hold the
   fixture value. Observe **Needs you** without creating an ask. A missing
   revision, incomplete inventory, mismatch, or enabled trigger blocks
   the handoff and the smoke.

   Only after successful readback, make the verified binding effective and
   emit one [`bot-setup`](../../kit/STAGE-CONTRACTS.md#setup-or-evolve--bot-operator-bot-setup)
   for the exact Bot. Resolve `instance_id` and all refs to that Bot and
   binding. Fill `disabled_capabilities` from observed IDs, not placeholders.
   Verify the refs and caller access separately from the shape check:

   ```sh
   "$KIT/kit/scripts/check-stage-handoff" --expect-operation bot-setup "$HANDOFF"
   ```

6. **Read one synthetic record.** Separately authorize and grant a test
   connector read access only to `SAMPLE-001`. A B7c smoke can read only with
   existing target authority. To count the read as a B8 pilot, also verify
   H15 for the exact binding, action, scope, fixture, and stop conditions.
   H15 does not grant target access. Record the initial target counters.
   In the verified conversation for the same Bot, the authorized operator
   sends **Read record SAMPLE-001** once. The fixture's value is `jade-17`.
   Do not include the value in the request, Instructions, or memory.
   Within the agreed timeout, confirm the tool returned that exact value
   and the answer matches. Record the final target counters and confirm
   one authorized read by the intended caller and zero business mutations.
   Recheck that all trigger sources remain off.
   A direct user message is not a wake, Tasks dispatch, or trigger enable.
7. **Close the run.** Keep ACL-redacted refs for the Bot, revision, trigger
   snapshots, receipt, single handoff, message, and independent target
   counts. Confirm an authorized recipient can reopen the evidence from
   a new session. A recipient reopening evidence is not a fresh-worker
   qualification. Run any [revocation cases](../../docs/harness-v1.md#record-read-and-revocation-evidence)
   separately. Clean up test access or data only under a cleanup grant.
   Do not delete the Bot or change other Bots. If you have an approved
   comparison Bot, verify it is unchanged. This smoke neither requires H16
   nor satisfies H18, wake, fresh-worker qualification, or blind Eval.

For the evidence, record the host and pin, manual baseline, and actual sample
count. Measure elapsed time from the first pinned selection read to the
final host readback. Compare only runs on the same route. The smoke budget is
two selection reads, one disabled apply, one receipt, and one authorized
fixture read. Preview writes nothing. A passing run has no product, Tasks,
or Inbox writes and no schedule, notification, wake, or other unapproved
effect. Mark the smoke unqualified if it exceeds the budget. Report actual
time and any difference from the baseline without inferring an SLO from one run.
