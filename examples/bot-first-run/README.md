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
