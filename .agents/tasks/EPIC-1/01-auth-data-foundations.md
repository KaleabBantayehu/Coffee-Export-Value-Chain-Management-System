# Task Title

Password Hashing Utility, Role/Permission Seed Data, Bootstrap Admin User

## Task ID

EPIC-1-AUTH-001

## Epic

EPIC 1 — Authentication & Role-Based Access Control

## Owner

Kaleab (Backend/Auth), per Baseline §5 and Implementation Specification
EPIC 1 ownership.

## Status

Not started.

## Priority

Critical — every later Auth/RBAC task depends on this one.

## Objective

Implement the password hashing utility, seed the four V1.0 roles (and their
baseline permissions) into the `Role`/`Permission`/`RolePermission` tables
created in `EPIC-0-DB-002`, and create exactly one bootstrap Admin user so
that `EPIC-1-AUTH-002` (login) has a real account to authenticate against.

## Why This Task Exists

Every subsequent Auth/RBAC task needs two things that do not yet exist after
EPIC 0: a way to hash and verify passwords, and at least one user account to
log in as. Without a bootstrap Admin account, `AUTH-002`'s login endpoint
cannot be tested end to end, and `AUTH-005`'s admin-only user-management
endpoints have no way to be reached in the first place (they require an
authenticated Admin, and only an Admin can create new users). This task
breaks that circularity.

## Authoritative Sources

