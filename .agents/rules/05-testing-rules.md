# Rule 05 — Testing Rules

## Purpose

Defines what "tested" means for CEVCMS V1.0, so that Definition of Done is an
observable, checkable state rather than a claim.

Source of authority: Implementation Specification (EPIC 6 — Testing & QA);
Baseline §5 (Ephratha owns testing/QA); Implementation Playbook §9, step 4.

## Testing is not optional

**A task's Definition of Done cannot be declared satisfied without its
required tests passing.** "It works when I tried it manually" is not
sufficient evidence of completion for any task in `tasks/`.

## Required testing categories, by situation

- **Unit testing** — any new business-logic function (validation rule, area
  calculation, HMAC signing/verification, FIN/GIN generation, etc.) has at
  least one unit test covering its main success path and at least one
  covering a known failure/edge case.
- **API testing (Postman)** — every new or changed API endpoint has a
  corresponding Postman request (or collection entry) exercising it, per the
  Implementation Specification's frozen choice of Postman for API testing.
  This is in addition to, not instead of, automated backend tests.
- **Integration testing** — whenever a task connects previously separate
  pieces (e.g., Farmer Registry writing to the database configured in EPIC-0-
  DB-001), a test confirms the connected path works end to end, not just each
  piece in isolation.
- **Validation testing** — every endpoint that accepts input is tested with
  at least one invalid-input case (missing required field, wrong type,
  out-of-range value) and confirmed to return a structured 400-level error,
  not a crash or a silent accept.
- **RBAC / authorization testing** — once Authentication & RBAC exists,
  every protected endpoint added afterward is tested for: an unauthenticated
  request being rejected, and a request from a role without permission being
  rejected (403), in addition to the authorized happy path.
- **Regression testing** — before a feature branch is merged into `develop`,
  the previously-passing test suite is re-run and confirmed green. A merge
  that breaks an existing passing test is not acceptable, per Implementation
  Playbook §9, step 7.

## What "Definition of Done" requires, in testing terms

For any task, Definition of Done includes, at minimum:

1. The specific tests listed in that task's `Testing Requirements` section
   exist and pass.
2. The full existing automated test suite still passes (no regressions).
3. Manual verification of the acceptance criteria has been performed at
   least once, in addition to automated tests — automated tests catch
   regressions, but the human/agent doing the work confirms the feature
   actually behaves as intended before calling it done.
4. Test evidence (what was run, and that it passed) is reported in the task's
   `Expected Agent Report`, so a human reviewer does not have to take
   "tests pass" on faith.

## What testing does not need to cover in V1.0

Consistent with `01-scope-boundaries.md` and Design Document §14:

- No load or performance testing at national scale (5,000 TPS is explicitly
  out of scope).
- No penetration testing or formal security audit.
- No test coverage of out-of-scope integrations (real NBE, real customs,
  real telecom gateways) — there is nothing real to test against.

## Ownership

Ephratha owns Postman API testing, unit/integration testing, input
validation testing, and RBAC security testing across all core modules, per
Baseline §5. Task files may still specify the tests a given task's author
must write; Ephratha's ownership covers the overall QA process and defect
tracking, not sole responsibility for every test in every task.
