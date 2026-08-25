# EPIC-4-QR-005 - Frontend Public Verification Page

## Objective

Provide the unauthenticated React page reached from a generated QR verification URL and render the approved valid/invalid public result.

## Scope

Create a public route that reads the approved QR identifier from the URL, calls `GET /api/v1/verify/{qrId}`, and displays the exact approved verification status and non-sensitive origin summary. Handle valid, invalid/tampered, unknown/nonexistent, inactive/deleted, loading, network, and malformed URL states.

## Out of scope

Authentication, protected trace view, QR generation/signing, public writes, farmer PII, exact polygon coordinates, new public data fields, offline caching, native mobile, and marketing/portal functionality.

## Preconditions and dependencies

QR-001 approved; QR-003 merged and actual response inspected; existing React/Vite app and routing are available. Dependency: QR-003. If its response or identifier contract is not stable, stop and escalate.

## Inputs and expected outputs

Input: QR identifier from the approved URL. Output: approved public response, limited to non-sensitive verification/origin fields, with explicit valid/invalid state and no internal error detail.

## Relevant files/modules

`frontend/src/pages/` public verification page, `frontend/src/api/` verification client, route configuration, `frontend/src/tests/` or current test location, and existing CSS. Reuse existing app patterns.

## Backend responsibilities

None; consume QR-003 only.

## Frontend responsibilities

Ensure route is intentionally public, validate/encode the path parameter safely, render approved fields and states, avoid PII, and make invalid/tampered results understandable without exposing implementation details.

## Database responsibilities

None.

## API requirements

Call only `GET /api/v1/verify/{qrId}` with the approved encoded identifier. Do not add authentication headers as a requirement for the public flow or create a fallback to protected trace data.

## Security requirements

Treat URL and response as hostile input; avoid injection via rendered values; do not log secrets or sensitive response fields. Confirm the page does not expose farmer national ID, phone number, exact coordinates, raw payload/signature, database internals, or stack traces.

## Acceptance criteria

- Opening a valid generated QR URL without authentication displays the approved valid result and permitted origin information.
- A tampered, malformed, unknown, nonexistent, inactive, or deleted QR displays the approved invalid/error state without sensitive detail.
- The page is reachable without login and does not redirect public users to the protected trace view.
- Rendered fields exactly match QR-001/003 and contain no unapproved PII.
- No page crash or blank state occurs for API/network errors.

## Testing requirements

Frontend test/manual evidence for valid, invalid/tampered, unknown, unauthenticated, malformed URL, and network-error states; public-data snapshot/inspection; injection-safe rendering check; frontend checks and regression suite; manual browser walkthrough from the generated QR link.

## Traceability

Design Document Sections 5.3, 8, 9.4, 13; Implementation Specification EPIC 4 user flow/DoD and EPIC 5 frontend integration; Minimum Project Plan Sections 6.4, 7.1-7.2; Baseline Section 4; QR-001/003. Missing public response details remain **Traceability gap - requires review.**

## Ownership, Git, and change control

Primary: Biniyam. Abel support requires PM resolution of the ownership conflict. Verification: Ephratha plus independent human reviewer; Kidus records evidence. Branch `feature/EPIC-4-QR-005-public-verification`; commit `feat(qr): add public QR verification page`; PR to `develop`. Definition of done requires all criteria/tests, public minimization evidence, review, merge, and traceability update. Do not add public search, account creation, or extra fields without approval.
