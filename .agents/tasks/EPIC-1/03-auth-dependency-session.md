# Task Title

Authentication Dependency, `GET /auth/me`, `POST /auth/logout`

## Task ID

EPIC-1-AUTH-003

## Epic

EPIC 1 — Authentication & Role-Based Access Control

## Owner

Kaleab (Backend/Auth)

## Status

Not started.

## Priority

Critical.

## Objective

Implement a reusable authentication dependency that decodes and validates
the JWT issued by `AUTH-002` on any route that requires it, and implement
`GET /api/v1/auth/me` and `POST /api/v1/auth/logout` using that dependency.

## Why This Task Exists

`AUTH-002` issues tokens but nothing yet checks them. This task creates the
single, reusable mechanism every protected route in the entire project
(Auth's own routes and, later, Farmer/Farm/Traceability/QR routes) will use
to confirm "who is making this request." Building it once here, correctly,
prevents every later module from reinventing JWT validation.

## Authoritative Sources

- Design Document §4.1 ("Authorization: an authorization middleware runs on
  every protected route, decoding the JWT and checking the caller's role
  against the permissions required by that route")
- Design Document §8 (API Design — `GET /api/v1/auth/me`: "Return the
  current authenticated user's profile" — Auth: JWT — "Used by the frontend
  to render role-specific navigation." `POST /api/v1/auth/logout`: "Client-
  side token discard acknowledgement" — Auth: JWT — "No server-side session
  store in V1.0; endpoint exists for API symmetry/logging.")
- Design Document §4.1 ("Logout / token expiration: logout is client-side
  token discard; the JWT's own expiry enforces server-side invalidation,
  since no server-side session/refresh-token store is built in Version
  1.0.")

## Requirements Traceability

```text
SRS:
- Module 01 (FR-AUTH-001), session-validation portion. As with AUTH-002,
  the enterprise refresh-token/session-store elements of FR-AUTH-001 are
  narrowed away per Design Document §4.1.

Design Document:
- Section 4.1 (authorization dependency concept; logout as client-side
  discard)
- Section 8 (GET /auth/me and POST /auth/logout contracts)

Implementation Specification:
- EPIC 1, Backend Tasks: "...JWT generation/validation, Auth & Role
  middleware..." (this task covers the validation/middleware portion;
  AUTH-004 covers the Role/RBAC portion specifically)

Minimum Project Plan:
- Not available — see EPIC-1 overview traceability note.

Baseline Scope Freeze:
- Section 4, Critical Workflow (login precedes every other core action)

Implementation Playbook:
- Section 3, confirmed environment ("JWT: python-jose")
```

## Dependencies

`EPIC-1-AUTH-002` (JWT issuance — this task validates tokens issued by that
one; the signing secret and claim structure must match exactly).

## Preconditions

- `AUTH-002` merged to `develop`.
- A valid JWT can be obtained by logging in as the bootstrap Admin.

## Allowed Scope

- A reusable authentication dependency (e.g., a FastAPI dependency function)
  that: extracts the JWT from the request, validates its signature and
  expiry, and resolves it to the corresponding `User` record (or rejects
  the request).
- `GET /api/v1/auth/me`, using that dependency, returning the authenticated
  user's profile (at minimum: user ID, username, full name, role).
- `POST /api/v1/auth/logout`, using that dependency, acknowledging the
  request (no server-side token invalidation, per Design Document §4.1).

## Out of Scope

- Role-based permission checks beyond "is this token valid and whose is
  it" — checking whether the resolved user's role is *permitted* to access
  a given route is `AUTH-004`'s responsibility, not this task's.
- Any server-side token store, blocklist, or refresh mechanism (explicitly
  not built in V1.0, per Design Document §4.1).
- User-management endpoints (`AUTH-005`).

## Files/Directories Potentially Affected

Indicative paths, to be matched against the actual `EPIC-0-BE-001` layout:

- `backend/app/core/security.py` (or equivalent) — the authentication
  dependency function.
- `backend/app/api/v1/auth.py` — `GET /auth/me`, `POST /auth/logout`
  routes, added alongside the login route from `AUTH-002`.
- `backend/app/schemas/auth.py` — response schema for the `/me` profile.
- `backend/tests/` — tests for the dependency and both new routes.

## Implementation Requirements

- The dependency must reject a request with no `Authorization` header, an
  invalid/malformed JWT, an expired JWT, or a JWT signed with the wrong
  secret — in every case, returning `401`.
- On a valid JWT, the dependency resolves and makes available the
  corresponding authenticated `User` (or at minimum, their ID and role) to
  the route handler, so both this task's routes and future protected routes
  can use it without re-decoding the token themselves.
- `GET /auth/me` returns the profile of the user identified by the token —
  never a different user's data, and never data for a user ID that no
  longer exists (if the underlying `User` was deleted after token issuance,
  this must fail cleanly rather than return stale/partial data).
- `POST /auth/logout` performs no server-side state change beyond
  acknowledging the call (Design Document §4.1 confirms no server-side
  session store exists); the actual token discard happens client-side in
  `AUTH-006`/`AUTH-007`.

## Acceptance Criteria

- `GET /api/v1/auth/me` with a valid Admin JWT returns `200` with the
  Admin's correct profile and role.
- `GET /api/v1/auth/me` with no `Authorization` header returns `401`.
- `GET /api/v1/auth/me` with a malformed or expired JWT returns `401`.
- `GET /api/v1/auth/me` with a JWT signed by a different secret (simulating
  a forged token) returns `401`.
- `POST /api/v1/auth/logout` with a valid JWT returns a successful
  acknowledgement response.
- The authentication dependency is implemented once and is structurally
  reusable by a different route without duplicating its logic (verify by
  using it in both `/me` and `/logout`, not by copy-pasting the decode
  logic into each route).

## Testing Requirements

Per `05-testing-rules.md`:

- Test: `/me` with valid token succeeds and returns correct data.
- Test: `/me` with missing token returns `401`.
- Test: `/me` with expired token returns `401`.
- Test: `/me` with a token signed by an incorrect secret returns `401`.
- Test: `/logout` with a valid token returns a successful response.
- Test: `/logout` with an invalid token returns `401` (it is still a
  protected route, per Design Document §8's "Auth: JWT").

## Security Requirements

- Token validation checks signature, expiry, and structure — not just
  "does a token exist."
- No token content (even partially) is logged.
- `/me`'s response never includes the password hash or any other sensitive
  internal field.

## Error Handling Requirements

- Every authentication failure path returns the project's structured
  `401` shape established in `EPIC-0-BE-001`, not a raw exception.

## Documentation Requirements

- Kidus updates the requirements-traceability entry to reflect that
  session validation (`/me`, `/logout`) is implemented, and that no
  server-side session/refresh-token store exists in V1.0 by design.

## Commit Guidance

- Branch: `feature/auth-session-dependency`, from `develop`.
- Commit message pattern: `feat(auth): add authentication dependency, /me, and /logout endpoints`.
- PR references Task ID `EPIC-1-AUTH-003`.
- Merge target: `develop`.

## AI Agent Safety Notes

- Do not add role/permission checks in this task's dependency — keep
  authentication (who are you) and authorization (are you allowed) as
  separate concerns; authorization is `AUTH-004`.
- Do not build a server-side token blocklist or session store "to make
  logout more real" — this is an explicit Design Document simplification,
  not an oversight to correct.

## Expected Agent Report

1. Confirmation that the same authentication dependency is used by both
   `/me` and `/logout` without duplicated decode logic.
2. The exact set of failure conditions tested (missing token, expired,
   malformed, wrong signature) and their results.
3. Any point where a requirement was unclear or untraceable, and how it was
   handled.
4. Test results.
