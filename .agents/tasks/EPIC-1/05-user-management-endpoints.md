# Task Title

Admin-Only User Management Endpoints

## Task ID

EPIC-1-AUTH-005

## Epic

EPIC 1 — Authentication & Role-Based Access Control

## Owner

Kaleab (Backend/Auth)

## Status

Not started.

## Priority

High. Not on the critical path to the Baseline's primary acceptance
workflow (that workflow does not require user self-service), but required
by Implementation Specification EPIC 1's backend task list and necessary
for the team to onboard more than one real user without manually editing
the database.

## Objective

Implement the Admin-only endpoints to list users, create a new user
account, and change a user's role: `GET /api/v1/users`,
`POST /api/v1/users`, `PATCH /api/v1/users/{id}/role`.

## Why This Task Exists

`AUTH-001` created exactly one bootstrap Admin via a seed script, which is
not a sustainable way to onboard the rest of the team (Field/Registry
Agents, ECTA Officer accounts, etc.) as later epics need real accounts to
test against. Design Document §8 and §9.1 both specify this as an Admin
capability.

## Authoritative Sources

- Design Document §8 (API Design — Users & Roles table:
  `GET /api/v1/users` "List users (Admin only)... Supports pagination.";
  `POST /api/v1/users` "Create a user account... Validates unique username;
  hashes password before storage."; `PATCH /api/v1/users/{id}/role`
  "Change a user's role... Writes an AuditLog entry.")
- Design Document §9.1 ("User & role management (Admin only)")
- Design Document §7.2 (`AuditLog` entity, from `EPIC-0-DB-002`)
- Design Document §10 (Security Design — Audit logging row: "AuditLog table
  records create/update actions on Farmer, Farm, and Lot records with
  old/new values" — this task extends that same pattern to `User` role
  changes, per §8's explicit statement that the role-change endpoint
  "Writes an AuditLog entry")

## Requirements Traceability

```text
SRS:
- Section 6.3, SEC-05 (audit trail requirement) — the enterprise version
  requires IP address and device fingerprint per CRUD action; Design
  Document §10 scales this down to old/new value tracking without those
  fields for V1.0. This task's AuditLog writes for role changes follow the
  Design Document's scaled-down version, not the full SEC-05 specification.

Design Document:
- Section 7.2 (User, AuditLog entities)
- Section 8 (Users & Roles API table)
- Section 9.1 (Admin/ECTA Officer UI — user & role management)
- Section 10 (audit logging scope)

Implementation Specification:
- EPIC 1, Backend Tasks (protected API routes, generally)

Minimum Project Plan:
- Not available — see EPIC-1 overview traceability note.

Baseline Scope Freeze:
- Section 3.1, "Authentication and RBAC"

Implementation Playbook:
- Section 9, Per-Feature Development Workflow (applies to this task like
  any other)
```

## Dependencies

`EPIC-1-AUTH-004` (RBAC authorization mechanism — these endpoints are
Admin-only and must be protected by it) and `EPIC-1-AUTH-001` (password
hashing utility, needed to hash the password of any newly created user).

## Preconditions

- `AUTH-004` merged to `develop`, with its authorization mechanism
  available for reuse.
- `AUTH-001`'s hashing utility available for reuse.

## Allowed Scope

- `GET /api/v1/users` — paginated list of users, Admin-only.
- `POST /api/v1/users` — create a new user account, Admin-only, validating
  unique username and hashing the password before storage.
- `PATCH /api/v1/users/{id}/role` — change a user's role, Admin-only,
  writing an `AuditLog` entry recording the old and new role.

## Out of Scope

- Self-service user registration (there is no public/unauthenticated
  "sign up" flow in V1.0 — Design Document §8 lists user creation only
  under the Admin-only Users & Roles table).
- Password reset / "forgot password" flows (not specified in Design
  Document §8 for V1.0).
- Deleting or deactivating a user (Design Document §8's Users & Roles table
  lists only list/create/change-role; deactivation is not specified — if
  genuinely needed later, it is a change-control matter, not an addition to
  this task).
- Any endpoint outside Authentication/RBAC's own scope.

## Files/Directories Potentially Affected

Indicative paths, to be matched against the actual `EPIC-0-BE-001` layout:

- `backend/app/api/v1/users.py` — the three routes (this may already
  contain the proof-of-mechanism route from `AUTH-004`; if so, this task
  completes its full implementation rather than duplicating it).
