# Task Title

Lot Traceability Chain Retrieval API

## Task ID

EPIC-3-TRACE-004

## Epic

EPIC 3 — Traceability Engine

## Owner

Fistum (Backend Developer — Traceability & QR)

## Status

Not started.

## Priority

Critical — this is the endpoint that actually proves traceability works:
given a Lot, trace it back to its Farm and Farmer.

## Purpose

Implement `GET /api/v1/lots/{id}/trace`: the protected (authenticated)
retrieval of a Coffee Lot's full traceability chain, including its
originating Farm, Farmer, and full Traceability Event history.

## Why This Task Exists

This is the Implementation Specification's own stated Definition of Done
for EPIC 3: *"Given a Coffee Lot ID, the system accurately displays its
origin trace back to the registered farm and farmer."* Every other task in
this epic exists to produce data; this task is what actually demonstrates
that data traces correctly.

## Authoritative Sources

- Design Document §8 (API Design — Traceability table):
  `GET /api/v1/lots/{id}/trace` — "Retrieve the full traceability chain
  for a lot" — Auth: "JWT (protected view) / public summary via
  verification endpoint below" — "Protected route returns full detail
  incl. farmer contact fields; see Section 5.3 on public vs protected
  data."
- Design Document §5.3 ("What is public vs protected: the verification
  endpoint (Section 8) returns only non-sensitive traceability
  information... It does not expose the farmer's national ID, phone
  number, or exact polygon coordinates... consistent with data-protection
  principles implied by the SRS's PII column-encryption requirement (SRS
  SEC-03)") — this describes the **public** endpoint (EPIC 4's
  `GET /api/v1/verify/{qrId}`), by explicit contrast establishing that
  **this task's protected route is where full detail, including farmer
  contact fields, is intentionally exposed** to authenticated users.
- Implementation Specification, EPIC 3 Definition of Done (quoted above).

## Requirements Traceability

```text
SRS:
- FR-TRACE-001 (Module 06) — the lineage-retrieval portion of the
  narrowed DAG Traceability Engine requirement.

Design Document:
- Section 5.3 (public vs. protected data distinction — establishes this
  task's route as the "full detail" side of that distinction)
- Section 8 (GET /lots/{id}/trace contract, quoted above)

Implementation Specification:
- EPIC 3, Tasks: "Traceability history & lot detail API endpoints"
- EPIC 3, Definition of Done (quoted above) — this task is the direct
  implementation of that Definition of Done.

Minimum Project Plan:
- Section 7.1 WBS: "Functional/system walkthrough of full traceability
  use case | AD Sec. 12 | Kidus Ergetachew | Test Report (draft)" — this
  is the WBS item this task's endpoint makes possible to walk through;
  the walkthrough itself is TRACE-007's responsibility, not this task's.

Baseline Scope Freeze:
- Section 4, Critical Workflow — implicitly, this endpoint is what proves
  the chain from "Register Farmer" through "Create Traceability
  Record/Event" actually connects; the Baseline does not name this
  endpoint directly but its acceptance test (Section 4's full sequence)
  depends on it existing.
```

## Prerequisites

- `TRACE-002` merged; at least one real Coffee Lot exists with its
  auto-created initial event.

## Dependencies

`EPIC-3-TRACE-002` only. Does **not** depend on `TRACE-003` to function
correctly (a Lot with only its auto-created initial event is enough to
build and test against), though testing is more meaningful once
`TRACE-003` also exists and additional events can be appended — the two
tasks may proceed in parallel, per `00-epic-overview.md`'s
Parallelization Opportunities.

## Scope

### Allowed Scope

- `GET /api/v1/lots/{id}/trace`: given a Lot ID, return the Lot's own
  fields (GIN, status, created_at), its originating Farm (including
  polygon/area/EUDR data, per Design Document §5.3's "full detail"
  framing for the protected route), the Farmer that Farm belongs to
  (including contact fields — national ID, phone number — per Design
  Document §5.3's explicit contrast with the public endpoint), and the
  full ordered list of `TraceabilityEvent` rows against the Lot.

### Out of Scope

- The public, unauthenticated verification endpoint
  (`GET /api/v1/verify/{qrId}`) — that is EPIC 4, and returns a
  deliberately reduced, non-PII summary, which this task's endpoint does
  **not** need to replicate or share logic with (they serve different
  audiences with different data-exposure rules).
- Any QR-related logic.
- Any Lot splitting/merging/multi-origin lineage — out of V1.0 scope.

## Backend/Frontend/Database Responsibilities

Backend only. No frontend work (that is `TRACE-006`) and no schema
change.

## Files/Modules Likely Affected

Indicative paths, matched against the existing backend layout:

- `backend/app/api/v1/lots.py` (extended from `TRACE-002`/`TRACE-003`).
- `backend/app/schemas/lot.py` (extended with a trace-response schema
  aggregating Lot + Farm + Farmer + Events).
- `backend/app/services/lot_service.py` (extended) — the aggregation
  query/logic joining Lot, Farm, Farmer, and Events.
- `backend/tests/` — tests for the endpoint.

## Implementation Requirements

- Requires authentication only (any of the four roles), per Design
  Document §8's "JWT (protected view)" — no additional role restriction,
  consistent with how `GET /api/v1/farms/{id}` and
  `GET /api/v1/farmers/{id}` were implemented in `EPIC-2`.
- The response includes, at minimum: the Lot's GIN, status, and creation
  timestamp; the originating Farm's polygon/area/EUDR data (reusing
  `EPIC-2-FARM-003`/`FARM-004`'s existing retrieval logic or data shape
  rather than reimplementing it); the Farmer's full profile including
  contact fields (reusing `EPIC-2-FARM-002`'s existing retrieval logic or
  data shape); and the full, chronologically-ordered list of
  `TraceabilityEvent` rows against the Lot.
