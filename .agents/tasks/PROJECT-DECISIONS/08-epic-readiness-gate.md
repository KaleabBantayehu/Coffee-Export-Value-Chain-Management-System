# PD-008 - EPIC Implementation Readiness Gate

## Objective

Define the governance gate that must pass before an EPIC is assigned for implementation.

## Why the decision is needed

The existing task tree is structurally complete, but task-file existence is not implementation readiness. A formal gate prevents developers from starting against missing predecessors, unresolved contracts, or incomplete acceptance/test definitions.

## Authoritative sources

- [execution/01-agent-start-procedure.md](../../execution/01-agent-start-procedure.md), Steps 1-6: read authority, inspect repository, verify dependencies, and stop on conflicts.
- [execution/07-task-completion-checklist.md](../../execution/07-task-completion-checklist.md): task and EPIC sign-off.
- [rules/06-change-control.md](../../rules/06-change-control.md): Required/Defect Fix/Stretch/Out of Scope classification and PM authority.
- [rules/04-git-workflow.md](../../rules/04-git-workflow.md): branch, review, merge process.
- EPIC-0 through EPIC-6 overviews: explicit preconditions, dependencies, acceptance criteria, testing, and handoffs.

## Current documented position

Existing rules require reading the task, rules, relevant documents, repository inspection, concrete dependency verification, tests, human review, and merge. Individual EPIC packages also require acceptance criteria, testing, ownership, traceability, and handoff evidence. No single project-wide assignment gate is currently recorded.

## Proposed gate, subject to approval

An EPIC is assignable only when all applicable conditions are true:

1. Upstream dependencies are verified as implemented, tested, verified, approved, and merged where required.
2. Required project decisions are approved or formally documented as non-blocking.
3. API, database, security, and UI contracts consumed by the EPIC are stable.
4. Task scope and out-of-scope boundaries are understood.
5. Every task has objective acceptance criteria and testing requirements.
6. Every task has traceability to authoritative sources.
7. Owner role is assigned without unresolved ownership overlap.
8. Branch, PR, review, merge, and worktree procedure is known.
9. Predecessor implementation is available on `develop` where the task requires it.
10. Synthetic data, environment, and required test tooling are available or the limitation is explicitly accepted for that task.
11. Known conflicts have an owner, decision status, and unblock condition.
12. The PM records an EPIC status of READY, READY WITH CONDITIONS, or BLOCKED.

## Impact

This gate controls assignment of EPIC-0 through EPIC-8 and prevents premature EPIC-7/EPIC-8 stretch work. It consumes PD-001 through PD-007 and all upstream completion evidence.

## Options

1. Adopt the twelve-condition gate above.
2. Use only each EPIC's existing local preconditions.
3. Adopt a lighter gate for preparation tasks and the full gate for implementation tasks.

## Recommended resolution

Recommendation only: option 3 provides useful planning progress while preserving a hard implementation gate. QA-001 and decision-package work may be assigned as preparation; feature implementation requires the full gate.

## Decision status

**UNRESOLVED - Project Manager approval required.** Final gate: `UNRESOLVED`.

## Approval authority

Project Manager Kaleab. Ephratha and Kidus verify QA/documentation readiness; relevant owners verify technical handoffs.

## Dependencies

PD-001 through PD-007; actual repository and branch state; upstream EPIC completion evidence.

## Acceptance criteria

- The approved gate distinguishes preparation assignment from implementation assignment.
- Each condition has an evidence source and responsible verifier.
- A failed condition produces BLOCKED or READY WITH CONDITIONS, never an implicit READY.
- The gate does not authorize scope expansion or silently resolve conflicts.
- EPIC-7/EPIC-8 remain blocked until the approved core gate passes.

## Developer/PM handoff instructions

**DO NOT ASSIGN FULL IMPLEMENTATION UNTIL APPROVED.** Use this package to prepare decisions and readiness evidence only. The PM must publish the final gate status before feature developers begin.
