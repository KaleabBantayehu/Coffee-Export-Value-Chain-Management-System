# Task Title

Area Calculation & EUDR Demonstration Flagging Logic

## Task ID

EPIC-2-FARM-004

## Epic

EPIC 2 — Farmer & Polygon Registry

## Owner

Yedenekachew (Database Lead & Backend Developer)

## Status

Not started.

## Priority

Critical — the primary acceptance path's "Calculate Area" and "Display
EUDR Status" steps; this is the last backend piece before frontend work
(`FARM-006`) can present a complete result to the user.

## Objective

Implement server-side area calculation (in hectares) from a Farm's
persisted polygon, and a simplified, clearly-labeled EUDR demonstration
flag, extending `FARM-003`'s `POST /api/v1/farms` to populate both fields
on creation, and implementing `POST /api/v1/farms/{id}/validate` to
re-run the check idempotently.

## Why This Task Exists

Design Document §4.2 requires area and an EUDR flag to be computed and
displayed, but explicitly as a "simplified, clearly-labeled demonstration
check" rather than the SRS's production forest-canopy validation —
"stated in the UI and in the Test Report so it is never presented as the
production-grade EUDR check." This task is where that specific, deliberate
narrowing is implemented; it must not accidentally build something closer
to the enterprise version than the Design Document allows.

## Authoritative Sources

