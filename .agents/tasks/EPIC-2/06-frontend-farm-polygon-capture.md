# Task Title

Frontend Farm Registration, Leaflet Polygon Capture & EUDR/Area Result Panel

## Task ID

EPIC-2-FARM-006

## Epic

EPIC 2 — Farmer & Polygon Registry

## Owner

Biniyam (Frontend Lead), with Yedenekachew (owns the underlying
polygon/area/EUDR data contract this UI must match exactly), per
Implementation Specification EPIC 2's dual frontend listing.

## Status

Not started.

## Priority

Critical — the primary acceptance path's "Draw / Save Farm Polygon,"
"Calculate Area," and "Display EUDR Status" steps all converge on this
screen.

## Objective

Implement the React frontend for farm registration: a farm form linked to
an existing farmer, an interactive Leaflet/React-Leaflet map for drawing a
polygon (with a single-point-radius fallback for small plots), and a
result panel displaying the computed area and EUDR demonstration status
immediately after submission.

## Why This Task Exists

Design Document §9.2 describes this as one integrated screen: "Farm
registration form with an interactive polygon-drawing map (Leaflet/Mapbox
GL) and a fallback single-point-radius entry mode for very small plots...
Validation result panel showing computed area and the EUDR demo-flag
outcome immediately after submission." (Note: Design Document §9.2's own
text says "Leaflet/Mapbox GL" in this one place, echoing the same
imprecision flagged as Known Ambiguity #3 in `00-epic-overview.md` — the
frozen stack decision, `.agents/rules/02-tech-stack.md`, and this
project's explicit current instruction not to introduce Mapbox GL both
govern here regardless of that one line's wording; this task uses Leaflet/
React-Leaflet only.)

## Authoritative Sources

