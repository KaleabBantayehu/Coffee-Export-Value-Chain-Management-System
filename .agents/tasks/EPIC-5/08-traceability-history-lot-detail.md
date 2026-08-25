# EPIC-5-FE-008 - Traceability History and Lot Detail Frontend

## Objective

Integrate the protected Lot trace/detail and event-entry experience with EPIC-3's verified contracts.

## Scope

Display the actual Lot, Farm, Farmer, and ordered event response from `GET /api/v1/lots/{id}/trace`; provide the documented event-entry form using `POST /api/v1/lots/{id}/events`; refresh the list after success; handle protected errors.

## Out of Scope

Traceability backend, event update/delete, QR screens, public verification, Lot creation, PII policy changes, or new event types/contracts.

## Preconditions

FE-001/003/007 available; EPIC-3-TRACE-003/004/006/007 implemented, tested, verified, approved; actual response shapes inspected.

## Dependencies

FE-001/003/007; EPIC-3-TRACE-003/004/006; EPIC-1 auth. Any EPIC-3 open decision remains upstream-owned.

## Inputs

Verified trace/event response and request shapes, Lot ID, role behavior, synthetic records, Design Document Sections 5.1, 5.3, 8, 9.3.

## Expected Outputs

Protected Lot trace screen with ordered history, documented authenticated event entry, refresh behavior, and controlled states.

## Relevant Files / Modules

Existing trace/Lot components and API clients under `frontend/src`; reuse EPIC-3-TRACE-006 where available.

## Backend Responsibilities

None.

## Frontend Responsibilities

Render actual response, event form, refresh/reconciliation, loading/404/401/403/error states, and role behavior exactly as backend documents it.

## Database Responsibilities

None.

## API Requirements

Call only the inspected `GET /lots/{id}/trace` and `POST /lots/{id}/events` contracts. Do not add update/delete calls.

## UI / UX Requirements

Authenticated users can see the protected trace data permitted by the contract; event history is chronological and readable; no blank error state.

## Security Requirements

Use JWT from existing auth state. Protected Farmer contact fields may appear only as permitted by EPIC-3's protected response; never expose them through the public QR route.

## Validation / Error Handling

Require non-empty documented event fields; display 404/401/403/backend/network errors without raw details; prevent duplicate submission.

## Acceptance Criteria

- Existing Lot trace displays actual Lot/Farm/Farmer/event data in documented order.
- Authenticated event entry succeeds according to EPIC-3 behavior and refreshed history shows it.
- Unauthenticated and nonexistent Lot access are handled clearly.
- No update/delete event UI or new API is introduced.

## Testing Requirements

Test/manual evidence for populated/empty trace, event success, invalid input, 401/404, role behavior, refresh, and protected-vs-public data boundary; run build/lint and EPIC-3 regression tests.

## Traceability

SRS FR-TRACE-001; Design Document Sections 5.1, 5.3, 8, 9.3, 13; Implementation Specification EPIC-3 DoD and EPIC-5 Traceability View; Minimum Project Plan Section 7.1 FR-TRACE frontend WBS; Baseline Section 4; EPIC-3-TRACE-003/004/006/007.

## Ownership, Git, and Change Control

Primary: Biniyam; Abel support. Verification: Ephratha; Kidus evidence. Branch `feature/EPIC-5-FE-008-traceability-view`; commit `feat(frontend): integrate traceability history view`; PR to `develop`. Any response/PII deviation escalates.

## Blockers / Stop Conditions

Stop if trace/event response or auth behavior is not verified. Do not reimplement EPIC-3.
