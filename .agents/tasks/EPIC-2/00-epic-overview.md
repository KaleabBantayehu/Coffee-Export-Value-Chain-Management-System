# EPIC 2 — Farmer & Polygon Registry: Overview

## Epic ID

EPIC-2

## Epic Name

Farmer & Polygon Registry

## Note on Source Hierarchy Discrepancy (read first)

This request's source list names `.agents/rules/02-architecture-rules.md`,
`.agents/rules/03-technology-rules.md`, and
`.agents/rules/07-current-project-decisions.md`. **None of these three
files exist in the actual `.agents/rules/` directory.** The real files are
`00-project-authority.md`, `01-scope-boundaries.md`, `02-tech-stack.md`,
`03-coding-rules.md`, `04-git-workflow.md`, `05-testing-rules.md`, and
`06-change-control.md`. Per the file-safety instruction to stop and report
rather than silently invent files, this discrepancy is recorded here
instead of creating placeholder rule files or guessing their content. This
EPIC-2 task set is built entirely against the actual, existing rule files.

The "known project decisions/conflicts" content the request expects in
`07-current-project-decisions.md` actually lives in
`.agents/execution/00-execution-overview.md`, under "Known documented
conflicts." That is the source used below.

## Objective

Implement the Farmer & Polygon Registry: farmer registration and
retrieval, farm registration with mandatory PostGIS polygon capture, area
calculation, and a simplified EUDR demonstration flag — completing the
second link in the V1.0 core chain, on top of the Authentication & RBAC
foundation EPIC 1 already delivered.

## Business / Project Purpose

Per the Baseline's critical workflow, "Register Farmer," "Register Farm,"
and "Draw / Save Farm Polygon" are the second and third steps of the
primary acceptance path, immediately after Login. Per Design Document §5.1,
every downstream Coffee Lot must reference exactly one originating Farm —
so EPIC 2 is also what makes EPIC 3 (Traceability) possible at all: without
a real Farmer/Farm/Polygon record, there is nothing for a Coffee Lot to
trace back to.

## Bounded V1.0 Scope

In scope, per Implementation Specification EPIC 2 and Design Document §4.2:

**Backend:**
- Farmer registration, retrieval, and validation (on top of the `Farmer`
  table already created by `EPIC-0-DB-002`).
- FIN (Farmer Identification Number) generation — **see the flagged
  ambiguity below; this is not fully specified and blocks part of
  `FARM-001`.**
- Farm model business logic and the mandatory Farmer -> Farm relationship
  (on top of the `Farm` table already created by `EPIC-0-DB-002`).
- PostGIS polygon geometry storage (`GEOMETRY(Polygon, 4326)`, already the
  column type fixed by `EPIC-0-DB-002`).