- Design Document §9.2 (quoted above)
- Design Document §4.2 (polygon capture method; "Validation result panel
  showing computed area and the EUDR demo-flag outcome immediately after
  submission" restated in the Field data flow figure)
- Design Document §8 (Farms API contract, from `FARM-003`/`FARM-004`)
- `.agents/rules/02-tech-stack.md` (frozen mapping library: Leaflet /
  React-Leaflet only)

## Requirements Traceability

```text
SRS:
- FR-FARM-002 — the frontend expression of the same requirement backing
  FARM-003/FARM-004; the SRS's production EUDR check is narrowed away at
  the backend (FARM-004), and this task must display the resulting flag
  with the same "demonstration check" labeling FARM-004's response
  provides, not present it as a production result.

Design Document:
- Section 9.2 (this screen's description, including the "Leaflet/Mapbox
  GL" wording discrepancy noted above)
- Section 4.2 (Field data flow: draw/enter polygon -> backend computes
  area, EUDR flag -> UI displays result)
- Section 8 (the Farms API contract this task's frontend must match
  exactly, as actually implemented by FARM-003/FARM-004)

Implementation Specification:
- EPIC 2, Frontend Tasks: "Farm registration form, Leaflet map
  integration, polygon drawing & EUDR status display"

Minimum Project Plan:
- Section 7.4 lists "Leaflet/Mapbox GL" as the mapping tooling option —
  this is the same imprecision as Design Document §9.2's wording; per
  00-epic-overview.md's Known Ambiguity #3, the frozen tech-stack rule and
  this project's explicit current instruction settle Leaflet/React-Leaflet
  as the only approved choice for this task, without this task set
  resolving the underlying document-level discrepancy.

Baseline Scope Freeze:
- Section 2, Technology Baseline — "Mapping: Leaflet / React-Leaflet"
- Section 4, Critical Workflow — "Draw / Save Farm Polygon"
```

## Dependencies

`EPIC-2-FARM-003` and `EPIC-2-FARM-004` (the Farm/polygon/area/EUDR API
contract this task builds against — both must be merged, since this
screen needs the fully-populated response, not just geometry persistence
alone) and `EPIC-2-FARM-005` (the farmer must already be selectable from a
working farmer list/detail view).

## Preconditions

- `FARM-003` and `FARM-004` merged; `POST /api/v1/farms` returns a fully
  populated response including `area_hectares`, `eudr_risk_flag`, and the
  demonstration-check labeling.
- `FARM-005` merged, so a registered farmer can be selected as the target
  of a new farm.
- Confirm the actual, current shape of `FARM-003`/`FARM-004`'s API
  responses by inspecting their implementation/tests before building the
  client, per `.agents/execution/01-agent-start-procedure.md` Step 4.

## Allowed Scope

- A farm registration form: farmer selection (reusing `FARM-005`'s farmer
  list/lookup), and a Leaflet/React-Leaflet map for drawing a polygon.
- A single-point-radius fallback input mode for small plots, matching
  `FARM-003`'s accepted second input shape exactly.
- Submission to `POST /api/v1/farms`, converting the drawn
  polygon/point-radius into the GeoJSON shape `FARM-003` expects.
- A result panel, shown immediately after successful submission, displaying
  the computed area (hectares) and the EUDR demonstration flag with its
  "demonstration check" labeling, per Design Document §4.2's Field data
  flow.
- A control to re-run `POST /api/v1/farms/{id}/validate` against an
  already-created farm (surfacing `FARM-004`'s idempotent re-validation
  capability in the UI, since Design Document §8 documents this endpoint
  as "used after a polygon edit" — even though polygon editing itself is
  out of scope, exposing a manual re-validate action is a reasonable,
  minimal UI for the endpoint that exists; if this is judged unnecessary
  for the demo, it may be omitted — record the decision either way in the
  `Expected Agent Report` rather than silently including or excluding it).

## Out of Scope

- Any mapping library other than Leaflet/React-Leaflet — see Known
  Ambiguity #3 in `00-epic-overview.md`; do not introduce Mapbox GL despite
  the wording in Design Document §9.2 and Minimum Project Plan §7.4.
- Editing an already-drawn polygon's geometry — Design Document §8 defines
  no update endpoint for a Farm's geometry; only creation and re-validation
  of the existing geometry exist.
- Farmer registration UI (`FARM-005`).
- Any real map-tile/basemap service requiring a paid API key or account
  beyond what Leaflet's standard open tile providers already support —
  do not introduce a new mapping-service dependency to make the map
  "nicer."

## Files/Directories Potentially Affected

Indicative paths — confirmed against the actual existing frontend project
structure:

- `frontend/src/pages/FarmRegistration.jsx` (or equivalent).
- `frontend/src/components/PolygonMap.jsx` (or equivalent Leaflet/
  React-Leaflet drawing component).
- `frontend/src/components/EudrResultPanel.jsx` (or equivalent).
- `frontend/src/api/farms.js` (or equivalent API client module).
- `frontend/package.json` — adding `react-leaflet`/`leaflet` if not
  already present; confirm first whether it is already installed (per
  `.agents/rules/02-tech-stack.md`'s dependency-inspection allowance)
  before adding it.
- `frontend/src/tests/` (or wherever frontend tests already live).

## Implementation Requirements

- The map component uses React-Leaflet (built on Leaflet) exclusively —
  verify this dependency's presence or add it as the one, specifically
  justified new frontend dependency this epic requires, per
  `.agents/rules/02-tech-stack.md`'s dependency procedure (verify not
  already installed; verify it is required; explain why; confirm
  compatibility; update `package.json`; test).
- The drawn polygon is converted to GeoJSON before submission, matching
  `FARM-003`'s accepted request shape exactly (as actually implemented,
  confirmed per Preconditions).
- The single-point-radius fallback mode is a genuinely separate UI path
  (not a degenerate case of the polygon-drawing tool), matching
  `FARM-003`'s second accepted input shape.
- The result panel displays the EUDR flag together with an explicit,
  visible statement that it is a demonstration/simplified check — this is
  a Design Document §4.2 requirement ("This limitation is stated in the
  UI... so it is never presented as the production-grade EUDR check"), not
  an optional nicety.
- Route protection and role restriction on the registration action mirror
  `FARM-005`'s pattern (Field/Registry Agent or Admin to submit; any
  authenticated role may view, once a farm-detail view exists in a later
  task/epic — this task itself does not need to build a separate farm
  detail/list view beyond what is needed to show the result panel
  immediately after submission).

