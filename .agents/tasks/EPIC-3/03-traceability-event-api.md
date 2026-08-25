# Task Title

Append-Only Traceability Event Logging API

## Task ID

EPIC-3-TRACE-003

## Epic

EPIC 3 — Traceability Engine

## Owner

Fistum (Backend Developer — Traceability & QR)

## Status

Not started.

## Priority

Critical — the primary acceptance path's "Create Traceability Record /
Event" step.

## Purpose

Implement `POST /api/v1/lots/{id}/events`: append a Traceability Event to
an existing Coffee Lot's event log, enforcing append-only behavior (no
update or delete route).

## Why This Task Exists

Baseline §4 lists "Create Traceability Record / Event" as its own step,
distinct from Lot creation. Design Document §5.1 describes
`TraceabilityEvent` as "an append-only log entry" and gives examples
beyond the automatic "lot created" event that `TRACE-002` already
produces (e.g., events a Field/Registry Agent or other actor might record
manually against an existing lot).

## Authoritative Sources

- Design Document §5.1 ("TraceabilityEvent (append-only log)")
- Design Document §7.2 (`TraceabilityEvent` entity: `event_id`, `lot_id`
  (FK), `event_type`, `event_timestamp`, `recorded_by` (FK to User),
  `notes` — already created by `EPIC-0-DB-002`)
- Design Document §8 (API Design — Traceability table):
  `POST /api/v1/lots/{id}/events` — "Append a traceability event" — Auth:
  "JWT" — "Body: event_type, notes; append-only, no update/delete route
  exposed."

## Requirements Traceability

```text
SRS:
- FR-TRACE-001 (Module 06) — the append-only event log is this task's
  implementation of the audit-trail portion of the narrowed DAG
  Traceability Engine requirement (Design Document §5.1).

Design Document:
- Section 5.1 (append-only log entry concept)
- Section 7.2 (TraceabilityEvent entity, from EPIC-0-DB-002)
- Section 8 (POST /lots/{id}/events contract, quoted above)

Implementation Specification:
- EPIC 3, Tasks: "Traceability event entity & append-only event
  recording"

Minimum Project Plan:
- Section 7.1 WBS: "Implement lot/traceability lineage linking (farmer ->
  farm -> lot) | FR-TRACE-001 | Fistum Adisu | Traceability API" (this
  task is part of that same WBS line's API deliverable)

Baseline Scope Freeze:
- Section 3.1, "Traceability events"
- Section 4, Critical Workflow — "Create Traceability Record / Event"
  (sixth step)
```

## Prerequisites

- `TRACE-002` merged; at least one real Coffee Lot exists to append events
  against.

## Dependencies

`EPIC-3-TRACE-002` only (a real Lot must exist). This task does **not**
depend on `TRACE-004` (trace retrieval) — the two may proceed in parallel,
per `00-epic-overview.md`'s Parallelization Opportunities.

## Scope

### Allowed Scope

- `POST /api/v1/lots/{id}/events`: accept `event_type` and `notes`,
  validate the target Lot exists, and insert a new `TraceabilityEvent`
  row.
- Enforcing that no update or delete operation on an existing
  `TraceabilityEvent` is exposed via the API, per Design Document §8's
  explicit "append-only, no update/delete route exposed."

### Out of Scope

- Lot creation — `TRACE-002`.
- Lot trace retrieval — `TRACE-004`.
- Restricting which `event_type` values are valid beyond what is needed
  to prevent obviously malformed input — Design Document §8 does not
  define a fixed enumeration of event types (it gives examples: "lot
  created," "quality certificate attached," "waybill issued," but does
  not say these are exhaustive). If a fixed enumeration is later needed,
  that is a separate, traceable decision — this task accepts a
  free-text-but-validated `event_type` (non-empty, reasonable length)
  rather than inventing a closed list not specified anywhere.

## Backend/Frontend/Database Responsibilities

Backend only. No frontend work (that is `TRACE-006`) and no schema change.

## Files/Modules Likely Affected

Indicative paths, matched against the existing backend layout:

- `backend/app/api/v1/lots.py` (extended from `TRACE-002`, or a
  sub-router if the existing pattern separates lot-level and
  event-level routes — match whatever `TRACE-002` already established).
