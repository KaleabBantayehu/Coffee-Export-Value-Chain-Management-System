# EPIC-6-QA-004 - Authentication, RBAC, and Security Testing

## Objective

Verify the V1.0 authentication/RBAC model and security boundaries across implemented core APIs and public QR verification.

## Scope

Test Admin, ECTA Officer, Field/Registry Agent, and Verifier permitted/forbidden access; missing/invalid/expired JWT; generic authentication errors; logout/session cleanup; protected routes; public QR verification exception; PII/secret exposure; tampering and malformed identifiers where QR is implemented.

## Out of Scope

Adding roles, changing permissions, MFA, refresh tokens, HSM, RS256, ABAC, OAuth/OIDC, formal penetration testing, load testing, or fixing implementation defects.

## Preconditions

QA-001 complete; EPIC-1 AUTH-008 and downstream protected APIs are implemented, verified, approved, and runnable. QR security tests require approved/implemented EPIC-4 contract.

## Dependencies

EPIC-1 auth/RBAC; EPIC-2/3 protected APIs; EPIC-4 QR verification; EPIC-5 route/navigation; QA-001 and QA-003 API setup.

## Inputs

Frozen four-role model, endpoint permission contracts, synthetic users, auth tokens generated during the test session, and public/private data rules.

## Expected Outputs

Role-permission matrix, auth/security test results, sanitized evidence, exposure checklist, and defects/blockers.

## Relevant Files / Modules

`backend/tests/`, auth/RBAC routes/dependencies, frontend route/auth files, Postman security requests, and evidence documentation. No source changes.

## Backend Responsibilities

Test backend enforcement and response behavior; no new middleware.

## Frontend Responsibilities

Verify protected routes, role-aware navigation, logout cleanup, public verification access, and controlled 401/403 rendering.

## Database Responsibilities

None beyond read-only confirmation that test users/roles and relationships are as expected.

## API Requirements

Exercise implemented auth/me/logout, protected Farmer/Farm/Lot/Trace/QR endpoints, and public verify endpoint according to their actual contracts. The Plan's “Exporter” test wording is not used; discrepancy is reported.

## UI / UX Requirements

Unauthorized screens/actions are unavailable or controlled; public verification is accessible without login; error states do not expose server details.

## Security Requirements

Confirm no plaintext credentials, JWT/signing secrets, farmer PII, exact polygon data, raw QR payload/signature, or stack trace appears in public output, logs, collections, or evidence. Test HMAC tampering where implemented.

## Validation / Error Handling

Check generic failed-login messaging, 401 for missing/invalid/expired credentials, 403 for insufficient role, and documented public invalid-QR outcomes. Avoid asserting undocumented distinctions.

## Acceptance Criteria

- All four frozen roles have an evidenced allowed and forbidden action where applicable.
- Unauthenticated, invalid, and expired JWT behavior is verified.
- Generic authentication errors do not disclose account details.
- Public QR verification is unauthenticated/read-only while protected data remains protected.
- Public output contains no unapproved sensitive data or secrets.
- Every failure is filed with reproduction/evidence; no test silently changes permissions.

## Testing Requirements

Run role matrix, Postman security requests, existing auth/RBAC tests, frontend route checks, and sanitized evidence review. No penetration test is claimed.

## Evidence Requirements

Role matrix, status/response results without tokens, screenshots of safe UI states, sanitized logs, and defect references.

## Traceability

SRS FR-AUTH-001/002, SEC-01/02/03/05 narrowed by V1.0; Design Document Sections 4.1, 5.3, 8, 9, 10, 14, 17; Implementation Specification EPIC-6 RBAC/security testing; Minimum Project Plan Section 6.4/7.1; Baseline Sections 3-5; EPIC-1/4 contracts.

## Ownership, Git, and Change Control

Primary: Ephratha. Kidus maintains evidence/defect documentation; Biniyam supports frontend observations. Branch `feature/EPIC-6-QA-004-auth-rbac-security`; commit `test(qa): verify authentication RBAC and security boundaries`; PR to `develop`. Role/security changes require PM authorization.

## Blockers / Stop Conditions

Stop affected tests if auth/RBAC implementation is missing, role meaning conflicts, or QR contract is unresolved. Use no role beyond four frozen roles.
