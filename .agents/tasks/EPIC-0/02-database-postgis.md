# Task Title

PostgreSQL/PostGIS Configuration

## Task ID

EPIC-0-DB-001

## Epic

EPIC 0 — Project Infrastructure

## Owner

Yedenekachew (Database Lead), per Baseline §5 ("Owns the database schema and
the Farmer & Polygon Registry backend"), in coordination with Kaleab
(repository/infrastructure owner).

## Status

Not started (blocked until `EPIC-0-BE-001` is complete).

## Priority

Critical. Every module that persists data (Farmer, Farm, CoffeeLot,
TraceabilityEvent, QRRecord, AuditLog, User/Role) depends on this connection
existing and being configured correctly, particularly the PostGIS extension
required for farm polygon storage.

## Objective

Establish a working, environment-configured connection from the FastAPI
backend (from `EPIC-0-BE-001`) to a PostgreSQL database with the PostGIS
extension enabled, using SQLAlchemy as the database layer, with credentials
handled safely and the connection verifiable in local development. **No
schema or tables are created in this task** — that is `EPIC-0-DB-002`.

## Why This Task Exists

Implementation Playbook §12 fixes the order: Backend Foundation ->
**Database Configuration** -> PostgreSQL/PostGIS connection -> first
migration/schema. Design Document §7 requires PostgreSQL 16 with the PostGIS
extension, as a single instance (not the SRS's multi-region cluster) — this
task establishes that connection at the scale appropriate for V1.0.

## Authoritative Sources

- Design Document §7 (Data Architecture — "The database is PostgreSQL 16
  with the PostGIS extension... as a single instance rather than the SRS's
  multi-region cluster")
- Design Document §18 (Design Decisions — Database row: "PostgreSQL +
  PostGIS, single instance... single instance is sufficient at demo scale")
- Design Document §10 (Security Design — secrets management via environment
  variables; database access via a single application-role DB user with
  least-privilege grants; no direct client DB access)
- Implementation Specification (Technical Stack Freeze: Database = PostgreSQL
  + PostGIS; EPIC 0 task: "Configure PostgreSQL/PostGIS database & create
  `.env.example`")
- Implementation Playbook §3 (confirmed environment: SQLAlchemy 2.0.51,
  psycopg2-binary 2.9.12), §12 (Immediate Next Steps ordering)
- SRS §2.4 (Operating Environment) — cited only for the PostgreSQL/PostGIS
  version reference; the SRS's multi-region/Redis/Kubernetes context in the
  same section is explicitly **not** part of this task (out of scope, see
  `01-scope-boundaries.md`)

## Requirements Traceability

- Design Document §7: single-instance PostgreSQL 16 + PostGIS — satisfied
  directly by this task.
- Design Document §10: environment-variable secrets, least-privilege DB user
  — satisfied by this task's credential handling.
- Implementation Specification EPIC 0: "Configure PostgreSQL/PostGIS
  database & create `.env.example`" — satisfied directly.
- **Not traceable / explicitly deferred:** no table/entity is created in
  this task (see `EPIC-0-DB-002`); no SRS FR-xxx requirement is directly
  satisfied yet.

## Dependencies

- `EPIC-0-BE-001` must be complete (the backend skeleton, including a
  database-layer stub folder, must exist).

## Preconditions

- Confirm PostgreSQL and the PostGIS extension are available in the local
  development environment (or provisioned per whatever setup the team has
  agreed, e.g., local install or a local container — but see "Out of Scope"
  regarding production infrastructure).
- Confirm `psycopg2-binary` and SQLAlchemy versions match Implementation
  Playbook §3. If they do not, stop and report — do not silently
  reinstall/upgrade.

## Allowed Scope

- Adding SQLAlchemy database engine/session configuration to the backend
  layer scaffolded in `EPIC-0-BE-001`.
- Adding environment-variable-based database configuration (host, port,
  database name, user, password, or a single connection-string variable) and
  updating `.env.example` accordingly.
- Verifying the PostGIS extension is enabled on the target database (e.g.,
  via a startup check or a documented manual step — not by building
  infrastructure automation).
- Adding a simple connection-verification mechanism (e.g., a database
  ping used by the health/status endpoint from `EPIC-0-BE-001`, or a
  dedicated verification script) so the team can confirm the connection
  works without manually querying the database.
- Documenting the required local setup steps (e.g., in the backend README)
  so any team member can reproduce the connection locally.

## Files/Directories in Scope

- The database-layer folder/module scaffolded (empty) in `EPIC-0-BE-001`.
- Backend configuration/settings module (extending it with DB variables).
- `.env.example`.
- Backend README or setup documentation, limited to the database setup
  section.

Do not touch models, schemas, migrations, or any feature-module code — this
task configures the connection only.

## Technical Requirements

- Database: PostgreSQL 16 with the PostGIS extension, per Design Document
  §7 and SRS §2.4's version reference — single instance, not a cluster.
- Database access layer: SQLAlchemy 2.0.51 (already installed per
  Implementation Playbook §3) with `psycopg2-binary` as the driver. No other
  ORM or driver.
- Connection configuration is entirely environment-variable driven; no
  hard-coded host, credentials, or database name anywhere in the code.
- Per Design Document §10: the application connects using a single
  application-role database user with least-privilege grants — not a
  database superuser, and no direct client (frontend) database access is
  introduced.
- No connection pooling infrastructure beyond SQLAlchemy's own default
  engine pooling — Design Document §14 explicitly does not require
  PgBouncer-level infrastructure at V1.0 scale.

## Implementation Steps

1. Confirm preconditions (see above).
2. Extend the backend settings/configuration module with database
   connection variables, sourced from the environment.
3. Update `.env.example` to document the new required variables (no real
   values).
4. Implement the SQLAlchemy engine and session factory in the database-layer
   module.
5. Add a connection-verification mechanism (e.g., extend the
   `EPIC-0-BE-001` status/health endpoint to report database connectivity,
   or provide a small standalone verification script/command).
6. Verify the PostGIS extension is enabled on the target database and
   document how this was confirmed.
7. Update the backend README with local database setup steps.
8. Follow the per-feature workflow in `04-git-workflow.md`.

## Acceptance Criteria

- The backend application can establish a database connection using only
  environment-variable configuration — no code changes required to point at
  a different database instance.
- The connection-verification mechanism confirms both a successful
  PostgreSQL connection and that the PostGIS extension is enabled and
  queryable.
- No table or model exists yet as a result of this task (confirm this
  explicitly — creating tables here would be premature and belongs to
  `EPIC-0-DB-002`).
- `.env.example` lists all required database variables with no real values.
- The backend README documents the local database setup steps clearly
  enough that another team member can reproduce it without asking a
  question.

## Testing Requirements

Per `05-testing-rules.md`:

- At least one automated test (or clearly documented manual verification
  step, if a live database is required and not available in CI) confirms
  the database connection succeeds when correct environment variables are
  provided.
- At least one test/verification confirms the PostGIS extension is active
  (e.g., a query such as checking the extension is installed, without
  creating any application table).
- At least one test confirms a clear, structured failure (not a crash) when
  database environment variables are missing or invalid.

## Security Requirements

- Database credentials are never committed, logged, or included in error
  messages returned to a client.
- The application database user follows least privilege, per Design
  Document §10 — do not connect as a superuser.
- `.env` (real values) remains git-ignored.

## Error Handling Requirements

- A failed database connection at startup produces a clear, structured
  error/log message identifying that the database is unreachable — not a
  generic unhandled exception.
- The connection-verification mechanism distinguishes between "database
  unreachable," "PostGIS extension missing," and "credentials invalid,"
  where feasible, so the failure is actionable.

## Out of Scope

- Creating any table, model, or migration (this is `EPIC-0-DB-002`).
- Any managed/cloud database provisioning, clustering, replication, or
  Kubernetes-based database infrastructure (explicitly out of scope per
  `01-scope-boundaries.md` and Design Document §16).
- Redis or any caching layer, despite its mention in SRS §2.4 — that is
  enterprise scope, not V1.0.
- Connection pooling infrastructure beyond SQLAlchemy's default engine
  pooling.

## Definition of Done

- All items in "Acceptance Criteria" are true and independently verifiable.
- All items in "Testing Requirements" pass or are documented as manual
  verification with evidence.
- Reviewed and approved by at least one other team member.
- Merged into `develop`.
- Requirements-traceability entry updated (Kidus).

## Git Requirements

- Branch: `feature/db-postgis-config`, from `develop`.
- Commit style: `feat(db): configure PostgreSQL/PostGIS connection`.
- PR references Task ID `EPIC-0-DB-001` and confirms no tables/models were
  created.
- Merge target: `develop`.

## Expected Agent Report

On completion, report:

1. The database configuration variables introduced and where they are
   documented (`.env.example`).
2. How PostGIS extension availability was verified, with the exact
   verification method/output.
3. Confirmation that no tables/models were created as part of this task.
4. Any environment discrepancy found versus Implementation Playbook §3.
5. Any point where a requirement was unclear or untraceable, and how it was
   handled.
6. Test/verification results.
