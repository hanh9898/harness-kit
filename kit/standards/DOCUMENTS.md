# Document checks

Use when selecting or applying document standards. These are six selectable
families, not six mandatory tools or an approval lifecycle. For each applicable
family turn the consumer's existing criteria into an observable expected result
and check route. When proposing a missing criterion, label it as proposed and
explain its value. The [selection procedure](SELECT.md) owns effective selection,
conflicts and evidence state; it also supplies the source/qualification scope.

| Family | Useful check and evidence | Limits and continuation |
| --- | --- | --- |
| Structure/render | Check required sections, hierarchy, tables and format against the output contract. Run the available relevant parser/renderer on the actual version and inspect its output. For visual-layout criteria inspect rendered pages or the target view for clipping, overflow and legibility. | A successful conversion is not a visual inspection. Record renderer/version and inspected output. Missing rendering access leaves render/layout criteria unverified; structural prose is not acceptance. |
| Internal references | Resolve local links, fragment anchors, cross-references and referenced artifacts at the consuming location; inspect missing, ambiguous and stale destinations. Exercise available reference checks and inspect concrete failures. | An existing file can still be the wrong target. Generated anchors, relocation and permission limits need their actual consumer context. External/source access is separately evidenced. |
| Terminology | Compare actual usage with selected glossary and consumer language, including accepted synonyms, units, abbreviations and consistent meanings. Inspect representative ambiguous occurrences, not only word counts. | A literal match does not prove correct meaning. Preserve authoritative terms and flag unresolved definitions; do not impose the kit's English policy on another language. |
| Ownership/freshness | Resolve the accountable owner and actual version/review date; compare against the selected freshness rule and known source changes. Name the owner/action for stale material. | A file timestamp is not a review or owner's acceptance. Without a selected age threshold, report dates/known changes and propose a suitable policy instead of inventing a breach. |
| Editorial versus accuracy | Inspect clarity, consistency and presentation against the output contract. Separately trace substantive claims, quantities and quotations to accessible authoritative sources and record what the comparison establishes. | Under the selected standard, claims about sources only humans hold require real human accuracy review. Missing access means unknown truth, even when prose and automated checks pass. Preserve required reviewer authority/context/independence via team and the versioned review handoff via workflow. |
| Source drift | Compare the source revision used for the artifact with the current authoritative source. Identify changed claims/links/terms and affected criteria; keep the old basis and new evidence attributable. | A different hash detects change, not its meaning; unchanged bytes do not certify human-only facts. Missing historical/current source limits the comparison. Invalidate only affected conclusions and name recheck/review needed before dependent use. |

Reuse accessible tools and native review facilities. Separate a proposed command,
a command actually run, and evidence that its result meets the criterion. Under
a read-only request use permitted inline/output routes; temporary render files,
helper scripts and caches also need an applicable effect grant. If a useful check
requires ungranted scratch or unavailable tooling, expose that exact prerequisite
and continue independent checks. Do not install tools merely to select standards.

A useful result may report: structure parsed and HTML output inspected; one
fragment unresolved; accepted term violated; review stale under the selected
rule; editorial issues observed; an accessible count contradicted; human-only
consent still unknown; source revision changed the count but did not resolve
consent. Those are different conclusions, not a global pass or a claim that the
whole document is inaccurate. Repairs and release follow their actual grants.

A human handoff identifies the artifact/version and claims to review, applicable
criterion/source version, evidence already available, inaccessible source, review
owner/authority and required independence, expected findings or attestation,
blocked downstream decision and next trigger. A designated source holder is not
evidence of performed review. Accept actual review only for its evidenced scope;
a new artifact or source change may require affected re-review.
