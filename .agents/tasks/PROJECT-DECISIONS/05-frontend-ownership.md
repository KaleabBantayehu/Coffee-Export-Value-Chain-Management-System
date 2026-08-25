# PD-005 - Frontend Ownership Boundary Decision

## Objective

Define one non-duplicating ownership model for feature frontend work and EPIC-5 integration.

## Why the decision is needed

The current packages assign the same screens and API integration surfaces to both feature EPICs and EPIC-5. Two developers could implement competing versions of the same component.

## Authoritative sources

- Implementation Specification EPIC-1 frontend tasks and EPIC-5 screen list/ownership.
- Design Document Sections 9.1-9.4 and 8.
- Minimum Project Plan Sections 7.1-7.2 frontend WBS and ownership.
- Baseline Section 5 frontend ownership.
- [EPIC-1 overview](../EPIC-1/00-epic-overview.md), [EPIC-2 overview](../EPIC-2/00-epic-overview.md), [EPIC-3 overview](../EPIC-3/00-epic-overview.md), [EPIC-4 overview](../EPIC-4/00-epic-overview.md), and [EPIC-5 overview](../EPIC-5/00-epic-overview.md).

## Current overlap map

- EPIC-1 `AUTH-006/007`: login, auth state, protected routes, role navigation, logout. EPIC-5 `FE-002/003`: same integration surface.
- EPIC-2 `FARM-005/006`: Farmer and Farm/Polygon screens. EPIC-5 `FE-005/006`: same screens/integration.
- EPIC-3 `TRACE-005/006`: Lot and Traceability screens. EPIC-5 `FE-007/008`: same screens/integration.
- EPIC-4 `QR-004/005`: QR generation/public verification UI. EPIC-5 `FE-009`: same UI integration.
- EPIC-1/2/3/4 verification tasks and EPIC-5 `FE-010` also overlap with EPIC-6 QA, though independent verification can remain distinct.

## Impact

Without a decision, duplicated components, API clients, routes, divergent validation, merge conflicts, and unclear acceptance ownership are likely.

## Options

1. Feature EPICs own feature UI/API integration; EPIC-5 owns only cross-screen composition, shared navigation wiring, and final orchestration. Existing duplicate EPIC-5 screen tasks are reclassified by PM.
2. EPIC-5 owns all frontend implementation; feature EPIC frontend tasks become contracts/handoffs or are retired by PM.
3. Keep current overlap with explicit file ownership per task, requiring no shared file to have two owners.

## Recommended resolution

Recommendation only: option 1 or 2 can work, but the project should choose exactly one. The least disruptive model is option 1: feature EPICs own domain screens/components and EPIC-5 owns composition/integration only. Under that model EPIC-5 may modify app composition, route registration, shared shell, and integration wiring; it may not duplicate or redesign feature components, API clients, auth state, or backend contracts.

## Decision status

**UNRESOLVED - Project Manager approval required.** Final ownership model: `UNRESOLVED`.

## Approval authority

Project Manager Kaleab, with Biniyam as frontend lead, Abel as support subject to the existing ownership conflict, and relevant feature owners.

## Dependencies

PD-001. Must be approved before assigning overlapping frontend tasks or shared files.

## Acceptance criteria

- Every screen has exactly one implementation owner.
- EPIC-5 allowed files and prohibited duplicate responsibilities are explicit.
- Shared API client/auth/navigation ownership is assigned once.
- Feature verification and EPIC-6 independent QA remain separate.
- Existing task packages are not edited by this package; PM records any resulting task reclassification separately.

## Developer/PM handoff instructions

**DO NOT ASSIGN OVERLAPPING FRONTEND TASKS UNTIL APPROVED.** Developers must stop when their task would require modifying a component owned by another task.
