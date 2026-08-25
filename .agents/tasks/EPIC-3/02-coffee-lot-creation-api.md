# Task Title

Coffee Lot Creation API (Farm -> Lot)

## Task ID

EPIC-3-TRACE-002

## Epic

EPIC 3 — Traceability Engine

## Owner

Fistum (Backend Developer — Traceability & QR), with Yedenekachew jointly
responsible specifically for confirming this task correctly consumes the
Farm contract from `EPIC-2-FARM-003`/`FARM-004`, per the Minimum Project
Plan's WBS ("Integrate Farmer/Polygon module with Traceability module...
Fistum Adisu, Yedenekachew Fantahun").

## Status

Not started.

## Priority

Critical — the primary acceptance path's "Create Coffee Lot" step; the
precondition for `TRACE-003` and `TRACE-004`.

## Purpose

Implement `POST /api/v1/lots`: create a Coffee Lot against a mandatory,
existing Farm, generating a GIN via `TRACE-001`'s utility, and
auto-appending an initial Traceability Event recording the lot's creation.

## Why This Task Exists

Baseline §4 lists "Create Coffee Lot" as the fifth step of the primary
acceptance workflow. Design Document §5.1 states "a Coffee Lot references
exactly one originating Farm" — this task is where that reference is
actually created. Design Document §5.1 also gives "lot created" as its own
example of a `TraceabilityEvent`, which this task implements as an
automatic first event rather than requiring a separate manual call.

## Authoritative Sources

