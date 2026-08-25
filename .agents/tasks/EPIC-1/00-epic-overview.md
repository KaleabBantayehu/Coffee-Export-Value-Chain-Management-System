# EPIC 1 — Authentication & Role-Based Access Control: Overview

## Epic ID

EPIC-1

## Epic Name

Authentication & Role-Based Access Control (Auth/RBAC)

## Objective

Establish the authentication and authorization foundation that every other
V1.0 module (Farmer Registry, Farm/Polygon, Coffee Lot/Traceability, QR)
depends on: user login, JWT issuance and validation, role-based access
enforcement on protected routes, and the minimum frontend integration needed
to log in, navigate by role, and log out.

## Business / Project Purpose

Per the Baseline's critical workflow, every core action in CEVCMS (register
farmer, register farm, create lot, generate QR) is performed by an
authenticated, role-appropriate user; only public QR verification is
unauthenticated. Without Auth/RBAC, no other core module can be safely
demonstrated, tested, or protected. This is also the first link in the
project's fixed dependency chain (Baseline §4; Implementation Specification
§4):

```text
Authentication / RBAC
        |
        v
Farmer Registry
        |
        v
Farm & Polygon
        |
        v
Coffee Lot / Traceability
        |
        v
Dynamic QR
        |
        v
Public Verification
```

## V1.0 Scope

In scope for this epic, per Baseline §3.1, Implementation Specification EPIC
1, and Design Document §4.1/§8:

- User and Role/Permission data access logic built on the schema already
  created in `EPIC-0-DB-002` (this epic does not create new tables for
  Auth/RBAC beyond seed/reference data — see AUTH-001).
- Password hashing (bcrypt/Argon2).
- Login endpoint issuing a signed JWT carrying user ID and role claim.
- An authentication dependency that validates the JWT on protected routes.
- `GET /api/v1/auth/me` and `POST /api/v1/auth/logout`.
- RBAC authorization middleware enforcing role-based access on protected
  routes.
- Admin-only user management endpoints (list, create, change role).
- Frontend: login page, auth state management, protected routes,
  role-aware navigation, logout handling.

Explicitly **not** in scope (see "Out of Scope" below and
`01-scope-boundaries.md`): multi-factor authentication, refresh tokens, HSM
key custody, OAuth2/OIDC, ABAC regional partitioning, biometric binding.

## Dependencies

- `EPIC-0-BE-001` (backend foundation) — complete.
- `EPIC-0-DB-001` (PostgreSQL/PostGIS connection) — complete.
- `EPIC-0-DB-002` (initial schema, including `Role`, `Permission`, `User`,
  and the `RolePermission` join table) — complete. EPIC 1 builds on these
  tables; it does not recreate them.

## Preconditions

- The `develop` branch reflects the completed EPIC-0 state (commits
  `61353e3` and `74f2c92`, per the current project state supplied with this
  request).
- The `Role`, `Permission`, `User` tables exist and are reachable via the
  database connection configured in `EPIC-0-DB-001`.
