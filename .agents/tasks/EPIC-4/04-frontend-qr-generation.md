# EPIC-4-QR-004 - Frontend QR Generation

## Objective

Provide the authenticated React workflow to generate, display, and use the QR representation returned by QR-002 for an existing Coffee Lot.

## Scope

Add the QR generation screen/action to the existing role-aware React navigation; accept/select an existing Lot using the established Lot/trace flow; call `POST /api/v1/lots/{id}/qr`; render the approved QR image and identifier; support the approved display/download/print behavior; show loading, success, authorization, invalid-Lot, and backend-error states.

## Out of scope

QR signing, payload construction, public verification, new auth/token handling, new Lot lookup/trace logic, offline support, mobile app, UI framework changes, and a frontend-only security boundary different from QR-002.

## Preconditions and dependencies

QR-001 approved; QR-002 API merged and actual response inspected; EPIC-1 auth state/protected routing and EPIC-3 Lot/trace UI are implemented and verified. Dependency: QR-002, with EPIC-3-TRACE-005/006 reused as-is. If response/image shape differs, stop and escalate rather than guessing.

## Inputs and expected outputs

Input: authenticated user and existing Lot selection/ID. Output: approved QR image/identifier and verification link, with user-visible structured errors. No signing secret or private trace data is rendered.

## Relevant files/modules

`frontend/src/pages/` QR generation page, `frontend/src/api/` QR client, existing navigation/auth components, `frontend/src/tests/` or current test location, and existing styling files. Match actual repository structure before implementation.

## Backend responsibilities

None; consume QR-002 contract only.

## Frontend responsibilities

Use existing JWT/auth state, role-aware route/action visibility from EPIC-1, stable image rendering, response validation, error states, and approved download/print action.

## Database responsibilities

None.

## API requirements

Call only `POST /api/v1/lots/{id}/qr` with the approved path/input. Do not send client signature, payload, user attribution, or secret fields.

## Security requirements

Protected route/action must follow QR-002. Do not store or expose the HMAC secret. Do not display protected farmer PII on this screen. Treat image/URL response as untrusted until validated against the approved shape.

## Acceptance criteria

- An authorized authenticated user can choose an existing Lot and see the generated approved QR representation and identifier.
- Unauthenticated navigation redirects to login using existing protection.
- Unauthorized role/action is handled consistently with QR-002, without a weaker frontend-only claim.
- Backend failures and invalid Lots produce a clear error state without fabricated details.
- Verification link/identifier and download/print behavior match QR-001.

## Testing requirements

Frontend test/manual evidence for success rendering, loading/error states, unauthenticated redirect, unauthorized response, and approved image/link behavior. Confirm no secret/PII appears in rendered output. Run frontend checks and full regression where configured; record a manual browser walkthrough.

## Traceability

Design Document Sections 8, 9.3, 13; Implementation Specification EPIC 4 user flow and EPIC 5 frontend integration/QR UI ownership; Minimum Project Plan Section 7.1 “Build traceability lineage view + QR display/download” and Section 7.2 M4; Baseline Sections 2 and 4; QR-001/002 and EPIC-3 handoff. Any missing response/image contract is **Traceability gap - requires review.**

## Ownership, Git, and change control

Primary: Biniyam. Abel is supporting only if PM resolves the documented ownership conflict; do not silently reassign. Verification: Ephratha for integration and an independent human reviewer; Kidus updates traceability. Branch `feature/EPIC-4-QR-004-frontend-generation`; commit `feat(qr): add frontend QR generation workflow`; PR to `develop`. Definition of done requires criteria/tests, response-shape inspection, review, merge, and documentation. No new framework/library or public-data behavior without change control.