- Design Document §4.1 ("password verified against a bcrypt/Argon2 hash —
  never stored or logged in plaintext")
- Design Document §7.2 (`Role`, `Permission`, `User` entity definitions,
  already created by `EPIC-0-DB-002`)
- Design Document §18 (Design Decisions — "Authentication: JWT +
  bcrypt/Argon2 ... stateless, simple to implement and test in one month")
- Implementation Playbook §3 (confirmed environment: "Password
  passlib + bcrypt")
- Implementation Specification EPIC 1 ("Minimum Roles: Admin, ECTA Officer,
  Field/Registry Agent, Verifier")

## Requirements Traceability

```text
SRS:
- Module 01 (FR-AUTH-001) — password-based authentication is the relevant
  part of this requirement; the MFA portion is explicitly out of scope for
  V1.0 (see EPIC-1 overview, "Explicit Out-of-Scope Items").

Design Document:
- Section 4.1 (password hashing algorithm choice)
- Section 7.2 (Role, Permission, User entities)
- Section 18 (Authentication design decision)

Implementation Specification:
- EPIC 1, Backend Tasks: "User & Role entity models, password hashing..."
  (the entity models were created in EPIC-0-DB-002; this task adds the
  hashing utility and seed data on top of them)

Minimum Project Plan:
- Not available — see EPIC-1 overview traceability note.

Baseline Scope Freeze:
- Section 3.1, "Authentication and RBAC"

Implementation Playbook:
- Section 3, confirmed environment (passlib + bcrypt already installed)
```

## Dependencies

None within EPIC 1 (this is the first task). Requires `EPIC-0-DB-002`
(schema) to be complete.

## Preconditions

- Confirm `Role`, `Permission`, `RolePermission`, and `User` tables exist
  (re-run `EPIC-0-DB-002`'s verification method if any doubt exists).
- Confirm `passlib` and `bcrypt` are available in the environment per
  Implementation Playbook §3 — do not install a different hashing library.

## Allowed Scope

- A password hashing/verification utility (hash a plaintext password;
  verify a plaintext password against a stored hash).
- Seed data (via a script, fixture, or migration data-seed step — whichever
  mechanism is consistent with the migration tool chosen in
  `EPIC-0-DB-002`) that inserts:
  - the four roles: Admin, ECTA Officer, Field/Registry Agent, Verifier;
  - a minimal set of permissions sufficient for `AUTH-004`/`AUTH-005` to
    enforce role checks (e.g., a `users:manage` permission assigned only to
    Admin); the exact permission set may be extended by later epics as new
    protected actions are defined — this task only needs enough to prove
    the RBAC model works end to end for Auth's own endpoints.
  - the `RolePermission` associations linking roles to their permissions.
- Exactly one bootstrap Admin `User` record, with a hashed password, created
  via the seed mechanism (not via an API endpoint, since no user-creation
  endpoint exists yet).

## Out of Scope

- Any API endpoint (login, user management) — those are `AUTH-002` and
  `AUTH-005`.
- Any change to the `Role`/`Permission`/`User`/`RolePermission` table
  schema — this task populates data, it does not alter structure.
- Any role beyond the four listed above.
- MFA, refresh tokens, or any mechanism listed in EPIC-1 overview's
  "Explicit Out-of-Scope Items."

## Files/Directories Potentially Affected

Indicative paths, to be matched against the actual layout established in
`EPIC-0-BE-001` (confirm exact folder names against the existing repository
before creating new files):

- `backend/app/core/security.py` (or equivalent existing "core"/"utils"
  location) — password hashing utility.
- A seed-data script or migration-data step, placed consistent with the
  migration tool chosen in `EPIC-0-DB-002` (e.g.,
  `backend/app/db/seed.py` or a data migration file in the existing
  migrations directory).
- `backend/tests/` — unit tests for the hashing utility.

Do not create a new top-level directory structure that duplicates what
`EPIC-0-BE-001` already established.

## Implementation Requirements

- The hashing utility must use bcrypt (via `passlib`, already installed),
  consistent with Design Document §4.1 and the confirmed environment. Do
  not introduce Argon2 tooling instead — Design Document §4.1 names
  "bcrypt/Argon2" as an either/or, but the confirmed local environment
  (Playbook §3) already has `passlib + bcrypt` installed; use what is
  already installed rather than adding a new dependency for the alternative.
- The bootstrap Admin's password must be stored only as a hash — never in
  plaintext, in code, in a commit, or in `.env.example`. The plaintext value
  used to create it (for the team's own initial login) must be communicated
  out-of-band (e.g., told to the team directly), not committed anywhere in
  the repository.
- Seed data must be idempotent: running the seed step twice must not create
  duplicate roles, permissions, or a duplicate bootstrap Admin.

## Acceptance Criteria

- Calling the hashing utility's "hash" function on a plaintext password and
  then its "verify" function with the same plaintext against the resulting
  hash returns true; verifying an incorrect plaintext against that hash
  returns false.
- After running the seed step against a freshly migrated database, querying
  the `Role` table returns exactly the four roles named above, with no
  duplicates.
- The `RolePermission` associations exist and correctly link each role to
  its intended permission(s).
- Exactly one `User` row exists with the Admin role, and its
  `password_hash` field is a bcrypt hash, not plaintext.
- Running the seed step a second time against the same database does not
  create duplicate roles, permissions, or a second bootstrap Admin.

## Testing Requirements

Per `05-testing-rules.md`:

- Unit test: hash a known password, verify it succeeds against the same
  password and fails against a different one.
- Unit test/verification: after seeding, confirm exactly four roles exist
  and each has the expected permission(s) via a query.
- Unit test/verification: confirm exactly one Admin user exists after
  seeding, and that a second seed run does not duplicate it.

## Security Requirements

- No plaintext password appears in code, comments, commit messages, logs,
  or any committed file.
- The bootstrap Admin's plaintext password is generated or provided
  out-of-band, not hard-coded into the seed script in a way that would be
  visible in version control (e.g., read from an environment variable at
  seed time, not embedded as a string literal).

## Error Handling Requirements

- If the seed step is run before the schema exists (e.g.,
  `EPIC-0-DB-002`'s migration has not been applied), it fails with a clear
  error rather than a partial/inconsistent state.

## Documentation Requirements

- Kidus updates the requirements-traceability entry for FR-AUTH-001
  (password-based portion) to reflect "data foundations complete; login
  endpoint pending (AUTH-002)."
- The backend README documents how to run the seed step locally.

## Commit Guidance

- Branch: `feature/auth-data-foundations`, from `develop`.
- Commit message pattern: `feat(auth): add password hashing utility and role/permission seed data`.
- PR references Task ID `EPIC-1-AUTH-001` and confirms no plaintext
  credentials are present in the diff.
- Merge target: `develop`, per `04-git-workflow.md`.

## AI Agent Safety Notes

- Do not create a login endpoint, user-management endpoint, or any other
  API route in this task — see "Out of Scope."
- Do not alter the schema of `Role`, `Permission`, `User`, or
  `RolePermission`. If the existing schema is insufficient for the
  permission model this task needs, stop and report the gap
  (`06-change-control.md`) rather than migrating the schema unilaterally.
- Do not commit the bootstrap Admin's plaintext password anywhere.

## Expected Agent Report

1. Confirmation of the hashing library used and that it matches the
   confirmed environment (Playbook §3).
2. The exact roles and permissions seeded, and how idempotency was
   verified.
3. Confirmation that the bootstrap Admin's plaintext password is not
   present anywhere in the committed diff, and how the team will obtain it
   out-of-band.
4. Any point where the permission model needed for later tasks
   (`AUTH-004`/`AUTH-005`) was unclear or untraceable, and how it was
   handled.
5. Test results.
