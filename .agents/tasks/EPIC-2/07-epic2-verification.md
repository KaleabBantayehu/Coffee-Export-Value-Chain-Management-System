# Task Title

EPIC 2 End-to-End Verification & EPIC 3 Handoff Readiness

## Task ID

EPIC-2-FARM-007

## Epic

EPIC 2 — Farmer & Polygon Registry

## Owner

Ephratha (Backend & QA), with documentation updates by Kidus, per Baseline
§5, mirroring `EPIC-1-AUTH-008`'s ownership pattern.

## Status

Not started (final task of EPIC 2).

## Priority

Critical — this is the gate that confirms EPIC 2's Definition of Done
before EPIC 3 (Traceability & Coffee Lot) may begin, per the fixed
dependency chain (`.agents/rules/01-scope-boundaries.md`).

## Objective

Independently verify, end to end, that the whole of EPIC 2 (`FARM-001`
through `FARM-006`) satisfies the Implementation Specification's EPIC 2
Definition of Done and the Epic Acceptance/Completion Gate stated in
`00-epic-overview.md`, confirm the FIN-format and other flagged
ambiguities are either resolved or explicitly, formally accepted as
non-blocking, and confirm EPIC 3 has what it needs to begin.

## Why This Task Exists

Each individual `FARM-0xx` task tests its own slice in isolation. Nothing
so far proves the whole chain — authenticated login through a real,
persisted Farmer -> Farm -> Polygon -> Area -> EUDR-status record, created
through the actual UI — works together as one coherent flow. This mirrors
exactly why `EPIC-1-AUTH-008` exists for EPIC 1, per
`.agents/execution/00-execution-overview.md`'s EPIC completion gate
definition.

## Authoritative Sources

- Implementation Specification, EPIC 2 Definition of Done: "Complete
  workflow: Create Farmer -> Create Farm -> Draw Polygon -> Save Polygon
  -> Calculate Area -> Display EUDR Status."
- `00-epic-overview.md` (EPIC-2 Completion Gate section, this directory)
- `.agents/execution/07-task-completion-checklist.md` (EPIC-level
  sign-off)
- `.agents/execution/06-failure-and-escalation.md` (escalation status
  check)

## Requirements Traceability

```text
SRS:
- Consolidates FR-FARM-001 and FR-FARM-002 (as narrowed across
  FARM-001 through FARM-006) — this task verifies the narrowed, V1.0
  versions actually implemented, not the SRS's enterprise versions.

Design Document:
- Section 20 (Design Validation, by analogy — the same "every core module
  has a full design: entities, APIs, UI flow" validation standard applied
  to actual implementation here) — Section 20 itself covers the Design
  Document's own self-check at design time; this task performs the
  equivalent check at implementation time for EPIC 2 specifically.

Implementation Specification:
- EPIC 2 Definition of Done (quoted above).

Minimum Project Plan:
- Milestone M4 (Working Increment Delivered, end of Week 3) explicitly
  requires the three core modules — including Farmer & Polygon Registry —
  integrated and demonstrable; this task is the check that EPIC 2's
  contribution to M4 is real, not just individually-tested pieces.
- Section 7.3 Task Dependencies — confirms Farmer & Polygon Registry
  produces the records used by Traceability; this task confirms that
  handoff is actually usable, not just theoretically defined.

Baseline Scope Freeze:
- Section 4, Critical Workflow — "Register Farmer," "Register Farm,"
  "Draw / Save Farm Polygon" steps are now fully verified as a
  precondition for every later step.
```

## Dependencies

`EPIC-2-FARM-001` through `EPIC-2-FARM-006`, all merged to `develop`.

## Preconditions

- All six preceding EPIC-2 tasks report their Definition of Done satisfied
  and are merged into `develop`.
- A locally runnable instance of both backend and frontend is available for
  manual verification.

## Allowed Scope

