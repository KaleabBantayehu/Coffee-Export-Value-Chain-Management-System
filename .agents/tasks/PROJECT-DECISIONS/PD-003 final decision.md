# Final Project Manager Decision

**Decision: APPROVED**

The Project Manager approves a new project-specific V1.0 Coffee Lot Global Identification Number (GIN) format through controlled change control.

## Approved V1.0 Format

```text
ETH-LOT-YYYY-NNNNNN
```

Where:

* `ETH` = Ethiopia project identifier
* `LOT` = Coffee Lot identifier
* `YYYY` = four-digit year of GIN generation
* `NNNNNN` = six-digit sequence or generated numeric identifier

Example:

```text
ETH-LOT-2026-000001
```

## Validation Shape

```text
^ETH-LOT-\d{4}-\d{6}$
```

## Decision Rationale

The authoritative requirements require a unique Coffee Lot GIN but do not define a normative V1.0 format. The illustrative Appendix C example must not be adopted directly because it includes a grade segment belonging to stretch-scope e-Waybill context and not to the simplified V1.0 Coffee Lot model.

This approved format is therefore a controlled project-specific V1.0 decision. It does not claim to be an externally mandated Ethiopian Coffee GIN standard.

## Downstream Instruction

TRACE-001 may implement generation and validation using this exact format.

TRACE-002, QR-related tasks, UI display, API responses, test fixtures, and downstream traceability records may depend on this format.

The format must remain isolated behind a named constant or configuration point to make any future controlled migration manageable.

**Final approved format: `ETH-LOT-YYYY-NNNNNN`**

**Decision status: APPROVED**

**Approval authority: Project Manager Kaleab**
