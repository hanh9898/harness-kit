# Draft a spec and tickets with the Devin fixture

Use this fixture to check the handoff from a design decision to inline drafts
for a verification summary. It does not invoke Devin or write to a tracker.

1. From the root of a complete checkout with Python 3 and pytest, validate the
   shape of [the prepare handoff](prepare.json):

   ```sh
   kit/scripts/check-stage-handoff examples/devin-prepare/prepare.json --expect-operation prepare
   ```

   The command exits zero for a valid envelope. It does not open references
   or grant approval.
2. Run the fixture that opens [the pinned decision and route records](decision.json)
   and replays the approval cases:

   ```sh
   python3 -m pytest -q -p no:cacheprovider tests/test_m2_quickstarts.py -k devin_prepare
   ```

   The replay selects [the spec route](harness-m2-to-spec/SKILL.md) if the
   spec is missing. It waits at H5 before selecting [the ticket route](harness-m2-to-tickets/SKILL.md).
   Approval for an older spec revision does not unlock the ticket route.
   The fixture also checks that a resumed run can reopen its source records.

The example skills are not default entries. To try the route in Devin, use
an approved project-local binding and verify the exact caller, skill ID, and
source as described in the [host adapters](../../kit/HOST-ADAPTERS.md#load-internal-routes-on-demand).
Keep the result inline unless you have permission to store it. Publishing
requires a separate grant for the verified Harness destination.