- Server-side area calculation from the stored geometry.
- Simplified, clearly-labeled EUDR demonstration flagging logic (**not**
  the SRS's production forest-canopy check).

**Frontend:**
- Farmer registration form; farmer list/details view.
- Farm registration form with Leaflet/React-Leaflet polygon drawing (and a
  single-point-radius fallback for small plots).
- Display of the computed area and the EUDR demonstration status
  immediately after farm submission.

This is deliberately **not** expanded to: cherry collection/intake, coffee
lot creation, traceability events, QR generation, quality grading,
waybill, export licensing, forex, SMS/USSD, offline Android, GPS/IoT
hardware integration, or any external/production EUDR service — all of
these are later epics or explicitly out of V1.0 scope
(`.agents/rules/01-scope-boundaries.md`).

## Owner (from authoritative sources)

Per Baseline §5 and Implementation Specification EPIC 2 ("Owner:
Yedenekachew (Backend) / Biniyam + Yedenekachew (Frontend)"):

- **Yedenekachew** — owns all backend EPIC-2 tasks (`FARM-001` through
  `FARM-004`): Farmer model/FIN logic, Farmer API, Farm model and
  Farmer->Farm relationship, PostGIS polygon persistence, area
  calculation, and EUDR demonstration logic. Baseline §5 also states
  Yedenekachew "owns the database schema" generally — the schema itself
  was already created in `EPIC-0-DB-002`; EPIC 2's backend tasks build the
  business logic and API layer on top of it.
- **Biniyam** (Frontend Lead) with **Yedenekachew** — own the frontend
  tasks (`FARM-005`, `FARM-006`), per the Implementation Specification's
  explicit dual listing for EPIC 2's frontend work. Biniyam leads the
  React UI/API integration generally (Baseline §5); Yedenekachew's
  involvement reflects his ownership of the underlying polygon/EUDR data
  contract the map UI must match exactly.
- **Ephratha** — owns end-to-end verification (`FARM-007`), per Baseline
  §5 ("Ephratha... owns... RBAC security testing across all core
  modules... owns defect tracking").
- **Kidus** — updates requirements-traceability and test documentation as
  each task completes, per Baseline §5.

## Dependencies

- `EPIC-1` (Authentication & RBAC) — **complete**. All EPIC-2 write
  endpoints require a valid JWT and, per Design Document §8, the
  Field/Registry Agent or Admin role specifically; EPIC 2 consumes
  `EPIC-1-AUTH-003`'s authentication dependency and `EPIC-1-AUTH-004`'s
  RBAC authorization mechanism as-is. **EPIC 2 does not create a second
  authorization system.**
- `EPIC-0-DB-002` (initial schema) — complete. The `Farmer` and `Farm`
  tables, including the `Farm.polygon_geom` PostGIS column and the
  `Farmer.fin_code`/`Farmer.national_id` uniqueness constraints, already
  exist. EPIC 2 does not alter this schema; if a genuine schema gap is
  found, that is change control (`.agents/rules/06-change-control.md`),
  not a silent migration.

## Preconditions

- `develop` reflects EPIC 0 and EPIC 1 complete, per the current project
  state.
- The `Farmer` and `Farm` tables are reachable via the database connection
  configured in `EPIC-0-DB-001`.
- The authentication dependency (`EPIC-1-AUTH-003`) and RBAC authorization
  mechanism (`EPIC-1-AUTH-004`) are merged and usable by new routes without
  modification.

## Task Inventory

| Task ID | File | Title | Owner |
|---|---|---|---|
| EPIC-2-FARM-001 | `01-farmer-fin-foundation.md` | Farmer Data Foundation — FIN Generation & Validation Utility | Yedenekachew |
| EPIC-2-FARM-002 | `02-farmer-registration-api.md` | Farmer Registration & Retrieval API | Yedenekachew |
| EPIC-2-FARM-003 | `03-farm-polygon-persistence.md` | Farm Model, Farmer -> Farm Relationship & PostGIS Polygon Persistence | Yedenekachew |
| EPIC-2-FARM-004 | `04-area-eudr-logic.md` | Area Calculation & EUDR Demonstration Flagging Logic | Yedenekachew |
| EPIC-2-FARM-005 | `05-frontend-farmer-registration.md` | Frontend Farmer Registration & List/Details View | Biniyam (+ Yedenekachew) |
| EPIC-2-FARM-006 | `06-frontend-farm-polygon-capture.md` | Frontend Farm Registration, Leaflet Polygon Capture & EUDR/Area Result Panel | Biniyam (+ Yedenekachew) |
| EPIC-2-FARM-007 | `07-epic2-verification.md` | EPIC 2 End-to-End Verification & EPIC 3 Handoff Readiness | Ephratha (+ Kidus) |
| EPIC-2-FARM-008 | `08-farm-list-lookup-api.md` | Farm List and Lookup API | Yedenekachew |

## Dependency Graph

```text
EPIC-1 (complete)
   |
   v
EPIC-2-FARM-001  (FIN generation utility + validation foundation;
   |               also depends on EPIC-0-DB-002 schema)
   v
EPIC-2-FARM-002  (Farmer registration/retrieval API;
   |               depends on FARM-001's FIN utility and
   |               EPIC-1's auth/RBAC mechanism)
   v
EPIC-2-FARM-003  (Farm model, Farmer->Farm FK, polygon persistence;
   |               depends on FARM-002 — a real Farmer must exist
   |               to attach a Farm to)
   v
EPIC-2-FARM-004  (Area calculation + EUDR demonstration flag;
   |               depends on FARM-003 — needs a persisted polygon
   |               to compute against)
   |
   +----------------------------+
   v                            v
EPIC-2-FARM-005              EPIC-2-FARM-006
(Frontend: Farmer reg +      (Frontend: Farm registration,
list/detail view;            Leaflet polygon capture,
depends on FARM-002's        area/EUDR result panel;
API contract only —          depends on FARM-003 AND
can start once FARM-002      FARM-004's API contracts)
merges, in parallel with
FARM-003/004 backend work)
   |                            |
   +-------------+--------------+
                 v
         EPIC-2-FARM-007
   (End-to-end verification;
    depends on FARM-001 through FARM-006)
```

## Parallelization Opportunities

- `EPIC-2-FARM-005` (frontend Farmer registration) depends only on
  `FARM-002`'s API contract, not on `FARM-003`/`FARM-004`. Once
  `FARM-002` is merged, `FARM-005` may proceed **in parallel** with
  `FARM-003` and `FARM-004`'s backend work — this is the one genuine
  parallelization opportunity in this epic, consistent with the request's
  instruction not to build frontend work against an undefined API
  contract (Farmer's contract is defined by `FARM-002`; Farm/polygon's is
  not defined until `FARM-003`/`FARM-004`).
- `FARM-006` cannot start meaningfully before `FARM-004` merges, since its
  result panel displays the EUDR flag that `FARM-004` computes — building
  it earlier against a guessed contract would violate the "no frontend
  work against an undefined API" instruction.
- No other EPIC-2 backend task can run in parallel with another: `FARM-001
  -> FARM-002 -> FARM-003 -> FARM-004` is a strict chain, because each
  step's data must exist for the next (FIN utility before Farmer API;
  a real Farmer before a Farm can reference one; a persisted polygon
  before area/EUDR logic has anything to compute against).

## EPIC-2 Completion Gate

EPIC 2 is not complete, and EPIC 3 must not begin, until **all** of the
following hold (mirroring `.agents/execution/07-task-completion-checklist.md`'s
EPIC-level sign-off):

- All seven tasks (`FARM-001`–`FARM-007`) report Definition of Done
  satisfied and are merged to `develop`.
- `FARM-007`'s end-to-end verification passes every criterion in its own
  Acceptance Criteria, exercising the full chain: **Authenticated user ->
  Register Farmer -> Retrieve Farmer -> Register Farm -> Capture Polygon ->
  Persist Polygon -> Calculate Area -> Evaluate/display EUDR demonstration
  status.**
- The FIN-format ambiguity flagged under `FARM-001` has been resolved by
  the Project Manager (or explicitly, formally accepted as a documented
  open item that does not block the demo) — an EPIC cannot be "complete"
  while its core identifier format is still undecided in a way that could
  require regenerating already-created test data.
- No item from any task's `Out of Scope` section was implemented.
- At least one complete Farmer -> Farm -> Polygon record exists in the
  local/demo database, created through the actual UI (not inserted
  directly), proving the chain works end to end for a human, not just for
  automated tests.

## Traceability Summary

```text
SRS
  Module 02: Farmer & Farm Polygon Registry (FR-FARM)
    FR-FARM-001 Farmer Master Profiling
    FR-FARM-002 Geolocation Farm Polygon Capture (EUDR Ready)
        |
        v
Design Document V1.0
    Section 4.2 Farmer & Polygon Registry
      (narrows FR-FARM-001's input list; narrows FR-FARM-002's EUDR
       check to a demonstration-scale substitute)
    Section 7.1/7.2 ERD and Entity Descriptions (Farmer, Farm — already
      built by EPIC-0-DB-002)
    Section 8 API Design — Farmers; Farms
    Section 9.2 Field / Registry Agent UI
    Section 13 Sequence 2, Sequence 3
        |
        v
Implementation Specification
    EPIC 2 — Farmer & Polygon Registry (backend/frontend task list,
      Definition of Done)
        |
        v
Minimum Project Plan V1.0
    Week 2 Key Activities: "begin Authentication & RBAC and Farmer &
      Polygon Registry (backend + frontend)"
    Milestone M4 (Working Increment Delivered, end of Week 3) — EPIC 2
      is one of the three core modules that must be integrated by M4,
      per the Minimum Project Plan's own scope statement ("Deliver the
      three core-scope modules: Authentication & RBAC, Farmer & Polygon
      Registry, Traceability & QR Engine")
    Section 7.3 Task Dependencies — confirms "Database schema...must
      exist before any API work starts" and the Auth -> Farmer ->
      Traceability ordering, consistent with the dependency graph above
        |
        v
EPIC-2 tasks (FARM-001 through FARM-007)
```

## Known Ambiguities (flagged, not resolved)

1. **FIN format conflict — genuinely blocking, not yet escalated.**
   The SRS states two different FIN formats in two different places:
   FR-FARM-001 (Module 02, functional requirement): *"Unique Farmer
   Identification Number (FIN - Format: ETH-FAR-XXXX-XXXXXX)"* — a 4-digit
   then 6-digit segment. UC-01 (Use Case, "Register Smallholder Farmer"):
   *"System generates FIN (ETH-FAR-XXX-XXXXXX)"* — a 3-digit then 6-digit
   segment. The Design Document does not restate a specific format at all
   (§4.2 only says a FIN is generated "per FR-FARM-001" and is unique).
   **This is not implementable safely without a decision.** `FARM-001`
   is written to stop at this exact point and escalate per
   `.agents/execution/06-failure-and-escalation.md`, rather than guessing
   between the two SRS-stated formats.

2. **RBAC role-list conflict (carried over from `.agents/execution/00-execution-overview.md`).**
   The frozen four-role model (Admin, ECTA Officer, Field/Registry Agent,
   Verifier) governs EPIC-2's RBAC requirements, per Design Document §8's
   explicit per-endpoint role columns. The Minimum Project Plan's own
   testing table uses a different, five-item role list including
   "Exporter," which does not exist in the Baseline/Design Document role
   model. This remains unresolved; `FARM-007`'s RBAC verification uses the
   frozen four-role model and restates this discrepancy, consistent with
   how `EPIC-1-AUTH-008` already handles it.

3. **Mapping library — practically settled for this epic's purposes, formal document conflict still open.**
   `.agents/execution/00-execution-overview.md` records an unresolved
   Level-3-vs-Level-3 conflict between the Baseline ("Leaflet /
   React-Leaflet" only) and the Minimum Project Plan ("Leaflet/Mapbox GL").
   This request's own Section 4 explicitly directs: *"Do NOT introduce:
   Mapbox GL... If an existing project decision explicitly resolves one of
   these, follow that decision."* `.agents/rules/02-tech-stack.md` is that
   explicit, already-frozen decision. **`FARM-006` therefore uses Leaflet /
   React-Leaflet only.** The underlying document-level discrepancy between
   the Baseline and the Minimum Project Plan is restated here for the
   record and is not resolved by this task set — only the practical
   implementation choice for EPIC 2 is settled, by the operative
   instruction and the frozen tech-stack rule, not by this task set
   adjudicating between two Level-3 documents.

4. **Area calculation method is not fully specified.**
   Design Document §4.2 states only that "area in hectares is computed
   server-side from the geometry" — it does not name a specific PostGIS
   function or method (e.g., planar `ST_Area` on the raw SRID-4326 geometry
   versus a geography-cast calculation that accounts for the earth's
   curvature). This is not treated as a blocking ambiguity of the same kind
   as the FIN format: `.agents/rules/02-tech-stack.md`'s allowance for
   "fulfilling an already-approved requirement" without separate change
   control applies here, since *that* area is computed is fixed and only
   *how* is open. `FARM-004` requires the chosen method to be explicitly
   recorded and justified in its `Expected Agent Report`, not silently
   picked.

## Explicit Out-of-Scope Items for EPIC 2

Per `.agents/rules/01-scope-boundaries.md` and Design Document §4.2/§19:

- Cherry collection / batch intake (SRS Module 03, FR-COLL) — a later,
  currently unplanned epic; not started under cover of Farmer/Farm work.
- Coffee Lot creation, Traceability events, or QR generation (EPIC 3/4) —
  EPIC 2 produces the Farmer/Farm/Polygon data those epics will consume;
  it does not begin building them.
- Any production/enterprise EUDR check against real forest-canopy datasets
  (Design Document §4.2 explicitly narrows this to a demonstration-scale
  substitute).
- SMS OTP phone-number verification (SRS FR-FARM-001's validation rule) —
  not part of the Design Document's narrowed V1.0 input list (§4.2: full
  name, national ID, gender, phone number, optional cooperative only); no
  OTP/telecom integration exists in V1.0 (Baseline §3.3).
- Photo capture of the National ID document, bank/Telebirr account
  details, household size, or cryptographic per-transaction signing (all
  present in SRS UC-01/FR-FARM-001 but not in the Design Document's
  narrowed §4.2 field list) — these are enterprise/UC-01-specific
  elaborations that the Design Document does not carry forward into V1.0.
- Offline/SQLite queuing of farmer registration (SRS UC-01's "Alternative
  Flow (Offline)") — no offline capability exists in V1.0 (Baseline §3.3:
  "Native offline Android application" is out of scope).
- Editing an existing Farm's polygon geometry — Design Document §8 defines
  `POST /api/v1/farms` (create) and `POST /api/v1/farms/{id}/validate`
  (re-run the EUDR check on the existing polygon) but no update/PUT
  endpoint for Farm; V1.0 does not support geometry editing after
  creation. (`Farmer` records, by contrast, do have a `PUT` endpoint per
  Design Document §8 and are updatable.)
- Cooperative & Processing Management as a full module (SRS Module 04) —
  only the lightweight `Cooperative` lookup table already created by
  `EPIC-0-DB-002` is used, exactly as Design Document §4.2 specifies.
- Mapbox GL or any mapping library other than Leaflet/React-Leaflet (see
  Known Ambiguity #3).

## Handoff Requirements to EPIC 3

For Traceability & Coffee Lot (EPIC 3) to begin, EPIC 2 must leave behind:

- At least one real, persisted `Farmer` record with a valid FIN (once the
  FIN-format ambiguity is resolved) reachable via
  `GET /api/v1/farmers/{id}`.
- At least one real, persisted `Farm` record with a valid PostGIS polygon,
  a computed `area_hectares`, and an `eudr_risk_flag` value, linked to that
  Farmer, reachable via `GET /api/v1/farms/{id}`.
- A stable, documented API contract for both (`FARM-002`'s Farmer contract
  and `FARM-003`/`FARM-004`'s Farm contract) that EPIC 3's `CoffeeLot`
  creation endpoint can reference by `farm_id`, per Design Document §5.1
  ("a Coffee Lot references exactly one originating Farm").
- Confirmation, from `FARM-007`, that no defect remains open against the
  Farmer or Farm creation/retrieval path that would block a Coffee Lot from
  correctly resolving its originating Farm.

## AI-Agent Execution Rules for EPIC 2

In addition to the global rules in `.agents/rules/` and the procedures in
`.agents/execution/` (all of which apply in full), an agent executing any
EPIC-2 task must not:

- Modify any EPIC-0 or EPIC-1 task file, any `.agents/rules/` file, any
  `.agents/execution/` file, or `.agents/README.md`.
- Modify the Baseline, Design Document, SRS, Implementation Specification,
  Implementation Playbook, or Minimum Project Plan.
- Modify `backend/` or `frontend/` source code except within the specific
  `Allowed Scope` of the EPIC-2 task currently being executed.
- Guess a FIN format to unblock `FARM-001` — the two conflicting SRS
  statements must be escalated, not silently picked between.
- Introduce Mapbox GL, Google Maps, or any mapping library other than
  Leaflet/React-Leaflet.
- Begin `FARM-003` before `FARM-002` is merged (no Farm without a real
  Farmer to attach it to), or begin `FARM-004` before `FARM-003` is merged
  (no area/EUDR computation without a persisted polygon to compute
  against).
- Begin any EPIC-3 (Traceability/Coffee Lot), EPIC-4 (QR), or stretch-epic
  work under cover of an EPIC-2 task.
- Build a second authentication or authorization mechanism instead of
  reusing `EPIC-1-AUTH-003`/`EPIC-1-AUTH-004` exactly as they exist.