## Acceptance Criteria

- An authenticated Field/Registry Agent can select a farmer, draw a
  polygon with at least 6 vertices on the map, submit it, and see the
  correct area and EUDR demonstration status displayed immediately after.
- The same flow works using the single-point-radius fallback for a small
  plot.
- The EUDR result panel visibly labels the flag as a demonstration/
  simplified check, not a production determination.
- Submitting a polygon with fewer than 6 vertices in non-single-point-
  radius mode is rejected by the backend and the frontend displays that
  rejection clearly, without inventing a different message than the
  backend actually returns.
- Navigating to this screen while unauthenticated redirects to login.
- No mapping library other than Leaflet/React-Leaflet is present in the
  frontend dependency tree as a result of this task.

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- Test: successful polygon submission displays correct area and EUDR
  status.
- Test: successful single-point-radius submission displays correct area
  and EUDR status.
- Test: invalid polygon (too few vertices) submission surfaces the
  backend's rejection correctly.
- Test: unauthenticated access redirects to login.
- Test (if the re-validate control is implemented): triggering it against
  an existing farm returns and displays the same result as the original
  submission (confirming the frontend correctly surfaces `FARM-004`'s
  idempotency).

## Security Requirements

- No farmer/farm PII beyond what is already shown elsewhere in the
  application is exposed by this screen.
- The JWT used to call these endpoints is sourced from the existing auth
  state (`EPIC-1-AUTH-006`) — this task does not implement its own token
  handling.

## Error Handling Requirements

- Network/API failures are handled with a user-visible error state, not a
  silent failure, consistent with the pattern established in
  `EPIC-1-AUTH-006`/`FARM-005`.
- A geometry that the map-drawing tool cannot cleanly convert to valid
  GeoJSON (e.g., an unclosed polygon) is caught and reported to the user
  before submission, not sent to the backend to fail there.

## Documentation Requirements

- Kidus updates the requirements-traceability entry for Design Document
  §9.2's farm-registration screen to "implemented," and specifically notes
  that the EUDR demonstration-check labeling is present in the UI, per
  Design Document §4.2's explicit requirement.

## Commit Guidance

- Branch: `feature/EPIC-2-FARM-006-frontend-farm-polygon-capture`, from
  `develop`.
- Commit message pattern: `feat(farm): implement frontend farm registration with Leaflet polygon capture`.
- PR references Task ID `EPIC-2-FARM-006` and explicitly confirms no
  mapping library other than Leaflet/React-Leaflet was introduced.
- Merge target: `develop`.

## Verification Requirements

Self-review per `.agents/execution/03-verification-and-testing.md`;
specifically confirm the EUDR demonstration-check labeling is visibly
present in the rendered UI (not only in code/response data that isn't
actually displayed).

## Escalation / Change-Control Conditions

- If, during implementation, `FARM-003`/`FARM-004`'s actual response shape
  differs from this task file's description in a way that affects the UI,
  escalate per `.agents/execution/06-failure-and-escalation.md` rather
  than silently adapting.
- Do not resolve the Design Document §9.2 / Minimum Project Plan §7.4
  "Leaflet/Mapbox GL" wording as anything other than "use Leaflet /
  React-Leaflet only" — that specific practical point is already settled
  by `.agents/rules/02-tech-stack.md` and this project's current
  instruction; only the underlying document-level discrepancy remains
  open, and it does not block this task.

## Expected Agent Report

Standard format from `.agents/execution/04-human-review-and-approval.md`,
plus:

1. Confirmation that React-Leaflet/Leaflet was already present or was
   added following the dependency procedure in
   `.agents/rules/02-tech-stack.md`, with justification.
2. Confirmation that no other mapping library appears in the dependency
   tree.
3. Whether the manual re-validate control was implemented, and why.
4. Confirmation that the EUDR demonstration-check labeling is visibly
   rendered in the UI.
5. Test results.
