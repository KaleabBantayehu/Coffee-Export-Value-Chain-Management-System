# CEVCMS V1.0 — AI-Assisted Development Control System

This `.agents/` directory is the control system for human developers and AI coding
agents working on **Coffee Export Value Chain Management System (CEVCMS) V1.0**,
a seven-member university practical-course project for the Ethiopian Coffee and Tea
Authority (ECTA).

It does not contain application code. It contains the rules and task
specifications that govern what may be built, how, and in what order, so that
AI-assisted development accelerates the project without silently expanding scope,
changing architecture, or drifting from the documents already agreed with the
client, the supervisors, and the steering committee.

## Who must read this

Any human developer or AI coding agent, before writing a single line of code for
CEVCMS, must read:

1. `rules/00-project-authority.md`
2. `rules/01-scope-boundaries.md`
3. `rules/02-tech-stack.md`

Then the rule files relevant to the work at hand (`03`–`06`), then the specific
task file in `tasks/`.

## Directory structure

```text
.agents/
├── README.md                          <- this file
├── rules/
│   ├── 00-project-authority.md        <- document precedence, conflict handling
│   ├── 01-scope-boundaries.md         <- core / stretch / out-of-scope
│   ├── 02-tech-stack.md               <- frozen technology stack
│   ├── 03-coding-rules.md             <- code quality and architecture rules
│   ├── 04-git-workflow.md             <- branching, PR, review rules
│   ├── 05-testing-rules.md            <- testing expectations, Definition of Done
│   └── 06-change-control.md           <- Required / Defect Fix / Stretch / Out of Scope
│
└── tasks/
    └── EPIC-0/
        ├── 00-epic-overview.md        <- EPIC 0 scope and current status
        ├── 01-backend-foundation.md   <- EPIC-0-BE-001
        ├── 02-database-postgis.md     <- EPIC-0-DB-001
        └── 03-initial-migrations.md   <- EPIC-0-DB-002
```

Task files for later epics (Authentication, Farmer & Polygon Registry,
Traceability & QR, etc.) are deliberately not created yet. They will be added,
one epic at a time, following the dependency order fixed in the Implementation
Specification and Implementation Playbook, once the epic immediately ahead of
them is complete. This keeps the control system usable instead of speculative.

## The one rule that matters most

> **If a requirement, technology, or feature is not traceable to one of the
> eight authoritative project documents, it does not get implemented.**

Every rule and task file in this directory exists to make that one rule
enforceable by both humans and AI agents. See `rules/00-project-authority.md`
for the full document precedence and conflict-handling procedure.

## Current authoritative source documents

| # | Document | Reference |
|---|---|---|
| 1 | Project Baseline & Scope Freeze | `ECTA-CEVCMS-BASELINE-V1.0` |
| 2 | Implementation Specification & Development Backlog | (CEVCMS V1.0) |
| 3 | Design Document | `ECTA-CEVCMS-DD-V1.0` |
| 4 | Software Requirements Specification (SRS) | `ECTA-CEVCMS-SRS-V2.1` |
| 5 | Minimum Project Plan | `ECTA-CEVCMS-PP-V1.0` (referenced by the Design Document; **not available in the project repository at the time this control system was written — see the note below**) |
| 6 | Assignment Description | `ECTA-CEVCMS-AD-V1.0` |
| 7 | Implementation Playbook | `ECTA-CEVCMS-PLAYBOOK-V1.0` |
| 8 | ECTA Phase 1 Discovery Report | context only — never a source of scope |

**Open gap, flagged rather than silently resolved:** the Minimum Project Plan
V1.0 document is referenced by the Design Document and the Baseline as the
controlling source for the one-month schedule, dependencies, and milestone
dates, but its file was not among the documents available when this control
system was created. Wherever a schedule or milestone decision is needed, this
control system instead uses the four-week schedule already stated in the
Implementation Specification (Section 3, "Four-Week Implementation Order") and
the Implementation Playbook (Section 6), since both are authoritative
documents that restate the same plan. If the actual Minimum Project Plan
becomes available and its schedule differs, that difference must be treated as
a conflict under `rules/00-project-authority.md` and raised with the Project
Manager, not resolved by an agent.
