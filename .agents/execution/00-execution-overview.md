# 00 — Execution Overview

## Purpose

This directory (`.agents/execution/`) defines the mandatory procedure by
which an AI coding agent — or a human developer working the same way — takes
one already-approved CEVCMS V1.0 task from `.agents/tasks/` and turns it
into reviewed, merged code. It does not decide _what_ gets built (that is
`.agents/tasks/`); it does not decide _the rules code must follow_ (that is
`.agents/rules/`); it decides _how a task moves from "assigned" to "merged"
without drifting from either_.

> **AI agents execute approved tasks; they do not redefine project scope.**

This is the single sentence every other file in this directory exists to
enforce.

## Scope

This procedure governs execution of tasks in `.agents/tasks/EPIC-0/` and
`.agents/tasks/EPIC-1/` (and any later EPIC directory created the same way).
It does not itself contain scope, technology, or architecture decisions —
those live one level up, in `.agents/rules/` and the authoritative project
documents. Where this procedure needs to state a fact from those documents
(e.g., a milestone date), it cites the source; it does not restate policy
that could drift out of sync with the source.

## Relationship with `.agents/rules/`

`.agents/rules/` defines the durable, project-wide constraints: what is in
scope, what technology is frozen, how code should be written, how git and
testing and change control work. This execution directory assumes all of
`.agents/rules/` and does not repeat it — every step below that says "per
the rules" means the corresponding rule file governs and this directory
does not restate it. If anything in this directory ever appears to conflict
with `.agents/rules/`, `.agents/rules/` wins, and the conflict must be
reported (see `06-failure-and-escalation.md`), not silently worked around.

This execution directory also acknowledges the newly available Minimum
Project Plan V1.0 and the current decisions document
`.agents/rules/07-current-project-decisions.md` as the authoritative
schedule and implementation-reference sources for CEVCMS V1.0. Execution
is aligned to the confirmed one-month/four-week plan, the frozen
technology stack, the frozen core workflow, the four V1.0 roles
(Admin, ECTA Officer, Field/Registry Agent, Verifier), Abel's current
Frontend / Full-Stack Support role for the core implementation, the
Leaflet / React-Leaflet mapping decision, and the existing repository,
branches, frontend, backend, and dependency environments already
established by EPIC-0.

## Relationship with `.agents/tasks/`

`.agents/tasks/<EPIC>/<TASK>.md` files define _what_ a specific task is:
its objective, allowed scope, acceptance criteria, and traceability. This
execution directory defines the _process_ used to carry out any task file,
regardless of which one. A task file is never modified by the execution
procedure; if a task file itself needs correcting, that is a change-control
matter (`.agents/rules/06-change-control.md`), decided by the Project
Manager.

## Authority Hierarchy

This hierarchy governs every execution decision. Where two documents
conflict, the document in the higher (lower-numbered) level governs — see
"Conflict Handling" below for what happens when the hierarchy does not
cleanly resolve a conflict (e.g., between two documents at the same level).

```text
Level 1 — University assignment authority
  1. Assignment Description (ECTA-CEVCMS-AD-V1.0)

Level 2 — Approved CEVCMS requirements
  2. Software Requirements Specification (SRS, ECTA-CEVCMS-SRS-V2.1)

Level 3 — Approved project/design baseline
  3. Minimum Project Plan V1.0
  4. CEVCMS V1.0 Baseline Scope Freeze
  5. CEVCMS Design Document V1.0

Level 4 — Approved implementation planning
  6. CEVCMS V1.0 Implementation Specification
  7. CEVCMS V1.0 Implementation Playbook
  8. Development Backlog / EPIC task specifications (.agents/tasks/)

Level 5 — Agent execution controls
  9. .agents/rules/
 10. .agents/execution/ (this directory)
```

**This execution procedure sits at the bottom of the hierarchy.** It never
overrides Levels 1–4. If following a step in this directory would require
contradicting a higher-level document, the step is wrong and must be
reported, not followed.

## Conflict Handling

1. Identify the exact conflicting statements and which documents they come
   from.
2. If the documents are at different hierarchy levels, the higher level
   (lower number) governs — proceed under it, and record the conflict in
   the task's report (see `04-human-review-and-approval.md`) so a human
   sees it even though it was resolved.
3. **If the documents are at the same hierarchy level** (for example, two
   Level 3 documents), the hierarchy does **not** resolve the conflict.
   **Stop.** Do not guess which one is "more recent" or "more specific" as
   a substitute for a real decision. Report it per
   `06-failure-and-escalation.md` and wait for the Project Manager.
4. Never resolve a conflict by blending both positions into a third,
   invented one.

