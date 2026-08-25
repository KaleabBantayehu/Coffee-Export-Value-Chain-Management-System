# EPIC 0 — Project Infrastructure: Overview

## Epic

EPIC 0 — Project Infrastructure

## Owner

Kaleab (Project Manager & Backend/Auth lead), per Baseline §5 and
Implementation Specification (EPIC 0 Owner).

## Authoritative Sources

- Implementation Specification & Development Backlog, "EPIC 0 — Project
  Infrastructure"
- Project Baseline & Scope Freeze §2 (Technology Baseline), §4 (Critical
  Workflow)
- Implementation Playbook §3 (Frozen Technology Stack), §10 (Current
  Status), §12 (Immediate Next Steps)
- Design Document §3 (System Architecture), §16 (Deployment Design)

## Status of EPIC 0 as a whole

**Partially complete.** Per Implementation Playbook §10 (team-reported
status, to be verified rather than trusted blindly):

| Item | Status |
|---|---|
| Git repository | Created |
| `main` branch | Created |
| `develop` branch | Created, pushed to GitHub |
| Python virtual environment | Set up |
| Backend dependencies | Installed |
| FastAPI application skeleton | **Not yet done — this is the next step** |
| PostgreSQL/PostGIS connection | **Not yet done** |
| Initial database schema/migration | **Not yet done** |

**Consequence for agents:** do not create tasks or perform work that
reinstalls the Python virtual environment, reinitializes the Git repository,
or recreates the `main`/`develop` branches. That part of EPIC 0 is done.
The remaining, currently open work is exactly the three tasks below.

## What EPIC 0 covers, per the Implementation Specification

> Create GitHub repository & configure main/develop/feature workflows and
> branch protection rules; create GitHub Issues/Projects board; initialize
> React frontend & FastAPI backend projects; configure PostgreSQL/PostGIS
> database & create `.env.example`; establish folder structure, README.md,
> and pull-request review rules.

**Definition of Done (EPIC 0, as a whole, per the Implementation
Specification):** every team member can clone the repository; frontend,
backend, and database run successfully locally; a basic API request
succeeds; no secrets are committed.

This epic overview does not restate that Definition of Done as satisfied —
each task file below carries its own, narrower Definition of Done, and EPIC 0
as a whole is only complete once all three are.

## Task files in this epic

| Order | Task ID | File | Objective |
|---|---|---|---|
| 1 | `EPIC-0-BE-001` | `01-backend-foundation.md` | Establish the FastAPI backend application skeleton only — no feature modules yet. |
| 2 | `EPIC-0-DB-001` | `02-database-postgis.md` | Configure the PostgreSQL/PostGIS connection and the SQLAlchemy database layer. |
| 3 | `EPIC-0-DB-002` | `03-initial-migrations.md` | Create the initial schema/migration for the core entities needed by V1.0. |

These three tasks are strictly ordered: `EPIC-0-BE-001` must be complete
before `EPIC-0-DB-001` begins (the database layer is wired into the backend
skeleton), and `EPIC-0-DB-001` must be complete before `EPIC-0-DB-002` begins
(you cannot migrate a schema onto a connection that does not exist yet). This
mirrors Implementation Playbook §12: *"Backend Foundation -> Database
Configuration -> PostgreSQL/PostGIS connection -> first database
migration/schema."*

## What is explicitly not part of EPIC 0

Per Implementation Specification EPIC 1 onward, the following are **separate,
later epics** and must not be started as part of EPIC 0 work:

- Authentication & RBAC (EPIC 1)
- Farmer & Polygon Registry (EPIC 2)
- Traceability Engine (EPIC 3)
- Dynamic QR Engine (EPIC 4)
- Frontend Integration (EPIC 5)
- Testing & QA process setup beyond what each EPIC-0 task itself requires
  (EPIC 6)
- Any stretch module (EPIC 7, EPIC 8)

EPIC 0 produces an empty-but-correctly-structured, runnable backend
connected to an empty-but-correctly-structured database. It does not
implement any business feature.
