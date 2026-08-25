# EPIC-5-FE-005 - Farmer Registration, List, and Detail Frontend

## Objective

Integrate the Farmer registration, list, and detail views with the verified EPIC-2 Farmer API and existing auth/navigation.

## Scope

Implement the documented Farmer form, list/detail navigation, submit/reload behavior, validation, loading/error states, and role-appropriate actions using the actual EPIC-2 response shape.

## Out of Scope

Farmer backend/model changes, FIN generation/format decisions, OTP/SMS, ID photos/bank data, offline capture, new search endpoints, or changing EPIC-2 components/API.

## Preconditions

FE-001 and FE-003 complete; EPIC-2-FARM-002/005/007 are implemented, tested, verified, approved, and their actual contracts inspected.

## Dependencies

FE-001/003; EPIC-2-FARM-002 and FARM-005; EPIC-1 auth/RBAC. FIN ambiguity remains upstream and must be consumed, not resolved.

## Inputs

Approved Farmer fields/API shapes, role permissions, synthetic data, and Design Document Sections 4.2, 8, 9.2, 13.

## Expected Outputs

Working Farmer form and list/detail views integrated to the real API with controlled states.

## Relevant Files / Modules

Existing `frontend/src` farmer pages/components/API clients from EPIC-2 or FE-001. Reuse rather than duplicate.

## Backend Responsibilities

None.

## Frontend Responsibilities

Form fields, submit, list/detail display, navigation, validation, and error/loading/empty states.

## Database Responsibilities

None.

## API Requirements

Use only inspected EPIC-2 Farmer endpoints/request/response fields. Do not send client-generated FIN or unsupported fields.

## UI / UX Requirements

Use the approved Farmer screen; keep contact data within authenticated views and provide readable validation feedback.

## Security Requirements

Use existing JWT/auth state and role permissions; do not expose Farmer PII on public routes or log submitted values.

## Validation / Error Handling

Client validation mirrors documented constraints; backend 400/401/403/404 responses remain controlled and specific only to the extent documented.

## Acceptance Criteria

- Authorized user can submit the documented Farmer form and see the API result.
- List/detail views display actual returned Farmer data without guessed fields.
- Validation and API errors are visible without raw stack traces.
- Role restrictions and authentication match EPIC-2/EPIC-1 behavior.

## Testing Requirements

Test/manual evidence for valid submission, missing/invalid input, list/detail loading/empty/error, 401/403, and sensitive-data handling; run build/lint and EPIC-2 regression tests.

## Traceability

SRS FR-FARM-001; Design Document Sections 4.2, 8, 9.2, 13; Implementation Specification EPIC-2 frontend tasks and EPIC-5 Farmer Reg/List screen; Minimum Project Plan Section 7.1 Farmer/polygon frontend WBS; Baseline Sections 2-4; EPIC-2-FARM-002/005/007. FIN format remains an upstream decision/gap.

## Ownership, Git, and Change Control

Primary: Biniyam; Abel support. Verification: Ephratha; Kidus evidence. Branch `feature/EPIC-5-FE-005-farmer-screens`; commit `feat(frontend): integrate farmer registration and views`; PR to `develop`. FIN/API changes require escalation.

## Blockers / Stop Conditions

Stop if Farmer response shape, FIN handling, or permissions are not verified. Do not modify EPIC-2 or invent fields.
