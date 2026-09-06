# EPIC-5 FE-006 Farm/Polygon Reconciliation

**Task:** EPIC-5-FE-006 — Farm, Polygon Registration, and Farm Detail
Frontend

**Status:** COMPLETED — satisfied by existing verified implementation

## Reconciliation result

FE-006 overlaps the Farm frontend delivered by `EPIC-2-FARM-006` in commit
`9252768`. The current `/farms` screen is the existing immediate
registration/result surface: it captures a Farm, renders the returned Farm
result, and exposes the documented re-validation action. No separate Farm
list/detail endpoint or geometry-edit API is required by the accepted
FARM-006 screen contract, so none is invented here.

Since FARM-006, `api/farms.js` has only received FE-003's shared expired
session handling. The map, geometry serialization, fallback mode, response
display, re-validation, and role rules have not materially changed.

## Existing contract and implementation

| Capability | Existing implementation / contract |
| --- | --- |
| Farmer association | `FarmRegistration.jsx` loads the authenticated Farmer collection and submits the selected documented `farmer_id`. |
| Polygon capture | React-Leaflet `MapContainer`, `TileLayer`, `Polygon`, and `useMapEvents` collect `[longitude, latitude]` coordinates and submit a closed GeoJSON `Polygon` ring. |
| Small-plot fallback | Point mode submits GeoJSON `Point` coordinates plus positive `radius_meters`, matching the approved Farm API fallback. |
| Farm creation | `createFarm` calls authenticated `POST /api/v1/farms` using the existing API helper. |
| Result/re-validation | The immediate result panel renders returned Farm ID, server-calculated hectares, demonstration review flag, and `eudr_check_type`; `validateFarm` calls `POST /api/v1/farms/{id}/validate` and replaces the result with the returned response. |
| Session/RBAC | The existing protected route/auth shell is reused; submit controls are available only to Admin and Field/Registry Agent. FE-003 handles `401` expiry and bounded retained-session `403`. |

`frontend/package.json` contains `leaflet` and `react-leaflet`; no Mapbox or
other mapping library is present.

## Acceptance matrix

| FE-006 criterion | Status | Evidence |
| --- | --- | --- |
| Authorized user selects a Farmer, submits valid Leaflet polygon, and sees returned Farm/area/demonstration information | ALREADY SATISFIED | **REUSED FROM PRIOR VERIFIED IMPLEMENTATION:** `EPIC-2-verification.md` records the Farmer selection, polygon registration, backend-calculated area, flag, and visible demonstration-review label. |
| Point-plus-radius fallback works | ALREADY SATISFIED | **REUSED FROM PRIOR VERIFIED IMPLEMENTATION:** EPIC-2 manual evidence and successful sanitized Postman/Newman run cover point-plus-radius Farm creation. |
| Invalid geometry and API failures are controlled | ALREADY SATISFIED | `FarmRegistration.jsx` blocks missing Farmer, fewer than six polygon points, absent point, and invalid radius with visible controlled messages; existing Farm API/Postman evidence covers structured API errors, `401`, and `403`. |
| Farm result matches approved API response; no unapproved mapping technology | ALREADY SATISFIED | Result panel consumes the create/validate response fields. Source imports React-Leaflet/Leaflet only; no Mapbox package or source import exists. |
| No unsupported geometry edit or production EUDR behavior | ALREADY SATISFIED | No geometry update route/control exists. The UI renders the response-provided `eudr_check_type` and calls the flag a “Demonstration review flag.” |
| Protected-session behavior and role restriction | ALREADY SATISFIED | `App.jsx` protects `/farms`; the page limits creation to Admin/Field/Registry Agent. **REUSED FROM PRIOR VERIFIED IMPLEMENTATION:** completed FE-003 browser evidence verifies the shared session/RBAC behavior. |
| Frontend lint | PASS | `npm.cmd run lint` completed successfully. |
| Frontend production build | PASS | `npm.cmd run build` completed successfully. |
| Whitespace check | PASS | `git diff --check` completed with no whitespace errors. |

## Reused implementation

- `frontend/src/pages/FarmRegistration.jsx`
- `frontend/src/api/farms.js`
- `frontend/src/api/farmers.js`
- `frontend/src/App.jsx`
- `frontend/src/components/navigationItems.js`
- Existing AuthContext, protected route, Leaflet, and React-Leaflet setup

## Reused committed evidence

- [EPIC-2 verification](EPIC-2-verification.md): manual UI evidence for
  Farmer selection, polygon and point-radius paths, server-calculated area,
  demonstration flag/label, re-validation, and role-gated controls.
- The sanitized `docs/testing/postman/EPIC-2.postman_collection.json` and its
  recorded Newman execution: polygon creation/retrieval/revalidation,
  point-radius creation, and `401`/`403` rejection workflows.
- EPIC-2 backend/PostGIS regression evidence: closed GeoJSON persistence,
  server-side area calculation, idempotent re-validation, and the
  demonstration-only threshold behavior.
- [FE-003 reconciliation](EPIC-5-FE-003-protected-routes-role-navigation-reconciliation.md): completed browser evidence for protected routes, expiry cleanup, and controlled `403` behavior.

## Source changes

None for FE-006. No backend geometry/PostGIS logic, EUDR rule, mapping
library, API contract, geometry editing, or Coffee Lot functionality changed.

## Browser-evidence decision

**NO NEW BROWSER VERIFICATION REQUIRED.** Every FE-006 acceptance criterion
is demonstrated by current source inspection, passing frontend checks, and the
valid committed FARM-006/EPIC-2 and FE-003 evidence above. No browser result
is represented as newly collected for FE-006.

No credentials, JWTs, secrets, local environment values, Farmer PII, or raw
geometry coordinates are included in this evidence file.
