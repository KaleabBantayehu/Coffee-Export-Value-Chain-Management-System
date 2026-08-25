# Task Title

Authentication & RBAC End-to-End Verification

## Task ID

EPIC-1-AUTH-008

## Epic

EPIC 1 — Authentication & Role-Based Access Control

## Owner

Ephratha (Backend & QA), with documentation updates by Kidus, per Baseline
§5 ("Ephratha... owns Postman API testing, unit and integration testing,
input validation, and RBAC security testing across all core modules...
Kidus... tracks requirements traceability, test-case documentation").

## Status

Not started (final task of EPIC 1).

## Priority

Critical — this is the gate that confirms EPIC 1's Definition of Done
before Farmer Registry (EPIC 2) begins, per the fixed dependency chain.

## Objective

Independently verify, end to end, that the whole of EPIC 1 (`AUTH-001`
through `AUTH-007`) satisfies the Implementation Specification's EPIC 1
Definition of Done and the Epic Acceptance Criteria stated in
`00-epic-overview.md`, using Postman for API-level verification and manual/
automated frontend verification, and update the project's requirements-
traceability documentation accordingly.

## Why This Task Exists

Each individual `AUTH-0xx` task tests its own slice in isolation. Nothing
so far has proven the whole chain — login through role-gated frontend
navigation and logout — works together as one coherent flow, using the
actual deployed/running system rather than each task's own unit tests. Per
Implementation Playbook §9, step 7 ("Integration test — confirm nothing
existing broke") and the Baseline's insistence that the critical workflow
must work "without manual database intervention," this task is the
checkpoint before EPIC 2 (Farmer Registry) is allowed to begin.

## Authoritative Sources

- Implementation Specification, EPIC 1 Definition of Done: "User can log
  in, receive valid JWT, access permitted routes based on role, be rejected
  from unauthorized endpoints, and securely log out."
- `00-epic-overview.md` (Epic Acceptance Criteria section, this directory)
- Implementation Playbook §9 (per-feature workflow, step 7: integration
  testing; step 9: documentation update)
- `.agents/rules/05-testing-rules.md` (testing categories and Definition of
  Done requirements)

## Requirements Traceability

```text
SRS:
- Consolidates FR-AUTH-001 (as narrowed across AUTH-001 through AUTH-004)
  and SEC-01/SEC-05 (as narrowed in AUTH-004/AUTH-005) — this task verifies
  the narrowed, V1.0 versions actually implemented, not the SRS's
  enterprise versions.

Design Document:
- Section 20, Design Validation ("Authentication protects every
  non-public route; the only unauthenticated route is the public QR
  verification endpoint" — not yet applicable in full since QR does not
  exist yet, but the authentication-protects-everything principle is
  verified here for every route that does exist after EPIC 1).

Implementation Specification:
- EPIC 1 Definition of Done (quoted above).

Minimum Project Plan:
- Not available — see EPIC-1 overview traceability note. This task is the
  natural point at which, if the Minimum Project Plan becomes available
  before EPIC 1 closes, its Week 1/Week 2 milestone language for
  Authentication should be checked against actual completion.

Baseline Scope Freeze:
- Section 4, Critical Workflow — "Login" step is now fully verified as a
  precondition for every later step.

Implementation Playbook:
- Section 9, steps 7 and 9 (integration testing; documentation update)
```

## Dependencies

`EPIC-1-AUTH-001` through `EPIC-1-AUTH-007`, all merged to `develop`.

## Preconditions

- All seven preceding EPIC-1 tasks report their Definition of Done
  satisfied and are merged into `develop`.
- A locally runnable instance of both backend and frontend is available for
  manual verification.

## Allowed Scope

- Building and running a Postman collection (or extending an existing one,
  if `AUTH-002`–`AUTH-005` already produced individual Postman requests, per
  `05-testing-rules.md`) covering the full set of Epic Acceptance Criteria.
- Manual and/or automated frontend verification of the login -> role-aware
  navigation -> logout flow.
- Updating the requirements-traceability matrix and test documentation to
  reflect EPIC 1's actual, verified completion state (owned by Kidus).
- Filing defects (per Baseline §5, Ephratha "owns defect tracking") against
  any `AUTH-0xx` task found not to satisfy its own acceptance criteria
  during this verification — not fixing them directly under this task's
  scope unless the fix is trivial and clearly within one already-completed
  task's boundaries; substantive fixes go back to the relevant task/owner.

## Out of Scope

- Implementing new functionality — this is a verification and
  documentation task, not an implementation task. Any gap found is filed as
  a defect against the relevant `AUTH-0xx` task, not silently patched here.
- Beginning any EPIC 2 (Farmer Registry) work, even if this verification
  passes cleanly — EPIC 2 begins as its own, separately created task set.
- Load, performance, or penetration testing (explicitly out of scope per
  `05-testing-rules.md` and Baseline §3.3).

## Files/Directories Potentially Affected

- A Postman collection file (location consistent with wherever
  `AUTH-002`–`AUTH-005` already placed their individual requests, per
  `05-testing-rules.md`'s API-testing requirement).
- Project documentation / requirements-traceability matrix (owned by
  Kidus — exact location per the project's existing documentation
  structure, not invented by this task).
- No application source code should need to change as a result of this
  task; if it does, that change belongs to whichever `AUTH-0xx` task owns
  the affected area, reopened as a defect fix.

## Implementation Requirements

This task "implements" a verification procedure, not application code:

1. Confirm login succeeds for the bootstrap Admin and fails correctly for
   bad credentials (`AUTH-002`).
2. Confirm `/auth/me` and `/auth/logout` behave correctly, including all
   `401` cases (`AUTH-003`).
3. Confirm RBAC `403`/`401` behavior on the proof route(s) established in
   `AUTH-004`.
4. Confirm the three user-management endpoints correctly enforce Admin-only
   access and behave correctly for duplicate usernames, invalid roles, and
   audit logging (`AUTH-005`).
5. Confirm the frontend login flow, auth-state propagation, and error
   display (`AUTH-006`).
6. Confirm frontend route protection, role-aware navigation, and logout
   (`AUTH-007`), including the "unreachable after logout" behavior.
7. Confirm the Verifier-role authentication question (raised in `AUTH-004`,
   consumed in `AUTH-007`) was answered consistently across both backend
   and frontend — this is specifically checked here because it is the one
   item in EPIC 1 flagged as requiring cross-task consistency.

## Acceptance Criteria

- Every Epic Acceptance Criterion listed in `00-epic-overview.md` is
  independently confirmed true, with evidence (Postman run results,
  frontend test/manual-verification notes).
- Any criterion found not to be satisfied is filed as a defect against the
  owning `AUTH-0xx` task, with enough detail (request/response, screenshot,
  or reproduction steps) for that task's owner to act on it without
  re-discovering the problem.
- The requirements-traceability matrix accurately reflects, for each
  relevant FR-xxx/SEC-xxx identifier touched by EPIC 1, its actual V1.0
  implementation status (implemented / narrowed-and-implemented / not
  implemented, with the narrowing reason).

## Testing Requirements

Per `05-testing-rules.md`:

- The full Postman collection for Auth/RBAC runs green end to end against
  a freshly seeded local environment.
- The existing automated test suites from `AUTH-001`–`AUTH-007` are
  re-run together (not just individually) and confirmed to still pass —
  this is the regression check Implementation Playbook §9 step 7 calls
  for.
- At least one full manual walkthrough of login -> role-aware navigation ->
  logout is performed and recorded, per `05-testing-rules.md`'s requirement
  that automated tests are not treated as a substitute for a real
  walkthrough.

## Security Requirements

- Verification specifically re-confirms no plaintext password, JWT signing
  secret, or token appears in logs, Postman collection files, or
  documentation produced by this task.

## Error Handling Requirements

- Not applicable in the implementation sense; this task confirms error
  handling built by prior tasks behaves as specified, and files defects
  where it does not.

## Documentation Requirements

- Kidus updates: the requirements-traceability matrix; the test
  documentation/evidence record; and the project's progress-report content
  for the relevant reporting period, per Appendix 3's biweekly progress
  report format, noting EPIC 1 completion status honestly (including any
  open defects).

## Commit Guidance

- Branch: `feature/auth-epic-verification`, from `develop` (for the Postman
  collection and documentation changes only).
- Commit message pattern: `test(auth): verify EPIC 1 acceptance criteria end-to-end`;
  `docs(auth): update requirements traceability for EPIC 1`.
- PR references Task ID `EPIC-1-AUTH-008`, lists every Epic Acceptance
  Criterion, and states pass/fail for each with evidence.
- Merge target: `develop`.

## AI Agent Safety Notes

- Do not fix defects found during this verification directly unless the
  fix is trivial and unambiguously within an already-completed task's
  declared scope; otherwise, file the defect against the correct
  `AUTH-0xx` task and stop.
- Do not mark EPIC 1 complete, and do not signal that EPIC 2 (Farmer
  Registry) may begin, if any Epic Acceptance Criterion fails — report the
  gap and stop.
- Do not modify the Baseline, Design Document, or any `.agents/rules/`
  file, even if verification surfaces an apparent inconsistency in them —
  record the inconsistency and escalate per `00-project-authority.md`.

## Expected Agent Report

1. Pass/fail status for every Epic Acceptance Criterion in
   `00-epic-overview.md`, with evidence.
2. A list of any defects filed, against which `AUTH-0xx` task, with
   reproduction detail.
3. Confirmation of the Verifier-role consistency check result (Auth-004
   finding vs. Auth-007 implementation).
4. Explicit statement of whether EPIC 1 is considered complete and EPIC 2
   may begin, or whether it is blocked pending defect resolution.
5. Confirmation that no secrets/tokens/passwords appear in any artifact
   produced by this task.
