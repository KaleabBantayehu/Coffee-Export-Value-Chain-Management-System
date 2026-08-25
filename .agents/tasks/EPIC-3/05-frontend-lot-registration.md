# Task Title

Frontend Lot Registration Form

## Task ID

EPIC-3-TRACE-005

## Epic

EPIC 3 — Traceability Engine

## Owner

Biniyam (Frontend Lead), per Baseline §5 and the Minimum Project Plan's
WBS ("Build traceability lineage view + QR display/download... Biniyam
Abel").

## Status

Not started.

## Priority

High. On the primary acceptance path, but able to proceed in parallel with
`TRACE-003`/`TRACE-004`'s backend work once `TRACE-002` merges (see
`00-epic-overview.md`'s Parallelization Opportunities), mirroring
`EPIC-2-FARM-005`'s pattern.

## Purpose

Implement the React frontend for Coffee Lot registration: select an
existing Farm and create a Lot, calling `POST /api/v1/lots`, reusing the
authentication state and protected-route mechanism `EPIC-1-AUTH-006`/
`EPIC-1-AUTH-007` already established.

## Why This Task Exists

Design Document §9.3 lists "Lot registration form (select farm, create
lot)" as the first Traceability/Operations screen. Baseline §4 lists
"Create Coffee Lot" as its own step in the primary acceptance workflow —
it cannot be demonstrated without a real UI for it.

## Authoritative Sources

- Design Document §9.3 ("Traceability / Operations... Lot registration
  form (select farm, create lot).")
- Design Document §8 (Traceability API contract, from `TRACE-002`)

## Requirements Traceability

```text
SRS:
- Not directly cited beyond FR-TRACE-001, already traced under TRACE-001/
  TRACE-002; the frontend screen itself is a Design Document UI
  deliverable.

Design Document:
- Section 9.3 (Lot registration form, described under Traceability/
  Operations screens)
- Section 8 (the API contract this task's frontend must match exactly)

Implementation Specification:
- EPIC 5, Frontend Integration lists Traceability screens generally under
  Biniyam's ownership ("Coffee Lot Creation, Traceability View" among the
  screens listed); EPIC 3 itself does not enumerate frontend tasks
  separately in the Implementation Specification's own backlog table
  (unlike EPIC 1/EPIC 2, which list "Frontend Tasks" explicitly under
  their own EPIC number). This task package places Lot-registration
  frontend work under EPIC 3 rather than waiting for a separate EPIC 5,
  for continuity with EPIC 2's pattern (which built its own frontend
  tasks inside the epic that owns the underlying data, rather than
  deferring all frontend work to a later integration epic) — see
  "Traceability gap" note below.

Minimum Project Plan:
- Section 7.1 WBS: "Build traceability lineage view + QR display/
  download | FR-TRACE | Biniyam Abel | Frontend module" — this WBS line
  bundles the lineage view with QR display, which spans both this epic
  and EPIC 4; this task implements only the Lot-registration portion, and
  TRACE-006 implements the lineage/event-log viewing portion. QR display
  is explicitly EPIC 4's scope, not this task's or TRACE-006's.

Baseline Scope Freeze:
- Section 2, Technology Baseline — React + JavaScript
- Section 4, Critical Workflow — "Create Coffee Lot"
```

**Traceability gap — requires review:** the Implementation Specification's
own backlog table lists frontend integration under a separate "EPIC 5 —
Frontend Integration" item, owned by Biniyam (Lead) / Abel (Support),
covering screens across multiple modules including "Coffee Lot Creation"
and "Traceability View" — rather than listing frontend tasks under EPIC 3
itself (as it does for EPIC 1 and EPIC 2). This task package follows
EPIC 2's precedent (building the frontend task inside the epic that owns
the underlying feature) rather than deferring Lot-registration frontend
work to a separate EPIC 5 task package, for continuity and because
EPIC 5's own task package does not yet exist. This is recorded as an open
item for the Project Manager: confirm whether Lot-registration/
traceability-view frontend work should remain inside EPIC 3 (as built
here) or be moved into a future EPIC 5 task package once one exists.

## Prerequisites

- `TRACE-002` merged and reachable from the frontend's configured API
  base URL.
- `EPIC-2-FARM-005` merged (a farmer list exists) and `EPIC-2-FARM-003`/
  `FARM-004` merged (a farm list with computed area/EUDR data exists),
  since Lot registration requires selecting an existing Farm.
- `EPIC-1-AUTH-006`/`EPIC-1-AUTH-007` merged; the existing React frontend
  project is used as-is — do not scaffold a new one.
