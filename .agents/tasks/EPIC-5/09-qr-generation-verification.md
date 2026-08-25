# EPIC-5-FE-009 - QR Generation and Verification Frontend

## Objective

Integrate the authenticated QR generation screen and unauthenticated public verification page with the approved EPIC-4 contracts.

## Scope

Consume `POST /api/v1/lots/{id}/qr` for an existing Lot; display the approved QR image/identifier and documented download/print behavior; consume `GET /api/v1/verify/{qrId}` publicly; render approved valid/invalid/non-sensitive results.

## Out of Scope

QR signing/payload construction, QR library selection, QRRecord schema, public response design, backend verification, protected trace replacement, new auth, or invented QR fields.

## Preconditions

FE-001/003/007/008 available; EPIC-4-QR-001 approved and QR-002/003/004/005 implemented, tested, verified, approved; actual response shapes inspected.

## Dependencies

FE-001/003/007/008; EPIC-4-QR-001 through QR-005; EPIC-3 verified Lot/trace handoff. Any QR-001 gap blocks the affected UI.

## Inputs

Approved QR contract, generation and verification API responses, Lot ID, synthetic valid/tampered/unknown fixtures, and Design Document Sections 5.3, 8, 9.3-9.4, 13.

## Expected Outputs

Authenticated generation UI and public verification UI matching the approved contract and security boundary.

## Relevant Files / Modules

Existing EPIC-4 QR pages/API clients if present, route/navigation files, shared result components, and current `frontend/src` structure.

## Backend Responsibilities

None; consume EPIC-4 APIs only.

## Frontend Responsibilities

Generation action/result/download/print, public route parsing, valid/invalid states, loading/errors, and data minimization.

## Database Responsibilities

None.

## API Requirements

Use exactly the inspected QR-002 and QR-003 contracts. Do not invent payload/identifier/response fields or call protected trace data as a public fallback.

## UI / UX Requirements

QR image is visibly usable; public valid/invalid results are clear; public route requires no login; generation remains protected.

## Security Requirements

No HMAC/JWT secret in source or UI. Public page exposes no PII, exact coordinates, raw signature/payload, internal IDs unless explicitly approved, or stack traces. Existing auth state protects generation.

## Validation / Error Handling

Treat URL/response values as untrusted; handle tampered, malformed, unknown, inactive/deleted, 401/403, and network outcomes exactly as approved.

## Acceptance Criteria

- Authorized user can generate and display the approved QR for an existing Lot.
- Public user can open the approved verification URL without login.
- Valid and invalid outcomes render the approved non-sensitive response.
- Download/print and identifier behavior match QR-001.
- No QR contract detail is guessed or leaked.

## Testing Requirements

Test/manual evidence for generation success/error, protected access, public valid/tampered/malformed/unknown states, data minimization, safe URL handling, and image behavior; run build/lint and EPIC-4 regression tests.

## Traceability

SRS FR-TRACE-002; Design Document Sections 5.3, 8, 9.3-9.4, 10, 13, 17; Implementation Specification EPIC-4 QR flow and EPIC-5 QR Generation & Verification screen; Minimum Project Plan Sections 6.4, 7.1-7.2; Baseline Sections 2-4; EPIC-4-QR-001 through QR-005.

## Ownership, Git, and Change Control

Primary: Biniyam; Abel QR UI support subject to documented ownership decision. Verification: Ephratha; Kidus evidence. Branch `feature/EPIC-5-FE-009-qr-integration`; commit `feat(frontend): integrate QR generation and verification`; PR to `develop`. Any QR contract or public-data change escalates.

## Blockers / Stop Conditions

Stop if QR-001 is not approved or QR API/image/public response is unresolved. Do not choose a QR payload, identifier, library, or public schema.
