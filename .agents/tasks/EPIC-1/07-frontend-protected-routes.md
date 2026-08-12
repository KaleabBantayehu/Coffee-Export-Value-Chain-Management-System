# Task Title

Frontend Protected Routes, Role-Aware Navigation, and Logout

## Task ID

EPIC-1-AUTH-007

## Epic

EPIC 1 — Authentication & Role-Based Access Control

## Owner

Biniyam (Frontend Lead)

## Status

Not started.

## Priority

Critical — completes the frontend half of the Auth/RBAC epic and is the
last piece needed before later epics can add their own protected screens
behind it.

## Objective

Implement client-side route protection (unauthenticated users cannot reach
screens that require login), role-aware navigation (each of the four V1.0
roles sees only the navigation appropriate to it), and the logout flow
(calling `POST /api/v1/auth/logout` and clearing client-side auth state).

## Why This Task Exists

Design Document §9 groups all V1.0 screens by role. A frontend that lets any
authenticated user reach any screen regardless of role does not reflect the
Design Document's UI design, and does not let the team demonstrate RBAC
working end to end (Baseline §4's acceptance path implicitly assumes the
right actor performs each step). This task is also what makes
`EPIC-1-AUTH-006`'s auth state actually useful, by gating real navigation on
it.

## Authoritative Sources

