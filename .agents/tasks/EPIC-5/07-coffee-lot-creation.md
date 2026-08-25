# EPIC-5-FE-007 - Coffee Lot Creation Frontend

## Objective

Integrate the Coffee Lot creation screen with EPIC-3's verified `POST /api/v1/lots` contract.

## Scope

Allow an authorized user to select an existing Farm, submit the documented `farm_id`, display the returned Lot/GIN/status, and link to the trace view using the actual response.

## Out of Scope

Lot backend logic, GIN generation/format decisions, event/trace implementation, QR generation, Farm selector reimplementation, or unsupported Lot fields.

## Preconditions

FE-001/003 and FE-006 Farm capability available; EPIC-3-TRACE-002/005/007 implemented, tested, verified, approved; actual response shape inspected.

## Dependencies

FE-001/003/006; EPIC-3-TRACE-002 and TRACE-005; EPIC-1 auth; EPIC-2 Farm API. GIN format remains upstream-owned.

## Inputs

Verified Farm list/lookup and Lot create response, role permissions, synthetic Farm, and Design Document Sections 5.1, 8, 9.3, 13.

## Expected Outputs

Working authorized Lot form with Farm selection, success result, navigation, validation, loading, and API error states.

## Relevant Files / Modules

Existing Lot/Farm API clients, pages/components, navigation, and shared form primitives under `frontend/src`.

## Backend Responsibilities

None.

## Frontend Responsibilities

Farm selection, exact request construction, result display, role-aware action visibility, and trace-view navigation.

## Database Responsibilities

None.

## API Requirements

Submit exactly the inspected `farm_id` contract to `POST /api/v1/lots`; do not send `created_by`, GIN, or event fields from the client.

## UI / UX Requirements

Show the generated GIN and initial status returned by the API; make invalid Farm and authorization errors clear.

## Security Requirements

Use existing JWT/auth state and backend permissions; never trust or display client-created identity fields; do not expose private trace data.

## Validation / Error Handling

Require a selected existing Farm; preserve documented backend 400/401/403/404 behavior and avoid fabricated messages.

## Acceptance Criteria

- Field/Registry Agent or Admin can select an existing Farm and create a Lot through the documented API.
- Returned GIN/status are displayed and a valid Lot ID can reach traceability.
- Unauthorized/unauthenticated access is handled consistently.
- Invalid Farm/API failures are visible without a crash or invented contract.

## Testing Requirements

Test/manual evidence for success, missing Farm, invalid Farm, 401/403, response display, and navigation; run build/lint and EPIC-3 regression tests.

## Traceability

SRS FR-TRACE-001; Design Document Sections 5.1, 7.2, 8, 9.3, 13; Implementation Specification EPIC-3 Lot flow and EPIC-5 Coffee Lot Creation screen; Minimum Project Plan Sections 7.1-7.2; Baseline Section 4; EPIC-3-TRACE-002/005/007. GIN format is consumed, not decided.

## Ownership, Git, and Change Control

Primary: Biniyam; Abel support. Verification: Ephratha; Kidus evidence. Branch `feature/EPIC-5-FE-007-lot-creation`; commit `feat(frontend): integrate coffee lot creation`; PR to `develop`. API/GIN changes escalate.

## Blockers / Stop Conditions

Stop if Lot response, Farm selector contract, or GIN status is not verified. Do not modify EPIC-3.