- **Flagged precondition gap:** the Implementation Specification's EPIC 0
  description includes "Initialize React frontend... projects," but the
  EPIC-0 task files actually committed to this repository
  (`01-backend-foundation.md`, `02-database-postgis.md`,
  `03-initial-migrations.md`) cover backend infrastructure only — no EPIC-0
  task file scaffolds a React frontend project. This EPIC-1 spec assumes,
  per the current-state description supplied with this request ("base
  project structure... already created"), that a minimal React frontend
  project already exists as part of the completed baseline. `AUTH-006` (the
  first frontend task) must verify this before doing any frontend work, and
  must stop and report rather than silently scaffolding a new frontend
  project if one is not found — see `AUTH-006`'s Preconditions. This gap
  is recorded here rather than resolved silently, per
  `00-project-authority.md`.

## Expected Outputs

- Working `POST /api/v1/auth/login`, `GET /api/v1/auth/me`,
  `POST /api/v1/auth/logout` endpoints.
- A reusable authentication dependency and a reusable RBAC authorization
  dependency/decorator that later epics (Farmer Registry, Traceability, QR)
  will apply to their own protected routes.
- Admin-only user management endpoints:
  `GET /api/v1/users`, `POST /api/v1/users`, `PATCH /api/v1/users/{id}/role`.
- A functioning frontend login page, auth state management, role-aware
  protected routing, and logout handling.
- Passing backend and frontend tests demonstrating the Epic Acceptance
  Criteria below.

## Team Ownership

Per Baseline §5 and Implementation Specification EPIC 1 ("Owner: Kaleab
(Backend) / Biniyam (Frontend)"):

- **Kaleab** — owns all backend Auth/RBAC tasks (`AUTH-001` through
  `AUTH-005`): User/Role data access, password hashing, login endpoint, JWT
  issuance/validation, authentication and RBAC middleware, protected API
  routes, admin user-management endpoints.
- **Biniyam** — owns the frontend Auth tasks (`AUTH-006`, `AUTH-007`): login
  page UI, auth state management, protected routes, role-aware navigation,
  logout handling.
- **Ephratha** — owns cross-cutting verification (`AUTH-008`): API testing,
  RBAC security testing, defect tracking, per Baseline §5.
- **Kidus** — updates requirements-traceability and test documentation as
  each task completes, per Baseline §5 and `04-git-workflow.md` step 9.

## Task List

| Task ID | File | Title | Owner |
|---|---|---|---|
| EPIC-1-AUTH-001 | `01-auth-data-foundations.md` | Password Hashing Utility, Role/Permission Seed Data, Bootstrap Admin User | Kaleab |
| EPIC-1-AUTH-002 | `02-login-endpoint-jwt.md` | Login Endpoint & JWT Issuance | Kaleab |
| EPIC-1-AUTH-003 | `03-auth-dependency-session.md` | Authentication Dependency, `GET /auth/me`, `POST /auth/logout` | Kaleab |
| EPIC-1-AUTH-004 | `04-rbac-middleware.md` | RBAC Authorization Middleware & Protected-Route Enforcement | Kaleab |
| EPIC-1-AUTH-005 | `05-user-management-endpoints.md` | Admin-Only User Management Endpoints | Kaleab |
| EPIC-1-AUTH-006 | `06-frontend-login-auth-state.md` | Frontend Login Page & Auth State Management | Biniyam |
| EPIC-1-AUTH-007 | `07-frontend-protected-routes.md` | Frontend Protected Routes, Role-Aware Navigation, Logout | Biniyam |
| EPIC-1-AUTH-008 | `08-auth-rbac-verification.md` | Authentication & RBAC End-to-End Verification | Ephratha (+ Kidus for docs) |

## Task Dependency Order

```text
AUTH-001 (data foundations: hashing, seed roles, bootstrap admin)
   |
   v
AUTH-002 (login endpoint + JWT issuance)
   |
   v
AUTH-003 (auth dependency + /me + /logout)
   |
   v
AUTH-004 (RBAC middleware / protected-route enforcement)
   |
   +--------------------------+
   v                          v
AUTH-005                  AUTH-006 (frontend login + auth state;
(admin user mgmt              also depends on AUTH-002/AUTH-003
endpoints, RBAC-              for the login/me contract)
protected)                    |
   |                          v
   |                      AUTH-007 (frontend protected routes,
   |                      role-aware nav, logout; depends on
   |                      AUTH-004 for role semantics and
   |                      AUTH-006 for auth state)
   |                          |
   +------------+-------------+
                v
            AUTH-008 (end-to-end verification of the full epic)
```

No task may begin before every task listed as its dependency in its own
`Dependencies` section is merged into `develop` and passing its own
acceptance criteria.

## Acceptance Criteria for the Epic

Restating the Implementation Specification's EPIC 1 Definition of Done,
made observable:

- A user with valid credentials can log in via `POST /api/v1/auth/login`
  and receives a valid, correctly-signed JWT carrying their user ID and
  role.
- `GET /api/v1/auth/me`, called with that JWT, returns the correct user
  profile and role.
- A request to a role-protected endpoint from a user whose role has the
  required permission succeeds.
- A request to the same endpoint from an authenticated user whose role
  lacks the required permission is rejected with `403`.
- A request to a protected endpoint with no JWT, or an invalid/expired JWT,
  is rejected with `401`.
- `POST /api/v1/auth/logout` succeeds and the frontend discards the token
  client-side; frontend routes gated behind authentication become
  inaccessible afterward.
- The frontend renders role-appropriate navigation for at least the four
  V1.0 roles (Admin, ECTA Officer, Field/Registry Agent, Verifier), per the
  Role Model below.
- All automated tests specified across `AUTH-001`–`AUTH-007` pass, and
  `AUTH-008`'s end-to-end verification passes.

## Role Model (V1.0)

Per Baseline §3 (via Implementation Specification EPIC 1, "Minimum Roles")
and Design Document §4.1/§9:

| Role | Summary Access Level (Design Document §4.1, §9) |
|---|---|
| Admin | Full access; only role permitted to manage users and roles. |
| ECTA Officer | Back-office/oversight access: dashboards, farmer/traceability search, internal QR verification tool. |
| Field/Registry Agent | Farmer and farm/polygon registration, lot creation, traceability event entry, QR generation (once those modules exist in later epics). |
| Verifier | Read-only; the role model backing the **public, unauthenticated** QR verification endpoint — Design Document §4.1 notes this role exists in the Role table "for public QR verification" and is not necessarily tied to an authenticated login flow the same way the other three are. `AUTH-004` must treat this role's actual authentication requirement as an explicit open item (see that task) rather than assuming it needs a login screen, since the public verification endpoint itself is unauthenticated per Design Document §5.3/§8. |

No additional business role is introduced. This matches the four roles
already fixed in the Baseline, the Implementation Specification, and the
Design Document — the SRS's full "12-role model" (Design Document §4.1) is
explicitly not implemented in V1.0.

## Relevant Source Traceability (Epic-Level)

```text
SRS:
- Module 01: Authentication & Access Control (FR-AUTH-001, FR-AUTH-002)
- Section 6.1 Authentication & Authorization (SEC-01, SEC-02)
- Section 6.3 Audit Trail & Immutable Logging (SEC-05)
(Each narrowed for V1.0 per Design Document §4.1/§18 — see individual tasks.)

Design Document (ECTA-CEVCMS-DD-V1.0):
- Section 4.1 Authentication & Role-Based Access
- Section 7.2 Entity Descriptions (Role, Permission, User)
- Section 8 API Design — Authentication; Users & Roles
- Section 9.1 User Interface Design — Admin/ECTA Officer (login, user/role
  management)
- Section 10 Security Design
- Section 13 Sequence 1 — User Login
- Section 18 Design Decisions — Authentication, Authorization model rows

Implementation Specification & Development Backlog:
- EPIC 1 — Authentication & RBAC (Owner, Backend Tasks, Frontend Tasks,
  Minimum Roles, Definition of Done)
- Section 4 Critical Dependency Graph

Baseline Scope Freeze (ECTA-CEVCMS-BASELINE-V1.0):
- Section 3.1 Must Have / Core — "Authentication and RBAC"
- Section 4 V1.0 Critical Workflow — "Login" as the first step
- Section 5 Team Responsibilities — Kaleab (Auth/RBAC backend), Biniyam
  (frontend)

Implementation Playbook (ECTA-CEVCMS-PLAYBOOK-V1.0):
- Section 5 Development Order — Authentication & RBAC first
- Section 9 Per-Feature Development Workflow

Minimum Project Plan V1.0:
- **Not available at the time this epic specification was written.** The
  document referenced as "CEVCMS_Minimum_Project_Plan_V1.0.docx.pdf" was
  not found among the files accessible to this task; only the university's
  generic Appendix 2 template ("Minimum Project Plan" guidance document) is
  present in the project folder. Per `00-project-authority.md`, this gap is
  recorded rather than silently filled: the four-week schedule already
  stated in the Implementation Specification and Implementation Playbook is
  used as the schedule reference instead. If the actual Minimum Project Plan
  becomes available, its Week 1/Week 2 task and milestone assignments for
  Auth/RBAC must be checked against this epic's task order and dependency
  chain, and any discrepancy must be flagged, not silently resolved.

Assignment Description (ECTA-CEVCMS-AD-V1.0):
- Section 5, Objective O1/O5 area (project acceptance depends on
  demonstrating authenticated, role-appropriate access) — referenced for
  context; the Assignment Description does not add implementation detail
  beyond what the Baseline/Design Document/Implementation Specification
  already fix.
```

## Explicit Out-of-Scope Items for EPIC 1

Per `01-scope-boundaries.md` and Design Document §4.1/§18/§19:

- Multi-factor authentication / OTP (SRS FR-AUTH-001's MFA requirement is
  explicitly narrowed away by Design Document §4.1 — V1.0 implements
  username/password + JWT only).
- Refresh tokens or a server-side session/token store (Design Document
  §4.1: "no refresh-token/HSM infrastructure is built").
- HSM-backed key custody or RS256 keys (SRS SEC-02) — V1.0 signs the JWT
  with a server-held secret (symmetric signing), per Design Document §10.
- OAuth2/OpenID Connect identity federation (Design Document §19,
  Enterprise/Future).
- Biometric operator binding / Android biometric login (SRS FR-AUTH-002;
  Design Document §19: "no native Android app in V1.0").
- ABAC / regional data partitioning (SRS SEC-01's combined RBAC+ABAC is
  narrowed to RBAC-only per Design Document §18).
- Any role beyond the four listed in the Role Model above.
- Any endpoint or entity belonging to Farmer Registry, Farm/Polygon,
  Traceability, QR, or any stretch module — those are later epics and must
  not be started as part of EPIC 1, even if convenient to build alongside
  Auth/RBAC.
- Recreating or modifying the `Role`, `Permission`, `User`, or
  `RolePermission` tables created in `EPIC-0-DB-002` — EPIC 1 populates and
  uses them; it does not alter their schema. If a schema gap is discovered
  (e.g., a missing column needed for a genuine V1.0 requirement), that is a
  change-control matter (`06-change-control.md`), not a silent migration.

## AI-Agent Execution Rules for EPIC 1

In addition to the global rules in `.agents/rules/` (all of which apply in
full), an agent executing any EPIC-1 task must not:

- Modify any EPIC-0 task file or any file in `.agents/rules/`.
- Modify the Project Baseline, Design Document, SRS, Implementation
  Specification, Minimum Project Plan, Assignment Description, or
  Implementation Playbook source documents.
- Reinitialize Git, recreate `main`/`develop`, recreate the Python virtual
  environment, or reinstall already-approved dependencies.
- Introduce MFA, refresh tokens, HSM/RS256 signing, OAuth2/OIDC, ABAC, or
  any role not in the Role Model above, regardless of how directly the SRS
  describes them — see "Explicit Out-of-Scope Items."
- Begin any `AUTH-0xx` task before the task(s) listed in its `Dependencies`
  section are complete and merged to `develop`.
- Begin any Farmer Registry, Traceability, or QR work under cover of an
  EPIC-1 task, even if it seems efficient to "also" wire up a downstream
  module while touching related code.
- Silently scaffold a new frontend project if `AUTH-006`'s precondition
  check finds none — stop and report per the flagged precondition gap
  above.
- Push directly to `main` or `develop`, or merge its own pull request,
  per `04-git-workflow.md`.
- Declare a task's Definition of Done satisfied without its required tests
  passing, per `05-testing-rules.md`.
