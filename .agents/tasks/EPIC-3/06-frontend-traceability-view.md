# Task Title

Frontend Traceability Event Log View & Entry

## Task ID

EPIC-3-TRACE-006

## Epic

EPIC 3 — Traceability Engine

## Owner

Biniyam (Frontend Lead)

## Status

Not started.

## Priority

Critical — this screen is what actually demonstrates the Implementation
Specification's EPIC 3 Definition of Done to a human, visually.

## Purpose

Implement the React frontend for viewing a Coffee Lot's traceability
chain (calling `GET /api/v1/lots/{id}/trace`) and appending new
Traceability Events to it (calling `POST /api/v1/lots/{id}/events`).

## Why This Task Exists

Design Document §9.3 lists "Traceability event log view/entry for a lot"
as a Traceability/Operations screen. This is the UI expression of
`TRACE-004`'s retrieval endpoint and `TRACE-003`'s event-logging
endpoint — without it, both endpoints exist only as API contracts, not as
something a human evaluator (or the client) can see work.

## Authoritative Sources

- Design Document §9.3 ("Traceability event log view/entry for a lot.")
- Design Document §5.3 (public vs. protected data — this screen, being
  authenticated, may display full detail including farmer contact fields,
  per `TRACE-004`'s own documented behavior)
- Design Document §8 (Traceability API contract, from `TRACE-003`/
  `TRACE-004`)

## Requirements Traceability

```text
SRS:
- Not directly cited beyond FR-TRACE-001, already traced under TRACE-003/
  TRACE-004.

Design Document:
- Section 9.3 (this screen's description)
- Section 5.3 (protected-view data-exposure rules this screen follows)
- Section 8 (the API contracts this task's frontend must match exactly)

Implementation Specification:
- EPIC 3's Definition of Done ("Given a Coffee Lot ID, the system
  accurately displays its origin trace back to the registered farm and
  farmer") — this screen is the literal, visible fulfillment of that
  Definition of Done, not just TRACE-004's API response.

Minimum Project Plan:
- Section 7.1 WBS: "Build traceability lineage view + QR display/
  download | FR-TRACE | Biniyam Abel | Frontend module" (the lineage-view
  portion; QR display is EPIC 4, not this task).

Baseline Scope Freeze:
- Section 4, Critical Workflow — "Create Traceability Record / Event"
```

See `TRACE-005`'s "Traceability gap" note (EPIC 3 vs. EPIC 5 frontend
placement) — the same open item applies here and is not re-litigated in
this file.

## Prerequisites

- `TRACE-003` and `TRACE-004` merged; both API contracts confirmed by
  inspection, not assumption, per
  `.agents/execution/01-agent-start-procedure.md` Step 4.
- `TRACE-005` merged, so a Lot can already be created and its ID is
  available to navigate to this view.

## Dependencies

`EPIC-3-TRACE-003` (event creation contract) and `EPIC-3-TRACE-004` (trace
retrieval contract) — both required, since this screen both displays
retrieved data and creates new events.

## Scope

### Allowed Scope

