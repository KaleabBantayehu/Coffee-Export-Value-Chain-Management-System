# 06 — Failure and Escalation

## Purpose

Defines what happens the moment any execution step surfaces a problem an
agent is not authorized to resolve on its own: a missing precondition, a
document conflict, a scope question, or a discovery that the approved plan
does not actually work. This is not a rare-path document — every other
file in this directory routes here whenever it says "stop and report."

## The Governing Rule

> The agent must STOP rather than silently change the project when it
> discovers a problem. Only the human/project manager may approve a scope
> or architecture change.

Stopping is not a failure of the agent; continuing past an unresolved
problem is.

## When to Escalate

Escalate immediately, per `.agents/rules/06-change-control.md`, on
discovering any of the following:

- A missing requirement.
- A contradictory requirement (including anything already listed under
  "Known documented conflicts" in `00-execution-overview.md`, if the
  current task touches that area).
- A missing dependency that the task assumed would already exist.
- An architecture problem (the approved design does not actually fit what
  is being built).
- A technology limitation (the frozen stack cannot do something the task
  needs).
- A task dependency that was not documented in the task file's own
  `Dependencies` section but turns out to be real.
- A requirement that appears to require scope expansion to satisfy
  properly.
- A task whose objective already appears satisfied by existing code
  (see `01-agent-start-procedure.md` Step 4) — this is not a defect to
  hide by re-implementing anyway; it is a finding to report.

## The Report Format

```text
Issue:
Evidence:
Affected documents:
Why it blocks implementation:
Possible options:
Recommended action:
```

Notes on each field:

- **Issue** — one or two sentences, precise, not vague ("the task cannot
  proceed" is not an issue statement; "the `Role` table has no column for
  X, which `AUTH-005` needs" is).
- **Evidence** — the actual conflicting text, file, query result, or test
  output. Quote the specific lines from the specific documents, not a
  paraphrase.
- **Affected documents** — every document involved, with their hierarchy
  level from `00-execution-overview.md` (this determines whether the
  hierarchy can resolve it or whether it must go to the Project Manager
  as a same-level conflict).
- **Why it blocks implementation** — concretely, what cannot be done
  correctly until this is resolved.
- **Possible options** — the realistic ways this could be resolved,
  including "do nothing / defer," stated neutrally, without the agent
  picking a winner.
- **Recommended action** — the agent may suggest which option looks best
  and why, but this is a recommendation for the Project Manager, not a
  decision the agent is authorized to act on.

## Who Resolves It

**Only the Project Manager (Kaleab) may authorize a controlled scope,
architecture, or baseline change**, per `.agents/rules/06-change-control.md`.
This applies even to conflicts between two Level 3 documents where neither
is obviously "more authoritative" — the hierarchy in
`00-execution-overview.md` does not adjudicate same-level conflicts, and
no agent or individual team member other than the Project Manager may.

## What Happens While Escalated

- The task pauses at the point the issue was found. Work already completed
  up to that point is preserved (committed to the feature branch, not
  discarded), but the branch is not merged.
- The agent does not attempt a workaround that avoids the conflict without
  resolving it (e.g., building against an assumed answer "for now" and
  planning to fix it later) — an unresolved conflict blocks the affected
  part of the task, not the whole repository; unaffected, already-approved
  parts of the same task may still be completed and reported if genuinely
  independent.
- The task resumes only once the Project Manager's decision is recorded
  (per `.agents/rules/06-change-control.md`'s "Recording changes"
  requirement) and, if it changes a task file, the Project Manager (not
  the agent) updates that task file.

## CEVCMS V1.0 Is Frozen

Every escalation is handled with this constraint in view:

> **CEVCMS V1.0 is frozen.** Do not change the version number. Do not
> create V1.1, V2.0, or alternative scope. Do not use the change-control
> process to introduce features. If a change becomes necessary, it happens
> through change control while preserving the V1.0 baseline, unless the
> Project Manager formally authorizes a baseline change.

An escalation's "recommended action" should default toward the option that
preserves V1.0 as already scoped (e.g., defer, simplify further, or narrow
further) over the option that expands it, consistent with
`.agents/rules/01-scope-boundaries.md`'s "honest about limits" principle
and the Design Document's own stated design principle of the same name.

## Recognized Project-Level Risks (from the Minimum Project Plan V1.0)

These are not new risks discovered by this execution procedure; they are
the project's own, already-identified risk register (Minimum Project Plan
§4.3), restated here because several of them are exactly the failure modes
this execution directory exists to catch early rather than in Week 4:

| ID | Risk | Probability | Impact | Mitigation (as stated in the Minimum Project Plan) |
|---|---|---|---|---|
| RSK-01 | One month is not enough time to complete even the core scope. | Medium | High | Core scope limited to 3 modules; stretch scope explicitly deferred first if time runs short. |
| RSK-02 | Scope creep — team adds SRS features beyond the agreed scope. | Medium | Medium | All tasks traced to an in-scope FR ID; the PM rejects untraced tasks at weekly review. |
| RSK-03 | Integration problems when merging Auth, Farmer Registry, and Traceability modules. | Medium | Medium | Shared API contracts and DB schema agreed at design time (M3); integration attempted incrementally from Week 2, not left to Week 4. |
| RSK-04 | Database or backend defects discovered late (e.g., PostGIS polygon logic). | Medium | Medium | Early spike/prototype of polygon-capture and EUDR-flag logic in Week 1-2; unit tests written alongside the code, not after. |
| RSK-05 | Team coordination issues or uneven workload across 7 members. | Low | Medium | Fixed module ownership with shared cross-cutting duties; PM tracks task completion at each weekly meeting. |
| RSK-06 | Testing delayed to the last days of the project. | Medium | High | Testing is a continuous activity, not a Week-4-only activity; each module unit-tested as completed. |
| RSK-07 | Technical learning curve for GIS/PostGIS or QR/cryptographic signing. | Medium | Medium | Time-boxed Week 1 design spike; fallback to a simplified area/point-radius EUDR check if full polygon topology validation is not feasible in time. |
| RSK-08 | Dependency on client/supervisor scope confirmation at M3. | Low | High | Draft scope decision proposed by the project group ahead of M3, so confirmation (not fresh scoping) is what is required from the client. |

**RSK-02 is directly implemented by this `.agents/` control system as a
whole** — the traceability requirement in every task file, and the
Mandatory Scope Test in `02-task-execution-procedure.md`, exist specifically
to make "the PM rejects untraced tasks" enforceable continuously rather
than only at a weekly review. An agent that finds itself about to implement
something it cannot trace to an in-scope FR ID is, by definition, looking
at RSK-02 materializing — escalate rather than proceed.

**RSK-06 is directly implemented by `03-verification-and-testing.md`** —
testing is required per task, not deferred to a final pass.

## Escalating a Blocked Human Gate

If a human reviewer is unavailable and a task is complete and reported per
`04-human-review-and-approval.md`, the task waits. An agent does not
substitute its own approval to keep moving, regardless of schedule
pressure from the one-month timeline (RSK-01/RSK-06 above) — schedule
pressure is a reason to escalate the review bottleneck itself to the
Project Manager, not a reason to bypass review.