- `backend/app/schemas/user.py` (or equivalent) — request/response schemas.
- `backend/app/services/user_service.py` (or equivalent) — business logic
  (uniqueness validation, hashing, audit-log writing).
- `backend/tests/` — tests for all three endpoints.

## Implementation Requirements

- All three routes require Admin role, enforced via `AUTH-004`'s mechanism.
- `GET /api/v1/users` supports pagination (Design Document §8) — exact
  pagination parameters (e.g., page/limit or offset/limit) are an
  implementation decision; record the choice made in the `Expected Agent
  Report`.
- `POST /api/v1/users` validates username uniqueness at the database level
  (reusing the constraint already defined on `User` in `EPIC-0-DB-002`, if
  one exists there — if `username` uniqueness was not already enforced by
  that migration, flag this as a schema gap per `06-change-control.md`
  rather than silently adding the constraint here) and hashes the password
  using `AUTH-001`'s utility before storing it.
- `PATCH /api/v1/users/{id}/role` validates the target role exists among
  the four seeded roles, updates the user's role, and writes an `AuditLog`
  row capturing the old role, the new role, the acting Admin's user ID, and
  a timestamp — consistent with the scaled-down audit pattern in Design
  Document §10.

## Acceptance Criteria

- An Admin can list users via `GET /api/v1/users` and receives a paginated
  response.
- A non-Admin authenticated user calling any of the three endpoints
  receives `403`.
- An unauthenticated caller receives `401`.
- An Admin can create a new user via `POST /api/v1/users`; the new user's
  password is stored only as a hash, never plaintext.
- Attempting to create a user with a username that already exists is
  rejected with a structured `400`/`409` (not a database-level crash
  surfaced to the client).
- An Admin can change another user's role via
  `PATCH /api/v1/users/{id}/role`; the resulting `AuditLog` row correctly
  records the old and new role and the acting Admin's ID.
- Attempting to set a role to something outside the four seeded roles is
  rejected with a structured `400`.

## Testing Requirements

Per `05-testing-rules.md`:

- Test: Admin lists users successfully; non-Admin and unauthenticated
  requests are rejected (`403`/`401` respectively).
- Test: Admin creates a user successfully; password is hashed, not
  plaintext, in the database.
- Test: creating a user with a duplicate username fails with a structured
  error, not a raw database exception.
- Test: Admin changes a user's role successfully; the `AuditLog` row is
  correctly written with old/new values.
- Test: attempting to set an invalid role is rejected.
- Test: a non-Admin attempting the role-change endpoint is rejected with
  `403`.

## Security Requirements

- New user passwords are hashed before storage, never logged, never
  returned in any response.
- `AuditLog` entries do not themselves store the password or password hash
  — only role old/new values, actor, and timestamp.
- Role-change and user-creation actions are only reachable by an
  authenticated Admin — verified by the RBAC mechanism from `AUTH-004`, not
  a re-implemented check.

## Error Handling Requirements

- Duplicate username -> structured `400`/`409`, not an unhandled
  `IntegrityError`.
- Invalid role value -> structured `400`.
- Non-existent user ID in the role-change endpoint -> structured `404`.

## Documentation Requirements

- Kidus updates the requirements-traceability entry for the Users & Roles
  API (Design Document §8) and confirms the audit-log pattern from Design
  Document §10 is now demonstrated in a second location (Farmer/Farm/Lot
  audit logging will follow the same pattern in later epics).

## Commit Guidance

- Branch: `feature/auth-user-management`, from `develop`.
- Commit message pattern: `feat(auth): implement admin user management endpoints`.
- PR references Task ID `EPIC-1-AUTH-005`.
- Merge target: `develop`.

## AI Agent Safety Notes

- Do not add a public/self-service registration route.
- Do not add password-reset or user-deactivation functionality —
  not specified for V1.0; flag as a potential future item rather than
  building it.
- Do not weaken or bypass `AUTH-004`'s authorization mechanism by
  implementing a separate, ad hoc Admin check for these routes.

## Expected Agent Report

1. The pagination approach chosen for `GET /api/v1/users`.
2. Confirmation of how username uniqueness is enforced (existing DB
   constraint vs. a flagged schema gap).
3. Confirmation that new-user passwords are hashed and never appear in any
   response or log.
4. Confirmation that the `AuditLog` row for a role change is correctly
   populated, with example old/new values from a test run.
5. Any point where a requirement was unclear or untraceable, and how it was
   handled.
6. Test results.
