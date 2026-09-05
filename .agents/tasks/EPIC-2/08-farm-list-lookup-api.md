# Task Title

Farm List and Lookup API

## Task ID

EPIC-2-FARM-008

## Purpose

Provide the authenticated Farm collection lookup required by
`EPIC-3-TRACE-005` to select an existing Farm before creating a Coffee Lot.

## Classification

Required dependency. TRACE-005 already requires a Farm selector that reuses
an existing Farm list or lookup capability; the implemented EPIC-2 Farm API
only exposes retrieval by a known Farm ID.

## Scope

- Add `GET /api/v1/farms`, protected by the existing JWT authentication
  dependency used by `GET /api/v1/farms/{farm_id}`.
- Optionally filter results by the existing `farmer_id` relationship using
  `?farmer_id=<positive integer>`.
- Return the existing `FarmResponse` shape for each Farm, including the
  persisted GeoJSON Polygon, area, and demonstration EUDR fields.
- Return an empty list when the authenticated caller has no matching Farms.

## Out of Scope

- Farm creation, update, deletion, validation, geometry calculation, or EUDR
  business-logic changes.
- A new authorization model, frontend work, or TRACE-005 implementation.

## Contract

`GET /api/v1/farms?farmer_id=<optional positive integer>`

- Authentication: required; all authenticated roles follow the established
  Farm retrieval convention.
- Success: `200` and `FarmResponse[]`, ordered by `farm_id`.
- Invalid `farmer_id`: structured `400` validation response.
- Unauthenticated: `401`.

## Acceptance Criteria

- An authenticated caller can list existing Farms without supplying a Farm ID.
- `farmer_id` returns only Farms belonging to that Farmer.
- Returned items follow the existing `FarmResponse` convention.
- Unauthenticated requests are rejected.
- Existing Farm endpoints and focused regression tests continue to pass.

## Verification

- Focused Farm API tests for list, filter, authentication, and existing
  endpoint regression.
- Python compilation, full backend regression, Alembic current, and
  `git diff --check`.