### Known documented conflicts (identified during this review — not yet resolved by the Project Manager)

These were found while incorporating the actual Minimum Project Plan V1.0
into this execution procedure. They are recorded here, at the top level of
the execution system, so no individual task execution has to rediscover
them. **None of these has been resolved. An agent encountering the affected
area must stop and follow `06-failure-and-escalation.md`, not pick a side.**

1. **Abel Debalke's primary role (Level 3 vs. Level 3).**
   Baseline Scope Freeze §5 describes Abel as _"Frontend / Full-Stack
   Support. Supports Biniyam on reusable components, form validation, and
   API integration; may take stretch-module frontend or backend work only
   once the core chain is functional and only with the Project Manager's
   approval."_ The Minimum Project Plan's team table (§0, project data)
   describes Abel's **Primary Role** as _"Backend Developer"_ and his
   **Primary Module/Area** as _"Stretch: Quality Grading & Waybill Issuance
   (FR-QUAL, FR-LOG)"_ — not conditional, not framed as secondary to
   frontend support. Both documents are Level 3. This affects who owns any
   future EPIC-7 (Quality Grading & Waybill) task and whether Abel's early
   weeks are frontend-support work or stretch-backend design work. **Not
   resolved. Escalate before assigning Abel a task in either direction if
   ambiguity would matter.**

2. **RBAC role list used for testing (Level 3 vs. Level 3).**
   Baseline Scope Freeze, Design Document §4.1, and the already-committed
   `.agents/tasks/EPIC-1/00-epic-overview.md` all fix the V1.0 role model
   to exactly four roles: Admin, ECTA Officer, Field/Registry Agent,
   Verifier. The Minimum Project Plan's own testing plan (§7.1 WBS Testing
   category / Quality Plan test table, "Role-permission validation" row)
   describes testing _"RBAC rules for each in-scope user role (Farmer-facing
   staff, Coop/Field roles, ECTA officer, Exporter, Admin)"_ — a five-item
   list that does not match the frozen four roles and includes an
   "Exporter" role not defined anywhere in the Baseline or Design Document
   role model. This directly affects the scope of `EPIC-1-AUTH-008`
   (Authentication & RBAC End-to-End Verification). **Not resolved.**
   `EPIC-1-AUTH-008` is not modified by this review (per instruction); its
   owner (Ephratha) must raise this discrepancy before finalizing that
   task's RBAC test matrix, per `06-failure-and-escalation.md`.

3. **Mapping library: Leaflet only, or Leaflet/Mapbox GL (Level 3 vs. Level 3).**
   The Baseline Scope Freeze, Implementation Specification, and
   Implementation Playbook all freeze the mapping layer as _"Leaflet /
   React-Leaflet"_ with no alternative named. The Minimum Project Plan's
   resource table (§7.4, Software/Development Tools) lists the mapping
   library as _"Leaflet/Mapbox GL"_ — naming Mapbox GL as an apparent
   alternative. **Not resolved.** No task currently open depends on this
   (polygon capture is EPIC 2, not yet created), so this is recorded for
   whoever creates the EPIC-2 task files rather than requiring immediate
   escalation — but an agent must not introduce Mapbox GL into any task
   without the conflict being resolved first.

### Already-resolved items (recorded so they are not mistaken for open conflicts)

- **Frontend framework.** The Minimum Project Plan (§7.4) and the Design
  Document both describe the frontend framework as an open choice between
  Angular and React at the time they were written. The Baseline Scope
  Freeze — a later Level 3 document — explicitly records this as resolved:
  _"The Implementation Specification has since fixed this choice to React +
  JavaScript. This baseline adopts React as final; Angular is not to be
  introduced."_ This is settled by the Baseline itself, not merely by the
  lower-level Implementation Specification, so it is not an open
  same-level conflict. React only.
- **Backend framework.** Same pattern: Minimum Project Plan §7.4 lists
  "Node.js/Express or Python FastAPI" as an open team choice; the Baseline
  and Implementation Specification settle it to FastAPI. FastAPI only.

## Mandatory Execution Lifecycle

Every task, without exception, follows this sequence. No step may be
skipped, reordered, or merged into another.

