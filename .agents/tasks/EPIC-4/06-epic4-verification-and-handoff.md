# EPIC-4-QR-006 - EPIC Verification and Core-Chain Sign-off

## Objective

Independently verify the complete V1.0 acceptance workflow through QR generation and public verification, then produce the evidence-backed EPIC-4 completion and handoff report.

## Scope

Run API/Postman, automated regression, database, browser, and manual security/data-minimization checks across QR-001 through QR-005 and the EPIC-3 handoff. Exercise login -> existing Farmer/Farm/Polygon -> Lot -> Traceability Event -> protected trace -> authenticated QR generation -> open QR URL without authentication -> valid public origin result. Exercise tampered, malformed, unknown/nonexistent, inactive/deleted, unauthorized, and failure cases. File defects against the owning task; update traceability matrix, Test Report, and demo evidence.

## Out of scope

Implementing fixes or new functionality, resolving source conflicts unilaterally, load/performance testing, formal penetration testing, real external integrations, and modifying EPIC-0 through EPIC-3, rules, execution procedures, or authoritative documents.

## Preconditions and dependencies

QR-001 through QR-005 are implemented, tested, reviewed, and merged to `develop`; EPIC-3-TRACE-007 handoff is approved; backend/frontend run locally; synthetic/seeded data is available. Dependencies: all preceding EPIC-4 tasks and EPIC-3 completion evidence.

## Inputs and expected outputs

Inputs: merged application, Postman collection, test suites, database access, synthetic credentials/data, approved QR contract, and task reports. Outputs: completion-gate checklist, Postman results, automated test results, database linkage evidence, manual walkthrough/Test Report section, defect log entries, updated requirements traceability, and explicit GO/BLOCKED statement for EPIC completion.

## Relevant files/modules

Postman collection location established by QR-002/003, `backend/tests/`, `frontend/` test/manual evidence location, `docs/testing/` or current test documentation, requirements-traceability location, and Test Report. Do not modify application source merely to pass this task.

## Backend responsibilities

Verify QR-002/003 behavior, database links, transaction integrity, auth/RBAC, signature validity, public response minimization, and structured invalid/error handling.

## Frontend responsibilities

Verify QR-004/005 screens, routing, rendered image/link, public valid/invalid states, and the unbroken browser workflow.

## Database responsibilities

Read-only evidence query confirming Farmer -> Farm -> CoffeeLot -> TraceabilityEvent -> QRRecord relationships and no orphan/invalid QR records. Do not insert demo data directly when the acceptance requirement says it must be created through the UI.

## API requirements

Run every EPIC-4 endpoint request with success, invalid, unauthorized/protected, public, tampered, unknown, and failure cases supported by the approved contract. Record exact status/result evidence without secrets or PII.

## Security requirements

Confirm HMAC key and JWT secret do not appear in logs, collections, screenshots, or documents. Confirm public verification is unauthenticated but read-only and non-PII; protected generation remains authenticated/RBAC; malformed/tampered identifiers do not reveal internals; no unauthorized technologies or integrations were introduced.

## Acceptance criteria

- QR-001 contract gaps are resolved or explicitly recorded as PM-approved non-blocking gaps; no silent choices remain.
- A real synthetic Lot created through the UI can generate a QR and open its public URL successfully without authentication.
- Public valid output contains only approved non-sensitive origin data; farmer PII, exact coordinates, secrets, payload internals, and stack traces are absent.
- Invalid/tampered/malformed/unknown/nonexistent/inactive/deleted QR cases behave exactly as approved.
- Protected generation and all prior protected APIs enforce the approved auth/RBAC behavior.
- Database evidence confirms the complete linked chain and QRRecord relationship.
- EPIC-3 and full automated regression suites remain green.
- Any failure is filed against an owning task and EPIC-4 is marked BLOCKED until fixed/reverified.

## Testing requirements

Run all backend/frontend tests, every Postman request, database read-only verification, manual browser walkthrough, input-validation and RBAC checks, public-data inspection, and regression tests on the merged integration branch. No load or formal penetration test is required or permitted as a completion substitute.

## Traceability

SRS FR-TRACE-002 and security context; Design Document Sections 5.3, 8, 9.3-9.4, 10, 13, 17, 20; Implementation Specification EPIC 4 DoD and single acceptance target; Minimum Project Plan Sections 4.1, 6.4, 7.1-7.2 and M4; Baseline Section 4; `.agents/execution/03-verification-and-testing.md`, `06-failure-and-escalation.md`, `07-task-completion-checklist.md`; EPIC-3-TRACE-007 handoff.

## Ownership, Git, and change control

Primary verification owners: Ephratha (API/integration/RBAC) and Kidus (walkthrough, traceability, Test Report). Independent human reviewer required. Branch `feature/EPIC-4-QR-006-verification`; commits `test(qr): verify EPIC 4 acceptance workflow` and `docs(qr): record EPIC 4 verification evidence`; PR to `develop`. Definition of done requires evidence for every criterion, defect disposition, traceability/docs update, human approval, merge, and explicit GO only when no blocking gap remains. Any unresolved contract conflict, ownership conflict, or scope expansion follows the standard escalation format and blocks the affected work.
