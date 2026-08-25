# Task Title

Initial Database Migration / Schema — Core Entities

## Task ID

EPIC-0-DB-002

## Epic

EPIC 0 — Project Infrastructure

## Owner

Yedenekachew (Database Lead), per Baseline §5, with review from Kaleab
(Auth/RBAC entities) and Fistum (Traceability/QR entities, once his module
begins — schema only, not logic, is created here).

## Status

Not started (blocked until `EPIC-0-DB-001` is complete).

## Priority

Critical. This is the last EPIC 0 task; the core feature epics (EPIC 1–4)
cannot begin until this schema exists.

## Objective

Create the initial database schema and first migration for exactly the core
entities required by the V1.0 core-chain acceptance workflow
(`01-scope-boundaries.md`), derived from the Design Document's Version 1.0
Entity Relationship Diagram — **not** the SRS's full enterprise schema, and
**not** including stretch-module entities.

## Why This Task Exists

Design Document §7 states explicitly: "Only entities required by the core
scope, plus minimal stubs required for the stretch scope's foreign keys, are
included — the full enterprise schema (SRS §7.2) is not copied wholesale."
This task implements exactly that narrowed schema, no more and no less.

## Authoritative Sources

- Design Document §7.1 (Entity Relationship Diagram — Version 1.0 core
  scope)
- Design Document §7.2 (Entity Descriptions table — authoritative source for
  every field listed below)
- Project Baseline & Scope Freeze §3.1 (Core Scope) and §3.2 (Stretch —
  governs which entities are deferred)
