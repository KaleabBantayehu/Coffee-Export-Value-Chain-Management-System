# Task Title

Login Endpoint & JWT Issuance

## Task ID

EPIC-1-AUTH-002

## Epic

EPIC 1 — Authentication & Role-Based Access Control

## Owner

Kaleab (Backend/Auth)

## Status

Not started.

## Priority

Critical.

## Objective

Implement `POST /api/v1/auth/login`: accept a username and password, verify
the credentials against the `User` table using the hashing utility from
`AUTH-001`, and issue a signed JWT carrying the user's ID and role claim on
success.

## Why This Task Exists

This is the entry point of the entire CEVCMS acceptance workflow (Baseline
§4: "Login" is step one of the primary acceptance path). No other module
can be demonstrated without it.

## Authoritative Sources

- Design Document §4.1 ("Login: username/e-mail + password submitted over
  HTTPS; password verified against a bcrypt/Argon2 hash... Session
  handling: a signed JWT access token (short expiry, e.g. 30-60 minutes) is
  issued on successful login, carrying the user's ID and role claim; no
  refresh-token/HSM infrastructure is built")
- Design Document §8 (API Design — Authentication table:
  `POST /api/v1/auth/login` — Auth: None — "Body: username, password.
  Returns: JWT, role, expiry.")
- Design Document §13, Sequence 1 (User Login sequence diagram)
- Design Document §10 (Security Design — "rate-limiting on the login
  endpoint, generic error messages on failed login (no 'user not found' vs
  'wrong password' distinction), and parameterized queries throughout")

## Requirements Traceability

```text
SRS:
- Module 01 (FR-AUTH-001) — password-based login and JWT issuance portion.
  FR-AUTH-001's MFA, refresh-token pair (15 min/8 hour), and 1.2-second
  acceptance-time target are enterprise specifics narrowed away by Design
  Document §4.1/§18; this task implements the single short-lived access
  token version instead. The 5-failed-attempt account lockout described in
  FR-AUTH-001 is likewise not carried forward — Design Document §4.1
  substitutes "rate-limiting on the login endpoint" instead. This
  substitution is a Design Document decision, not one invented by this
  task.

Design Document:
- Section 4.1 (Login and session handling design)
- Section 8 (POST /api/v1/auth/login contract)
- Section 13, Sequence 1 (login sequence)
- Section 10 (rate-limiting, generic error messages)

Implementation Specification:
- EPIC 1, Backend Tasks: "...login endpoint, JWT generation/validation..."

Minimum Project Plan:
- Not available — see EPIC-1 overview traceability note.

Baseline Scope Freeze:
- Section 4, Critical Workflow — "Login" (first step of the primary
  acceptance path)

Implementation Playbook:
- Section 3, confirmed environment ("JWT: python-jose")
```

## Dependencies

`EPIC-1-AUTH-001` (hashing utility and at least one real user account to
authenticate against).

## Preconditions

- `AUTH-001` merged to `develop`; bootstrap Admin user exists and its
  plaintext credential is known to the implementer for testing.

## Allowed Scope

- The `POST /api/v1/auth/login` route.
- JWT signing/issuance logic (encoding user ID and role claim, setting a
  short expiry per Design Document §4.1).
- Basic rate-limiting on this specific endpoint.
- Generic (non-distinguishing) error responses for failed login attempts.

## Out of Scope

- JWT validation/decoding on protected routes — that is `AUTH-003`
  (authentication dependency).
- Any role-based authorization logic — that is `AUTH-004`.
- `GET /auth/me` and `POST /auth/logout` — that is `AUTH-003`.
- Refresh tokens, MFA/OTP, account lockout after N failed attempts (see
  Requirements Traceability note above), HSM/RS256 signing.
- Any user-management endpoint (`AUTH-005`).

## Files/Directories Potentially Affected

Indicative paths, to be matched against the actual `EPIC-0-BE-001` layout:

- `backend/app/api/v1/auth.py` (or equivalent existing auth router
  location) — the login route.
- `backend/app/core/security.py` (from `AUTH-001`) — extended with JWT
  encoding logic.
- `backend/app/schemas/auth.py` (or equivalent) — request/response schemas
  for login (username/password in; JWT/role/expiry out).
- `backend/tests/` — login endpoint tests.

## Implementation Requirements

- Request body: username, password (per Design Document §8).
- On success: return a JWT, the user's role, and the token's expiry,
  matching the Design Document §8 response description.
- The JWT payload carries at minimum the user's ID and role claim (Design
  Document §4.1).
- The JWT is signed with a server-held secret read from an environment
  variable (Design Document §10) — not a hard-coded secret, not an HSM key.
- Token expiry is short (30–60 minutes), per Design Document §4.1. The
  exact value within that range is an implementation decision; record the
  chosen value in the `Expected Agent Report`.
- On failure (unknown username or wrong password), return the same generic
  error response regardless of which is wrong, per Design Document §10.
- Apply basic rate-limiting to this endpoint (e.g., a request-count limit
  per IP/username over a time window) using a mechanism available in the
  existing approved stack — do not introduce a new infrastructure component
  (e.g., Redis) to implement this; if the simplest available in-process
  approach is insufficient, flag it as an open item rather than adding new
  infrastructure unilaterally.
- Use parameterized queries / the ORM's standard query interface throughout
  — never raw string-interpolated SQL, per Design Document §10.

## Acceptance Criteria

- A `POST /api/v1/auth/login` request with the bootstrap Admin's correct
  username and password returns `200` with a JWT, the role `"Admin"`, and
  an expiry value.
- The returned JWT, when decoded (e.g., in a test), contains the correct
  user ID and role claim.
- A request with a correct username but wrong password returns the same
  error shape and status code as a request with a nonexistent username —
  the response does not reveal which was wrong.
- Repeated rapid failed login attempts against the same endpoint are
  eventually rejected by the rate-limiting mechanism rather than processed
  indefinitely.
- No SQL is constructed via raw string interpolation anywhere in this
  task's code.

## Testing Requirements

Per `05-testing-rules.md`:

- Test: successful login with correct credentials returns a valid JWT and
  correct role.
- Test: login with wrong password returns the generic failure response.
- Test: login with a nonexistent username returns the identical generic
  failure response (same status/shape as the wrong-password case).
- Test: repeated failed attempts trigger the rate limit.
- Test: submitting a malformed request body (missing username or password)
  returns a structured `400`.

## Security Requirements

- JWT signing secret is read from an environment variable, never
  hard-coded, per `02-tech-stack.md` and Design Document §10.
- No password, hash, or JWT signing secret is ever logged.
- Error responses never distinguish "user not found" from "wrong password."

## Error Handling Requirements

- Malformed request body -> structured `400`.
- Invalid credentials -> structured `401` with the generic message
  described above.
- Rate limit exceeded -> structured `429` (or the project's equivalent
  structured-error convention established in `EPIC-0-BE-001`).

## Documentation Requirements

- Kidus updates the requirements-traceability entry for FR-AUTH-001 to
  "login/JWT issuance implemented; MFA/refresh-token/lockout narrowed per
  Design Document §4.1 — not implemented in V1.0" so the documentation
  stays honest about the deliberate simplification.

## Commit Guidance

- Branch: `feature/auth-login-jwt`, from `develop`.
- Commit message pattern: `feat(auth): implement login endpoint with JWT issuance`.
- PR references Task ID `EPIC-1-AUTH-002`.
- Merge target: `develop`.

## AI Agent Safety Notes

- Do not implement JWT validation on other routes in this task — that is
  `AUTH-003`/`AUTH-004`'s responsibility. Keep this task scoped to
  issuance only.
- Do not add MFA, refresh tokens, or account lockout — these were
  deliberately narrowed away; reintroducing them without a change-control
  decision would silently expand scope back toward the SRS's enterprise
  version.
- Do not add Redis or any new infrastructure component for rate limiting;
  if genuinely blocked, stop and flag it (`06-change-control.md`).

## Expected Agent Report

1. The exact token expiry chosen (within the 30–60 minute range) and why.
2. The rate-limiting mechanism used and its limits (e.g., N attempts per M
   minutes).
3. Confirmation that failed-login error responses are identical for
   "wrong password" and "user not found."
4. Any point where a requirement was unclear or untraceable, and how it was
   handled.
5. Test results.
