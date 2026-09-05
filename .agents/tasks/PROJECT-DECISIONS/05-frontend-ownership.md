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

## Approved resolution

The Project Manager approves the following operational ownership model for
EPIC-5:

- Biniyam is the frontend lead and Abel provides support.
- EPIC-1 `AUTH-007` remains historically complete and is not reopened.
- EPIC-5 `FE-003` owns the current frontend shell's protected-route,
  role-aware navigation, logout/session-cleanup, and invalid/expired-session
  integration behavior.
- FE-003 may modify the existing shared frontend auth/API integration where
  necessary for a protected API `401` to clear stale client auth state and
  lead to `/login`. It must reuse the existing AuthContext, router, and API
  helper architecture; it must not create a second auth system.
- Backend authentication and RBAC remain authoritative. A frontend route
  guard or navigation visibility rule is not an authorization substitute.
- This decision resolves Abel's historical EPIC-5 role wording operationally:
  Biniyam lead; Abel support.

Feature EPICs continue to own their domain API contracts and components.
EPIC-5 may integrate those existing contracts through the shared shell but
must not redesign or duplicate them.

## Decision status

**APPROVED - Project Manager decision recorded.** Final ownership model:
`EPIC-5 shared-shell integration ownership as specified above`.

## Approval authority

Project Manager Kaleab, with Biniyam as frontend lead, Abel as support subject to the existing ownership conflict, and relevant feature owners.

## Dependencies

PD-001. This decision is approved for the current EPIC-5 operational scope.

## Acceptance criteria

- Every screen has exactly one implementation owner.
- EPIC-5 allowed files and prohibited duplicate responsibilities are explicit.
- Shared API client/auth/navigation ownership is assigned once.
- Feature verification and EPIC-6 independent QA remain separate.
- Existing task packages are not edited by this package; PM records any resulting task reclassification separately.

## Developer/PM handoff instructions

For the approved scope above, developers may perform the specified EPIC-5
shared-shell integration. Any ownership change beyond that scope requires a
new Project Manager decision.
