# PD-002 - FIN Format Decision

**Decision date:** 2026-09-02

## Objective

Resolve the V1.0 Farmer Identification Number format without allowing an implementation task to invent one.

## Why the decision is needed

FARM-001 cannot finalize generation/validation or stable fixtures while authoritative sources specify different FIN shapes.

## Authoritative sources and references

- SRS `FR-FARM-001`: `ETH-FAR-XXXX-XXXXXX`.
- SRS `UC-01`, “Register Smallholder Farmer”: `ETH-FAR-XXX-XXXXXX`.
- Design Document Section 4.2: FIN is generated and unique per `FR-FARM-001`, but does not restate segment lengths.
- Design Document Section 7.2: Farmer `fin_code`, unique.
- Implementation Specification EPIC-2 Farmer/FIN task.
- [EPIC-2 overview](../EPIC-2/00-epic-overview.md), “Known Ambiguities”, item 1.

## Context

The two SRS references conflict on the first numeric segment. `FR-FARM-001`
specifies `ETH-FAR-XXXX-XXXXXX`, while UC-01 specifies
`ETH-FAR-XXX-XXXXXX`. The Design Document requires generated, unique FINs but
does not resolve the segment length.

## Conflicting formats

1. `ETH-FAR-XXXX-XXXXXX`
2. `ETH-FAR-XXX-XXXXXX`

## Approved canonical format

**CEVCMS V1.0 uses `ETH-FAR-XXXX-XXXXXX` as its canonical FIN format.**

Segment interpretation for V1.0:

- `ETH` = Ethiopia.
- `FAR` = Farmer.
- `XXXX` = a four-character regional or registration segment placeholder.
- `XXXXXX` = a six-character unique farmer sequence placeholder.

The placeholders do not currently represent a specified official Ethiopian
administrative code or prescribed generation scheme. A later approved
requirement may define their generation semantics without changing this
canonical V1.0 format.

## Rationale

The approved format adopts the explicit functional-requirement form in
`FR-FARM-001`. It resolves the same-document conflict before identifier
generation, validation, fixtures, and downstream Farmer/Farm relationships
are implemented.

## Impact

The format affects FARM-001 validation/generation, FARM-002 API responses, FARM-005/EPIC-5 Farmer screens, fixtures, traceability records, and any later public/QR display of Farmer-related identifiers. Regenerating identifiers after implementation would invalidate data and evidence.

## Decision status

**APPROVED - Project Manager decision.** Final approved format:
`ETH-FAR-XXXX-XXXXXX`.

## Approval authority

Project Manager Kaleab, with Yedenekachew as Farmer/Polygon owner and Kidus recording the requirements decision.

## Scope and impact

This decision applies to FIN generation, validation, Farmer API responses,
frontend Farmer displays, fixtures, traceability references, and later FIN
presentation. It changes no other identifier format, business rule, schema,
or role model.

Future EPIC-2 implementation, beginning with `EPIC-2-FARM-001`, must use
`ETH-FAR-XXXX-XXXXXX` consistently unless a higher-level approved project
requirement explicitly replaces it.

## Acceptance criteria

- Every cited FIN reference and both conflicting shapes are recorded.
- The approved final format is a single exact string.
- Downstream tasks identify this approved decision as their source.

## Developer/PM handoff instructions

`EPIC-2-FARM-001` is unblocked for its format-dependent generation and
validation work. It must use the approved canonical format above.
