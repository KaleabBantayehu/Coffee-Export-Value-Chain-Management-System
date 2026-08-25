# PD-004 - QR Contract Decision

## Objective

Approve the complete V1.0 QR contract required by EPIC-4-QR-001 before QR backend, frontend, or QA implementation.

## Why the decision is needed

The sources establish HMAC-signed QR generation and public verification, but leave payload, identifier, persistence, representation, and response details incomplete.

## Authoritative sources

- SRS Module 06 `FR-TRACE-002`; Appendix C is illustrative e-Waybill material.
- Design Document Sections 5.3, 7.2, 8, 9.3-9.4, 10, 13, 17.
- Implementation Specification EPIC-4: QR payload schema, generation/HMAC, QR record storage, verification endpoint, invalid QR handling, public page.
- Minimum Project Plan Sections 4.1, 6.4, 7.1-7.2.
- [EPIC-4 overview](../EPIC-4/00-epic-overview.md) and [QR-001](../EPIC-4/01-qr-contract-and-security-decision.md).

## A. Already-defined requirements

- V1.0 uses QR generation plus HMAC signing; current decision records specify HMAC-SHA256 and an environment-provided signing key.
- Generation endpoint: `POST /api/v1/lots/{id}/qr`.
- Public verification endpoint: `GET /api/v1/verify/{qrId}`.
- QR flow includes a verification URL and Lot ID, signed payload, QR image, scan/open, and valid/invalid origin result.
- Public verification is unauthenticated, read-only, and non-sensitive.
- Protected trace data and public verification data are distinct; public output must not expose farmer national ID, phone number, exact polygon coordinates, secrets, or internal details.
- Existing Lot/Traceability data is the source; no new microservice/database/infrastructure is authorized.

## B. Inferred implementation choices, not approved facts

A canonical serialization method, a separate public identifier, a QR image library, PNG/SVG transport, QRRecord columns/lifecycle, duplicate-generation behavior, precise error statuses, and the exact coarse-origin fields may be reasonable implementation choices, but the current authoritative material does not fully define them. They must not be treated as approved facts.

## C. Unresolved decisions requiring approval

- Exact payload field names, values, and version marker.
- Whether GIN is included and how its unresolved format is handled.
- Canonical serialization and exact HMAC input/output encoding.
- `qrId` format, uniqueness, relation to database ID, and lifecycle.
- QRRecord relationship to CoffeeLot, uniqueness, active/deleted handling, and duplicate generation.
- PNG/SVG representation and narrowly scoped library.
- Exact success/error status and response schemas for both endpoints.
- Valid/tampered/malformed/unknown/nonexistent/inactive/deleted behavior.
- Whether any Lot/Farm origin data beyond an approved non-sensitive summary is in the payload.
- Whether farmer or Lot PII may appear in the payload. Recommendation: no PII; final approval required.

## Impact

PD-004 controls EPIC-4-QR-002/003/004/005/006, EPIC-5-FE-009, and EPIC-6 QR assertions. It also depends on PD-003 if GIN is a payload/display field.

## Recommended resolution

Recommendation only: approve the narrowest contract that satisfies the explicit URL/Lot-ID/HMAC/public-summary requirements, excludes PII, and reuses the modular monolith and environment-secret model. Do not add enterprise cryptography, infrastructure, or data fields. The Project Manager must approve each unresolved field or formally mark it as a gap.

## Decision status

**UNRESOLVED - Project Manager approval required.** Final QR contract: `UNRESOLVED`.

## Approval authority

Project Manager Kaleab, with Fistum as QR owner, Biniyam for UI contract impact, Ephratha for security/testability, and Kidus for traceability.

## Dependencies

PD-001 and PD-003. Blocks QR implementation and QR-specific test completion.

## Acceptance criteria

- Sections A, B, and C are separated in the approved record.
- Every payload, identifier, storage, image, signature, response, invalid-case, and privacy decision has an approved value or explicit gap disposition.
- Public response excludes PII and signing material.
- Later tasks consume the contract without adding fields or behavior.

## Developer/PM handoff instructions

**DO NOT IMPLEMENT UNTIL APPROVED.** QR-002/003/004/005 and FE-009 must stop on unresolved contract fields and use the escalation procedure.
