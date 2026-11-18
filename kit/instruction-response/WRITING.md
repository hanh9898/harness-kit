# Writing scope

Apply this recommendation with current original writing-for-agents, not as its
replacement. The [accepted STE recovery](https://github.com/hanh9898/harness-kit/issues/13#issuecomment-6815333220)
records strict English agent instructions and inter-agent handoffs, flavored
human documentation, and structural habits for Vietnamese conversation.
It reports curated historical records, not a complete provider transcript.
[Spec 15, decision 37](https://github.com/hanh9898/harness-kit/issues/15) retains
that meaning. The habits below are the kit's inferred operational guidance;
they are not an ASD dictionary, a source-linter dependency or formal certification.

## English instructions and agent handoffs: strict

- Name the actor and action. Use direct verbs and one action per instruction.
- Put a condition next to the action it controls. Make order and prerequisites
  explicit when one action depends on another.
- Use one stable term for each concept. Define necessary technical terms from
  the consumer's own vocabulary; preserve identifiers and literal output keys.
- State inputs, allowed effects and observable completion. Replace vague success
  claims with criteria that another consumer can check.
- Keep warnings beside the affected action. State the safe next action when an
  input, authority, method or evidence is missing.

Check for ambiguous actors, hidden prerequisites, conflicting terms and steps
whose completion cannot be determined. Short wording must retain necessary
authority, uncertainty and source context. Strict structure is a writing choice,
not an execution or permissions mechanism.

## Human-facing documentation: flavored

Keep clear terms, explicit conditions and useful structure. Use connected prose,
examples and varied sentences to explain reasons and trade-offs for the reader.
Do not turn a human explanation into a forced sequence of commands. Preserve
the selected audience, tone, content, source and language requirements.

## Vietnamese conversation and consumer language

Use structural habits: clear sections, one point at a time, explicit conditions,
consistent Vietnamese terms, attribution and honest unknowns. Do not import
English vocabulary restrictions or translate the consumer's output to English
because the instructions are English. An English agent handoff can require a
Vietnamese deliverable. Check the instructions and that deliverable against
their own selected language/content criteria.

**Done:** select scope per artifact and inspect actual examples/results. Keep
exceptions explicit where a consumer criterion requires a different form;
resolve a real authority conflict under [the design procedure](DESIGN.md).