- A Lot detail/trace view: given a Lot ID (e.g., navigated to after
  `TRACE-005`'s registration succeeds, or reached via a Lot lookup),
  display the Lot's GIN/status, the originating Farm's data, the Farmer's
  profile, and the full chronological Traceability Event list, calling
  `GET /api/v1/lots/{id}/trace`.
- An event-entry form on the same screen (or a clearly linked sub-view):
  `event_type` and `notes` fields, submitting to
  `POST /api/v1/lots/{id}/events`, and refreshing the displayed event
  list on success.

### Out of Scope

- Lot registration itself — `TRACE-005`.
- QR display, generation, or the public verification page — EPIC 4.
- Any update/delete UI for an existing event — Design Document §8 exposes
  no such endpoint; none is built here either.

## Backend/Frontend/Database Responsibilities

Frontend only.

## Files/Modules Likely Affected

Indicative paths — confirmed against the actual existing frontend project
structure:

- `frontend/src/pages/LotTraceView.jsx` (or equivalent).
- `frontend/src/components/TraceabilityEventForm.jsx` (or equivalent).
- `frontend/src/api/lots.js` (extended from `TRACE-005`, adding trace-
  retrieval and event-creation calls).
- `frontend/src/tests/` (or wherever frontend tests already live).

## Implementation Requirements

- The trace view calls `GET /api/v1/lots/{id}/trace` and renders the
  Lot, Farm, Farmer, and Event data returned — matching the actual,
  inspected response shape, not a guessed one.
- Since `TRACE-004`'s endpoint requires only authentication (any role),
  this screen is reachable by any authenticated role for viewing — but
  the event-entry form's submission still succeeds for any authenticated
  role too, per `TRACE-003`'s documented "any authenticated role" Auth
  requirement (see `00-epic-overview.md` Open Decision #3) — do not add a
  frontend-only role restriction on the event-entry form that the backend
  does not itself enforce, since that would misrepresent the actual
  security boundary to the user.
- After successfully appending an event, the displayed event list
  refreshes to include it (either by re-fetching the trace or by
  optimistically appending it and reconciling on the next fetch — record
  which approach was used).

## Acceptance Criteria

- Navigating to the trace view for an existing Lot displays its GIN,
  Farm, Farmer (including contact fields, per Design Document §5.3's
  protected-view rule), and full Event list correctly.
- Submitting the event-entry form successfully appends a new event and
  the updated event list is visible without a full page reload being
  required to see it.
- Navigating to this screen while unauthenticated redirects to login.
- The event-entry form is usable by any authenticated role (matching
  `TRACE-003`'s backend behavior), not artificially restricted to
  Field/Registry Agent or Admin.
- Navigating to a non-existent Lot ID displays the backend's `404`
  response as a clear error state, not a broken/blank screen.

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- Test: trace view correctly renders Lot, Farm, Farmer, and Event data
  for an existing Lot.
- Test: appending an event via the form updates the displayed list.
- Test: unauthenticated access redirects to login.
- Test: a non-existent Lot ID is handled with a clear error state, not a
  crash.
- Test: the event-entry form is usable by a role other than Field/
  Registry Agent or Admin (confirming the frontend does not
  over-restrict relative to the backend).

## Security Considerations

- Farmer PII (national ID, phone number) is displayed on this screen
  because `TRACE-004`'s backend response includes it for authenticated
  users, per Design Document §5.3 — this is intentional, not a leak; do
  not redact it here without a change-control decision, matching
  `TRACE-004`'s own note.
- The JWT used to call these endpoints is sourced from the existing auth
  state (`EPIC-1-AUTH-006`).

## Expected Outputs / Deliverables

- A working, tested trace view and event-entry form that together make
  the Implementation Specification's EPIC 3 Definition of Done visibly
  demonstrable to a human.

## Definition of Done

- All items in "Acceptance Criteria" are true and independently
  verifiable.
- All items in "Testing Requirements" pass.
- Reviewed and approved by at least one other team member.
- Merged into `develop`.
- Requirements-traceability entry updated (Kidus).

## Change-Control Conditions

- If `TRACE-003`/`TRACE-004`'s actual response shapes differ from this
  task file's description in a way that affects the UI, escalate per
  `.agents/execution/06-failure-and-escalation.md` rather than silently
  adapting.
- Do not add a frontend-only role restriction on the event-entry form
  that the backend does not enforce (see Open Decision #3) — if the team
  later tightens the backend, this screen should follow that change, not
  anticipate it unilaterally.

## Git/Branch Expectations

- Branch: `feature/EPIC-3-TRACE-006-frontend-traceability-view`, from
  `develop`.
- Commit message pattern: `feat(traceability): implement frontend traceability event log view and entry`.
- PR references Task ID `EPIC-3-TRACE-006`.
- Merge target: `develop`.

## Expected Agent Report

Standard format from `.agents/execution/04-human-review-and-approval.md`,
plus:

1. Confirmation that `TRACE-003`/`TRACE-004`'s actual API response shapes
   were inspected before implementation.
2. Whether the event list refresh uses re-fetch or optimistic update, and
   why.
3. Confirmation that the event-entry form was not restricted beyond what
   the backend enforces.
4. Test results.