- A request for a non-existent Lot ID returns a structured `404`.
- The aggregation query correctly joins across `CoffeeLot -> Farm ->
  Farmer -> TraceabilityEvent` without an N+1 query pattern that would be
  unreasonably slow even at demo scale — a single well-formed query or a
  small, fixed number of queries is expected, not one query per event.

## Acceptance Criteria

- `GET /api/v1/lots/{id}/trace` for an existing Lot returns `200` with a
  response that correctly includes the Lot's GIN, the originating Farm's
  data, the Farmer's full profile (including contact fields), and all
  `TraceabilityEvent` rows for that Lot, in chronological order.
- The same request for a non-existent Lot ID returns `404`.
- An unauthenticated request is rejected with `401`.
- Given a Lot created against a specific Farm and Farmer (set up in a
  test), the response's Farm and Farmer data exactly match the source
  records — this is the literal "traces back to the registered farm and
  farmer" acceptance test from the Implementation Specification's EPIC 3
  Definition of Done.
- If additional events have been appended (via `TRACE-003`, once
  available), they all appear in the response in the correct order.

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- Test: retrieval for an existing Lot returns the correct, fully
  populated trace, verified against the exact Farm/Farmer records used to
  create it.
- Test: retrieval for a non-existent Lot returns `404`.
- Test: unauthenticated retrieval is rejected.
- Test: multiple events (if `TRACE-003` is available) appear in the
  correct chronological order.
- Test (performance-adjacent, at demo scale only — not a load test): the
  aggregation does not issue an unbounded number of queries proportional
  to event count in an obviously inefficient way.
- Regression: `TRACE-002`'s (and, if merged, `TRACE-003`'s) tests still
  pass.

## Security Considerations

- This route intentionally exposes farmer PII (national ID, phone number)
  to any authenticated user, per Design Document §5.3's explicit design —
  this is not a defect; it is the documented contrast with the public
  verification endpoint. Do not add PII redaction here — that would
  contradict Design Document §5.3, and if the team believes redaction is
  actually needed even for authenticated users, that is a change-control
  decision, not a change to make silently in this task.
- Authentication enforcement is via `EPIC-1-AUTH-003`'s dependency only.

## Expected Outputs / Deliverables

- A working, tested `GET /api/v1/lots/{id}/trace` endpoint that
  demonstrably satisfies the Implementation Specification's EPIC 3
  Definition of Done.

## Definition of Done

- All items in "Acceptance Criteria" are true and independently
  verifiable.
- All items in "Testing Requirements" pass.
- Reviewed and approved by at least one other team member.
- Merged into `develop`.
- Requirements-traceability entry updated (Kidus), explicitly noting this
  endpoint satisfies the Implementation Specification's EPIC 3 Definition
  of Done.

## Change-Control Conditions

- If reusing `EPIC-2`'s Farm/Farmer retrieval logic proves impractical
  (e.g., its actual implementation shape differs from what this task file
  assumes), escalate per
  `.agents/execution/06-failure-and-escalation.md` rather than
  duplicating that logic wholesale without recording why.

## Git/Branch Expectations

- Branch: `feature/EPIC-3-TRACE-004-lot-trace-retrieval-api`, from
  `develop`.
- Commit message pattern: `feat(traceability): implement lot traceability chain retrieval API`.
- PR references Task ID `EPIC-3-TRACE-004` and confirms the response
  includes Farm, Farmer, and full Event history.
- Merge target: `develop`.

## Expected Agent Report

Standard format from `.agents/execution/04-human-review-and-approval.md`,
plus:

1. Confirmation that the response correctly traces back to the exact
   Farm/Farmer records used in a test, with the verification method used.
2. Confirmation of how `EPIC-2`'s existing Farm/Farmer retrieval logic was
   reused (vs. duplicated, and why).
3. The query/aggregation approach used, and confirmation it does not
   produce an N+1 pattern.
4. Test results.
