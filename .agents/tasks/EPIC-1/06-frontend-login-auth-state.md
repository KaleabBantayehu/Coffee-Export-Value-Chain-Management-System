# Task Title

Frontend Login Page & Auth State Management

## Task ID

EPIC-1-AUTH-006

## Epic

EPIC 1 — Authentication & Role-Based Access Control

## Owner

Biniyam (Frontend Lead), per Baseline §5 and Implementation Specification
EPIC 1 ownership.

## Status

Not started.

## Priority

Critical — the first user-visible piece of the entire acceptance workflow.

## Objective

Implement the React login page and client-side authentication state
management: submit credentials to `POST /api/v1/auth/login`, store the
returned JWT and role for the session, and expose that state to the rest of
the frontend application.

## Why This Task Exists

Baseline §4 lists "Login" as the first step of the primary acceptance
workflow. Without a working frontend login, none of the workflow can be
demonstrated even if every backend endpoint is correct.

## Authoritative Sources

- Design Document §9.1 ("Login screen" — listed first under Admin/ECTA
  Officer screens)
- Design Document §9.2 ("Field / Registry Agent" screens — implies the same
  login screen is shared across roles, with role-specific navigation
  applied afterward, per §9's framing "Screens are grouped by the roles
  implemented in Version 1.0")
- Design Document §13, Sequence 1 (User Login sequence: "creds -> POST
  /auth/login -> ... -> JWT + role -> nav to role dashboard")
- Design Document §8 (login request/response contract, from `AUTH-002`)

## Requirements Traceability

```text
SRS:
- Not directly cited; the frontend login screen is a Design Document/
  Implementation Specification deliverable implementing the backend
  requirement already traced under FR-AUTH-001 in AUTH-002/AUTH-003.

Design Document:
- Section 9.1 (Login screen)
- Section 13, Sequence 1 (login sequence, frontend side)

Implementation Specification:
- EPIC 1, Frontend Tasks: "Login page UI, auth state management..."

Minimum Project Plan:
- Not available — see EPIC-1 overview traceability note.

Baseline Scope Freeze:
- Section 4, Critical Workflow — "Login" (first step)
- Section 2, Technology Baseline — React + JavaScript (frontend framework)

Implementation Playbook:
- Section 3, Frozen Technology Stack (Frontend: React + JavaScript)
```

## Dependencies

`EPIC-1-AUTH-002` (login endpoint contract) and `EPIC-1-AUTH-003`
(`GET /auth/me` contract, used to confirm the session and fetch role/profile
after login).

## Preconditions

- **Verify, before any other work, that a React frontend project already
  exists in the repository** (per the EPIC-1 overview's flagged
  precondition gap: the EPIC-0 task files committed to this repository
  covered backend infrastructure only, and no confirmed EPIC-0 frontend
  scaffold task exists). If a React project is found, proceed within it,
  matching its existing structure and conventions. **If no React project is
  found, stop and report this as a blocking gap rather than silently
  initializing a new one** — frontend project initialization was described
  as part of EPIC 0 in the Implementation Specification but is not covered
  by any committed EPIC-0 task file, and creating one now would be
  infrastructure work outside this task's declared scope and outside this
  task's authority to decide unilaterally (see `06-change-control.md`).
- `AUTH-002` and `AUTH-003` merged to `develop` and reachable from the
  frontend's configured API base URL.

## Allowed Scope

- A login page/component (form: username, password, submit).
- A call to `POST /api/v1/auth/login`.
- Client-side auth state management (storing the JWT and role for the
  current session, and making that state available to the rest of the
  application — e.g., via React context or an equivalent mechanism already
  consistent with the existing frontend project's patterns, if one exists).
- A call to `GET /api/v1/auth/me` after login (or immediately using the
  role returned by the login response itself, per Design Document §8's
  "Returns: JWT, role, expiry" — either satisfies the requirement; do not
  make a redundant second call if the login response already provides what
  is needed, per `03-coding-rules.md`'s "no unnecessary abstraction"
  guidance).
- Basic client-side display of login failure (e.g., "invalid username or
  password" — matching the backend's generic error, not inventing a more
  specific message the backend does not actually distinguish).

## Out of Scope

- Protected route logic and role-aware navigation — that is `AUTH-007`.
- Logout button/flow beyond what is needed to demonstrate auth state can be
  cleared — the full logout UX (calling `POST /auth/logout` and clearing
  routes) is `AUTH-007`'s responsibility; this task only needs to prove the
  auth state mechanism can be set and read.
- Any styling/design-system work beyond what is needed for a functional,
  usable login form — this is a course-scale prototype, not a polished
  product; do not over-invest in visual design at the expense of the
  remaining EPIC-1 backend/frontend tasks within the four-week schedule.
- Initializing a new frontend project (see Preconditions — flag and stop
  instead).

## Files/Directories Potentially Affected

Indicative paths — **must be confirmed against the actual existing
frontend project structure, if one exists**, rather than assumed:

- `frontend/src/pages/Login.jsx` (or equivalent, matching existing
  conventions).
- `frontend/src/context/AuthContext.jsx` (or equivalent auth-state
  mechanism).
- `frontend/src/api/auth.js` (or equivalent API client module).
- `frontend/src/tests/` (or wherever frontend tests already live).

## Implementation Requirements

- The login form submits username and password to
  `POST /api/v1/auth/login` and handles both success and failure responses.
- On success, the JWT and role are stored in client-side state accessible
  to the rest of the application for the duration of the session.
- On failure, the generic error message returned by the backend is
  displayed to the user without alteration into something more specific
  than the backend actually distinguishes (consistent with `AUTH-002`'s
  deliberate "no 'user not found' vs 'wrong password' distinction").
- No token is persisted in a way that violates
  `persistent_storage_for_artifacts`-style browser-storage restrictions if
  this frontend is ever rendered as an Artifact; for the actual CEVCMS
  React application (not an Artifact), standard React state/context is
  sufficient and preferred over introducing a new state-management library
  not already part of the approved stack.

## Acceptance Criteria

- Submitting valid bootstrap-Admin credentials on the login form results in
  the application holding a valid JWT and the correct role in its
  client-side state.
- Submitting invalid credentials displays the backend's generic error
  message and does not set any auth state.
- The stored auth state is accessible from at least one other component
  (proven in this task by a simple demonstration, e.g., a temporary debug
  display or a unit test reading the context — full role-aware navigation
  is `AUTH-007`).

## Testing Requirements

Per `05-testing-rules.md`:

- Test: successful login sets auth state correctly (JWT and role present).
- Test: failed login does not set auth state and surfaces the generic
  error message.
- Test: the auth-state mechanism is readable from a component other than
  the login page itself.

## Security Requirements

- The JWT is not logged to the browser console in production-style code
  paths (temporary debug logging, if used during development, must be
  removed before commit).
- No credential (username/password) is stored beyond the lifetime of the
  submit action.

## Error Handling Requirements

- Network/API failures (e.g., backend unreachable) are handled with a
  user-visible error state, not a silent failure or an unhandled promise
  rejection.

## Documentation Requirements

- Kidus updates the requirements-traceability entry for the frontend login
  screen (Design Document §9.1) to "implemented."

## Commit Guidance

- Branch: `feature/frontend-login-auth-state`, from `develop`.
- Commit message pattern: `feat(auth): implement login page and auth state management`.
- PR references Task ID `EPIC-1-AUTH-006` and confirms whether an existing
  frontend project was found and used, per the Preconditions check.
- Merge target: `develop`.

## AI Agent Safety Notes

- Do not initialize a new frontend project if none exists — stop and
  report per Preconditions.
- Do not introduce a new frontend state-management library (e.g., Redux,
  Zustand, MobX) without going through `06-change-control.md` — React's
  built-in state/context mechanisms are sufficient for V1.0's four roles
  and limited screen count.
- Do not implement route protection or navigation in this task — that is
  `AUTH-007`, to keep the two concerns independently reviewable.

## Expected Agent Report

1. Confirmation of whether an existing React frontend project was found,
   and its location/structure.
2. The auth-state mechanism chosen (e.g., React Context) and why it fits
   within the approved stack.
3. Whether a separate `GET /auth/me` call was made after login or the
   login response's own role/JWT was reused directly, and why.
4. Any point where a requirement was unclear or untraceable, and how it was
   handled.
5. Test results.
