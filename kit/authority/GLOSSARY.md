# Harness authority

Terms used to distinguish automation design, task adoption and actual permission.
Accepted sources and operational guidance: [authority design](DESIGN.md).

## Language

**Function ceiling**:
The maximum automation behavior selected for acquisition, analysis, decision selection
or action implementation in a specified task and scope.
_Avoid_: permission level, task stage

**Task adoption stage**:
The selected degree of operational adoption of a task, with its applicable controls.
_Avoid_: function level, authority grant

**Effect grant**:
Actual authority from a competent issuer for specified actions and targets, subject
to its conditions and revocation; effect duration can exceed permission duration.
_Avoid_: tool availability, automation score

**Decision review**:
Assessment of a delegated choice against the authority, information and criteria
applicable when it was made, distinct from application and resulting outcome.
_Avoid_: automatic approval

**Authority calibration**:
Evidence-informed adjustment of reliance and proposed function ceilings for a
particular use, distinct from authorization to adopt the proposal.
_Avoid_: automatic promotion, trust score
