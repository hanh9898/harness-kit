# Adopt selected material into consumers

Use this branch within evolve for selected updates, parent replacement,
carry-forward or legacy upgrade. Library editing, updating, exclusion, restoration
and promotion manage reusable material; they leave applied consumers unchanged.
An adoption request supplies its own target scope and authority. Keep library
work separate even when composing it within the same request.

## 1. Reconcile selections and live targets

Read the existing consumer records and relevant history, actual applied material,
effective contracts and grants. Identify each target's role, location and consuming
host independently of the invoking host. Reuse adequate legacy foundations and
their discovery routes; fill only gaps that affect this request. A legacy layout
is not a reason to restart onboarding or the old six-module checklist.

Use the [M2 target and runtime contract](../../../kit/M2-CONFIG.md) when
reconciling an affected binding. A target profile describes what changes;
runtime mode describes who is running the work. A persistent caller doing
repo-only work does not authorize Bot changes. Bot-only work uses its owning
workspace and scope without a synthetic repo or Product tracker. If both targets
are affected, reconcile their binding, revision, grant and outcome separately.
Hold only the branch that needs a missing prerequisite; never roll back an
independent Repo effect because a Bot effect failed.

Compare the live target and binding to the original approved scope and basis.
Verify needed unproven routes and reverify any affected route whose host, caller,
source, revision/digest, destination or authority changed, in the actual caller
context for the intended operation.
Keep compatible references and unaffected evidence. An unavailable or ambiguous
route blocks its dependent step; do not reinstall, bootstrap, or substitute
another host, tool or caller to make reconciliation pass.

