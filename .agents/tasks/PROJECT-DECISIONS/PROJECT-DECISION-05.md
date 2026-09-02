# PROJECT-DECISION-05 — FARM-004 EUDR Demonstration Flagging Rule

## Decision

For CEVCMS V1.0, the EUDR-related Farm validation result shall be implemented as a **demonstration review flag**, not as a production EUDR compliance determination.

The system shall use a deterministic local area threshold.

### Demonstration Rule

A Farm shall receive:

* `eudr_risk_flag = true` when the calculated Farm area is **greater than 10 hectares**.
* `eudr_risk_flag = false` when the calculated Farm area is **less than or equal to 10 hectares**.

The threshold is a demonstration-only business rule selected for the V1.0 prototype. It does not represent an official EUDR threshold, legal requirement, deforestation determination, forest-canopy analysis, or production compliance decision.

## Area Calculation

Farm area shall be calculated server-side from the persisted `polygon_geom`.

The calculation shall use PostGIS geography semantics:

`ST_Area(polygon_geom::geography) / 10000`

This produces area in hectares and avoids using raw SRID 4326 geometry area in square degrees.

The calculation applies identically to:

* Polygon-mode Farms.
* Point-plus-radius Farms, because FARM-003 persists both modes as Polygon geometries.

## Creation-Time Behavior

When a Farm is created:

1. The geometry is validated according to FARM-003 rules.
2. The Farm geometry is persisted.
3. The Farm area is calculated from the persisted Polygon geometry.
4. `area_hectares` is populated.
5. The demonstration review flag is calculated.
6. `eudr_risk_flag` is populated before the API response is returned.

## Validation Endpoint

FARM-004 shall provide:

`POST /api/v1/farms/{id}/validate`

The endpoint shall:

1. Retrieve the existing Farm.
2. Recalculate the area from the stored geometry.
3. Recalculate the demonstration review flag using the same 10-hectare rule.
4. Persist the calculated values.
5. Return the updated validation result.

Repeated validation requests with unchanged geometry must produce the same persisted values.

## API Labeling

Responses exposing the EUDR-related result must clearly communicate that it is a demonstration check.

The implementation must not claim:

* Production EUDR compliance.
* Deforestation verification.
* Forest monitoring.
* Satellite verification.
* Legal certification.

## Out of Scope

FARM-004 shall not:

* Call external forest, satellite, canopy, or deforestation services.
* Introduce production EUDR compliance logic.
* Add Farm update or delete functionality.
* Implement FARM-005 or FARM-006 functionality.

## Rationale

A deterministic area threshold provides a reproducible and testable demonstration rule without fabricating geographic restricted-zone data or making external network calls.

This decision resolves the FARM-004 blocking dependency.
