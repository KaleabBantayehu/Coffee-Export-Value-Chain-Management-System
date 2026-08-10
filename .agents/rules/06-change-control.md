# Rule 06 — Change Control

## Purpose

A lightweight policy to prevent scope creep during the remaining one-month
implementation period. This is not a formal change-management bureaucracy —
it exists so the team always has a single, current, agreed statement of what
CEVCMS V1.0 means.

Source of authority: Project Baseline & Scope Freeze §6; Implementation
Playbook §2.

## Classification — required before any work begins

Every proposed new feature, deviation, or change — whether proposed by a
human or surfaced by an AI agent — must first be classified into exactly one
of these four categories:

| Classification | Meaning | Action |
|---|---|---|
| **Required** | Directly needed to satisfy an existing, already-documented requirement (SRS, Design Document, or Implementation Specification). | Implement in the current or next task, once traced. |
| **Defect Fix** | Corrects a bug in already-scoped functionality; does not add new capability. | Implement immediately; log it. |
| **Stretch** | Falls under `01-scope-boundaries.md`'s stretch list. | Queue behind core scope; do not start early. |
| **Out of Scope** | Falls under the out-of-scope list, or otherwise expands the project beyond the Baseline. | Reject; do not implement. |

## When a change is accepted

A change to scope, design, or the technology baseline is accepted only if at
least one of the following applies:

1. It is necessary to satisfy an existing requirement already documented in
   the SRS, Design Document, or Implementation Specification.
2. It fixes a blocking defect that prevents the core workflow
   (`01-scope-boundaries.md`) from functioning.
3. It is required to make the core workflow operational.
4. The team explicitly approves it as a controlled scope change, with the
   Project Manager's sign-off.

If none of these apply, the change is not accepted, regardless of how small
or reasonable it seems in isolation.

## Authorization

**Only the Project Manager (Kaleab) may authorize a controlled scope
change.** An AI agent must never treat its own judgment that "this seems like
a good idea" as authorization. Team members other than the Project Manager
may propose and classify a change, but cannot approve category 4 above on
their own.

## Recording changes

The Project Manager records every accepted change of consequence: what
changed, its classification, and its impact on schedule or scope, so the
team always has a single, current statement of what V1.0 means.
Documentation owned by Kidus (per Baseline §5) must be updated to stay
consistent with any accepted change — an accepted change that is not
reflected in the documentation is treated as incomplete.

## What an AI coding agent must never do, under any classification

Regardless of how a change is classified, an agent must never, on its own
initiative:

- Redesign the architecture (see `03-coding-rules.md`).
- Change the frozen technology stack (see `02-tech-stack.md`).
- Expand V1.0 scope (see `01-scope-boundaries.md`).
- Install unnecessary packages.
- Upgrade or downgrade dependencies without a documented, specific reason.
- Modify modules or files unrelated to its current task.
- Implement future or stretch features prematurely.
- Commit secrets.
- Bypass testing (`05-testing-rules.md`).
- Bypass human review (`04-git-workflow.md`).
- Declare its own work complete without satisfying the task's Definition of
  Done as written — an agent does not get to redefine "done" for its own
  convenience.

If an agent believes one of the above is genuinely necessary, it must stop
and raise the issue through this change-control process rather than act
first and explain afterward.