Read the selected source and complete assembly contents, including applicable
child material. Call `harness-library` for source identity, content/origin
history, lineage and independent selection history in the exact store.
For a configured Library, first verify the pinned store, owner, scope and
identity against the original binding, then use `--require-existing-store`
before `selection` or `selection-history`. Missing, unreadable or wrong-identity
stores block dependent work; none is equivalent to an unconfigured store or
revision 0 from a verified store with no selection row. No fallback store or raw
catalog selection. Reread the scoped
[v1 selection](../harness-library/READ.md#selection-handoff), including source,
canonical ID, effective status and the applicable revisions, digest and lineage.
Base provenance and transformation claims on decoded source values and actual
target bytes. JSON display escaping is not evidence of literal content escapes.
Claim a normalization only when a before/after comparison demonstrates it;
otherwise leave the transformation unestablished. Preserve a mistaken historical
claim with a linked correction when reconciling evidence.
Check the intended store's effective selection even for directly retrieved
supplied material. Preserve disabled selections until explicit authorized
restoration. Exclusion alone neither removes an already-applied consumer nor
revokes its authority; inspect whether that prior use is still valid.

Distinguish historical origin, current library selection and actual target
customization. Preserve valid project-built and personal material; map it to a
resource only when the evidence supports that relationship. Keep unknown origin
and historical verification explicit. A similar name or matching text is not
provenance. Missing old origin can prevent a three-way comparison without
invalidating independently checked personal material or a new selection.

Report known uses only from authorized authoritative records. Name those sources
and their coverage limits; a stale reference is a known recorded use, not proof
of current application. Search only the assigned scope. Neither a list of known
uses nor access to a target grants adoption into it; no global inventory is needed.

**Done:** each assigned target has an inspected applied state, selected candidate,
effective criteria and authority, or an explicit missing prerequisite. Library
facts remain library-owned; consumer application facts remain target-owned.

For a core, standard or provider replacement, nested harness authority or changed
application timing, read [governed replacement](../../../kit/authority/REPLACE.md).
It resolves the minimum-core criterion, prior procedure and each consumer boundary.

## 2. Choose the compatible action per target

Apply evolve's original-method and standards prerequisites before dependent
authoring. Check meaning, dependencies, actual target and existing authority;
textual non-overlap is not semantic compatibility. Keep content/language criteria,
disabled choices, prior authority and change procedure effective until a competent
authorized change supersedes them. Select the application boundary under that
procedure; default ordinary changes to future runs. Stop/revocation still applies.

- **Update:** retain valid target customizations and apply independently compatible
  changes. Leave conflicting parts on a valid prior selection, with the pending
  candidate and consequences explicit. If the prior use is invalid, block that
  dependent use rather than describe retention as safe.
- **Replace parent:** adopt the complete selected new assembly. Preserve prior
  target content in accessible history before replacement; library history alone
  may lack later target-only edits. Old child customizations stay recoverable,
  rather than silently becoming active in the replacement. Check the replacement
  against criteria outside the replaced parent too; conflicts block that target.
- **Carry forward:** use an explicit request and recover the actual historical
  customization. Locate its intended target in the *actual currently applied*
  assembly and check that target's effective contract. A matching library label
  alone is insufficient. Carry only the requested compatible part and preserve
  the rest of the new assembly. Missing targets or incompatible contracts leave
  that carry-forward blocked; retain valid replacement and independent work.

**Done:** compatible actions can proceed under existing grants; each blocked part
names the missing authority, provider, source, target or compatibility decision.
One blocked target does not stop independent authorized targets.

## 3. Capture, apply and reconcile

Use [UPDATE.md](UPDATE.md) for discoverable pre-action capture/readback, the
existing serialization facility, scratch boundaries and result history. Include
the inspected source revision/selection, target state, compatibility basis,
preserved customizations or historical replacement, timing and per-target check.
Reuse adequate references instead of creating a second adoption registry.

Under the same record ownership, reopen live inputs before each dependent effect:
selected source/selection, target, contract and authority can change after a plan.
Compare with the captured basis. Reconcile material differences and refresh the
affected decision before writing; preserve valid late changes. A newly available
library revision is not permission to substitute it for a pinned selection.
Use the [Implement write gate](../harness-implement/WORK.md#write-boundary-and-reconciliation).
Use a target-enforced atomic condition or, when allowed, a live authorized
supervisor for each non-atomic send. Cooperating local record locks alone do
not protect against late writes.

Inspect exact applied artifacts and protected scope, including the library and
unselected consumers. Record each target's selected revision, actual effect,
check result/evidence, remaining blocker and next trigger separately. Distinguish
decision review, application, representative use and measured improvement; a file
comparison establishes only the observed application. Keep former choices and
their authority discoverable when updating the current view.

For a resumed or uncertain action, use [DRIFT.md](DRIFT.md): inspect the actual
effect before retry, retain valid completed work and finish only missing records
or evidence. A completed unchanged resume adds neither an effect nor a duplicate
history event. Reopen a blocker only when new evidence or authority can resolve it.

### Bot binding changes

Only enter this branch for an affected Bot target. Resolve the selected role
and `bot-portable-template` separately through Library, pinning the role and
contract text to the same distribution revision. Hold adoption if either
selection is disabled, unavailable or unverified. When changing hosts, confirm
old triggers are off, drain or fence old work, and reconcile all `Unknown`
effects before the owner rebinds and reads back the disabled configuration.
While draining, the new host may only inspect or run isolated fixtures.
Keep the instance only if the new host can reopen the approved authoritative
records; otherwise an independently authorized new instance needs scope
separation or a stopped old instance. Never copy secrets, grants, transcripts,
or schedules. Do not allow two hosts to send effects for the same scope.

After applying and reading back the changed Bot configuration, hand the operator
one [`bot-setup`](../../../kit/STAGE-CONTRACTS.md#setup-or-evolve--bot-operator-bot-setup)
v1. Reference the
observed instance, scope, adapter and configuration, the pinned template and
contract, accessible evidence and the capability IDs actually read back as
disabled. If readback is incomplete, report the blocker; repo-only and
unchanged runs do not emit `bot-setup`. For example:

```json
{
  "version": 1,
  "operation": "bot-setup",
  "instance_id": "bot:workspace",
  "template_ref": "catalog:software-factory@kit-1",
  "contract_ref": "catalog:bot-portable-template@kit-1",
  "scope_ref": "scope:harness",
  "adapter_ref": "adapter:workspace@1",
  "configuration_ref": "configuration:workspace@2",
  "evidence_refs": ["evidence:configuration-readback@2"],
  "disabled_capabilities": ["wake"]
}
```

Configuration is not activation. Keep affected triggers disabled until manual
qualification, fresh-worker checkpoint readback and deduplication checks have
passed, and the operator has separately granted and verified each trigger.

**Done:** each assigned target has honest applied or blocked state with inspectable
evidence and continuation; known-use coverage and unverified hosts/uses remain
explicit. Report partial adoption as partial even when the library update is complete.
