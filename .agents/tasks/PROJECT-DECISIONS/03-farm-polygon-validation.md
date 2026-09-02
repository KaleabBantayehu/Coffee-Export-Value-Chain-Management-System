# Project Decision: FARM-003 Polygon Validation Contract

## Decision ID

PROJECT-DECISION-03

## Related Task

EPIC-2-FARM-003 — Farm Model, Farmer → Farm Relationship & PostGIS Polygon Persistence

## Status

APPROVED

## Decision

For CEVCMS V1.0, FARM-003 polygon submissions must contain a minimum of six vertices.

The six-vertex minimum is applied at the FARM-003 geometry validation boundary and does not depend on calculating the polygon's area.

FARM-003 must not calculate polygon area in order to determine whether a polygon qualifies for a reduced vertex requirement.

For small or irregular plots that cannot reasonably be represented through a six-or-more-vertex polygon, the supported point-plus-radius mode is the alternative submission method.

## Validation Contract

### Polygon mode

A polygon submission must:

1. Provide a valid polygon geometry.
2. Contain at least six vertices, excluding any repeated closing coordinate if the geometry representation includes one.
3. Be structurally valid for persistence as a PostGIS polygon.

A polygon with fewer than six vertices must be rejected.

### Point-plus-radius mode

Point-plus-radius mode is permitted as the alternative representation for plots where polygon capture is not appropriate.

The request must provide the required center point and radius fields defined by the FARM-003 API contract.

The six-vertex polygon requirement does not apply to point-plus-radius submissions.

## Relationship to the 4,000 m² Requirement

The SRS requirement referring to plots over 4,000 m² does not require FARM-003 to calculate polygon area during request validation.

Area calculation and area-dependent EUDR/business logic remain the responsibility of:

EPIC-2-FARM-004 — Area & EUDR Logic.

FARM-003 is responsible only for geometry validation and persistence.

## Rationale

This decision preserves the EPIC dependency boundary.

FARM-003 establishes and persists farm geometry.

FARM-004 calculates and evaluates area.

Requiring FARM-003 to calculate area before geometry persistence would duplicate or prematurely implement FARM-004 responsibilities.

Applying a universal six-vertex minimum to polygon submissions provides an unambiguous API validation contract while preserving point-plus-radius mode as the alternative for small plots.

## Impacted Requirements

* EPIC-2-FARM-003 — Farm Polygon Persistence
* SRS FR-FARM-002
* EPIC-2-FARM-004 — Area & EUDR Logic

## Implementation Instruction

FARM-003 may proceed using the following rule:

* Polygon mode: minimum six vertices.
* Point-plus-radius mode: permitted alternative mode.
* FARM-003: no area calculation for determining vertex requirements.
* FARM-004: owns polygon area calculation and area-dependent EUDR logic.

## Final Authority

This project decision resolves the FARM-003 validation ambiguity for CEVCMS V1.0.
