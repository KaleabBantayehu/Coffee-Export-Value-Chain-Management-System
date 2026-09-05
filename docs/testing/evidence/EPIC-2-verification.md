# EPIC-2 Farmer & Polygon Registry Verification

**Task ID:** EPIC-2-FARM-007  
**Verification date:** 2026-09-04  
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

**Execution status: PASS.**

The collection was executed successfully against the local backend using
Newman 6.2.2 and a local, non-committed environment file containing synthetic
test credentials.

Command:

`newman run .\docs\testing\postman\EPIC-2.postman_collection.json -e .\docs\testing\postman\EPIC-2.local.postman_environment.json`

Result:

- Iterations: 1
- Requests: 11
- Failed requests: 0
- Test scripts: 11
- Pre-request scripts: 0
- Assertions: 11
- Failed assertions: 0
- Total run duration: approximately 6 seconds
- Exit code: 0

The successful execution verified:

1. Authorized authentication.
2. Farmer creation and FIN capture.
3. Farmer search.
4. Farmer detail retrieval.
5. Farmer update.
6. Six-vertex Polygon Farm creation.
7. Polygon Farm retrieval.
8. Polygon Farm revalidation.
9. Point-plus-radius Farm creation.
10. Unauthenticated Farm creation rejection with HTTP 401.
11. Read-only role Farm creation rejection with HTTP 403.

The local environment file used for execution contains local credentials and/or
tokens and is not committed to the repository.

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
modes remains recommended for final human EPIC sign-off, but it is not an
outstanding automated API verification failure.

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
- Postman/Newman API verification passed successfully using Newman 6.2.2.
  The run completed 11 requests and 11 assertions with 0 failures and exit
  code 0.
- The local Postman/Newman environment file used during execution is not
  committed because it contains local credential/token configuration.

## Scope boundaries

No application behavior was changed. No external EUDR, forest, satellite,
deforestation, or network compliance service was introduced. No EPIC-3 work
was started. This record contains no real Farmer PII, credentials, tokens, or
database connection strings.

## Final EPIC-2 verification status

**VERIFICATION COMPLETE — READY FOR HUMAN SIGN-OFF.**

The implemented EPIC-2 Farmer and Polygon Registry has passed:

- Backend regression testing.
- Frontend lint verification.
- Frontend production build verification.
- Automated Farm/PostGIS database verification.
- Sanitized Postman/Newman API verification.
- Established manual UI verification.

The Newman collection completed successfully with 11 requests and 11 assertions
passing, 0 failures, and exit code 0.

A consolidated single-session UI walkthrough or screenshot artifact remains
recommended for final human review, but no outstanding automated verification
blocker remains.

No production EUDR compliance, satellite verification, forest verification,
or external compliance service is claimed by this EPIC.
