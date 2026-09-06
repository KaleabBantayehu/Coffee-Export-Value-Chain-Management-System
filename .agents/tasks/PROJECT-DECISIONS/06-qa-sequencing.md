# PD-006 - EPIC-6 QA Sequencing Decision

## Objective

Resolve the QA-005/QA-006 ordering issue and establish a non-circular QA execution sequence.

## Why the decision is needed

EPIC-6 QA-005 requires EPIC-5-FE-010, while QA-006 verifies frontend behavior and EPIC-5-FE-010 is itself a frontend end-to-end verification handoff. The current graph can require frontend verification before the QA task that is supposed to verify it.

## Authoritative sources

- [EPIC-6 overview](../EPIC-6/00-epic-overview.md), Dependency graph and Recommended execution order.
- [QA-005](../EPIC-6/05-integration-and-core-chain-testing.md), Preconditions/Dependencies.
- [QA-006](../EPIC-6/06-frontend-functional-and-ui-verification.md), Preconditions/Dependencies.
- [EPIC-5 FE-010](../EPIC-5/10-frontend-integration-e2e-verification.md).
- Minimum Project Plan Sections 6.4, 7.1-7.2 and Implementation Playbook Sections 5-6.

## Current documented position

The overview orders QA-005 before QA-006. QA-005 depends on EPIC-5-FE-010 and says it coordinates with QA-006. QA-006 also depends on EPIC-5-FE-010 and says it uses QA-005 evidence. FE-010 requires the full EPIC-5 screen set and upstream EPIC verification gates.

## Conflict/gap

This is an actual circular or redundant dependency if FE-010 is required as a completed frontend verification before QA-006 can run. It may instead be intentional if FE-010 is treated as an upstream frontend handoff and QA-006 as independent QA, but that distinction is not cleanly reflected in the graph.

## Options

1. Make QA-005 backend/API/database integration, remove FE-010 from its hard dependency, then run QA-006 frontend verification, QA-007 regression, QA-008 evidence, QA-009 reporting, QA-010 final gate.
2. Run QA-005 and QA-006 in parallel after all upstream EPIC gates, then QA-007 onward.
3. Treat FE-010 as a prerequisite frontend handoff and retain the order, explicitly separating FE-010 evidence from QA-006 independent verification.

## Recommended resolution

Recommendation only: option 1 is clearest. QA-005 should verify cross-module backend/API/database integration; QA-006 should independently verify frontend; QA-005 and QA-006 may share a core-chain fixture but neither should depend on the other's final result. QA-010 remains the only final QA gate.

## Decision status

**APPROVED - Project Manager/project owner approval recorded 2026-09-06.**

**Final sequence:**

1. QA-005 verifies cross-module **backend/API/database** integration using the
   implemented upstream contracts and read-only persistence checks. EPIC-5
   FE-010 remains supporting frontend handoff evidence, not a hard QA-005
   execution dependency.
2. QA-006 independently verifies the EPIC-5 frontend/browser workflow after
   QA-005's backend/API/database evidence is available. It does not relabel
   FE-010 evidence as independent QA verification.
3. QA-007 regression/defect disposition and QA-008 requirements/evidence
   traceability follow the applicable QA-005 and QA-006 results.
4. QA-009 reporting/manual and QA-010 final QA/M6 gate remain last. QA-010 is
   the only final QA gate.

## Approval authority

Project Manager Kaleab, with Ephratha as QA owner, Kidus as documentation owner, and Biniyam for FE-010 handoff clarification.

## Dependencies

PD-001. PD-005 may affect whether FE-010 remains an independent implementation task or a handoff.

## Acceptance criteria

- Existing order and the exact circularity are recorded.
- One approved sequence identifies preparation versus execution.
- QA-005, QA-006, FE-010, and QA-010 responsibilities are non-duplicating.
- No final QA result is claimed before all required upstream evidence exists.

## Developer/PM handoff instructions

The former instruction, **"DO NOT APPLY THE CORRECTED ORDER UNTIL APPROVED,"**
is satisfied by the explicit Project Manager/project-owner approval recorded
above. Schedule and execute QA-005 and QA-006 in the approved final sequence.
This decision does not mark either task started, executed, or complete.

## PD-011 solo-review record

- **Decision/branch:** PD-006 / `feature/pd-006-qa-sequencing-approval`.
- **Author/reviewer:** Kaleab Bantayehu, Project Manager/project owner.
- **Reason the exception applies:** CEVCMS is a genuine single-developer
  project with no second human reviewer available; PD-011 preserves the
  documented owner self-review control.
- **Exact governance diff reviewed:** this decision record, the project
  decision overview, and the affected EPIC-6 QA-005/QA-006 sequencing text.
  No application source, QA execution evidence, credentials, or environment
  file is changed.
- **Consistency finding:** the approved Option 1 sequence removes FE-010 as a
  hard QA-005 dependency, retains QA-006 as independent frontend verification,
  and leaves QA-010 as the final gate. It resolves the recorded circularity
  without changing task acceptance behavior beyond the necessary sequencing
  clarification.
- **Unresolved blockers:** none for PD-006 sequencing. PD-007 remains a
  separate later-task evidence-location governance item.
- **Explicit approval:** **APPROVED** by the Project Manager/project owner on
  2026-09-06. No AI assistant or tool is represented as an independent human
  reviewer.
