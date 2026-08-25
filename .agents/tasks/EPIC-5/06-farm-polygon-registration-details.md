# EPIC-5-FE-006 - Farm, Polygon Registration, and Farm Detail Frontend

## Objective

Integrate Farm registration/detail and approved Leaflet/React-Leaflet polygon capture with the verified EPIC-2 contracts.

## Scope

Provide the Farm form, Farmer association, interactive polygon capture using Leaflet/React-Leaflet, documented small-plot fallback if present in the verified contract, submit behavior, and display of returned area/EUDR demonstration status and farm details.

## Out of Scope

PostGIS/backend geometry logic, Mapbox or another map library, polygon editing if no API exists, production EUDR checks, GPS/IoT, offline/mobile capture, or schema/API changes.

## Preconditions

FE-001/003 and FE-005 Farmer selection capability available; EPIC-2-FARM-003/004/006/007 implemented, tested, verified, approved; Leaflet contract inspected.

## Dependencies

FE-001/003/005; EPIC-2-FARM-002/003/004/006/007; EPIC-1 auth. The documented Level-3 mapping conflict remains operationally governed by Leaflet/React-Leaflet.

## Inputs

Verified Farm request/response shape, polygon coordinate contract, area/EUDR fields, Farmer IDs, synthetic data, Design Document Sections 4.2, 8, 9.2, 13.

## Expected Outputs

Working Farm/polygon form and detail/result display consuming actual API data.

## Relevant Files / Modules

Existing `frontend/src` map/farm components/API clients and Leaflet setup. Reuse EPIC-2 components when present.

## Backend Responsibilities

None.

## Frontend Responsibilities

Map interaction, coordinate capture/serialization exactly as documented, Farmer selection, submit, result panel, validation, and states.

## Database Responsibilities

None; no direct PostGIS access.

## API Requirements

Call only inspected Farm create/detail/validate APIs and fields. Do not invent update geometry or validation endpoints.

## UI / UX Requirements

Map remains usable and stable; display computed area and clearly labeled demonstration EUDR status; preserve approved fallback behavior only if actually documented.

## Security Requirements

Protected registration/details use existing auth/RBAC; do not expose Farmer PII or raw geometry on public pages; safely handle map/API input.

## Validation / Error Handling

Reject missing Farmer/geometry according to contract; handle invalid polygon/backend errors, 401/403, and network failures without blank UI.

## Acceptance Criteria

- Authorized user can select the documented Farmer, capture a valid polygon with Leaflet/React-Leaflet, submit, and see returned farm/area/EUDR information.
- Invalid geometry and API failures show controlled errors.
- Farm details match the API response; no Mapbox or new mapping technology is introduced.
- No unsupported polygon-edit or production EUDR behavior is added.

## Testing Requirements

Test/manual evidence for valid polygon, documented fallback if applicable, invalid/missing geometry, 401/403, API/network errors, area/EUDR display, and mobile/desktop map usability; run build/lint and EPIC-2 regression tests.

## Traceability

SRS FR-FARM-001/002; Design Document Sections 4.2, 7.2, 8, 9.2, 13; Implementation Specification EPIC-2 frontend tasks and EPIC-5 Farm/Polygon screen; Minimum Project Plan Sections 7.1-7.2; Baseline Sections 2-4; EPIC-2-FARM-003/004/006/007.

## Ownership, Git, and Change Control

Primary: Biniyam; Abel support; Yedenekachew supports contract seam. Verification: Ephratha; Kidus documentation. Branch `feature/EPIC-5-FE-006-farm-polygon`; commit `feat(frontend): integrate farm polygon workflow`; PR to `develop`. Mapping deviations require change control.

## Blockers / Stop Conditions

Stop if polygon serialization, map choice, or Farm response is unresolved. Do not introduce Mapbox or modify EPIC-2.
