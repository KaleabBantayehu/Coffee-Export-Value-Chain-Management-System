# Task Title

Frontend Farmer Registration & List/Details View

## Task ID

EPIC-2-FARM-005

## Epic

EPIC 2 — Farmer & Polygon Registry

## Owner

Biniyam (Frontend Lead), with Yedenekachew (backend/domain support for the
Farmer API contract), per Implementation Specification EPIC 2's explicit
dual frontend listing ("Biniyam + Yedenekachew").

## Status

Not started.

## Priority

High. On the primary acceptance path, but able to proceed in parallel with
`FARM-003`/`FARM-004`'s backend work once `FARM-002` merges (see
`00-epic-overview.md`'s Parallelization Opportunities).

## Objective

Implement the React frontend for farmer registration (a form calling
`POST /api/v1/farmers`) and a farmer list/details view (calling
`GET /api/v1/farmers?search=` and `GET /api/v1/farmers/{id}`), reusing the
authentication state and protected-route mechanism `EPIC-1-AUTH-006`/
`EPIC-1-AUTH-007` already established.

## Why This Task Exists

Design Document §9.2 lists "Farmer registration form" as the first
Field/Registry Agent screen. Baseline §4 lists "Register Farmer" as the
second step of the primary acceptance workflow — the workflow cannot be
demonstrated without a real UI for it, not just a working API.

## Authoritative Sources

