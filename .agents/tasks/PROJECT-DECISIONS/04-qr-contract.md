# PD-004 — Dynamic QR Contract and Security Decision

## Status

**APPROVED**

**Project Manager: APPROVED**

## Approved contract

This decision defines the bounded CEVCMS V1.0 QR contract consumed by
EPIC-4-QR-002 through EPIC-4-QR-006. It preserves the existing FastAPI,
PostgreSQL, JWT, and HMAC architecture.

### Payload and canonical serialization

The signed payload is compact JSON with exactly these fields in this order:

```json
{"v":1,"qrId":123,"gin":"ETH-LOT-2026-000001","issuedAt":"2026-09-05T10:00:00Z"}
```

`v` is payload version `1`; `qrId` is the public immutable QR identifier;
`gin` is the canonical Coffee Lot GIN; and `issuedAt` is server-generated UTC
creation time. Serialization uses compact JSON with no whitespace, UTF-8,
standard JSON escaping, ASCII-safe output, unsigned decimal integers without
leading zeroes, and an RFC 3339 UTC whole-second timestamp
(`YYYY-MM-DDTHH:MM:SSZ`). Generation and verification use the same shared
canonicalization function. `payload_hash` is the SHA-256 hexadecimal digest
of the exact canonical UTF-8 bytes.

### HMAC and QR identifier

HMAC-SHA256 signs the canonical UTF-8 bytes. The signature is unpadded
Base64URL and is compared using a constant-time comparison. The signing key is
the environment-provided `QR_HMAC_SECRET_KEY`; it is separate from
`JWT_SECRET_KEY` and must never be persisted, logged, returned, committed, or
included in artifacts.

The existing `QRRecord.qr_id` is the public `qrId`. It is unique, immutable,
distinct from the Coffee Lot GIN, non-secret, safe to place in a public URL,
and is never an authorization credential.

### Verification URL and verification

The QR encodes:

```text
{{PUBLIC_QR_BASE_URL}}/verify/{qrId}?sig={signature}
```

The backend route is:

```text
GET /api/v1/verify/{qrId}?sig={signature}
```

The server retrieves QRRecord by `qrId`, obtains trusted Coffee Lot GIN and
persisted `generated_at`, reconstructs the canonical payload, recomputes
HMAC-SHA256, and compares stored and supplied signatures using constant-time
comparison. Attacker-modified URL values are never authoritative payload data.
This path form supersedes the Design Document's illustrative
`/verify?id=<QR-ID>` form for V1.0.

### Lifecycle and generation authorization

Only one QRRecord is active for a Coffee Lot. A first generation creates an
active record and returns `201`. The optional request body is:

```json
{"regenerate": false}
```

With an active QR and `regenerate: false`, generation returns that active
record with `200`. With `regenerate: true`, it atomically deactivates the old
active record and creates a new active record with a new `qrId`, returning
`201`. Multiple inactive records may remain for audit/history. No physical
delete or separate revoke endpoint is added in V1.0. Unknown, inactive, and
unavailable QR/Lot records return the same generic public `404` response.
QR-002 must add the minimal lifecycle persistence required by this contract.

Only Admin and Field/Registry Agent may generate or regenerate QR codes. ECTA
Officer and Verifier cannot generate them. Backend authorization is the
security authority.

### Public response and status matrix

A valid public response contains only `status`, `gin_code`, nullable
`origin_region`, and `grade`. `origin_region` is sourced only from the
existing associated Cooperative `region` and is `null` when unavailable.
`grade` is populated only for a separately approved stretch record. The public
response excludes Farmer name, national ID, phone, Farm ID, polygon, exact
coordinates, credentials, signing secret, payload hash, signature, and other
internal database details.

| Endpoint | Status | Meaning |
| --- | --- | --- |
| `POST /api/v1/lots/{id}/qr` | `201` | New QRRecord, including explicit regeneration. |
|  | `200` | Existing active QRRecord. |
|  | `400` | Malformed request. |
|  | `401` | Unauthenticated. |
|  | `403` | Unauthorized. |
|  | `404` | Coffee Lot not found. |
|  | `500` | Generic generation failure without internal detail. |
| `GET /api/v1/verify/{qrId}?sig={signature}` | `200` | Valid public summary. |
|  | `400` | Malformed or tampered input; generic invalid detail. |
|  | `404` | Unknown, inactive, or unavailable QR/Lot; generic not-found detail. |

Generation success responses contain `qr_id`, `verification_url`, `image_svg`,
and `image_png_data_url`; they do not expose raw payload, payload hash, or a
separate signature field.

### Images, library, and exclusions

QR images are generated server-side on demand as SVG and PNG data URLs. No
image file, blob, CDN, or object storage is introduced. The approved QR-002
library is `segno`; it is narrowly scoped to server-side SVG and PNG QR image
generation and is not installed or implemented by this decision task.

This decision authorizes no HSM, RS256, OAuth/OIDC, MFA, Redis, blockchain,
microservice, new database, external QR service, or production infrastructure.

## Superseded proposal record

The following original proposal is retained for decision-history context only.
It is superseded by the approved contract above and has no normative effect.

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

## C. Previously unresolved decisions

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

## Historical proposal status

**SUPERSEDED — resolved by the approved contract above.**

## Approval authority

Project Manager Kaleab, with Fistum as QR owner, Biniyam for UI contract impact, Ephratha for security/testability, and Kidus for traceability.

## Dependencies

PD-001 and PD-003. Blocks QR implementation and QR-specific test completion.

## Acceptance criteria

- Sections A, B, and C are separated in the approved record.
- Every payload, identifier, storage, image, signature, response, invalid-case, and privacy decision has an approved value or explicit gap disposition.
- Public response excludes PII and signing material.
- Later tasks consume the contract without adding fields or behavior.

## Downstream implementation instruction

QR-002/003/004/005 and FE-009 must consume the approved contract above and
must not add fields or behavior beyond it.
