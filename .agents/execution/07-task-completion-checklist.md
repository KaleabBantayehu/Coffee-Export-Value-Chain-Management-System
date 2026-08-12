# 07 — Task Completion Checklist

## Purpose

A concise, practical checklist an agent completes before requesting human
review, and a human reviewer uses to confirm before approving. It does not
introduce new rules — every item here is already required by
`.agents/rules/` or the preceding execution files; this is the compressed,
usable version.

## Requirements

- [ ] Task requirements understood (the task file itself, read in full).
- [ ] Relevant SRS requirements identified (from the task's own
      `Requirements Traceability` section).
- [ ] Design requirements identified (Design Document sections cited in
      the task file).
- [ ] Implementation Specification checked (backlog item, ownership,
      dependency order).
- [ ] `.agents/rules/07-current-project-decisions.md` checked for the latest
      project decisions and schedule interpretation.
- [ ] Minimum Project Plan schedule checked — confirm the task is
      consistent with the confirmed Week/Milestone table in
      `00-execution-overview.md`, and flag it if the task appears to be
      running materially ahead of or behind the Minimum Project Plan's
      week-by-week expectations (this is a schedule observation to report,
      not something the agent adjusts on its own).

## Scope

- [ ] Inside V1.0 scope (`.agents/rules/01-scope-boundaries.md`).
- [ ] No future or stretch features added ahead of the core chain being
      operational.
- [ ] No unauthorized architecture changes.
- [ ] The Mandatory Scope Test (`02-task-execution-procedure.md`) applied
      to anything built beyond the task's literal `Allowed Scope`.
- [ ] Nothing from the task's own `Out of Scope` section was implemented.
- [ ] If the task touches team ownership, the RBAC role list, or the
      mapping library, the corresponding "Known documented conflict" in
      `00-execution-overview.md` was checked and, if relevant, escalated
      rather than silently decided.

## Implementation

- [ ] Existing implementation inspected before writing new code
      (`01-agent-start-procedure.md`, Step 4) — nothing re-built that
      already existed.
- [ ] Existing dependencies reused where possible; nothing reinstalled or
      re-provisioned that EPIC 0 already established.
- [ ] Code follows `.agents/rules/03-coding-rules.md`.
- [ ] Only files within the task's allowed scope were changed.
- [ ] No secret, credential, or real `.env` value appears anywhere in the
      diff.

## Testing

- [ ] Required tests created/updated, per the task's own `Testing
    Requirements` and `.agents/rules/05-testing-rules.md`.
- [ ] All required tests pass.
- [ ] Regression check completed — the pre-existing test suite still
      passes, not just the tests added by this task.
- [ ] RBAC/role-permission tests, where applicable, used the frozen
      four-role model (Admin, ECTA Officer, Field/Registry Agent,
      Verifier), with the Minimum Project Plan's differing five-role
      testing-table language flagged rather than silently followed.

## Review

- [ ] Acceptance criteria verified, each with evidence, per the task
      file's own `Acceptance Criteria` section.
- [ ] Agent self-review completed (`03-verification-and-testing.md`).
- [ ] Agent report produced in the required format
      (`04-human-review-and-approval.md`).
- [ ] Human review completed by someone other than the implementer.
- [ ] Any "Questions requiring human decision" in the report were actually
      answered or explicitly escalated per `06-failure-and-escalation.md`
      — not left silently unresolved in an approved task.

## Git

- [ ] Correct branch (feature branch from current `develop`, not `main`
      and not an older commit).
- [ ] Clean diff understood by both implementer and reviewer — nothing
      unexplained in the changeset.
- [ ] Commit created only after human approval.
- [ ] Changes pushed and a pull request opened into `develop`.
- [ ] Merge performed by a reviewer other than the implementer, never by
      the agent merging its own PR.

## Task-Level Sign-Off

A task is only marked complete in team tracking once every box above is
checked **and** the task's own file-specific Definition of Done (stated in
the task file itself) is satisfied. A task with unchecked boxes is not
"mostly done" for the purpose of unblocking a dependent task — dependent
tasks treat it as not done at all, per each task file's own `Dependencies`
section and `01-agent-start-procedure.md` Step 5.

## EPIC-Level Sign-Off

Restated from `00-execution-overview.md` for use at the end of an EPIC
(e.g., after `EPIC-1-AUTH-008`'s own verification task completes its work):

```text
All tasks implemented
        +
All acceptance criteria passed
        +
Required tests passing
        +
No unresolved blockers
        +
No unauthorized scope changes
        +
Human review complete
        +
Git history clean
        +
Traceability verified
        =
EPIC COMPLETE
```

"No unresolved blockers" explicitly includes checking whether any of the
"Known documented conflicts" in `00-execution-overview.md` that the EPIC
touched are still open — an EPIC can have every task file individually
"complete" while a same-level document conflict relevant to that EPIC
remains unresolved (for example, EPIC 1's RBAC role-list discrepancy). In
that case the EPIC is not complete until the Project Manager resolves it or
explicitly accepts it as a documented, non-blocking gap.
