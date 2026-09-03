# EPIC-2 Farmer & Polygon Registry Verification

**Task ID:** EPIC-2-FARM-007  
**Verification date:** 2026-09-03  
**Branch:** `develop`

## Scope

This record covers the implemented V1.0 Farmer and Polygon Registry only:
Farmer FIN generation and registration, Farmer retrieval/search/update, Farm
geometry persistence, server-side area calculation, the demonstration-review
flag, and the corresponding React screens. It does not claim production EUDR
compliance, satellite/forest verification, or EPIC-3 functionality.

## Automated verification

| Check | Command | Result |
|---|---|---|
| Backend regression | `cd backend; .\\.venv\\Scripts\\python.exe -m unittest discover -s tests -v` | **PASS** — 56 tests in 152.740 seconds; final result `OK`; exit code 0. |
| Frontend lint | `cd frontend; npm.cmd run lint` | **PASS** — ESLint completed successfully. |
| Frontend production build | `cd frontend; npm.cmd run build` | **PASS** — Vite transformed 71 modules and completed successfully. |
| Frontend automated tests | `npm.cmd run` inspection | **NOT APPLICABLE** — no frontend test script is configured. |

The backend run includes Farmer FIN/API, Farm API, PostGIS schema, and
authentication/RBAC tests.

## API/Postman verification

The sanitized collection is stored at
[`EPIC-2.postman_collection.json`](../postman/EPIC-2.postman_collection.json).
It contains the implemented login, Farmer create/search/detail/update, Farm
polygon create/get/revalidate, point-plus-radius create, and unauthenticated/
read-only-role rejection workflows. It uses variables for URLs, credentials,
tokens, and returned identifiers; no credential, JWT, database URL, or private
connection value is stored.

**Execution status: NOT RUN.** No installed Postman-compatible runner was
available during this verification pass. The collection has therefore been
created and structurally reviewed, but no green Postman/Newman execution is
claimed. Run it against a local environment using synthetic credentials and
store no populated environment file in the repository.

## Manual UI verification

Established manual verification evidence confirms the following UI behavior:

1. An authorized Field/Registry Agent authenticated successfully.
2. The Farmer registry loads Farmer data; authorized users can create a
   Farmer, see the generated FIN, search/list it, and open its details.
3. The Farm registration page provides a Farmer selection flow and supports
   both polygon capture and point-plus-radius input.
4. Polygon mode requires six or more distinct vertices. Point mode requires a
   positive radius.
5. A Farm submission displays the backend-calculated area, the demonstration
   review flag, and the explicit demonstration-review label.
6. The revalidation action calls the implemented Farm validation endpoint.
7. Farm creation controls are limited to Admin and Field/Registry Agent;
   read-only roles do not receive those controls.

No screenshot artifact was supplied or fabricated for this record. A complete
single-session walkthrough that creates a new synthetic Farmer and both Farm
modes should still be captured before human EPIC sign-off.

## Database/PostGIS verification

Current automated Farm API/database evidence verifies:

- Persisted Farm geometry type is `POLYGON` and SRID is `4326`.
- A Farm persists with its required Farmer relationship.
- Polygon GeoJSON round-trips through creation and retrieval.
- `area_hectares` and `eudr_risk_flag` are populated after FARM-004 processing.
- Point-plus-radius input is persisted and returned as Polygon geometry.
- Area is calculated server-side from persisted geometry using
  `ST_Area(polygon_geom::geography) / 10000`.
- The V1.0 demonstration-review flag is `true` only for area greater than
  10 hectares, and `false` at or below 10 hectares; validation is idempotent.

These statements rely on the passing automated tests executed for this task;
this pass did not run a separate ad-hoc database query.

## Known decisions, warnings, and limitations

- **FIN format:** resolved by PD-002 as `ETH-FAR-XXXX-XXXXXX`.
- **RBAC role baseline:** Admin, ECTA Officer, Field/Registry Agent, and
  Verifier. The older Exporter mention remains a documented source
  inconsistency, not an implemented role.
- **Mapping:** Leaflet/React-Leaflet is the approved and implemented choice.
- **Area rule:** PD-005 approves PostGIS geography semantics and the local,
  demonstration-only 10-hectare review threshold.
- The backend emitted a non-fatal `python-dotenv` parse warning for `.env`
  line 14 during tests. It did not prevent the passing regression run and was
  not changed by this verification task.
- Postman/Newman execution remains outstanding because no compatible runner
  was available. This is the only outstanding automated API-evidence item.

## Scope boundaries

No application behavior was changed. No external EUDR, forest, satellite,
deforestation, or network compliance service was introduced. No EPIC-3 work
was started. This record contains no real Farmer PII, credentials, tokens, or
database connection strings.

## Final EPIC-2 verification status

**INCOMPLETE.** Implementation, backend regression, frontend lint/build,
manual UI evidence, and automated PostGIS evidence are passing. EPIC-2 cannot
be signed off, and EPIC-3 must not begin, until the sanitized Postman
collection is executed successfully against a local synthetic environment and
the resulting status is recorded here. A final consolidated UI walkthrough
artifact is also recommended for human sign-off.
