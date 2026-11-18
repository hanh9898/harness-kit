# Instruction and response examples

These invented examples illustrate [the design procedure](DESIGN.md). Substitute
the consumer's actual sources, authority, language and checks. The example names
and values impose no global schema or policy.

## Reconciled English instruction, Vietnamese output

Suppose the project owner explicitly adopted `report-policy` revision 3 for
consumer A. It supersedes revision 2's English JSON preference and requires
Vietnamese Markdown with source attribution and visible missing evidence.
That recorded adoption resolves this conflict; a newer file date alone would not.

Strict English instruction:

> For consumer A's report, read the selected report-policy and the supplied ledger.
> Use Vietnamese Markdown. Preserve the term “hồ sơ”.
> State the supplied count under “Kết quả”. Name its ledger under “Nguồn”.
> List missing evidence under “Còn thiếu”.
> If approval evidence is absent, report that gap and withhold the readiness claim.
> Finish when the report meets the selected content and language criteria.

Illustrative input: ledger `sample-4` contains 12 hồ sơ; approval is unknown.
Acceptable output:

```markdown
## Kết quả
Có 12 hồ sơ. Chưa đủ bằng chứng để kết luận sẵn sàng.

## Nguồn
Sổ sample-4: số lượng hồ sơ là 12.

## Còn thiếu
Chưa có bằng chứng phê duyệt.
```

Externally checkable criteria:

| Criterion | Inspection | Failure and continuation |
| --- | --- | --- |
| Accurate count and attribution | Compare 12 and sample-4 with the supplied ledger | Reject 13 or an invented ledger; correct from the source |
| Language and terms | Inspect Vietnamese prose, the required headings and “hồ sơ” | Reject English JSON despite valid JSON syntax; restore the selected form |
| Honest missing evidence | Check unknown approval remains visible and readiness is withheld | Reject “approved” or missing-equals-zero; obtain evidence before the dependent conclusion |
| Scope | Inspect the actual output and target effects | A dry-run report authorizes no consumer installation or delivery |

Strict English handoff:

> Produce consumer A's report from sample-4 using report-policy revision 3.
> Read the policy before drafting. Keep its Vietnamese headings and term “hồ sơ”.
> This call permits a reply only. Approval evidence is missing.
> Check the count, attribution and missing-evidence statement against the ledger.
> Return the report and any blocker. Delivery needs its own granted tool route.

Flavored human explanation:

> The report keeps missing approval visible so the reader can distinguish a known
> count from readiness. Vietnamese headings fit this audience, while the English
> handoff gives the drafting agent a clear task and stopping point.

## Unsupported precedence

Two applicable sources require evidence retention for 30 and 90 days. Their
owners have equal authority, and neither source establishes priority. The result
is a blocked retention rule with both references and the missing owner's choice,
not a blended 60-day rule or “nearest file wins”. Independent language guidance
can finish. Adopt retention only after a competent authority resolves the rule
under the procedure already in force.

## Content validity and exchanged protocol

For an illustrative `send_report` operation, assume its actual inspected contract
requires a string `body` and a permitted `destination`. A correct Vietnamese
report with no destination passes the report checks but cannot pass that exchange
contract. Preserve the report and resolve the delivery prerequisite before use.

Conversely, a structurally valid exchange containing a fabricated count fails
content acceptance. Successful transport cannot make the count true. Inspect
actual operation effects before retrying an uncertain send. When no exchange
was requested or tested, report protocol validity as unverified or outside the
requested scope, with the missing test if later delivery is intended.
