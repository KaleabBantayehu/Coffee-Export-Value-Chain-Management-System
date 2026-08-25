# EPIC-4-QR-001 - QR Contract and Security Decision

## Objective

Produce the approved V1.0 QR contract that all later backend/frontend tasks consume, without inventing details absent from authoritative documents.

## Scope

Define, obtain PM review for, and record the QR payload fields, canonical serialization, versioning if required, `qrId`/public identifier semantics, verification URL construction, PNG/SVG representation contract, QR library choice if needed, HMAC-SHA256 signing input/output, allowed public response fields, and invalid/inactive/deleted-record behavior. Preserve the documented requirement that the payload includes a verification URL and lot ID and that the signature is HMAC-based.

## Out of scope

Coding endpoints, database migrations, UI, enterprise cryptography, HSM, RS256, OAuth/OIDC, new infrastructure, or changing EPIC-3 identifiers.

## Preconditions and dependencies

EPIC-3-TRACE-007 must be approved with a real persisted Lot/Traceability handoff, or a PM-recorded exception. Read the Baseline, Design Document, Implementation Specification, Minimum Project Plan, SRS Module 06, and EPIC-3 package. Dependencies: EPIC-3-TRACE-007; PM decision on all listed gaps.

## Inputs

Authoritative documents, EPIC-3 API/GIN contract, frozen environment configuration, and PM decision record.

## Expected outputs

An approved decision/contract document or traceability entry consumed by QR-002 through QR-006, including exact payload examples using synthetic data, field sensitivity classification, error/status matrix, HMAC canonicalization, and selected narrowly scoped QR library with reason and dependency-file impact. If a point remains unspecified, write exactly: **Traceability gap - requires review.**

## Relevant files/modules

`.agents/tasks/EPIC-4/`, `docs/`, QR service/schema/router modules to be created by later tasks, `.env.example` only if an already-approved configuration name must be documented. No application source code is required for this task.

## Backend responsibilities

Specify the contract consumed by FastAPI/SQLAlchemy QR services and the HMAC signing/verification boundary; do not implement it here.

## Frontend responsibilities

Specify generation result and public verification result shapes, image representation, verification URL, and error states.

## Database responsibilities

Specify the minimum QRRecord relationship and uniqueness/lifecycle requirements only if supported by the Design Document; identify missing schema details for PM review rather than authorizing a migration.

## API requirements

Record the exact contracts for `POST /api/v1/lots/{id}/qr` and `GET /api/v1/verify/{qrId}`, including auth, success, malformed, unknown, inactive/deleted, and tampered cases. Do not fabricate status codes where the sources are silent; mark the gap.

## Security requirements

HMAC-SHA256 with an environment-provided secret is frozen. Define canonical signing input and public minimization. Reject tampering and malformed payloads, never disclose the secret, and do not approve enterprise mechanisms outside V1.0.

## Acceptance criteria

- PM-reviewed contract states the exact payload/serialization or explicitly records the gap.
- PM-reviewed `qrId` semantics, QRRecord identity/lifecycle, and public response fields exist or are explicitly marked as gaps.
- HMAC-SHA256 signing and verification input is identical and documented.
- PNG/SVG and library decisions are traceable and do not expand the frozen stack.
- No QR implementation task is authorized to guess an unresolved item.

## Testing requirements

Review/consistency checks against every cited document; contract examples parse as the approved shape; security review confirms no PII/secret in public examples. No application test is required because this is a decision artifact.

## Traceability

SRS FR-TRACE-002 and Appendix C (illustrative only); Design Document Sections 5.3, 8, 9.3-9.4, 10, 13, 17; Implementation Specification EPIC 4 first task and DoD; Minimum Project Plan Sections 4.1, 7.1, 7.2; Baseline Sections 3.1 and 4; EPIC-3-TRACE-007 handoff. Missing exact details remain **Traceability gap - requires review.**

## Ownership, Git, and change control

Primary: Fistum. Supporting: Ephratha and Kidus. Verification: PM/human reviewer plus Ephratha security review. Use `feature/EPIC-4-QR-001-qr-contract` from `develop`; commit `docs(qr): define QR contract and security decision`; PR to `develop`, human review required. Any new field, identifier rule, response field, library, or architecture deviation is Required only when directly documented; otherwise stop and use `.agents/execution/06-failure-and-escalation.md`. Definition of done includes approved decision record, traceability update, review, merge, and no silent resolution.
