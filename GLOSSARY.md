# Harness-kit

Vocabulary for the harness-kit product and the environment in which its users run it.

## Harness and kit

**Plugin**:
The harness-kit product that provides setup and evolution workflows to a coding agent.

**Host**:
The coding-agent application in which a user runs the plugin.
_Avoid_: Platform, when referring specifically to the coding-agent application.

**Harness**:
The project-specific working environment around an agent, including the instructions and tools that support its work.

**Kit**:
The library of resources used to design, build, and review harnesses, including reusable pieces and the standards governing their use.

**Resource**:
Reusable knowledge or building material for harness work, including pieces, rules, delegation guidance, and workflows.

**Core resources**:
The resources supplied and maintained as part of harness-kit.

**Personal resources**:
Harness resources that a user maintains for their own use.

**Piece (LEGO piece)**:
A reusable building block that can be combined with other pieces to form a project harness.

**Assembly**:
A combination of harness pieces arranged to meet a project's needs.

**Recommended assembly**:
The assembly the kit proposes for a capability, which a project or user may replace with its own.
_Avoid_: Default configuration, preset

**Standard**:
A shared requirement governing a harness or its pieces wherever that requirement applies.

**Recommendation**:
Guidance for a harness design choice that permits an alternative with a recorded rationale.

**Verification**:
An evidence-based assessment of whether a harness piece or assembly satisfies its intended behavior and applicable standards.

**Record**:
The project's durable account of selected harness pieces, applicable standards, decisions, and verification evidence.

**Capability**:
An ability available in a host session that a selected harness workflow requires or can optionally use.

**Workflow**:
The set of tasks in a project and the triggers, handoffs, and human re-entry points that connect them.

**Harness location**:
The directory or repository that holds a project's harness files, record, and decision log.

**Target**:
A repository or folder that a harness works on, with its own role and write permission.

**Decision log**:
The single record of choices an agent made on a person's behalf, with their review status.
_Avoid_: Ledger, choice log

**Evolve**:
The harness workflow through which a user investigates, designs, changes, or reviews their harness by expressing the intended outcome.

## Software factory

**Software factory**:
A system of agents that turns tickets, pull requests, and schedules into completed work without a human attending each run.
_Avoid_: Pipeline, automation

**Task**:
A kind of work defined once and run many times, such as explore, implement, review, or rework.
_Avoid_: Job, workflow, action

**Factory direction**:
A project's recorded answer to whether it aims to grow a software factory: yes, not now, or no.

**Task stage**:
How far one task has moved toward unattended operation, from manual work to chained runs with a human only at irreversible points.
_Avoid_: Autonomy switch, automation mode

**Handoff state**:
The named state in the ticket tracker or git host in which a run ends and from which a human or another run continues.

**Commitment point**:
The point from which a ticket counts as committed work and falls under the project's flow limits; before it, a ticket is only an option.

**Claim**:
An actor's reservation of a ticket before working on it, so that no other run or session takes the same ticket.
_Avoid_: Lock, reserve

**Flow function**:
One of the functions that keep work flowing without duplication or overload, such as claim or reconciliation, which each assembly fills with a piece or records as deliberately unused.

**Trigger**:
The event that starts a run: a change in the ticket tracker or git host, a clock, another run, or a user's direct request.

**Run**:
One execution of a task from its trigger to its finish; it ends instead of waiting for a human.
_Avoid_: Session

**Runner**:
The machine or workspace on which a run executes, intended to keep nothing after the run.
_Avoid_: Host, server, sandbox

**Orchestrator**:
The component that receives triggers, starts runs on runners, and tracks which runs are queued, in progress, or finished.
_Avoid_: Dispatcher, scheduler, control plane

**Ticket tracker**:
The service where tickets live and through which humans schedule work and respond to agents.
_Avoid_: Issue tracker, project board

**Ticket source**:
Anything outside the factory that creates tickets, such as a feedback form, monitor, or inbox.
_Avoid_: Intake, data source

**Git host**:
The service where branches, pull requests, and reviews live.
_Avoid_: Code host, forge

**Observability platform**:
The optional service where runs send logs, traces, and status for humans to inspect.
_Avoid_: Monitoring, dashboard
