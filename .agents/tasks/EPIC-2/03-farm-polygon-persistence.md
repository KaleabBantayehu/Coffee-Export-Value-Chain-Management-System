# Task Title

Farm Model, Farmer -> Farm Relationship & PostGIS Polygon Persistence

## Task ID

EPIC-2-FARM-003

## Epic

EPIC 2 — Farmer & Polygon Registry

## Owner

Yedenekachew (Database Lead & Backend Developer)

## Status

Not started.

## Priority

Critical — the primary acceptance path's "Register Farm" and "Draw / Save
Farm Polygon" steps; the direct precondition for `FARM-004` and, later, all
of EPIC 3.

## Objective

Implement `POST /api/v1/farms` and `GET /api/v1/farms/{id}`: create a Farm
record with a mandatory link to an existing Farmer, persist its boundary as
PostGIS geometry, and return it (including GeoJSON for map rendering) on
retrieval. Area calculation and EUDR flagging logic are `FARM-004`'s
responsibility; this task calls into that logic rather than implementing it
inline, once `FARM-004` exists — for this task alone, area/flag fields may
be left as placeholders or computed inline temporarily, with the refactor
to call `FARM-004`'s functions completed as part of `FARM-004` itself (see
"Sequencing Note" below).

## Why This Task Exists

Design Document §5.1 states "a Coffee Lot references exactly one
originating Farm" — nothing in EPIC 3 can exist without a real, persisted
Farm. Design Document §7 requires the polygon to be stored as PostGIS
geometry, "never a plain latitude/longitude text field... a Design
Document requirement, not a style preference" (also restated in
Implementation Playbook §8).

## Authoritative Sources

