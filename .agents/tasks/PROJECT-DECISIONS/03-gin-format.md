# PD-003 - GIN Format Decision

## Objective

Determine and approve the V1.0 Global Identification Number format, or formally accept a documented gap without inventing one.

## Why the decision is needed

EPIC-3-TRACE-001 needs a stable identifier for generation, validation, Lot responses, QR payloads, and test fixtures. The authoritative sources establish uniqueness but not a V1.0 format.

## Authoritative sources and references

- SRS Module 06, `FR-TRACE-001` and `FR-TRACE-002`: traceability/cryptographic QR requirements; no V1.0 GIN format string.
- SRS Appendix C: illustrative `ETH-LOT-2026-G1-00392` in an e-Waybill context; not a V1.0 normative format and includes stretch grading information.
- Design Document Section 5.2: unique GIN in the spirit of the SRS concept, scoped to the simplified lot model, without a format.
- Design Document Section 7.2: unique `CoffeeLot.gin_code`.
- Implementation Specification EPIC-3 Lot/GIN task.
- [EPIC-3 overview](../EPIC-3/00-epic-overview.md), Open Decision 2 and handoff requirements.

## Current documented position

Uniqueness and existence are required. The Appendix C string is illustrative and unsuitable as a direct V1.0 requirement because it embeds `G1` grade information and belongs to stretch e-Waybill context. No other source defines prefix, segment lengths, sequence, or validation rule.

## Impact

A GIN decision affects TRACE-001/002, Lot and trace UI, QR-001 payload, public output if GIN is approved for display, fixtures, and database evidence. Changing it after Lots exist risks invalidating the chain and QR records.

## Options

1. Approve a minimal V1.0 format derived from an explicit source, if the Project Manager determines the sources support that interpretation.
2. Approve a new project-specific format through controlled change control.
3. Keep format unresolved and allow only format-independent preparation; defer final Lot/QR implementation.

## Recommended resolution

No format-specific recommendation is authorized from the current documents. The minimum defensible recommendation is option 3 until the Project Manager explicitly approves a format or formally accepts a non-blocking gap with migration/test consequences. This preserves traceability and avoids converting an illustrative example into a requirement.

## Decision status

**UNRESOLVED - Project Manager approval required.** Final approved format: `UNRESOLVED`.

## Approval authority

Project Manager Kaleab, with Fistum as Traceability/QR owner and Kidus recording the decision.

## Dependencies

PD-001. Blocks final TRACE-001 format, format-dependent TRACE-002 fixtures, QR-001 payload decisions that include GIN, and downstream QR/UI assertions.

## Acceptance criteria

- Normative requirements are separated from Appendix C's illustrative example.
- The absence of a V1.0 format is explicitly recorded.
- An approved format or formal non-blocking disposition is recorded.
- Downstream tasks have an unambiguous instruction and cannot invent a format.

## Developer/PM handoff instructions

**DO NOT IMPLEMENT UNTIL APPROVED** for any format-dependent generator/validator or QR assertion. Do not use the Appendix C example as-is.
