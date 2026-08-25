# PD-002 - FIN Format Decision

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

## Current documented position

The two SRS references conflict on the first numeric segment: four digits in `FR-FARM-001`, three digits in `UC-01`. The Design Document narrows the implementation to V1.0 farmer registration and uniqueness but does not select a shape. EPIC-2-FARM-001 correctly marks the issue as blocking and requires escalation.

## Impact

The format affects FARM-001 validation/generation, FARM-002 API responses, FARM-005/EPIC-5 Farmer screens, fixtures, traceability records, and any later public/QR display of Farmer-related identifiers. Regenerating identifiers after implementation would invalidate data and evidence.

## Options

1. Use the functional requirement's four-digit form: `ETH-FAR-XXXX-XXXXXX`.
2. Use the use case's three-digit form: `ETH-FAR-XXX-XXXXXX`.
3. Approve another format only through a documented scope/requirements decision.
4. Defer Farmer implementation; no format-dependent coding.

## Recommended resolution

Recommendation only: prefer the explicit functional requirement (`FR-FARM-001`) over the use-case example if the approved hierarchy treats the SRS functional requirement as controlling detail. This remains subject to the authority decision PD-001 and Project Manager approval; no code may adopt it yet.

## Decision status

**UNRESOLVED - Project Manager approval required.** Final approved format: `UNRESOLVED`.

## Approval authority

Project Manager Kaleab, with Yedenekachew as Farmer/Polygon owner and Kidus recording the requirements decision.

## Dependencies

PD-001 authority hierarchy. Blocks finalization of EPIC-2-FARM-001 and any downstream task that asserts a FIN pattern. Does not block non-format planning.

## Acceptance criteria

- Every cited FIN reference and both conflicting shapes are recorded.
- Approved final format is a single exact string with validation semantics.
- Downstream tasks identify the approved decision as their source.
- Until approval, FARM-001 explicitly rejects developer-selected formats and uses escalation.

## Developer/PM handoff instructions

**DO NOT IMPLEMENT UNTIL APPROVED.** FARM-001 may prepare isolated collision/validation structure only if it does not encode an unapproved format; no Farmer fixture may claim a final FIN shape.