- Design Document §4.2 ("area in hectares is computed server-side from the
  geometry... EUDR risk flagging in Version 1.0: rather than the SRS's
  full production check against 2020 Global Forest Canopy datasets... the
  design implements a simplified, clearly-labeled demonstration check —
  e.g. an area-threshold and/or a static, project-seeded 'restricted zone'
  polygon layer used only to prove the flagging workflow. This limitation
  is stated in the UI and in the Test Report so it is never presented as
  the production-grade EUDR check.")
- Design Document §7.2 (`Farm.area_hectares`, `Farm.eudr_risk_flag` —
  already created by `EPIC-0-DB-002`)
- Design Document §8 (`POST /api/v1/farms/{id}/validate` — "Re-run the
  EUDR demo-flag check" — Auth: "JWT + Field/Registry Agent or Admin" —
  "Idempotent; used after a polygon edit.")
- Design Document §13, Sequence 3 (Capture / Validate Farm Polygon)
- SRS FR-FARM-002 ("Business Rules: Plots overlapping designated national
  forest reserves or deforested zones (post-December 31, 2020 baseline)
  are automatically flagged as non-EU export compliant.")

## Requirements Traceability

```text
SRS:
- FR-FARM-002's production business rule (overlap against real forest-
  reserve/deforestation datasets) is explicitly NOT implemented here —
  Design Document §4.2 substitutes a demonstration-scale check instead.
  This task implements the Design Document's substitute, not the SRS's
  literal rule, and must keep that substitution visibly labeled as such
  (see Implementation Requirements).

Design Document:
- Section 4.2 (the narrowing decision, quoted in full above)
- Section 7.2 (area_hectares, eudr_risk_flag fields, from EPIC-0-DB-002)
- Section 8 (POST /farms area/flag computation; POST /farms/{id}/validate)
- Section 13, Sequence 3

Implementation Specification:
- EPIC 2, Backend Tasks: "area calculation, EUDR demonstration logic"

Minimum Project Plan:
- Week 2 Key Activities include Farmer & Polygon Registry implementation;
  no EUDR-specific detail beyond what the SRS/Design Document already
  state.

Baseline Scope Freeze:
- Section 3.1, "Farm polygon mapping" (area/EUDR are part of this core
  item, per the Implementation Specification's EPIC 2 backend task list)
```

## Dependencies

`EPIC-2-FARM-003` (a persisted polygon must exist to compute area and an
EUDR flag against).

## Preconditions

- `FARM-003` merged; `POST /api/v1/farms` successfully persists geometry
  with `area_hectares`/`eudr_risk_flag` currently unset, per that task's
  Sequencing Note.

## Allowed Scope

- Extending `FARM-003`'s `POST /api/v1/farms` handler to compute
  `area_hectares` and `eudr_risk_flag` before returning the response and
  persisting both onto the same `Farm` row (not a second write elsewhere).
- Implementing `POST /api/v1/farms/{id}/validate`, re-running the same
  area/flag computation against the already-stored geometry, idempotently
  (running it twice on an unmodified polygon produces the same result both
  times).
- The area-calculation method and the EUDR demonstration-flag method
  themselves (see Implementation Requirements for what is and is not
  specified by the Design Document).

## Out of Scope

- Any real satellite/GIS forest-canopy dataset integration — Design
  Document §4.2 is explicit that this is out of one-month scope.
- Any change to `FARM-003`'s geometry validation or persistence logic
  beyond adding the area/flag computation call.
- A Farm update/edit endpoint that lets a user redraw the polygon — Design
  Document §8 only supports re-running validation on the *existing*
  geometry via `/validate`, not editing it.
- Presenting the EUDR flag anywhere (backend response or, later,
  frontend UI) without it being clearly labeled as a demonstration check —
  this labeling requirement is binding on this task's response shape (a
  field/message indicating "demonstration check" is expected) and is
  restated for `FARM-006`'s frontend display.

## Files/Directories Potentially Affected

Indicative paths, matched against the existing backend layout:

- `backend/app/services/farm_service.py` (extended from `FARM-003`) or a
  new `backend/app/services/eudr_service.py` (or equivalent) if the team's
  existing structure separates geometry-math from business-rule logic —
  match whichever pattern `FARM-003` already established rather than
  introducing a new one without reason.
- `backend/app/api/v1/farms.py` — the new `/validate` route.
- `backend/tests/` — tests for area calculation and EUDR flagging.

## Implementation Requirements

- **Area calculation method is not fully specified by the Design
  Document** (§4.2 says only "computed server-side from the geometry").
  This is not treated as a blocking ambiguity of the same severity as
  `FARM-001`'s FIN-format conflict — `.agents/rules/02-tech-stack.md`'s
  allowance for fulfilling an already-approved requirement without
  separate change control applies, since *that* area is computed is fixed
  and only *how* is open. Choose and explicitly record a specific,
  justified method (e.g., PostGIS `ST_Area` on a geography-cast of the
  SRID-4326 geometry, which accounts for the earth's curvature and returns
  a metric result convertible to hectares, versus a raw planar `ST_Area`
  on the SRID-4326 geometry, which is not areally accurate in degrees and
  would need an explicit projection step to be meaningful in hectares).
  Do not pick silently — the `Expected Agent Report` must state which was
  used and why.
- **EUDR demonstration flag** implements one or both of the two
  Design-Document-suggested mechanisms: an area threshold (e.g., flagging
  unusually large plots as warranting closer review) and/or a static,
  project-seeded "restricted zone" polygon layer that the computed
  geometry is checked for overlap against. Whichever is chosen (or both),
  it must be:
  - deterministic and reproducible (the same polygon always produces the
    same flag);
  - clearly distinguishable, in the response, from a real regulatory
    determination — e.g., a boolean flag alone is insufficient if it could
    be mistaken for a production result; include or require a
    demonstration-check indicator alongside it, consistent with Design
    Document §4.2's labeling requirement.
- `POST /api/v1/farms/{id}/validate` requires `Field/Registry Agent or
  Admin`, re-runs the same computation against the Farm's existing
  `polygon_geom`, updates `area_hectares`/`eudr_risk_flag` on the record,
  and is idempotent.

## Acceptance Criteria

- After `POST /api/v1/farms` succeeds (extended by this task), the
  returned Farm record includes a populated `area_hectares` value and a
  populated `eudr_risk_flag` value, both persisted to the database.
- The area value is plausible for the submitted geometry (verified in a
  test against a polygon with a known, calculable area) — not zero, not
  null, and within a reasonable tolerance of the expected value.
- Calling `POST /api/v1/farms/{id}/validate` on an unmodified Farm returns
  the same `area_hectares`/`eudr_risk_flag` values as were already stored
  (idempotency).
- The EUDR flag response is accompanied by an explicit indication that it
  is a demonstration/simplified check, not a production determination.
- The same `/validate` request from an unauthorized role is rejected with
  `403`; unauthenticated is rejected with `401`.
- A request to `/validate` for a non-existent Farm ID returns `404`.

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- Test: area calculation against a polygon with a known, independently
  calculable area returns a value within acceptable tolerance.
- Test: EUDR flag is deterministic — the same polygon always produces the
  same flag across repeated calls.
- Test: `/validate` is idempotent (two calls on an unmodified Farm produce
  identical results).
- Test: `/validate` role/auth enforcement (`403`/`401`) and `404` for a
  non-existent Farm.
- Test: the response includes the demonstration-check labeling.
- Regression: `FARM-003`'s existing Farm creation/retrieval tests still
  pass with the area/flag fields now populated.

## Security Requirements

- RBAC enforcement is via `EPIC-1-AUTH-004`'s mechanism only.
- No external network call is made for the EUDR check (per Design
  Document §4.2, this is a local/static, project-seeded check, not a live
  integration — introducing an external call here would silently expand
  scope toward the SRS's enterprise version and is not permitted without
  change control).

## Error Handling Requirements

- If area calculation fails for a malformed or degenerate geometry (e.g.,
  zero-area or self-intersecting polygon that passed `FARM-003`'s vertex-
  count check but is otherwise invalid), return a structured `400` rather
  than a raw computation exception.
- Non-existent Farm ID on `/validate` -> `404`.

## Documentation Requirements

- Kidus updates the requirements-traceability entry for FR-FARM-002's
  EUDR business rule to explicitly state the demonstration-scale
  substitution, referencing Design Document §4.2, so the Test Report
  never implies production-grade EUDR compliance — consistent with the
  Design Document's own instruction that this limitation must appear "in
  the UI and in the Test Report."

## Commit Guidance

- Branch: `feature/EPIC-2-FARM-004-area-eudr-logic`, from `develop`.
- Commit message pattern: `feat(farm): implement area calculation and EUDR demonstration flagging`.
- PR references Task ID `EPIC-2-FARM-004` and states the exact area-
  calculation method chosen.
- Merge target: `develop`.

## Verification Requirements

Self-review per `.agents/execution/03-verification-and-testing.md`;
specifically verify the demonstration-check labeling is present in the
actual API response, not only in code comments.

## Escalation / Change-Control Conditions

- If, during implementation, no reasonable static "restricted zone" data
  source is available to seed the overlap check (e.g., no such data exists
  anywhere in the repository or project documents), and an area-threshold-
  only approach seems insufficient to "prove the flagging workflow" as
  Design Document §4.2 requires, escalate per
  `.agents/execution/06-failure-and-escalation.md` rather than inventing
  arbitrary restricted-zone data without recording that it is arbitrary.

## Expected Agent Report

Standard format from `.agents/execution/04-human-review-and-approval.md`,
plus:

1. The exact area-calculation method chosen and why.
2. The exact EUDR demonstration-flag mechanism chosen (area threshold,
   static restricted-zone overlap, or both) and, if a restricted-zone
   layer was used, where its (synthetic) data came from.
3. Confirmation that the demonstration-check labeling appears in the
   actual API response.
4. Test results, including the known-area tolerance check.