```text
Approved Task
     |
     v
Agent reads project authority        (01-agent-start-procedure.md, Steps 1-3)
     |
     v
Agent reads applicable rules         (01-agent-start-procedure.md, Step 2)
     |
     v
Agent inspects current repository    (01-agent-start-procedure.md, Step 4)
     |
     v
Agent verifies dependencies/         (01-agent-start-procedure.md, Step 5)
preconditions
     |
     v
Agent implements ONLY the            (02-task-execution-procedure.md)
assigned task
     |
     v
Agent runs required tests            (03-verification-and-testing.md)
     |
     v
Agent performs self-review           (04-human-review-and-approval.md)
     |
     v
Agent reports changes                (04-human-review-and-approval.md)
     |
     v
Human reviews                        (04-human-review-and-approval.md)
     |
     v
Human approves
     |
     v
Git commit                           (05-git-and-commit-procedure.md)
     |
     v
Next task
```

If any step surfaces a conflict, a missing precondition, or a scope
question, the lifecycle stops at that step and routes to
`06-failure-and-escalation.md`. It does not skip ahead.

## Human Approval Gates

There are exactly two mandatory human gates, and no task may pass either
one by an agent's own declaration:

1. **Review gate** — a human reviews the agent's implementation and report
   before anything is approved for commit (`04-human-review-and-approval.md`).
2. **Merge gate** — per the existing `.agents/rules/04-git-workflow.md`, at
   least one human reviewer other than the implementer approves the pull
   request before it merges into `develop`. An agent's own self-review
   never substitutes for this.

## Definition of Task Completion

A task is complete only when **all** of the following are true:

- Every item in the task file's own `Acceptance Criteria` is verified true,
  with evidence.
- Every item in the task file's own `Testing Requirements` passes.
- The task's `Expected Agent Report` has been produced and reviewed by a
  human.
- No item from the task's `Out of Scope` section was implemented.
- No unresolved conflict was left unreported.
- The change is merged into `develop` (not left on an unmerged branch) per
  `.agents/rules/04-git-workflow.md`.

A task that has been "coded" but not merged, or merged without human
review, is not complete.

## Definition of EPIC Completion

Restated from this request's own specification, and consistent with
`.agents/tasks/EPIC-1/00-epic-overview.md`'s own Epic Acceptance Criteria
concept:

```text
All tasks implemented
        +
All acceptance criteria passed
        +
Required tests passing
        +
No unresolved blockers
        +
No unauthorized scope changes
        +
Human review complete
        +
Git history clean
        +
Traceability verified
        =
EPIC COMPLETE
```

For EPIC 1 specifically, `EPIC-1-AUTH-008` (Authentication & RBAC
End-to-End Verification) is the task that formally checks and reports this
state — but `EPIC-1-AUTH-008` passing is a _necessary_, not _automatically
sufficient_, condition: the "no unresolved blockers" and "no unauthorized
scope changes" conditions above also require that none of the "Known
documented conflicts" in this file remain open in a way that affects what
was actually built.

## A Note on the Minimum Project Plan and Existing Task Files

The Minimum Project Plan V1.0 is now available and has been incorporated
into this execution directory. Execution uses `CEVCMS_Minimum_Project_Plan_V1.0`
and `.agents/rules/07-current-project-decisions.md` as the authoritative
schedule and decision references. Existing `.agents/tasks/EPIC-0/` and
`.agents/tasks/EPIC-1/` files are not modified by this update, even when
their traceability sections predate the newly available plan.

## Confirmed Schedule and Milestones (from the Minimum Project Plan V1.0)

Now that the Minimum Project Plan is available, the following are the
authoritative milestones — used by `07-task-completion-checklist.md` and
`06-failure-and-escalation.md` for schedule-risk judgment:

| Milestone | Description                   | Timing        |
| --------- | ----------------------------- | ------------- |
| M1        | Assignment Description Agreed | End of Week 1 |
| M2        | Project Plan Approved         | End of Week 1 |
| M3        | Scope and Design Finalized    | Mid Week 2    |
| M4        | Working Increment Delivered   | End of Week 3 |
| M5        | Client Acceptance Review      | Mid Week 4    |
| M6        | Project Closure               | End of Week 4 |

Per the Minimum Project Plan §7.2/§7.3: Week 1 is initiation, planning, and
design (repository/task-board/environment setup, architecture and database
schema _design_, wireframes); Week 2 is when database schema
_implementation_ and Authentication & RBAC / Farmer & Polygon Registry
_implementation_ begin; Week 3 completes and integrates the core chain
(Traceability & QR) and is where stretch modules may begin, conditionally;
Week 4 is testing, defect-fixing, documentation, and the final
demonstration. Since `.agents/tasks/EPIC-0/` and `EPIC-1/` are already
past their originally-implied Implementation-Specification week framing
(EPIC-0 is confirmed complete per this request's current project state),
this schedule detail matters going forward primarily for judging whether
EPIC 1 and the eventual EPIC 2 are tracking Week 2's plan, not for
re-litigating when EPIC 0 should have happened.