- `backend/app/schemas/traceability_event.py` (or equivalent).
- `backend/app/services/lot_service.py` (extended) or a new
  `traceability_event_service.py` (or equivalent) — match `TRACE-002`'s
  established pattern.
- `backend/tests/` — tests for the endpoint.

## Implementation Requirements

- **Per Design Document §8, this endpoint's Auth requirement is simply
  "JWT"** — any authenticated role, not restricted to Field/Registry
  Agent or Admin. Implement this literally, as documented — see
  `00-epic-overview.md`'s Open Decision #3 for why this is deliberate,
  not an oversight to "fix" by adding a stricter role check.
- The request body accepts `event_type` and `notes`; `event_type` is
  validated as non-empty; `notes` may be optional (Design Document §8
  does not mark it required).
- `recorded_by` is populated from the authenticated user's ID, never from
  client input.
- The target Lot (`{id}` in the path) must exist; a request against a
  non-existent Lot is rejected with a structured `404`.
- No route, in this task or anywhere else in this epic, allows updating
  or deleting an existing `TraceabilityEvent` row.

## Acceptance Criteria

- An authenticated user of **any** of the four roles can append a
  Traceability Event to an existing Lot and receives `200`/`201`.
- An unauthenticated request is rejected with `401`.
- A request against a non-existent Lot ID is rejected with `404`.
- A request with an empty/missing `event_type` is rejected with a
  structured `400`.
- `recorded_by` on the new event correctly reflects the authenticated
  user, not a client-supplied value.
- No API route exists that can update or delete an existing
  `TraceabilityEvent` row (confirmed by inspecting the implemented routes,
  not just by absence of a task requesting one).
- Appending multiple events to the same Lot results in all of them being
  persisted and retrievable in creation order (verified in conjunction
  with `TRACE-004`, or independently via a direct database query if
  `TRACE-004` is not yet merged).

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- Test: any of the four roles can successfully append an event.
- Test: unauthenticated request is rejected.
- Test: non-existent Lot ID is rejected with `404`.
- Test: empty/missing `event_type` is rejected with `400`.
- Test: `recorded_by` reflects the authenticated user.
- Test: multiple events against the same Lot are all persisted correctly.
- Regression: `TRACE-002`'s Lot creation tests still pass.

## Security Considerations

- Authentication enforcement is via `EPIC-1-AUTH-003`'s dependency only;
  no additional role restriction is added beyond what Design Document §8
  specifies (see Implementation Requirements — this is a deliberate,
  documented choice, not a gap).
- `recorded_by` is server-derived, never trusted from client input.

## Expected Outputs / Deliverables

- A working, tested `POST /api/v1/lots/{id}/events` endpoint.
- Confirmation, in the agent report, of the literal "any authenticated
  role" behavior and that it was implemented as documented rather than
  silently tightened.

## Definition of Done

- All items in "Acceptance Criteria" are true and independently
  verifiable.
- All items in "Testing Requirements" pass.
- Reviewed and approved by at least one other team member.
- Merged into `develop`.
- Requirements-traceability entry updated (Kidus).

## Change-Control Conditions

- Do not add a role restriction beyond "any authenticated role" without a
  Project Manager decision — see `00-epic-overview.md`'s Open Decision #3.
  If the reviewing human believes this is clearly unintended, that
  observation goes into the change-control process, not into a unilateral
  code change during this task.

## Git/Branch Expectations

- Branch: `feature/EPIC-3-TRACE-003-traceability-event-api`, from
  `develop`.
- Commit message pattern: `feat(traceability): implement append-only traceability event logging`.
- PR references Task ID `EPIC-3-TRACE-003` and explicitly notes the
  "any authenticated role" Auth behavior as implemented per Design
  Document §8, flagged per Open Decision #3.
- Merge target: `develop`.

## Expected Agent Report

Standard format from `.agents/execution/04-human-review-and-approval.md`,
plus:

1. Explicit confirmation that the endpoint's Auth requirement was
   implemented as "any authenticated role" per Design Document §8's
   literal text, and that this was not tightened.
2. Confirmation that no update/delete route exists for
   `TraceabilityEvent`.
3. Test results.