- Design Document §9 ("Screens are grouped by the roles implemented in
  Version 1.0") and its subsections §9.1–§9.4 (per-role screen lists)
- Design Document §4.1 ("Logout / token expiration: logout is client-side
  token discard")
- Implementation Specification EPIC 1, Frontend Tasks: "...protected
  routes, role-aware navigation, logout handling"

## Requirements Traceability

```text
SRS:
- Not directly cited beyond the role model already traced in AUTH-004's
  overview reference (Module 01 / FR-AUTH context); role-aware navigation
  itself is a Design Document UI deliverable, not a separately numbered SRS
  requirement.

Design Document:
- Section 9 (all subsections — per-role screen groupings)
- Section 4.1 (logout as client-side token discard)

Implementation Specification:
- EPIC 1, Frontend Tasks: "protected routes, role-aware navigation, logout
  handling"

Minimum Project Plan:
- Not available — see EPIC-1 overview traceability note.

Baseline Scope Freeze:
- Section 4, Critical Workflow (every step after Login assumes the correct
  authenticated, role-appropriate actor is performing it)

Implementation Playbook:
- Section 3, Frozen Technology Stack (React + JavaScript)
```

## Dependencies

`EPIC-1-AUTH-006` (login page and auth state — this task consumes that
state) and `EPIC-1-AUTH-004` (RBAC role semantics on the backend, so the
frontend's role-based navigation logic matches what the backend will
actually permit for each role, avoiding a frontend that shows a screen the
backend will simply reject).

## Preconditions

- `AUTH-006` merged to `develop`.
- `AUTH-004` merged to `develop` (for the authoritative role/permission
  model this task's navigation logic should mirror).

## Allowed Scope

- A route-protection mechanism (e.g., a wrapper/guard component) that
  redirects an unauthenticated user to the login page when they attempt to
  reach a route that requires authentication.
- Role-aware navigation: rendering only the navigation items relevant to
  the current user's role, per Design Document §9.1–§9.4's per-role screen
  groupings.
- A logout action that calls `POST /api/v1/auth/logout`, clears the
  client-side auth state established in `AUTH-006`, and redirects to the
  login page.

## Out of Scope

- Building the actual destination screens for Farmer registration, Farm/
  Polygon capture, Traceability, or QR (Design Document §9.2/§9.3) — those
  screens belong to their respective later epics (EPIC 2–4). This task
  only builds the routing/navigation shell and gating logic; placeholder
  routes are acceptable for screens that do not exist yet, provided they
  are clearly marked as placeholders and not presented as finished
  functionality.
- Server-side session invalidation on logout (not built in V1.0, per
  Design Document §4.1 — logout remains a client-side-only action backed by
  token expiry).
- Any change to the RBAC role/permission model itself — that is
  `AUTH-004`'s domain; this task only reads and reflects it.

## Files/Directories Potentially Affected

Indicative paths, to be matched against the actual frontend project
structure confirmed in `AUTH-006`:

- `frontend/src/routes/ProtectedRoute.jsx` (or equivalent route-guard
  component).
- `frontend/src/components/Navigation.jsx` (or equivalent, made
  role-aware).
- `frontend/src/context/AuthContext.jsx` (from `AUTH-006`) — extended with
  a logout action if not already present.
- `frontend/src/tests/` — tests for route protection, role-aware nav, and
  logout.

## Implementation Requirements

- An unauthenticated user attempting to reach any route other than the
  login page is redirected to login.
- Navigation renders differently for each of the four roles, matching
  Design Document §9's groupings at least at the level of which top-level
  sections are visible (e.g., an Admin sees user/role management; a
  Field/Registry Agent sees farmer/farm registration entry points once
  those exist; a Verifier's authenticated navigation, if any, reflects
  whatever `AUTH-004`'s findings on Verifier authentication established —
  reuse that finding rather than re-deciding it here).
- Logout clears the JWT/role from client-side state, calls
  `POST /auth/logout`, and returns the user to the login page; after
  logout, previously-reachable protected routes are no longer reachable
  without logging in again.
- Placeholder routes for not-yet-built screens (Farmer, Farm, Traceability,
  QR) are visually and functionally distinguishable as placeholders — not
  broken links, but not implying finished functionality either.

## Acceptance Criteria

- Navigating directly to a protected route URL while unauthenticated
  redirects to the login page.
- After logging in as the bootstrap Admin, the navigation shown includes
  Admin-appropriate items (per Design Document §9.1) and does not include
  items exclusive to a different role's screen grouping.
- Clicking logout clears auth state, calls the logout endpoint, and returns
  to the login page.
- After logout, attempting to navigate back to a previously-reachable
  protected route redirects to login again (confirms state was actually
  cleared, not just visually hidden).
- The navigation/role mapping used by the frontend is consistent with the
  role/permission findings established in `AUTH-004`'s `Expected Agent
  Report` (in particular, the Verifier-role authentication answer).

## Testing Requirements

Per `05-testing-rules.md`:

- Test: unauthenticated access to a protected route redirects to login.
- Test: authenticated Admin sees Admin-appropriate navigation.
- Test: authenticated non-Admin does not see Admin-only navigation items.
- Test: logout clears auth state and redirects to login.
- Test: a protected route is unreachable immediately after logout without
  re-authenticating.

## Security Requirements

- Route protection is a UX convenience, not a security boundary by itself
  — the task must not create a false impression that hiding a navigation
  item is equivalent to the backend's actual RBAC enforcement (`AUTH-004`).
  Document this distinction in code comments if helpful for future
  developers/agents.
- Auth state is fully cleared on logout — no residual token left in memory
  or storage that would allow a stale request to succeed after logout.

## Error Handling Requirements

- If the logout API call fails (e.g., network error), the frontend still
  clears local auth state and returns the user to login, rather than
  leaving them in a broken authenticated-but-unable-to-do-anything state.

## Documentation Requirements

- Kidus updates the requirements-traceability entries for Design Document
  §9.1–§9.4 to reflect which screens are fully implemented in this task
  (navigation shell only) versus placeholder, so later epics know exactly
  what they are replacing.

## Commit Guidance

- Branch: `feature/frontend-protected-routes`, from `develop`.
- Commit message pattern: `feat(auth): implement protected routes, role-aware navigation, and logout`.
- PR references Task ID `EPIC-1-AUTH-007` and lists which routes are real
  versus placeholder.
- Merge target: `develop`.

## AI Agent Safety Notes

- Do not build out full Farmer/Farm/Traceability/QR screens under cover of
  "just making the placeholder more complete" — placeholders stay
  placeholders until their own epic.
- Do not treat frontend route hiding as a substitute for backend RBAC
  enforcement in any documentation or communication about this task's
  security properties.

## Expected Agent Report

1. Confirmation of which routes are fully functional versus placeholder,
   and how placeholders are marked.
2. Confirmation that the role-to-navigation mapping matches Design
   Document §9.1–§9.4 and `AUTH-004`'s Verifier-role finding.
3. Confirmation that auth state is fully cleared on logout, including how
   this was verified.
4. Any point where a requirement was unclear or untraceable, and how it was
   handled.
5. Test results.