- Design Document §5.1 ("a Coffee Lot references exactly one originating
  Farm, and any number of TraceabilityEvent rows (e.g. 'lot created'...)
  are appended against it.")
- Design Document §7.2 (`CoffeeLot` entity: `lot_id`, `gin_code` (unique),
  `farm_id` (FK), `created_by` (FK to User), `status`, `created_at` —
  already created by `EPIC-0-DB-002`)
- Design Document §8 (API Design — Traceability table):
  `POST /api/v1/lots` — "Create a coffee lot against a farm" — Auth:
  "JWT + Field/Registry Agent or Admin" — "Generates a unique GIN;
  validates the farm exists."
- Design Document §13, Sequence 4 (Create Traceable Coffee Lot)

## Requirements Traceability

```text
SRS:
- FR-TRACE-001 (Module 06) — the DAG Traceability Engine requirement.
  Its full scope (multi-source lineage graphs, JSON-LD lineage payloads,
  lot split/merge events) is narrowed by Design Document §5.1 to a
  single-origin, non-splitting/merging lot model. This task implements
  the narrowed version: one Lot, one Farm, no splitting/merging.

Design Document:
- Section 5.1 (Lot -> Farm relationship; "lot created" as an example
  TraceabilityEvent)
- Section 7.2 (CoffeeLot entity, from EPIC-0-DB-002)
- Section 8 (POST /lots contract, quoted above)
- Section 13, Sequence 4

Implementation Specification:
- EPIC 3, Tasks: "Mandatory Farm -> Lot relationship mapping & lot
  creation backend"

Minimum Project Plan:
- Section 7.1 WBS: "Implement lot/traceability lineage linking (farmer ->
  farm -> lot) | FR-TRACE-001 | Fistum Adisu | Traceability API"; "Integrate
  Farmer/Polygon module with Traceability module | FR-FARM, FR-TRACE |
  Fistum Adisu, Yedenekachew Fantahun"

Baseline Scope Freeze:
- Section 3.1, "Coffee lot registration"
- Section 4, Critical Workflow — "Create Coffee Lot" (fifth step)
```

## Prerequisites

- `TRACE-001` merged, with its GIN format either finalized or still
  pending (proceed with the placeholder if still pending, per
  `TRACE-001`'s own pattern).
- **Confirm, not assume, that `EPIC-2-FARM-003`/`FARM-004` are actually
  implemented and that at least one real Farm exists with a persisted
  polygon, computed area, and EUDR flag** — per
  `.agents/execution/01-agent-start-procedure.md` Step 4/5 and this
  epic's overview note that task-file existence does not prove
  implementation. If no real Farm can be created/retrieved, stop and
  report per `.agents/execution/06-failure-and-escalation.md` rather than
  building against a guessed Farm contract.
- **Confirm, not assume, that `EPIC-1-AUTH-003`/`AUTH-004` are actually
  implemented and enforceable** for the same reason.

## Dependencies

`EPIC-3-TRACE-001` (GIN utility), `EPIC-2-FARM-003`/`FARM-004` (a real
Farm to attach the Lot to), and `EPIC-1-AUTH-003`/`AUTH-004`
(authentication and RBAC, reused as-is).

## Scope

### Allowed Scope

- `POST /api/v1/lots`: accept a `farm_id`, validate the Farm exists,
  generate a GIN via `TRACE-001`'s utility, persist the new `CoffeeLot`
  row, and auto-append one `TraceabilityEvent` (e.g., `event_type =
  "lot_created"`) against it in the same transaction.
- Validation that the referenced `farm_id` exists, rejecting a request
  that cites a non-existent Farm with a structured error.

### Out of Scope

- Traceability event logging beyond the automatic "lot created" event —
  manual event appending is `TRACE-003`.
- Lot trace retrieval — `TRACE-004`.
- Any Lot update, status-change, or deletion endpoint — Design Document
  §8 defines none.
- Lot splitting or merging across multiple Farms (SRS UC-22/UC-23) —
  explicitly out of V1.0 scope.
- Cherry collection or batch intake — not part of this epic's Farm-to-Lot
  model.

## Backend/Frontend/Database Responsibilities

Backend only — API endpoint and service logic on top of the existing
`CoffeeLot`/`TraceabilityEvent` schema. No frontend work (that is
`TRACE-005`) and no schema change (already exists per `EPIC-0-DB-002`).

## Files/Modules Likely Affected

Indicative paths, matched against the existing backend layout:

- `backend/app/api/v1/lots.py` (or equivalent, matching the existing
  router-per-domain pattern).
- `backend/app/schemas/lot.py` (or equivalent).
- `backend/app/services/lot_service.py` (or equivalent) — Farm-existence
  validation, GIN generation call, persistence, auto-event creation.
- `backend/tests/` — tests for the endpoint.

## Implementation Requirements

- `POST /api/v1/lots` requires `Field/Registry Agent or Admin`, enforced
  via `EPIC-1-AUTH-004`'s mechanism — not a bespoke check.
- The request body accepts a `farm_id`; the endpoint rejects a
  non-existent `farm_id` with a structured `400`/`404`, not a raw
  foreign-key violation.
- On success, the endpoint: (1) calls `TRACE-001`'s GIN generation
  utility, (2) persists the new `CoffeeLot` row with `farm_id`,
  `created_by` (the authenticated user), and an initial `status`, (3)
  inserts one `TraceabilityEvent` row (`event_type` indicating lot
  creation) referencing the new lot, and (4) returns the lot including its
  generated GIN — all within a single database transaction, so a failure
  partway through does not leave an orphaned Lot without its initial
  event, or vice versa.
- `created_by` is populated from the authenticated user's ID (from
  `EPIC-1-AUTH-003`'s resolved user), not from client input.

## Acceptance Criteria

- An authenticated Field/Registry Agent can create a Lot against an
  existing Farm via `POST /api/v1/lots` and receives `200`/`201` with the
  generated GIN in the response.
- The same request from a role other than Field/Registry Agent or Admin
  is rejected with `403`; unauthenticated is rejected with `401`.
- A request citing a `farm_id` that does not exist is rejected with a
  structured error, not a raw database exception.
- After successful creation, querying `TraceabilityEvent` for the new
  lot's ID returns exactly one row, with an `event_type` indicating lot
  creation.
- `created_by` on the new Lot correctly reflects the authenticated user
  who made the request, not a client-supplied value.
- If GIN generation fails after multiple collision retries (simulated in
  a test), the entire operation fails cleanly with no partial `CoffeeLot`
  or `TraceabilityEvent` row left behind (transactional integrity).

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- Test: successful Lot creation returns the expected shape including a
  generated GIN.
- Test: role-based rejection (`403`) and unauthenticated rejection
  (`401`).
- Test: non-existent `farm_id` is rejected cleanly.
- Test: the auto-created initial `TraceabilityEvent` exists and is
  correctly linked after successful creation.
- Test: `created_by` reflects the authenticated user.
- Test: a simulated GIN-generation failure leaves no partial state
  (transaction rollback).
- Regression: `EPIC-2`'s Farm tests and `EPIC-1`'s auth/RBAC tests still
  pass unchanged after this task's routes are added — confirmed by
  actually re-running them, not assumed.

## Security Considerations

- RBAC enforcement is via `EPIC-1-AUTH-004`'s mechanism only.
- `created_by` is server-derived, never trusted from client input, to
  prevent a caller from attributing a Lot's creation to a different user.

## Expected Outputs / Deliverables

- A working, tested `POST /api/v1/lots` endpoint.
- A real, persisted Coffee Lot with its auto-created initial
  Traceability Event, usable by `TRACE-003`, `TRACE-004`, and later EPIC 4.

## Definition of Done

- All items in "Acceptance Criteria" are true and independently
  verifiable.
- All items in "Testing Requirements" pass.
- Reviewed and approved by at least one other team member.
- Merged into `develop`.
- Requirements-traceability entry updated (Kidus) for FR-TRACE-001's
  narrowed, single-origin implementation.

## Change-Control Conditions

- If, during implementation, `EPIC-2-FARM-003`/`FARM-004`'s actual API
  response shape differs materially from what Design Document §8
  describes, escalate per
  `.agents/execution/06-failure-and-escalation.md` rather than silently
  adapting — the discrepancy might need correcting in EPIC 2, not just
  worked around here.
- If `EPIC-1`/`EPIC-2` are found not to be actually implemented when this
  task begins, stop and report per the same procedure rather than
  building this task against assumptions.

## Git/Branch Expectations

- Branch: `feature/EPIC-3-TRACE-002-lot-creation-api`, from `develop`.
- Commit message pattern: `feat(traceability): implement coffee lot creation API`.
- PR references Task ID `EPIC-3-TRACE-002` and confirms the auto-created
  initial Traceability Event is present and tested.
- Merge target: `develop`.

## Expected Agent Report

Standard format from `.agents/execution/04-human-review-and-approval.md`,
plus:

1. Confirmation that `EPIC-1`/`EPIC-2`'s actual implementation status was
   verified (not assumed) before proceeding, with what was found.
2. Confirmation of the transaction boundary covering Lot creation, GIN
   generation, and the auto-created event.
3. Whether `TRACE-001`'s GIN format was finalized or still pending.
4. Test results.
