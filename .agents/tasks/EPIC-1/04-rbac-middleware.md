# Task Title

RBAC Authorization Middleware & Protected-Route Enforcement

## Task ID

EPIC-1-AUTH-004

## Epic

EPIC 1 — Authentication & Role-Based Access Control

## Owner

Kaleab (Backend/Auth)

## Status

Not started.

## Priority

Critical — this is the mechanism every later epic's protected routes will
depend on.

## Objective

Implement a reusable role-based authorization mechanism that checks whether
the authenticated user (resolved by `AUTH-003`'s dependency) has the role or
permission required for a given route, and apply it to at least one real
protected route within this task so the mechanism is proven working before
later epics rely on it.

## Why This Task Exists

Design Document §4.1 requires "an authorization middleware... on every
protected route." Design Document §12 states Authentication/RBAC "sits in
front of, and protects, every other module." Every future Farmer, Farm,
Traceability, and QR endpoint (Design Document §8) declares a required role
(e.g., "JWT + Field/Registry Agent or Admin") — this task builds the one
mechanism that will enforce all of those declarations consistently, per
Design Document §20 ("RBAC is applied consistently — the same middleware and
Role/Permission model is reused across Farmer, Farm, Lot, and (when reached)
stretch-module routes, rather than a bespoke check per module").

## Authoritative Sources

- Design Document §4.1 (authorization middleware description)
- Design Document §7.2 (`Role`, `Permission`, `RolePermission` entities)
- Design Document §12 (Module Interaction — "Authentication/RBAC sits in
  front of, and protects, every other module")
- Design Document §18 (Design Decisions — "Authorization model: RBAC only
  (no ABAC regional partitioning)... four roles and no regional
  partitioning is sufficient to demonstrate the concept")
- Design Document §20 (Design Validation — "the same middleware and
  Role/Permission model is reused across Farmer, Farm, Lot, and (when
  reached) stretch-module routes")

## Requirements Traceability

```text
SRS:
- Section 6.1, SEC-01 ("Implement Role-Based Access Control (RBAC) combined
  with Attribute-Based Access Control (ABAC) to enforce regional data
  partitioning"). Design Document §18 explicitly narrows this to
  RBAC-only for V1.0 — this task implements RBAC only; ABAC/regional
  partitioning is out of scope, not an oversight.

Design Document:
- Section 4.1 (authorization middleware)
- Section 7.2 (Role/Permission/RolePermission entities, from EPIC-0-DB-002)
- Section 12 (module interaction — Auth/RBAC protects every other module)
- Section 18 (RBAC-only decision)
- Section 20 (consistent middleware reuse requirement)

Implementation Specification:
- EPIC 1, Backend Tasks: "...Auth & Role middleware, protected API routes"

Minimum Project Plan:
- Not available — see EPIC-1 overview traceability note.

Baseline Scope Freeze:
- Section 3.1, "Authentication and RBAC"

Implementation Playbook:
- Section 8, Backend Architecture (Auth/RBAC as the first layer protecting
  all subsequent modules)
```

## Dependencies

`EPIC-1-AUTH-003` (authentication dependency — this task's authorization
check runs after authentication succeeds, using the user/role it resolves).

## Preconditions

- `AUTH-003` merged to `develop`.
- Role/Permission seed data from `AUTH-001` is present and correct.

## Allowed Scope

- A reusable authorization mechanism (e.g., a FastAPI dependency or
  decorator parameterized by required role(s)/permission(s)) that, given
  the user resolved by `AUTH-003`'s authentication dependency, allows or
  rejects the request.
- Application of this mechanism to `GET /api/v1/users` as the one
  real protected route proven within this task (this route will be fully
  implemented by `AUTH-005`; this task may implement it minimally — e.g.,
  returning the current user list with only Admin-role fields required for
  the authorization proof — provided `AUTH-005` is understood to complete
  its full implementation; if simpler, this task may instead prove the
  mechanism against a minimal placeholder route created solely for this
  test and removed once `AUTH-005` supplies the real one — record which
  approach was taken in the `Expected Agent Report`).
- Resolution of the "Verifier role authentication" open item flagged in the
  EPIC-1 overview's Role Model: this task must explicitly confirm, in its
  `Expected Agent Report`, whether the Verifier role requires its own
  authenticated login flow in V1.0 or exists in the `Role` table solely as
  a data-model placeholder for the public QR verification endpoint (which,
  per Design Document §5.3/§8, is unauthenticated by design and will not
  route through this task's authorization mechanism at all). Do not assume
  an answer and build a Verifier login flow speculatively — investigate
  Design Document §4.1, §5.3, §8, and §9.4 and report what they establish;
  if genuinely ambiguous, flag it for the Project Manager rather than
  deciding unilaterally.

## Out of Scope

- The full, final implementation of `GET/POST /api/v1/users` and
  `PATCH /api/v1/users/{id}/role` — that is `AUTH-005`; this task proves
  the authorization mechanism, it does not deliver the finished
  user-management feature.
- ABAC or regional data partitioning (explicitly narrowed away, see
  Requirements Traceability).
- Applying this mechanism to any Farmer, Farm, Traceability, or QR route —
  those routes do not exist yet (later epics); this task only proves the
  mechanism works, for reuse later.

## Files/Directories Potentially Affected

Indicative paths, to be matched against the actual `EPIC-0-BE-001` layout:

- `backend/app/core/security.py` (or equivalent) — the authorization
  dependency/decorator.
- `backend/app/api/v1/users.py` (or the placeholder route location chosen)
  — the one route this task protects as proof.
- `backend/tests/` — authorization tests.

## Implementation Requirements

- The mechanism must be parameterizable by role (at minimum) so a route can
  declare "Admin only," "Admin or Field/Registry Agent," etc., matching the
  per-route auth column already specified in Design Document §8 for future
  routes (e.g., "JWT + Admin," "JWT + Field/Registry Agent or Admin").
- An authenticated request whose role does not satisfy the route's
  requirement is rejected with `403` (distinct from `401`, which is reserved
  for "not authenticated at all," per `AUTH-003`).
- The mechanism must be reusable without modification by future epics — do
  not hard-code the "Admin" check into the mechanism itself in a way that
  would require rewriting it for a Field/Registry Agent-only route later.

## Acceptance Criteria

- A request to the protected route used as this task's proof, made with a
  valid Admin JWT, succeeds.
- The same request, made with a valid JWT for a role that does not have the
  required permission, is rejected with `403`.
- The same request, made with no token at all, is rejected with `401` (via
  `AUTH-003`'s dependency, confirming the two layers compose correctly).
- The mechanism's role/permission requirement is declared at the route
  level in a way that is visibly reusable (e.g., a parameter or decorator
  argument), not duplicated per-route logic.
- The `Expected Agent Report` explicitly answers the Verifier-role
  authentication question described in "Allowed Scope."

## Testing Requirements

Per `05-testing-rules.md`:

- Test: Admin-authorized request to the proof route succeeds.
- Test: authenticated-but-wrong-role request to the proof route returns
  `403`.
- Test: unauthenticated request to the proof route returns `401`.
- Test: the authorization mechanism correctly reads the seeded
  `RolePermission` data from `AUTH-001` rather than a hard-coded role name
  string, where the design calls for permission-based (not literal
  role-name) checks.

## Security Requirements

- Authorization checks happen server-side only; no reliance on
  frontend-supplied role claims outside the verified JWT.
- A `403` response does not leak information about what role *would* have
  been allowed beyond what Design Document §8's documented per-route
  requirements already make public knowledge (i.e., do not enumerate
  permitted roles in the error body if that were not already the case).

## Error Handling Requirements

- `403` responses use the project's structured error shape from
  `EPIC-0-BE-001`.
- The mechanism fails closed: if role/permission data cannot be resolved
  for any reason, the request is rejected, not allowed by default.

## Documentation Requirements

- Kidus updates the requirements-traceability entry for SEC-01 to record:
  "RBAC implemented; ABAC/regional partitioning explicitly out of scope per
  Design Document §18."
- The Verifier-role authentication finding (see Allowed Scope) is recorded
  in the traceability documentation so `AUTH-005`/`AUTH-006`/`AUTH-007`
  and later epics (public QR verification) build on a settled answer
  rather than re-investigating it.

## Commit Guidance

- Branch: `feature/auth-rbac-middleware`, from `develop`.
- Commit message pattern: `feat(auth): implement RBAC authorization mechanism`.
- PR references Task ID `EPIC-1-AUTH-004` and states which route was used
  as the proof-of-mechanism route.
- Merge target: `develop`.

## AI Agent Safety Notes

- Do not implement ABAC or any regional-partitioning logic.
- Do not apply this mechanism to any route outside Auth/RBAC's own scope in
  this task — that is scope creep into later epics.
- Do not guess an answer to the Verifier-role authentication question;
  investigate the cited sections and report findings, flagging genuine
  ambiguity rather than resolving it unilaterally.

## Expected Agent Report

1. Which route was used to prove the mechanism, and why (real
   `/users` route vs. a temporary placeholder).
2. The explicit answer to the Verifier-role authentication question, with
   the Design Document sections that support it.
3. Confirmation that the mechanism reads seeded permission data rather than
   hard-coded role-name strings (or an explanation if a role-name check was
   used instead, and why that is still consistent with Design Document
   §7.2's `Role`/`Permission` model).
4. Any point where a requirement was unclear or untraceable, and how it was
   handled.
5. Test results.
