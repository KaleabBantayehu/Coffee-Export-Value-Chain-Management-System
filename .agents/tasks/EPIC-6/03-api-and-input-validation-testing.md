# EPIC-6-QA-003 - API and Input Validation Testing

## Objective

Test documented backend endpoints with Postman and existing automated API tests, including malformed input and structured error behavior.

## Scope

Cover login/me/logout, user/RBAC APIs where implemented, Farmer, Farm/Polygon, Lot, Traceability event/trace, QR generation, and public verification. Test malformed credentials, farmer/farm/polygon/lot/event/QR identifiers and payloads, missing records, and documented 400/401/403/404 behavior.

## Out of Scope

Creating or changing endpoints, inventing request/response fields/statuses, frontend testing, load/performance, formal penetration testing, and stretch APIs.

## Preconditions

QA-001 complete; each endpoint under test is implemented, merged, and its upstream task contract is available. Local backend and synthetic data are runnable.

## Dependencies

EPIC-1 through EPIC-4 endpoint implementations and verification; EPIC-5 only where API calls are observed through the UI; QA-001.

## Inputs

Endpoint contracts, Postman collections, automated API tests, synthetic credentials/data, role matrix, and approved QR-001 contract where applicable.

## Expected Outputs

Postman/API test results, malformed-input matrix, structured-error evidence, endpoint coverage list, and blocked endpoint register.

## Relevant Files / Modules

`backend/app/api/`, `backend/tests/`, Postman collection location, API documentation/evidence location. No application modifications.

## Backend Responsibilities

None; test actual APIs and file defects against owning implementation tasks.

## Frontend Responsibilities

None except optional correlation of frontend request evidence; frontend behavior is QA-006.

## Database Responsibilities

Use database checks only to confirm API persistence/relationship outcomes where needed; do not repair data directly.

## API Requirements

Use exact documented routes: `/api/v1/auth/*`, Farmer/Farm routes, `/api/v1/lots`, `/api/v1/lots/{id}/events`, `/api/v1/lots/{id}/trace`, `/api/v1/lots/{id}/qr`, and `/api/v1/verify/{qrId}` only when implemented and approved. QR assertions remain conditional on QR-001.

## UI / UX Requirements

None directly. Record API errors that frontend tasks must render.

## Security Requirements

Use synthetic data, sanitized collections, no saved tokens/passwords/secrets, and no PII. Check public QR response minimization where implemented.

## Validation / Error Handling

For each accepting endpoint test missing, wrong-type, malformed, out-of-range, nonexistent, unauthorized, and duplicate cases supported by the actual contract. Do not invent an expected response for an unresolved contract.

## Acceptance Criteria

- Every implemented in-scope endpoint has a Postman request and automated/API evidence where available.
- Invalid inputs produce the documented structured 400-level behavior or a defect is filed.
- Authenticated/protected and public QR exceptions are tested distinctly.
- Unknown/nonexistent resources and QR identifiers are tested without raw exceptions.
- Results are linked to requirements, upstream task, evidence, and defect status.

## Testing Requirements

Run Postman collection against a fresh synthetic environment and relevant backend API tests; rerun after fixes through QA-007. Record blocked tests for absent implementation/contracts.

## Evidence Requirements

Sanitized Postman export/results, request/response status samples, test output, environment/build identifier, and defect references. Never include JWTs, passwords, keys, or PII.

## Traceability

Implementation Specification EPIC-6 API/input-validation testing; Minimum Project Plan Section 6.4/7.1 Postman and validation rows; Design Document Section 8 and error/security Sections 10/14; SRS FR-AUTH, FR-FARM, FR-TRACE; upstream endpoint tasks.

## Ownership, Git, and Change Control

Primary: Ephratha. Kidus records test cases/evidence; owning developers address defects. Branch `feature/EPIC-6-QA-003-api-validation`; commit `test(qa): verify API and input validation matrix`; PR to `develop`. Contract/status deviations escalate under change control.

## Blockers / Stop Conditions

Block an assertion when the endpoint or contract is only specified, missing, or unresolved. Do not create a substitute endpoint or silently adapt expected behavior.
