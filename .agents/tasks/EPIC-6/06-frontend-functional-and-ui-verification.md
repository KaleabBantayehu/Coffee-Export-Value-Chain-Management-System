# EPIC-6-QA-006 - Frontend Functional and UI Verification

## Objective

Verify the implemented EPIC-5 React screens and browser workflow against approved upstream API contracts and V1.0 acceptance behavior.

## Scope

Verify Login, Dashboard, Farmer registration/list/detail, Farm/polygon registration/details, Coffee Lot creation, Traceability view, QR generation, and public QR verification. Cover navigation, validation, loading/empty/error/401/403/404 states, role visibility, responsive/manual behavior, and public/private data boundaries.

## Out of Scope

Frontend implementation or fixes, new test framework, backend/API changes, UI redesign, offline/mobile application, stretch screens, and claims of automated coverage where no runner exists.

## Preconditions

QA-001 complete; EPIC-5-FE-010 and EPIC-1-4 verification handoffs are implemented/approved; frontend/backend runnable. Current frontend tooling must be inspected, not assumed.

## Dependencies

EPIC-5 FE-001 through FE-010; EPIC-1 auth; EPIC-2 farmer/farm; EPIC-3 lot/trace; EPIC-4 QR; QA-003/004 for API/security outcomes.

## Inputs

Approved screen/API map, synthetic accounts/data, browser walkthrough script, role matrix, design/wireframes, and known-defect list.

## Expected Outputs

Screen-by-screen results, manual browser walkthrough evidence, responsive observations, public-data inspection, and defects/blockers.

## Relevant Files / Modules

`frontend/src/`, `frontend/package.json`, existing test/config files, browser/manual evidence location, and EPIC-5 task contracts. No source changes.

## Backend Responsibilities

None; APIs must be available for real integration testing.

## Frontend Responsibilities

Execute UI verification and report behavior; Biniyam supports interpretation but does not replace independent QA.

## Database Responsibilities

None directly; use QA-005 evidence for persisted state.

## API Requirements

Observe actual documented requests/responses; do not create a new endpoint for a missing screen dependency. QR assertions require approved QR-001 contract.

## UI / UX Requirements

Check the documented screens, role-aware actions, clear states, map usability, generated QR display, public verification without login, and readable desktop/mobile presentation.

## Security Requirements

No secrets/passwords/tokens in screenshots/logs; protected routes remain protected; public verification exposes only approved non-sensitive data and never protected trace PII.

## Validation / Error Handling

Exercise invalid credentials, form fields, polygon data, Lot/event/QR identifiers, network failures, and 401/403/404 states as supported by actual contracts.

## Acceptance Criteria

- Every implemented EPIC-5 screen has a pass/fail/blocked result.
- The full browser core workflow is recorded or explicitly blocked at the first failed dependency.
- Unauthenticated protected access, role navigation, logout, and public QR access behave as approved.
- Loading, empty, validation, API, and not-found states are controlled.
- Public verification does not display sensitive data.

## Testing Requirements

Run existing frontend `build`/`lint` and any available frontend tests; otherwise perform documented manual walkthroughs. Coordinate backend/API regression with QA-005/007.

## Evidence Requirements

Screenshots, browser steps/results, viewport notes, console/error output sanitized of secrets, and defect references. Do not include farmer PII in artifacts.

## Traceability

Design Document Sections 9.1-9.4, 5.3, 8, 13; Implementation Specification EPIC-5 screen list and core-chain DoD; Minimum Project Plan Sections 6.4, 7.1-7.2; Baseline Sections 2-4; EPIC-5 handoff and upstream API tasks.

## Ownership, Git, and Change Control

Primary QA: Ephratha. Biniyam supports frontend clarification; Kidus collects evidence. Branch `feature/EPIC-6-QA-006-frontend-verification`; commit `test(qa): verify frontend core workflow`; PR to `develop`. No UI fixes in this task.

## Blockers / Stop Conditions

Block if a screen/API is not implemented or its contract is unresolved. Do not install a framework or silently redesign the EPIC-5 flow.
