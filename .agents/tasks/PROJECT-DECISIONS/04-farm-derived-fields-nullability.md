# Project Decision: FARM-003 Derived Field Nullability

## Decision ID

PROJECT-DECISION-04

## Related Tasks

* EPIC-2-FARM-003 — Farm Model, Farmer → Farm Relationship & PostGIS Polygon Persistence
* EPIC-2-FARM-004 — Area & EUDR Logic

## Status

APPROVED

## Decision

The Farm fields `area_hectares` and `eudr_risk_flag` shall be nullable.

During FARM-003, these fields must remain unset (`NULL`) when a Farm is initially created.

FARM-003 must not populate these fields with placeholder or sentinel business values.

FARM-004 is responsible for calculating and populating both values.

## Required Database Change

The database schema and ORM model must permit:

* `area_hectares = NULL`
* `eudr_risk_flag = NULL`

A database migration shall change both existing columns from non-nullable to nullable.

The corresponding ORM model shall also declare both fields as nullable.

## FARM-003 Contract

When a Farm is created in FARM-003:

* Farm identity and farmer relationship are persisted.
* Geometry is persisted according to the approved FARM-003 polygon validation contract.
* `area_hectares` remains `NULL`.
* `eudr_risk_flag` remains `NULL`.

FARM-003 must not:

* Calculate polygon area.
* Infer farm area from point-plus-radius data.
* Assign `0` as a placeholder area.
* Assign `false` as a placeholder EUDR result.

## FARM-004 Responsibility

FARM-004 owns:

1. Geometry area calculation.
2. Conversion of the calculated area into hectares.
3. Application of EUDR-related business rules.
4. Population of `area_hectares`.
5. Population of `eudr_risk_flag`.

Once FARM-004 completes the required calculation and evaluation, the previously unset Farm fields may be populated with their actual business values.

## Rationale

A `NULL` value represents that the area and EUDR evaluation have not yet been calculated.

Using `0` for `area_hectares` or `false` for `eudr_risk_flag` would incorrectly represent unknown or unprocessed information as a valid business result.

Making the fields nullable preserves the dependency boundary between FARM-003 and FARM-004 and allows FARM-003 to persist Farm records without prematurely implementing FARM-004 logic.

## Impacted Components

* `backend/app/db/models.py`
* Existing Farm database schema
* Alembic migration history
* EPIC-2-FARM-003
* EPIC-2-FARM-004

## Implementation Instruction

FARM-003 may proceed with the following persistence rule:

* Newly created Farm records may have `area_hectares = NULL`.
* Newly created Farm records may have `eudr_risk_flag = NULL`.
* A migration must make both columns nullable.
* The ORM model must reflect the nullable database contract.
* FARM-004 will populate both fields with calculated business values.

## Final Authority

This decision resolves the FARM-003 persistence conflict between the required EPIC sequencing and the existing non-null database schema.