- Design Document §4.2 ("A Field/Registry Agent draws the farm boundary on
  an interactive web map... using vertex points, or enters a single point
  with a radius for very small plots — matching the SRS FR-FARM-002 rule
  (single-point radius allowed under 4,000 sqm). The captured polygon is
  stored as a PostGIS `GEOMETRY(Polygon, 4326)` value... Every farm is
  linked 1-to-many from Farmer.")
- Design Document §7.2 (`Farm` entity: `farm_id`, `farmer_id` (FK),
  `polygon_geom` (PostGIS Polygon, 4326), `area_hectares`,
  `eudr_risk_flag`, `created_at` — already created by `EPIC-0-DB-002`)
- Design Document §8 (API Design — Farms table):
  - `POST /api/v1/farms` — "Register a farm with polygon/point geometry"
    — Auth: "JWT + Field/Registry Agent or Admin" — "Body includes GeoJSON
    geometry; server computes area_hectares and eudr_risk_flag."
  - `GET /api/v1/farms/{id}` — "Retrieve a farm, including geometry" —
    Auth: "JWT" — "Returns GeoJSON for map rendering."
- SRS FR-FARM-002 ("Inputs: GPS Spatial Vertices (Minimum 6 coordinate
  pairs for plots > 4,000 sqm; single point radius for plots < 4,000 sqm)")
- Design Document §13, Sequence 2 and Sequence 3

## Requirements Traceability

```text
SRS:
- FR-FARM-002 (Module 02) — Geolocation Farm Polygon Capture. Its
  6-coordinate-minimum and 4,000-sqm single-point-radius threshold are
  restated directly (Design Document §4.2 references the same 4,000-sqm
  threshold without contradicting the 6-coordinate minimum, so both are
  carried forward here as authoritative validation rules, not narrowed
  away). Its production forest-canopy EUDR check is narrowed away by
  Design Document §4.2 — but that narrowing is FARM-004's concern, not
  this task's; this task only persists geometry.

Design Document:
- Section 4.2 (polygon capture method, PostGIS storage requirement,
  farmer 1:N farm relationship)
- Section 7.1/7.2 (ERD, Farm entity, from EPIC-0-DB-002)
- Section 8 (Farms API — POST/GET, quoted above)
- Section 13, Sequence 2 (Register Farmer and Farm), Sequence 3 (Capture/
  Validate Farm Polygon)

Implementation Specification:
- EPIC 2, Backend Tasks: "Farm model, Farmer -> Farm mapping, PostGIS
  geometry storage" (area calculation and EUDR logic are separately listed
  and are FARM-004's scope)

Minimum Project Plan:
- Section 7.3 Task Dependencies: "Database schema (users/roles, farmers,
  farms/polygons...) must exist before any API work starts" — already
  satisfied by EPIC-0-DB-002; this task is the API work that schema
  requirement was written to unblock.

Baseline Scope Freeze:
- Section 3.1, "Farm registration"; "Farm polygon mapping"
- Section 4, Critical Workflow — "Register Farm"; "Draw / Save Farm
  Polygon"
```

## Dependencies

`EPIC-2-FARM-002` (a real, persisted Farmer must exist to attach a Farm
to) and `EPIC-1-AUTH-003`/`EPIC-1-AUTH-004`.

## Preconditions

- `FARM-002` merged; at least one real Farmer can be created and retrieved.
- The `Farm` table, including its `polygon_geom` PostGIS column, exists per
  `EPIC-0-DB-002`.

## Sequencing Note (read before implementing)

`FARM-004` (area calculation and EUDR flagging) is a separate task in this
epic's dependency chain, listed as depending on this one. Since Design
Document §8 describes `POST /api/v1/farms` as computing `area_hectares` and
`eudr_risk_flag` in the *same* request, there is a real question of whether
that computation belongs inside this task or is added by `FARM-004`
extending this task's endpoint. **Resolution for this epic:** this task
implements `POST /api/v1/farms` accepting and persisting geometry only,
storing `area_hectares` and `eudr_risk_flag` as `NULL`/unset at the end of
this task; `FARM-004` then extends the same endpoint to compute and
populate both fields before returning the response. This keeps geometry
persistence (a storage/validation concern) and area/EUDR computation (a
business-logic concern) independently reviewable, mirroring how
`EPIC-1-AUTH-003` (session mechanics) and `EPIC-1-AUTH-004` (authorization
business rule) were kept separate. Record in this task's `Expected Agent
Report` that `area_hectares`/`eudr_risk_flag` are intentionally
unpopulated pending `FARM-004`, so a reviewer does not mistake this for an
oversight.

## Allowed Scope

- `POST /api/v1/farms`: accept a `farmer_id` and a GeoJSON geometry
  (polygon vertices, or a single point + radius for small plots), validate
  and persist it as `polygon_geom`.
- `GET /api/v1/farms/{id}`: retrieve a Farm, returning its geometry as
  GeoJSON.
- Geometry validation: vertex-count rule (minimum 6 coordinate pairs for
  plots reasoned to be over 4,000 sqm; single-point-radius accepted for
  smaller plots), per SRS FR-FARM-002 and Design Document §4.2.
- The mandatory `farmer_id` foreign-key relationship, rejecting a Farm
  creation request that references a non-existent Farmer.

## Out of Scope

- Area calculation and EUDR demonstration flagging logic (`FARM-004`) —
  this task's endpoint leaves those fields unset, per "Sequencing Note."
- Any Farm update/edit endpoint — Design Document §8 defines no `PUT`/
  `PATCH` for Farm; only creation and the separate `/validate` re-run
  endpoint (`FARM-004`'s scope) exist.
- Any Farm deletion endpoint.
- Cherry collection, Coffee Lot creation, or Traceability (later epics).
- Real satellite/GIS forest-canopy validation (SRS FR-FARM-002's
  production behavior; explicitly narrowed away, and in any case not this
  task's concern — see Sequencing Note).

## Files/Directories Potentially Affected

Indicative paths, matched against the existing backend layout:

- `backend/app/api/v1/farms.py` (or equivalent).
- `backend/app/schemas/farm.py` (or equivalent) — including GeoJSON
  request/response shape.
- `backend/app/services/farm_service.py` (or equivalent) — geometry
  validation, Farmer-existence check, persistence.
- `backend/tests/` — tests for both endpoints.

## Implementation Requirements

- `POST /api/v1/farms` requires `Field/Registry Agent or Admin`, enforced
  via `EPIC-1-AUTH-004`'s mechanism.
- The request body's geometry is accepted as GeoJSON and converted to
  PostGIS `GEOMETRY(Polygon, 4326)` on persistence — never stored as plain
  latitude/longitude fields, per Design Document §7 and Implementation
  Playbook §8.
- A polygon with fewer than 6 vertices is rejected **unless** the request
  represents the single-point-radius mode for small plots, per SRS
  FR-FARM-002 — implement both accepted input shapes explicitly (a
  multi-vertex polygon, or a single point + radius value), not just one.
- `farmer_id` must reference an existing `Farmer`; a request citing a
  non-existent `farmer_id` is rejected with a structured `400`/`404`, not a
  raw foreign-key violation surfaced to the client.
- `GET /api/v1/farms/{id}` returns the stored geometry converted back to
  GeoJSON, per Design Document §8's "Returns GeoJSON for map rendering."

## Acceptance Criteria

- An authenticated Field/Registry Agent can create a Farm with a valid
  multi-vertex polygon, linked to an existing Farmer, and receives
  `200`/`201`.
- An authenticated Field/Registry Agent can create a Farm using the
  single-point-radius mode for a small plot and receives `200`/`201`.
- A request with fewer than 6 vertices, not using single-point-radius mode,
  is rejected with a structured `400`.
- A request citing a `farmer_id` that does not exist is rejected with a
  structured error, not a raw database exception.
- The same creation request from a role other than Field/Registry Agent or
  Admin is rejected with `403`; unauthenticated is rejected with `401`.
- `GET /api/v1/farms/{id}` for an existing Farm returns `200` with a valid
  GeoJSON representation of the stored geometry.
- `GET /api/v1/farms/{id}` for a non-existent Farm returns `404`.
- Querying the database directly confirms `polygon_geom` is stored as a
  PostGIS geometry column value, not a text/JSON blob standing in for one.

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- Test: valid multi-vertex polygon creation succeeds and is retrievable.
- Test: valid single-point-radius creation succeeds and is retrievable.
- Test: fewer-than-6-vertex polygon (non-single-point-radius) is rejected.
- Test: invalid/non-existent `farmer_id` is rejected cleanly.
- Test: role-based rejection (`403`) and unauthenticated rejection (`401`).
- Test: retrieved GeoJSON round-trips correctly against what was submitted
  (same vertex coordinates, allowing for reasonable floating-point
  tolerance).
- Regression: `FARM-002`'s Farmer tests and `EPIC-1`'s auth/RBAC tests
  still pass.

## Security Requirements

- RBAC enforcement is via `EPIC-1-AUTH-004`'s mechanism only.
- No farmer PII is exposed via the Farm endpoints beyond the `farmer_id`
  reference itself.

## Error Handling Requirements

- Invalid geometry (malformed GeoJSON, self-intersecting polygon if
  detectable at this layer, wrong vertex count) -> structured `400`.
- Non-existent `farmer_id` -> structured `400`/`404`.
- Non-existent Farm ID on retrieval -> `404`.
- Unauthorized role -> `403`; unauthenticated -> `401`.

## Documentation Requirements

- Kidus updates the requirements-traceability entry for FR-FARM-002 to
  "polygon persistence implemented; area calculation and EUDR flagging
  pending FARM-004."

## Commit Guidance

- Branch: `feature/EPIC-2-FARM-003-farm-polygon-persistence`, from
  `develop`.
- Commit message pattern: `feat(farm): implement farm creation with PostGIS polygon persistence`.
- PR references Task ID `EPIC-2-FARM-003` and explicitly notes
  `area_hectares`/`eudr_risk_flag` are unpopulated pending `FARM-004`.
- Merge target: `develop`.

## Verification Requirements

Self-review per `.agents/execution/03-verification-and-testing.md`;
specifically confirm, by querying the database (not just reading the ORM
model), that `polygon_geom` is a genuine PostGIS geometry value.

## Escalation / Change-Control Conditions

- If the 6-vertex-minimum / 4,000-sqm threshold from SRS FR-FARM-002 turns
  out to be ambiguous in practice (e.g., the request does not include an
  explicit area estimate to decide which validation branch applies before
  the polygon is even parsed), escalate per
  `.agents/execution/06-failure-and-escalation.md` rather than inventing a
  resolution order — do not guess whether vertex count or a pre-computed
  area estimate is checked first if the SRS does not make this clear from
  the request payload alone.

## Expected Agent Report

Standard format from `.agents/execution/04-human-review-and-approval.md`,
plus:

1. Confirmation that `polygon_geom` is a genuine PostGIS geometry column
   value, with the verification query used.
2. Confirmation that both accepted input shapes (multi-vertex polygon;
   single-point-radius) were implemented and tested.
3. Explicit confirmation that `area_hectares`/`eudr_risk_flag` are left
   unpopulated in this task, per the Sequencing Note.
4. Test results.