- Design Document §9.2 ("Field / Registry Agent... Farmer registration
  form.")
- Design Document §9.1 ("Admin / ECTA Officer... Farmer registry:
  searchable list, farmer detail view with linked farms and lots.")
- Design Document §8 (Farmers API contract, from `FARM-002`)
- Design Document §4.2 (the narrowed farmer field list)

## Requirements Traceability

```text
SRS:
- Not directly cited beyond FR-FARM-001, already traced under FARM-001/
  FARM-002; the frontend screen itself is a Design Document UI
  deliverable, not a separately numbered SRS requirement.

Design Document:
- Section 9.1 (farmer registry list/detail view, described under
  Admin/ECTA Officer screens)
- Section 9.2 (farmer registration form, described under Field/Registry
  Agent screens)
- Section 8 (the API contract this task's frontend must match exactly)

Implementation Specification:
- EPIC 2, Frontend Tasks: "Farmer registration form, list/details view..."

Minimum Project Plan:
- Week 2 Key Activities: "begin Authentication & RBAC and Farmer &
  Polygon Registry (backend + frontend)" — confirms frontend work is
  scheduled alongside backend, not deferred to a later week.

Baseline Scope Freeze:
- Section 2, Technology Baseline — React + JavaScript (frontend framework)
- Section 4, Critical Workflow — "Register Farmer"
```

## Dependencies

`EPIC-2-FARM-002` (Farmer API contract — this task builds against it
exactly as implemented, not as guessed) and `EPIC-1-AUTH-006`/
`EPIC-1-AUTH-007` (auth state and protected routing, already established).

## Preconditions

- `FARM-002` merged and reachable from the frontend's configured API base
  URL.
- `EPIC-1-AUTH-006`/`EPIC-1-AUTH-007` merged; the existing React frontend
  project (confirmed present per the current project state — `frontend/`
  already exists with `src/`, `package.json`, etc.) is used as-is. Per
  `.agents/rules/01-scope-boundaries.md` and the current project state, do
  not scaffold a new frontend project or run `npm create vite` — the
  frontend already exists.
- Confirm the actual, current shape of `FARM-002`'s API responses by
  inspecting its implementation/tests (per
  `.agents/execution/01-agent-start-procedure.md` Step 4) rather than
  assuming the shape from this task file's paraphrase of Design Document
  §8.

## Allowed Scope

- A farmer registration form component (full name, national ID, gender,
  phone number, optional cooperative selector — matching `FARM-002`'s
  field list exactly, no more, no fewer).
- A farmer list/search view (calling `GET /api/v1/farmers?search=`) and a
  farmer detail view (calling `GET /api/v1/farmers/{id}`).
- Client-side display of the generated FIN after successful registration.
- Client-side validation mirroring the backend's required-field rules
  (defense in depth — the backend remains the authority per
  `.agents/rules/03-coding-rules.md`'s "do not rely on frontend validation
  alone").
- Wiring these screens into the existing role-aware navigation from
  `EPIC-1-AUTH-007`, visible to Field/Registry Agent (registration) and to
  all authenticated roles (list/detail view, per Design Document §8's
  "Auth: JWT" on the `GET` endpoints).

## Out of Scope

- Farm registration or polygon capture UI (`FARM-006`).
- Any change to `EPIC-1`'s auth state, routing, or navigation mechanism
  beyond adding new routes/nav items to it.
- Building a new frontend project or replacing the existing React/Vite
  setup.
- Household size, bank/Telebirr, SMS OTP, or ID-photo-capture UI (not part
  of `FARM-002`'s implemented field list).

## Files/Directories Potentially Affected

Indicative paths — **must be confirmed against the actual existing
frontend project structure** (established prior to EPIC 1 per the current
project state, and extended by `EPIC-1-AUTH-006`/`007`):

- `frontend/src/pages/FarmerRegistration.jsx` (or equivalent).
- `frontend/src/pages/FarmerList.jsx` / `FarmerDetail.jsx` (or a combined
  component, matching whatever pattern the existing frontend already
  uses).
- `frontend/src/api/farmers.js` (or equivalent API client module,
  matching the pattern established by `EPIC-1-AUTH-006`'s `api/auth.js`).
- `frontend/src/tests/` (or wherever frontend tests already live).

## Implementation Requirements

- The registration form submits exactly `FARM-002`'s accepted fields and
  handles both success (displaying the generated FIN) and failure
  (duplicate national ID, missing field) responses distinctly.
- The list/search view supports searching by FIN, name, or cooperative,
  matching `FARM-002`'s `GET /api/v1/farmers?search=` contract.
- The detail view displays the farmer's profile and, once `FARM-003`
  exists, will show linked farms — for this task, an empty "linked farms"
  section is expected and correct if no farms exist yet, matching
  `FARM-002`'s documented behavior at this point in the epic.
- Route protection: only an authenticated user reaches these screens
  (via `EPIC-1-AUTH-007`'s existing guard); registration specifically is
  only reachable/actionable for Field/Registry Agent or Admin — a
  different authenticated role should see the list/detail view (a "GET"-
  level permission) but not a usable registration action, mirroring the
  backend's own role split rather than inventing a different frontend-only
  rule.

## Acceptance Criteria

- An authenticated Field/Registry Agent can submit the registration form
  with valid data and sees the generated FIN displayed on success.
- Submitting the form with a duplicate national ID displays the backend's
  error without the frontend inventing a more specific message than the
  backend actually returns.
- Submitting the form with a missing required field is caught by
  client-side validation before the request is sent, and would also be
  correctly rejected if that validation were bypassed (confirmed by a test
  that calls the API client directly).
- The list/search view returns and displays correct results for each of
  the three supported search criteria.
- The detail view correctly displays a registered farmer's profile.
- Navigating to the registration screen while unauthenticated redirects to
  login, per `EPIC-1-AUTH-007`'s existing route protection.
- An authenticated role without Field/Registry Agent or Admin permissions
  can view the list/detail screens but does not see a functional
  registration action.

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- Test: successful registration displays the FIN.
- Test: duplicate-national-ID failure displays the correct error.
- Test: missing-field client-side validation blocks submission.
- Test: search by each of the three criteria returns correct results.
- Test: detail view renders a farmer's profile correctly.
- Test: unauthenticated access redirects to login.
- Test: a non-Field/Registry-Agent, non-Admin authenticated role sees the
  list/detail view but not a usable registration action.

## Security Requirements

- No farmer PII (national ID, phone number) is logged to the browser
  console in committed code.
- The JWT used to call these endpoints is sourced from `EPIC-1-AUTH-006`'s
  existing auth state — this task does not implement its own token
  handling.

## Error Handling Requirements

- Network/API failures are handled with a user-visible error state, not a
  silent failure or unhandled promise rejection, consistent with
  `EPIC-1-AUTH-006`'s established pattern.

## Documentation Requirements

- Kidus updates the requirements-traceability entries for Design Document
  §9.1/§9.2's farmer-related screens to "implemented."

## Commit Guidance

- Branch: `feature/EPIC-2-FARM-005-frontend-farmer-registration`, from
  `develop`.
- Commit message pattern: `feat(farmer): implement frontend farmer registration and list/detail views`.
- PR references Task ID `EPIC-2-FARM-005`.
- Merge target: `develop`.

## Verification Requirements

Self-review per `.agents/execution/03-verification-and-testing.md`;
confirm the actual `FARM-002` API response shape was inspected (not
assumed) before building the client, per
`.agents/execution/01-agent-start-procedure.md` Step 4.

## Escalation / Change-Control Conditions

- If `FARM-002`'s actual implemented response shape differs from this task
  file's paraphrase of Design Document §8 in a way that matters for the
  UI, escalate per `.agents/execution/06-failure-and-escalation.md` rather
  than silently adapting the frontend to an undocumented backend behavior
  — the backend and this task file might both need correcting, and that is
  not this task's call to make alone.

## Expected Agent Report

Standard format from `.agents/execution/04-human-review-and-approval.md`,
plus:

1. Confirmation that `FARM-002`'s actual API response shape was inspected
   before implementation.
2. Confirmation that no field outside `FARM-002`'s accepted list appears
   in the registration form.
3. Test results.
