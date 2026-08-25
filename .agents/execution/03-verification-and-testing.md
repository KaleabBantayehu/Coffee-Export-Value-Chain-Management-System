# 03 — Verification and Testing

## Purpose

Defines how an agent verifies its own implementation before handing it to
a human, consistent with `.agents/rules/05-testing-rules.md`. This file
does not replace that rule file; it sequences it into the execution
lifecycle and adds the categories relevant to CEVCMS's specific stack.

## The Governing Principle

> Agents must never claim a task is complete merely because the code
> "looks correct."

Every category below produces **evidence** — a test result, a command
output, a screenshot, a Postman run — that goes into the agent's report
(`04-human-review-and-approval.md`). "I reviewed it and it looks right" is
not evidence.

## Testing Categories

### Unit tests

For isolated functions/modules — e.g., the password-hashing utility in
`EPIC-1-AUTH-001`, JWT encode/decode logic in `AUTH-002`/`AUTH-003`, or any
future business-logic function (area calculation, EUDR flag, HMAC signing).
Run per the task's own `Testing Requirements`; use the test runner already
configured in the backend/frontend project (do not introduce a new one).

### Integration tests

For interactions between components that did not previously talk to each
other — e.g., an authentication dependency talking to the actual
`User`/`Role` tables, not a mock. Confirms the pieces work together, not
just each piece alone.

### API tests

For backend endpoints, using Postman, per
`.agents/rules/05-testing-rules.md` and the Minimum Project Plan's own
Quality Assurance and Testing Plan (§6.4): *"Integration testing | REST API
endpoints and database interactions for each in-scope module | Postman
collections run manually and, where time allows, via a simple CI script."*
Every new or changed endpoint gets a corresponding Postman request.

### Frontend verification

For UI behavior and frontend integration — e.g., `AUTH-006`'s login form,
`AUTH-007`'s route protection. Automated where the existing frontend test
setup supports it; otherwise a recorded manual walkthrough, per the
Minimum Project Plan's testing plan, which explicitly allows "manual
walkthroughs against the acceptance criteria... using seeded demonstration
data" for functional/system-level checks.

### Regression testing

Before anything is proposed for merge, the **existing** test suite (not
just the new tests this task added) is re-run and confirmed to still pass,
per `.agents/rules/04-git-workflow.md` step 7 and
`.agents/rules/05-testing-rules.md`. A task that makes its own new tests
pass while breaking a previously-passing test is not done — it is a
regression, and it blocks merge.

### Role-permission / RBAC testing

Applies from `EPIC-1-AUTH-004` onward. Per the Minimum Project Plan's
testing plan: each in-scope role attempts an allowed action and a
disallowed action; unauthorized actions must be rejected. **Use the
frozen four-role model** (Admin, ECTA Officer, Field/Registry Agent,
Verifier) as fixed by the Baseline and Design Document — **not** the
five-item role list that appears in the Minimum Project Plan's own testing
table (which includes "Exporter," a role not defined in the Baseline/Design
Document role model). This discrepancy is recorded as an open, unresolved
conflict in `00-execution-overview.md`; until the Project Manager resolves
it, RBAC testing follows the Baseline/Design Document's four roles, and the
discrepancy itself is reported in the agent's report for any task where
role-permission testing is performed, so a human sees it every time, not
just once.

### Input validation & error handling

Boundary-value and invalid-input test cases per endpoint/form, per the
Minimum Project Plan's testing plan and `.agents/rules/03-coding-rules.md`'s
validation requirements.

### Basic security checks

Password hashing, JWT validation/expiry, parameterized queries (ORM-based,
no raw SQL string interpolation), per the Minimum Project Plan's testing
plan: *"Manual verification checklist; no formal penetration test."* This
is a checklist-style confirmation, not a security audit — do not attempt or
imply penetration testing, which is explicitly out of scope
(`.agents/rules/05-testing-rules.md`; Minimum Project Plan §6.4).

## What Testing Does Not Cover in V1.0

Consistent with `.agents/rules/05-testing-rules.md` and the Minimum
Project Plan §6.4:

- No load or performance testing at national/enterprise scale.
- No formal penetration testing.
- No test coverage of any out-of-scope integration (real NBE, real
  customs, real telecom gateways) — nothing real exists to test.

## Self-Review, Before Handing Off

Before producing the report for human review
(`04-human-review-and-approval.md`), the agent performs its own check
against:

1. The task file's `Acceptance Criteria` — each one, explicitly, pass or
   fail.
2. The task file's `Out of Scope` section — confirm nothing there was
   touched.
3. The Mandatory Scope Test in `02-task-execution-procedure.md` — for
   anything added that was not explicitly named in `Allowed Scope`.
4. `.agents/rules/03-coding-rules.md` — code quality, no unnecessary
   abstraction, no duplicate functionality.
5. `.agents/rules/02-tech-stack.md` — no unauthorized technology
   introduced, including no accidental use of a library the task did not
   call for.
6. Secrets — confirm no credential, key, or `.env` value with a real
   secret is present in the diff.

Self-review is not a substitute for human review (see
`04-human-review-and-approval.md`); it is what makes the human review fast
and trustworthy instead of a from-scratch audit.

## Exit Condition for This Procedure

All required tests for the task pass, the regression suite passes, and the
self-review above is complete. Only then does the agent produce its report
and move to `04-human-review-and-approval.md`.
