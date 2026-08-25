# EPIC-5-FE-004 - Dashboard and Authenticated Application Shell

## Objective

Implement the documented authenticated dashboard entry and shell using only available API contracts.

## Scope

Provide the dashboard screen, authenticated layout, role-appropriate entry actions, and counts/data only where documented API endpoints and response fields exist. Present loading, empty, unauthorized, and API-error states.

## Out of Scope

New dashboard backend endpoints, invented aggregate queries, stretch-module counts, analytics, reporting, exports, or replacing upstream screen logic.

## Preconditions

FE-003 complete; EPIC-1 auth and any documented dashboard/count APIs are implemented and verified; source documents and actual routes inspected.

## Dependencies

FE-003; EPIC-1-AUTH-007; any documented Farmer/Farm/Lot APIs needed for counts. If no approved count contract exists, the count portion is blocked and must be escalated.

## Inputs

Design Document dashboard description, existing API contracts, role permissions, synthetic data, and approved UI.

## Expected Outputs

Authenticated dashboard/shell that links users to the appropriate core screens and does not fabricate data.

## Relevant Files / Modules

Dashboard/page/layout/navigation files under `frontend/src`, existing API clients, and shared styles from FE-001.

## Backend Responsibilities

None. No endpoint changes.

## Frontend Responsibilities

Compose dashboard data from approved clients only, role-aware actions, loading/error/empty states, and navigation.

## Database Responsibilities

None.

## API Requirements

Use only inspected, documented APIs. The Design Document does not establish a dedicated dashboard-count endpoint; if counts cannot be sourced without inventing one, record **Traceability gap - requires review** and defer that sub-feature.

## UI / UX Requirements

Dashboard is a working operational entry, not a marketing page; show only approved counts/actions and maintain responsive readable layout.

## Security Requirements

Protected dashboard requires JWT/auth state; role visibility mirrors backend permissions; no farmer PII is unnecessarily shown in aggregate cards.

## Validation / Error Handling

Handle partial API failure, empty datasets, 401/403, and network errors without blank/crashing layout.

## Acceptance Criteria

- Authenticated users reach the dashboard through protected navigation.
- Role-appropriate actions are shown using the frozen four-role model.
- Every displayed count/value comes from an approved contract or is explicitly omitted/escalated.
- Loading, empty, unauthorized, and error states are observable and controlled.

## Testing Requirements

Test/manual evidence for each applicable role, empty/partial/error states, protected access, and navigation; run build/lint and relevant upstream regression tests.

## Traceability

Design Document Sections 8, 9.1-9.4; Implementation Specification EPIC-5 Dashboard screen; Minimum Project Plan Section 7.1 frontend integration; Baseline Sections 2-4; FE-003 and EPIC-1/2/3 API contracts. Dashboard count contract gap is **Traceability gap - requires review**.

## Ownership, Git, and Change Control

Primary: Biniyam; Abel support. Verification: Ephratha and independent reviewer; Kidus documentation. Branch `feature/EPIC-5-FE-004-dashboard`; commit `feat(frontend): integrate authenticated dashboard shell`; PR to `develop`. No new endpoint or analytics without change control.

## Blockers / Stop Conditions

Stop the affected count/widget if its source endpoint or field is not documented and verified. Do not add a backend workaround.