- Building and running a Postman collection covering the full set of
  EPIC-2 Acceptance/Completion criteria, per
  `.agents/execution/03-verification-and-testing.md`.
- A full manual walkthrough of the actual UI: authenticated login (reusing
  EPIC 1) -> register a farmer -> register a farm with a drawn polygon ->
  observe the computed area and EUDR demonstration status.
- Confirming the status of every "Known Ambiguity" listed in
  `00-epic-overview.md` (FIN format, RBAC role list, mapping library, area-
  calculation method) — recording whether each is resolved, still open, or
  formally accepted as a non-blocking documented gap.
- Filing defects (per Baseline §5, Ephratha "owns defect tracking") against
  any `FARM-0xx` task found not to satisfy its own acceptance criteria —
  not fixing them directly under this task's scope unless the fix is
  trivial and clearly within one already-completed task's boundaries.
- Updating the requirements-traceability matrix and test documentation to
  reflect EPIC 2's actual, verified completion state (Kidus).

## Out of Scope

- Implementing new functionality — this is a verification and
  documentation task. Any gap found is filed as a defect against the
  relevant `FARM-0xx` task, not silently patched here.
- Beginning any EPIC 3 (Traceability & Coffee Lot) work, even if this
  verification passes cleanly — EPIC 3 begins as its own, separately
  created task set, per this request's own instruction to stop after
  EPIC 2.
- Load, performance, or penetration testing.

## Files/Directories Potentially Affected

- A Postman collection file (location consistent with wherever
  `FARM-002`–`FARM-004` already placed their individual requests).
- Project documentation / requirements-traceability matrix (Kidus).
- No application source code should need to change as a result of this
  task; if it does, that change belongs to whichever `FARM-0xx` task owns
  the affected area, reopened as a defect fix.

## Implementation Requirements

This task "implements" a verification procedure, not application code:

1. Confirm FIN generation succeeds and is unique for repeated registrations
   (`FARM-001`), and record whether the FIN-format escalation has been
   resolved by the Project Manager.
2. Confirm Farmer registration, retrieval, update, and search all behave
   correctly, including RBAC enforcement (`FARM-002`).
3. Confirm Farm creation correctly requires an existing Farmer, persists a
   genuine PostGIS polygon (verified by direct database query, not just
   API response inspection), and supports both the multi-vertex and
   single-point-radius input modes (`FARM-003`).
4. Confirm area calculation and EUDR demonstration flagging are correct,
   deterministic, idempotent via `/validate`, and visibly labeled as a
   demonstration check (`FARM-004`).
5. Confirm the frontend farmer registration/list/detail flow works
   end to end against the real backend (`FARM-005`).
6. Confirm the frontend farm registration, Leaflet polygon capture, and
   EUDR/area result panel work end to end against the real backend,
   including the demonstration-check labeling being visibly rendered
   (`FARM-006`).
7. Perform one complete, unbroken manual walkthrough: log in -> register a
   new farmer -> register a farm for that farmer with a drawn polygon ->
   confirm the displayed area and EUDR status -> independently query the
   database to confirm the Farmer and Farm rows exist correctly linked,
   with genuine PostGIS geometry.

## Acceptance Criteria

- Every item in `00-epic-overview.md`'s EPIC-2 Completion Gate is
  independently confirmed true, with evidence (Postman run results,
  database query output, and the manual walkthrough's outcome).
- The FIN-format ambiguity's status is explicitly recorded (resolved / open
  / formally accepted as non-blocking) — EPIC 2 is not signed off as
  complete if this is still silently unresolved and unrecorded.
- The RBAC role-list discrepancy's status is explicitly recorded, using the
  same handling as `EPIC-1-AUTH-008` established.
- The mapping-library discrepancy's status is explicitly recorded (the
  practical choice — Leaflet/React-Leaflet — is already settled and
  verified as actually used; the underlying document conflict's formal
  resolution status is recorded separately).