- Confirm the actual, current shape of `TRACE-002`'s API responses by
  inspecting its implementation/tests before building the client, per
  `.agents/execution/01-agent-start-procedure.md` Step 4.

## Dependencies

`EPIC-3-TRACE-002` (Lot creation API contract) and `EPIC-1-AUTH-006`/
`EPIC-1-AUTH-007` (auth state and protected routing).

## Scope

### Allowed Scope

- A Lot registration form: a Farm selector (reusing `EPIC-2`'s existing
  Farm list/lookup capability rather than rebuilding one) and a submit
  action calling `POST /api/v1/lots`.
- Client-side display of the generated GIN and the Lot's initial status
  after successful creation.
- Wiring this screen into the existing role-aware navigation from
  `EPIC-1-AUTH-007`, visible to Field/Registry Agent and Admin (matching
  `TRACE-002`'s backend role restriction).

### Out of Scope

- Traceability event log view/entry — `TRACE-006`.
- QR display or generation — EPIC 4.
- Any change to `EPIC-1`'s or `EPIC-2`'s existing components beyond
  reusing them as-is (e.g., importing an existing Farm-selector component
  rather than modifying it).

## Backend/Frontend/Database Responsibilities

Frontend only.

## Files/Modules Likely Affected

Indicative paths — confirmed against the actual existing frontend project
structure:

- `frontend/src/pages/LotRegistration.jsx` (or equivalent).
- `frontend/src/api/lots.js` (or equivalent API client module, matching
  the pattern established by `EPIC-2-FARM-005`'s `api/farmers.js`).
- `frontend/src/tests/` (or wherever frontend tests already live).

## Implementation Requirements

- The form submits exactly a `farm_id` (selected from an existing Farm
  list) to `POST /api/v1/lots` and handles both success (displaying the
  generated GIN) and failure (e.g., role rejection surfaced as a clear
  error) responses distinctly.
- Route protection: only an authenticated Field/Registry Agent or Admin
  sees a usable registration action, mirroring `TRACE-002`'s backend role
  restriction rather than inventing a different frontend-only rule.

## Acceptance Criteria

- An authenticated Field/Registry Agent can select an existing Farm,
  submit the form, and sees the generated GIN displayed on success.
- An authenticated role without Field/Registry Agent or Admin permissions
  does not see a functional registration action (mirroring the backend's
  `403` behavior at the UI level).
- Navigating to this screen while unauthenticated redirects to login.
- Submitting against a Farm that turns out to be invalid (e.g., removed
  between page load and submission, if testable) surfaces the backend's
  error without the frontend inventing a more specific message.

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- Test: successful Lot creation displays the GIN.
- Test: unauthenticated access redirects to login.
- Test: a non-Field/Registry-Agent, non-Admin authenticated role does not
  see a usable registration action.

## Security Considerations

- No farmer/farm PII beyond what is already shown elsewhere in the
  application is exposed by this screen.
- The JWT used to call this endpoint is sourced from the existing auth
  state (`EPIC-1-AUTH-006`) — this task does not implement its own token
  handling.

## Expected Outputs / Deliverables

- A working, tested Lot registration screen, reachable from role-aware
  navigation.

## Definition of Done

- All items in "Acceptance Criteria" are true and independently
  verifiable.
- All items in "Testing Requirements" pass.
- Reviewed and approved by at least one other team member.
- Merged into `develop`.
- Requirements-traceability entry updated (Kidus).

## Change-Control Conditions

- If `TRACE-002`'s actual implemented response shape differs from this
  task file's description in a way that matters for the UI, escalate per
  `.agents/execution/06-failure-and-escalation.md` rather than silently
  adapting.
- The "EPIC 3 vs. EPIC 5" frontend-placement question (see "Traceability
  gap" above) is not resolved by this task — it proceeds under EPIC 3 for
  continuity, with the open item recorded for the Project Manager.

## Git/Branch Expectations

- Branch: `feature/EPIC-3-TRACE-005-frontend-lot-registration`, from
  `develop`.
- Commit message pattern: `feat(traceability): implement frontend lot registration form`.
- PR references Task ID `EPIC-3-TRACE-005`.
- Merge target: `develop`.

## Expected Agent Report

Standard format from `.agents/execution/04-human-review-and-approval.md`,
plus:

1. Confirmation that `TRACE-002`'s actual API response shape was
   inspected before implementation.
2. Confirmation that the Farm selector reuses `EPIC-2`'s existing
   capability rather than duplicating it.
3. Test results.