- Implementation Specification (EPIC 2 "Farmer & Polygon Registry", EPIC 3
  "Traceability Engine", EPIC 4 "Dynamic QR Engine" — confirms which
  entities each later epic will need, without this task implementing that
  epic's logic)

## Requirements Traceability

- `Role`, `Permission`, `User` — Design Document §7.2; supports FR-AUTH-001
  (SRS) and Baseline §3.1 "Authentication and RBAC," to be implemented by
  EPIC 1. This task creates only the tables, not the auth logic.
- `Cooperative` — Design Document §7.2, "lightweight lookup so a Farmer can
  reference an affiliated cooperative," consistent with SRS's
  `tbl_farmers.cooperative_id` foreign key referenced in Design Document
  §4.2. Full Cooperative & Processing Management (SRS MOD-04) is **not**
  implemented — only this minimal lookup table.
- `Farmer`, `Farm` — Design Document §7.2; supports FR-FARM-001 and
  FR-FARM-002 (SRS), to be implemented by EPIC 2.
- `CoffeeLot`, `TraceabilityEvent`, `QRRecord` — Design Document §7.2;
  supports FR-TRACE-001/002 (SRS), to be implemented by EPIC 3 and EPIC 4.
- `AuditLog` — Design Document §7.2, scaled-down implementation of SEC-05
  (SRS); cross-cutting, used by multiple later modules.
- **Explicitly deferred, not created by this task:** `QualityCertificate`,
  `Waybill`, `ExportContract` — these are stretch-scope stub entities per
  Design Document §7.1/§7.2. Per Baseline §3.2 and `01-scope-boundaries.md`,
  stretch work has not started; creating their tables now would pre-build
  structure for work that may never be reached and is explicitly deferred
  until the stretch epics (EPIC 7/EPIC 8) are actually started, at which
  point a follow-up migration adds them.

## Dependencies

- `EPIC-0-DB-001` must be complete (working PostgreSQL/PostGIS connection).

## Preconditions

- Confirm the database connection from `EPIC-0-DB-001` is functioning
  (re-run its verification mechanism) before creating any table.

## Allowed Scope

- Defining SQLAlchemy models for exactly the ten core entities listed below.
- Creating the initial migration that creates these tables, their columns,
  primary/foreign keys, and the uniqueness/PostGIS constraints specified in
  Design Document §7.2.
- Configuring a migration tool consistent with the confirmed environment
  (SQLAlchemy 2.0.51) — if a migration tool is not yet chosen, choose the
  standard, well-established option for SQLAlchemy-based FastAPI projects
  and record the choice in the `Expected Agent Report`, per
  `02-tech-stack.md`'s allowance for fulfilling an already-approved
  requirement without separate change control.
- Applying the migration to the local development database and confirming
  the tables exist as specified.

## Files/Directories in Scope

- The models module scaffolded (empty) in `EPIC-0-BE-001`.
- A new migrations directory/configuration.
- Backend configuration, only if needed to register the migration tool.

Do not touch API routes, schemas (Pydantic request/response models), or
service/business logic — this task creates the persistence layer only. No
endpoint reads or writes to these tables yet; that begins in EPIC 1–4.

## Technical Requirements

Entities to create, with fields as specified in Design Document §7.2 (field
lists below are the authoritative set — do not add speculative columns):

| Entity | Key Attributes | Relationships |
|---|---|---|
| `Role` | `role_id` (PK), `role_name`, `description` | 1:N to `User` |
| `Permission` | `permission_id` (PK), `permission_code`, `description` | N:M to `Role` (via a `RolePermission` join table) |
| `User` | `user_id` (PK), `username`, `password_hash`, `full_name`, `role_id` (FK), `is_active`, `created_at` | N:1 to `Role`; 1:N to `AuditLog` |
| `Cooperative` | `cooperative_id` (PK), `name`, `region` | 1:N to `Farmer` |
| `Farmer` | `farmer_id` (PK), `fin_code` (unique), `full_name`, `national_id` (unique), `gender`, `phone_number`, `cooperative_id` (FK, nullable), `created_at` | 1:N to `Farm` |
| `Farm` | `farm_id` (PK), `farmer_id` (FK), `polygon_geom` (PostGIS `Polygon`, SRID 4326), `area_hectares`, `eudr_risk_flag`, `created_at` | N:1 to `Farmer`; 1:N to `CoffeeLot` |
| `CoffeeLot` | `lot_id` (PK), `gin_code` (unique), `farm_id` (FK), `created_by` (FK to `User`), `status`, `created_at` | N:1 to `Farm`; 1:N to `TraceabilityEvent`, `QRRecord` |
| `TraceabilityEvent` | `event_id` (PK), `lot_id` (FK), `event_type`, `event_timestamp`, `recorded_by` (FK to `User`), `notes` | N:1 to `CoffeeLot`; append-only (no update/delete operation is exposed at the API layer in later epics — this task just ensures the table has no soft-delete/versioning columns that would suggest otherwise) |
| `QRRecord` | `qr_id` (PK), `lot_id` (FK), `payload_hash`, `hmac_signature`, `verification_url`, `generated_at` | N:1 to `CoffeeLot` |
| `AuditLog` | `audit_id` (PK), `user_id` (FK), `action`, `entity_type`, `entity_id`, `old_value`, `new_value`, `timestamp` | N:1 to `User` |

- `Farm.polygon_geom` uses the PostGIS `GEOMETRY(Polygon, 4326)` type, per
  Design Document §4.2 and §7.1 — never a plain latitude/longitude text
  field (this is a Design Document requirement, restated in Implementation
  Playbook §8, not a style preference).
- `fin_code` and `national_id` on `Farmer`, and `gin_code` on `CoffeeLot`,
  are enforced unique at the database level, per Design Document §4.2/§5.2.
- Foreign keys are enforced at the database level (not application-only),
  consistent with Design Document §14's reliance on "database constraints
  (foreign keys, uniqueness)" for data integrity in place of enterprise
  column-level encryption.

## Implementation Steps

1. Confirm preconditions.
2. Define SQLAlchemy models for the ten entities above, matching field names
   and types from the table.
3. Configure the migration tool.
4. Generate the initial migration from the models.
5. Review the generated migration for correctness: correct PostGIS column
   type, correct uniqueness constraints, correct foreign keys.
6. Apply the migration to the local development database.
7. Verify all ten tables exist with the expected columns and constraints.
8. Confirm no stretch-module tables were created (see "Requirements
   Traceability," deferred entities).
9. Follow the per-feature workflow in `04-git-workflow.md`.

## Acceptance Criteria

- All ten core tables listed above exist in the local development database
  after running the migration.
- `Farm.polygon_geom` is a PostGIS geometry column, verified by inspecting
  the column type in the database (not just the model definition).
- `Farmer.fin_code`, `Farmer.national_id`, and `CoffeeLot.gin_code` have
  database-level uniqueness constraints, verified by attempting a duplicate
  insert and observing a database-level rejection.
- All foreign keys listed in the table above exist and are enforced,
  verified by attempting an insert with a non-existent foreign key and
  observing a database-level rejection.
- No table for `QualityCertificate`, `Waybill`, or `ExportContract` exists
  as a result of this task.
- The migration can be run against a fresh, empty database and succeeds
  without manual intervention.

## Testing Requirements

Per `05-testing-rules.md`:

- At least one test/verification confirms the migration applies cleanly to
  an empty database.
- At least one test confirms the PostGIS geometry column on `Farm` accepts
  a valid polygon and rejects invalid geometry input, at the database
  constraint level or via a minimal model-level check.
- At least one test confirms each of the three explicit uniqueness
  constraints (`fin_code`, `national_id`, `gin_code`) rejects a duplicate.
- At least one test confirms a foreign-key violation is rejected (e.g.,
  creating a `Farm` referencing a non-existent `farmer_id`).

## Security Requirements

- No seed data containing real farmer, financial, or personal information
  is included in the migration — per Baseline §3.3 and
  `01-scope-boundaries.md` ("no real farmer or live financial data").
- If any demonstration/seed data is added for local testing convenience, it
  must be clearly synthetic and not committed as part of this task without
  being explicitly labeled as such — synthetic seed data itself is only
  in scope if a later task calls for it; if added here for convenience, it
  must be flagged in the `Expected Agent Report`, not silently included.

## Error Handling Requirements

- Running the migration against a database that lacks the PostGIS extension
  produces a clear, actionable error rather than a partial/inconsistent
  schema state.
- Re-running the migration on an already-migrated database is safe (does
  not error or duplicate tables), consistent with standard migration-tool
  behavior.

## Out of Scope

- `QualityCertificate`, `Waybill`, `ExportContract` tables (stretch scope;
  deferred — see Requirements Traceability).
- Any API endpoint, schema (Pydantic), or service logic that reads or writes
  these tables (EPIC 1–4).
- Column-level encryption of PII (explicitly deferred to hosting-provider
  defaults per Design Document §14 — not built in V1.0).
- Any seed/demo data population beyond what is explicitly flagged as
  synthetic and minimal for local verification.

## Definition of Done

- All items in "Acceptance Criteria" are true and independently verifiable.
- All items in "Testing Requirements" pass.
- Reviewed and approved by at least one other team member.
- Merged into `develop`.
- Requirements-traceability entries updated (Kidus) for each entity, noting
  "schema created, logic pending" against the relevant FR-xxx identifiers.

## Git Requirements

- Branch: `feature/db-initial-schema`, from `develop`.
- Commit style: `feat(db): add initial core schema migration`.
- PR references Task ID `EPIC-0-DB-002`, lists the ten entities created, and
  explicitly confirms the three stretch-stub entities were not created.
- Merge target: `develop`.

## Expected Agent Report

On completion, report:

1. The migration tool chosen (if not already fixed by an earlier task) and
   why, per the allowance in `02-tech-stack.md`.
2. The full list of tables created, cross-checked one-to-one against the
   ten entities in this task's table.
3. Explicit confirmation that `QualityCertificate`, `Waybill`, and
   `ExportContract` were not created.
4. How the PostGIS geometry column, uniqueness constraints, and foreign
   keys were verified (commands/queries used).
5. Whether any seed/demo data was added, and if so, confirmation it is
   synthetic and clearly labeled.
6. Any point where a requirement was unclear or untraceable to a source
   document, and how it was handled.
7. Test results.
