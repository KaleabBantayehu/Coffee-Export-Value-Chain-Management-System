# EPIC-4-QR-002 - QR Record and Generation API

## Objective

Implement authenticated QR generation for an existing CoffeeLot using only the approved QR-001 contract.

## Scope

Create/reuse the QRRecord persistence boundary permitted by the approved design; validate Lot existence and active state as specified; build the approved payload; compute HMAC-SHA256; generate the approved PNG/SVG representation; persist the record; and implement `POST /api/v1/lots/{id}/qr` as one consistent operation.

## Out of scope

Public verification, public page, Lot/Traceability changes, GIN redesign, duplicate speculative endpoints, QR rotation/revocation rules not approved in QR-001, HSM/RS256/Redis/offline sync, and new databases/frameworks.

## Preconditions and dependencies

EPIC-3-TRACE-007 handoff is verified and approved; EPIC-4-QR-001 is PM-approved; EPIC-1 JWT/auth and the applicable role model are actually implemented and verified; EPIC-0 database access works. Dependencies: QR-001 and EPIC-3 Lot/trace APIs. Stop if any prerequisite is only specified rather than implemented/tested/verified/approved.

## Inputs and expected outputs

Input: Lot path ID and authenticated context. Output: the approved QRRecord/generation response including the approved public identifier and QR image representation, without the signing key. Persisted output is linked to the target CoffeeLot with the approved uniqueness and lifecycle behavior.

## Relevant files/modules

`backend/app/api/v1/` QR router, `backend/app/schemas/` QR schemas, `backend/app/services/` QR/HMAC service, `backend/app/db/models.py` or an approved migration location, `backend/app/core/config.py`, dependency manifest only if QR-001 approved a narrowly scoped library, and `backend/tests/`.

## Backend responsibilities

Validate path/auth input, load the Lot, build canonical payload, sign, encode, persist, return structured success/errors, and preserve transaction integrity. Reuse EPIC-3 models/services; do not duplicate Lot logic.

## Frontend responsibilities

None beyond documenting the response contract consumed by QR-004.

## Database responsibilities

Implement only the QRRecord relationship/constraints approved in QR-001. Ensure failed signing/encoding/persistence cannot leave an invalid or orphaned QR record.

## API requirements

`POST /api/v1/lots/{id}/qr`; protected by the existing JWT/RBAC mechanism as specified by the approved contract. Handle nonexistent Lot, invalid ID, inactive/deleted Lot, duplicate generation if applicable, and internal failure with structured responses and no stack traces.

## Security requirements

Never accept client-supplied HMAC/signature/created_by fields. Read the QR signing secret from environment configuration. Sign exactly the canonical approved payload. Avoid predictable public identifiers if QR-001 requires otherwise; do not decide that format here. Do not log payload secrets or PII.

## Acceptance criteria

- Authorized authenticated caller generates a QR for an existing traceable Lot and receives the approved image/identifier shape.
- Unauthorized/unauthenticated calls are rejected according to the existing V1.0 auth/RBAC contract.
- Nonexistent or inactive/deleted Lot is rejected without a partial QRRecord.
- Persisted QRRecord links to the correct Lot and can be consumed by QR-003.
- Recomputed signature over the stored canonical payload matches the stored signature.
- Failure at any generation/persistence step leaves no invalid persisted record.

## Testing requirements

Unit tests for canonical payload signing and generation success/failure; endpoint tests for success, invalid input, missing Lot, auth/RBAC, transaction failure, and duplicate behavior if required; Postman request; database relationship/rollback check; regression suite. Manual verification must inspect the generated representation without exposing the secret.

## Traceability

SRS FR-TRACE-002; Design Document Sections 5.3, 7.2, 8, 10, 13, 17; Implementation Specification EPIC 4 tasks “QR payload schema design, QR generation logic & HMAC signing” and “QR record storage”; Minimum Project Plan Sections 7.1-7.2; Baseline Sections 3.1 and 4; dependency EPIC-3-TRACE-007. Any unresolved QR-001 field is **Traceability gap - requires review** and blocks the affected code.

## Ownership, Git, and change control

Primary: Fistum. Supporting: Ephratha for tests; Biniyam/Abel only for contract coordination. Verification: Ephratha plus independent human reviewer. Branch `feature/EPIC-4-QR-002-generation-api`; commit `feat(qr): implement signed QR generation API`; merge to `develop` by PR after review. Definition of done requires all criteria/tests, regression, traceability update by Kidus, review, merge, and no out-of-scope technology. Any schema/API/crypto deviation is escalated, not improvised.
