# Task Title

EPIC 3 End-to-End Verification & EPIC 4 Handoff Readiness

## Task ID

EPIC-3-TRACE-007

## Epic

EPIC 3 — Traceability Engine

## Owner

Ephratha (integration/API/RBAC testing) and Kidus (functional/system
walkthrough, Test Report draft), per the Minimum Project Plan's WBS
("Integration tests for module APIs (Postman)... Ephratha Samuel";
"Functional/system walkthrough of full traceability use case... Kidus
Ergetachew | Test Report (draft)") — see `00-epic-overview.md`'s "Cross-
EPIC Issues" note on why this ownership split is more precise than the
pattern `EPIC-1-AUTH-008`/`EPIC-2-FARM-007` used.

## Status

Not started (final task of EPIC 3).

## Priority

Critical — this is the gate that confirms EPIC 3's Definition of Done
before EPIC 4 (Dynamic QR) may begin, per the fixed dependency chain
(`.agents/rules/01-scope-boundaries.md`).

## Purpose

Independently verify, end to end, that the whole of EPIC 3 (`TRACE-001`
through `TRACE-006`) satisfies the Implementation Specification's EPIC 3
Definition of Done and the Epic Completion Gate stated in
`00-epic-overview.md`; confirm the GIN-format gap and Open Decisions #1
and #3 are recorded and, where required, escalated; and confirm EPIC 4 has
what it needs to begin.

## Why This Task Exists

Each individual `TRACE-0xx` task tests its own slice in isolation. Nothing
so far proves the whole chain — authenticated login through a real,
persisted Farmer -> Farm -> Coffee Lot -> Traceability Event chain,
created through the actual UI — works together as one coherent flow. This
mirrors exactly why `EPIC-1-AUTH-008` and `EPIC-2-FARM-007` exist for
their respective epics.

## Authoritative Sources

- Implementation Specification, EPIC 3 Definition of Done: "Given a
  Coffee Lot ID, the system accurately displays its origin trace back to
  the registered farm and farmer."
- `00-epic-overview.md` (EPIC-3 Completion Gate section, this directory)
- `.agents/execution/07-task-completion-checklist.md` (EPIC-level
  sign-off)
- `.agents/execution/06-failure-and-escalation.md` (escalation status
  check)
- Minimum Project Plan §7.1 WBS ("Functional/system walkthrough of full
  traceability use case | AD Sec. 12")

## Requirements Traceability

```text
SRS:
- Consolidates FR-TRACE-001 (as narrowed across TRACE-001 through
  TRACE-006) — this task verifies the narrowed, V1.0 version actually
  implemented, not the SRS's enterprise DAG version.

Design Document:
- Section 20 (Design Validation, by analogy, as used in
  EPIC-2-FARM-007's equivalent section) — the same implementation-time
  validation standard applied here for EPIC 3 specifically.

Implementation Specification:
- EPIC 3 Definition of Done (quoted above).

Minimum Project Plan:
- Milestone M4 (Working Increment Delivered, end of Week 3) explicitly
  requires Traceability integrated and demonstrable as part of the core
  chain; this task is the check that EPIC 3's contribution to M4 is real.
- Section 7.1 WBS's testing rows (Ephratha: integration tests; Kidus:
  functional walkthrough).

Baseline Scope Freeze:
- Section 4, Critical Workflow — "Create Coffee Lot," "Create
  Traceability Record / Event" steps are now fully verified as a
  precondition for "Generate QR" (EPIC 4).
```

## Prerequisites

- All six preceding EPIC-3 tasks report their Definition of Done
  satisfied and are merged into `develop`.
- A locally runnable instance of both backend and frontend is available
  for manual verification.

## Dependencies

`EPIC-3-TRACE-001` through `EPIC-3-TRACE-006`, all merged to `develop`.

## Scope

### Allowed Scope

- Building and running a Postman collection covering the full set of
  EPIC-3 Completion Gate criteria (Ephratha).
- A full manual walkthrough of the actual UI: authenticated login ->
  select an existing Farm -> create a Coffee Lot -> observe the
  auto-created initial event -> append at least one additional event ->
  view the full trace and confirm it correctly resolves back to the
  originating Farm and Farmer (Kidus, drafting the Test Report per the
  Minimum Project Plan's WBS assignment).
- Confirming the status of every "Open Decision" listed in
  `00-epic-overview.md` (epic-boundary framing, GIN format, "any
  authenticated role" event-logging behavior) — recording whether each is
  acknowledged, escalated, resolved, or formally accepted as non-blocking.
- Filing defects against any `TRACE-0xx` task found not to satisfy its own
  acceptance criteria — not fixing them directly under this task's scope
  unless the fix is trivial and clearly within one already-completed
  task's boundaries.
- Updating the requirements-traceability matrix and test documentation to
  reflect EPIC 3's actual, verified completion state.

### Out of Scope

- Implementing new functionality — this is a verification and
  documentation task. Any gap found is filed as a defect against the
  relevant `TRACE-0xx` task, not silently patched here.
- Beginning any EPIC 4 (Dynamic QR) work, even if this verification
  passes cleanly — EPIC 4 begins as its own, separately created task set.
- Load, performance, or penetration testing.

## Backend/Frontend/Database Responsibilities

Verification only — no implementation in any layer. Database queries are
used for verification evidence only (e.g., confirming a real Lot/Event
chain exists), not for inserting data directly.

## Files/Modules Likely Affected

- A Postman collection file (location consistent with wherever
  `TRACE-002`–`TRACE-004` already placed their individual requests).
- Project documentation / requirements-traceability matrix (Kidus).
- No application source code should need to change as a result of this
  task; if it does, that change belongs to whichever `TRACE-0xx` task
  owns the affected area, reopened as a defect fix.

## Implementation Requirements

This task "implements" a verification procedure, not application code:

1. Confirm GIN generation succeeds and is unique for repeated Lot
   creations (`TRACE-001`), and record whether the GIN-format traceability
   gap has been resolved by the Project Manager.
2. Confirm Coffee Lot creation correctly requires an existing Farm, is
   RBAC-restricted to Field/Registry Agent or Admin, and auto-creates its
   initial Traceability Event within the same transaction (`TRACE-002`).
3. Confirm Traceability Event logging is genuinely append-only (no
   update/delete route reachable) and correctly usable by any
   authenticated role, per Open Decision #3 (`TRACE-003`).
4. Confirm `GET /lots/{id}/trace` correctly and completely resolves a
   Lot's chain back to its Farm and Farmer, matching the Implementation
   Specification's EPIC 3 Definition of Done exactly (`TRACE-004`).
5. Confirm the frontend Lot registration flow works end to end against
   the real backend (`TRACE-005`).
6. Confirm the frontend trace view and event-entry form work end to end
   against the real backend (`TRACE-006`).
7. Perform one complete, unbroken manual walkthrough: log in -> select an
   existing Farm -> create a Lot -> observe the auto-created event ->
   append a manual event -> view the trace -> independently query the
   database to confirm the Farmer -> Farm -> CoffeeLot -> TraceabilityEvent
   chain exists correctly linked.

## Acceptance Criteria

- Every item in `00-epic-overview.md`'s EPIC-3 Completion Gate is
  independently confirmed true, with evidence (Postman run results,
  database query output, and the manual walkthrough's outcome).
- The GIN-format traceability gap's status is explicitly recorded
  (resolved / open / formally accepted as non-blocking).
- Open Decision #1 (epic-boundary framing) is explicitly acknowledged as
  reviewed by the Project Manager, even if not formally reconciled in
  documentation.
- Open Decision #3 ("any authenticated role" event logging) is confirmed
  as implemented literally and either explicitly accepted or flagged for
  a future change-control decision — not silently left ambiguous.
- Any criterion found not to be satisfied is filed as a defect against
  the owning `TRACE-0xx` task, with enough detail for that task's owner
  to act on it without re-discovering the problem.
- At least one complete Farmer -> Farm -> Coffee Lot -> Traceability Event
  chain exists in the local/demo database, created through the actual UI,
  confirmed by direct database query.
- The requirements-traceability matrix accurately reflects, for
  FR-TRACE-001, its actual V1.0 implementation status (narrowed and
  implemented, with the narrowing reason).

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- The full Postman collection for EPIC 3 runs green end to end against a
  freshly seeded local environment (including a valid EPIC-1 login and an
  existing EPIC-2 Farm to obtain first).
- The existing automated test suites from `TRACE-001`–`TRACE-006` are
  re-run together and confirmed to still pass — the regression check,
  mirroring `EPIC-1-AUTH-008`/`EPIC-2-FARM-007`'s approach.
- The one full manual walkthrough described in "Implementation
  Requirements," item 7, is performed and recorded, not skipped in favor
  of automated tests alone.
- Regression: `EPIC-1`'s and `EPIC-2`'s full test suites still pass after
  all of EPIC 3 is merged.

## Security Considerations

- Verification specifically re-confirms no farmer PII, credential, or
  signing secret appears in logs, Postman collection files, or
  documentation produced by this task, even though `TRACE-004`'s response
  legitimately includes farmer PII within the application itself.

## Expected Outputs / Deliverables

- A completed, evidence-backed EPIC-3 Completion Gate checklist.
- A Postman collection covering all EPIC-3 endpoints.
- A drafted Test Report section covering the traceability use case
  (Kidus).
- An explicit go/no-go statement on whether EPIC 4 may begin.

## Definition of Done

- All items in "Acceptance Criteria" are true and independently
  verifiable.
- All items in "Testing Requirements" pass.
- Reviewed and approved by at least one other team member (in addition to
  the joint Ephratha/Kidus ownership).
- Merged into `develop`.
- Requirements-traceability matrix and Test Report updated.

## Change-Control Conditions

- Do not mark EPIC 3 complete, and do not signal that EPIC 4 (Dynamic QR)
  may begin, if any Completion Gate item fails or if the GIN-format gap
  remains genuinely unresolved and unaddressed — report the gap and stop,
  per `.agents/execution/06-failure-and-escalation.md`.
- Do not modify the Baseline, Design Document, SRS, Implementation
  Specification, Minimum Project Plan, or any `.agents/rules/`,
  `.agents/execution/`, or earlier-EPIC task file, even if verification
  surfaces an apparent inconsistency in them — record the inconsistency
  and escalate, consistent with this epic's own "Cross-EPIC Issues"
  section.

## Git/Branch Expectations

- Branch: `feature/EPIC-3-TRACE-007-verification`, from `develop` (for
  the Postman collection and documentation changes only).
- Commit message pattern: `test(traceability): verify EPIC 3 acceptance criteria end-to-end`;
  `docs(traceability): update requirements traceability for EPIC 3`.
- PR references Task ID `EPIC-3-TRACE-007`, lists every EPIC-3 Completion
  Gate item, and states pass/fail/open-status for each with evidence.
- Merge target: `develop`.

## Expected Agent Report

1. Pass/fail/open status for every EPIC-3 Completion Gate item in
   `00-epic-overview.md`, with evidence.
2. A list of any defects filed, against which `TRACE-0xx` task, with
   reproduction detail.
3. The recorded status of all three Open Decisions from
   `00-epic-overview.md` (epic-boundary framing, GIN format, "any
   authenticated role" event logging).
4. Confirmation of the database-level check that a genuine
   Farmer -> Farm -> CoffeeLot -> TraceabilityEvent chain exists, created
   through the actual UI.
5. Explicit statement of whether EPIC 3 is considered complete and EPIC 4
   may begin, or whether it is blocked pending defect/decision resolution.
6. Confirmation that no farmer PII, credential, or signing secret appears
   in any artifact produced by this task itself (Postman collection,
   documentation).