- Any criterion found not to be satisfied is filed as a defect against the
  owning `FARM-0xx` task, with enough detail for that task's owner to act
  on it without re-discovering the problem.
- At least one complete Farmer -> Farm -> Polygon record exists in the
  local/demo database, created through the actual UI, confirmed by direct
  database query to have genuine PostGIS geometry (not a placeholder or a
  record inserted directly by a script).
- The requirements-traceability matrix accurately reflects, for FR-FARM-001
  and FR-FARM-002, their actual V1.0 implementation status (implemented /
  narrowed-and-implemented / not implemented, with the narrowing reason).

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- The full Postman collection for EPIC 2 runs green end to end against a
  freshly seeded local environment (including a valid EPIC-1 login to
  obtain a token first).
- The existing automated test suites from `FARM-001`–`FARM-006` are
  re-run together (not just individually) and confirmed to still pass —
  the regression check, mirroring Implementation Playbook §9 step 7 and
  `EPIC-1-AUTH-008`'s approach.
- The one full manual walkthrough described in "Implementation
  Requirements," item 7, is performed and recorded, not skipped in favor
  of automated tests alone.
- Regression: `EPIC-1`'s full auth/RBAC test suite still passes after all
  of EPIC 2 is merged.

## Security Requirements

- Verification specifically re-confirms no farmer PII (national ID, phone
  number) or credential appears in logs, Postman collection files, or
  documentation produced by this task.

## Error Handling Requirements

Not applicable in the implementation sense; this task confirms error
handling built by prior tasks behaves as specified, and files defects
where it does not.

## Documentation Requirements

- Kidus updates: the requirements-traceability matrix; the test
  documentation/evidence record; and the project's progress-report
  content for the relevant reporting period, per Appendix 3's biweekly
  progress report format, noting EPIC 2 completion status honestly,
  including any open defects or unresolved ambiguities.

## Commit Guidance

- Branch: `feature/EPIC-2-FARM-007-verification`, from `develop` (for the
  Postman collection and documentation changes only).
- Commit message pattern: `test(farm): verify EPIC 2 acceptance criteria end-to-end`;
  `docs(farm): update requirements traceability for EPIC 2`.
- PR references Task ID `EPIC-2-FARM-007`, lists every EPIC-2 Completion
  Gate item, and states pass/fail/open-status for each with evidence.
- Merge target: `develop`.

## Verification Requirements

This entire task is a verification task; its own self-review consists of
re-checking every acceptance criterion above against actual evidence
before submitting the report, per
`.agents/execution/03-verification-and-testing.md`.

## Escalation / Change-Control Conditions

- Do not mark EPIC 2 complete, and do not signal that EPIC 3 (Traceability
  & Coffee Lot) may begin, if any Completion Gate item fails or if the
  FIN-format ambiguity remains genuinely unresolved and unaddressed —
  report the gap and stop, per
  `.agents/execution/06-failure-and-escalation.md`.
- Do not modify the Baseline, Design Document, SRS, Implementation
  Specification, Minimum Project Plan, or any `.agents/rules/` or
  `.agents/execution/` file, even if verification surfaces an apparent
  inconsistency in them — record the inconsistency and escalate.

## Expected Agent Report

1. Pass/fail/open status for every EPIC-2 Completion Gate item in
   `00-epic-overview.md`, with evidence.
2. A list of any defects filed, against which `FARM-0xx` task, with
   reproduction detail.
3. The recorded status of all four Known Ambiguities from
   `00-epic-overview.md` (FIN format, RBAC role list, mapping library,
   area-calculation method).
4. Confirmation of the database-level check that a genuine
   Farmer -> Farm -> PostGIS-polygon chain exists, created through the
   actual UI.
5. Explicit statement of whether EPIC 2 is considered complete and EPIC 3
   may begin, or whether it is blocked pending defect/ambiguity
   resolution.
6. Confirmation that no farmer PII or credential appears in any artifact
   produced by this task.
