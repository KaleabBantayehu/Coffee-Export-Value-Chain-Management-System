# 04 — Human Review and Approval

## Purpose

Defines the mandatory human checkpoint between "agent believes the task is
done" and "the change is committed." No task is approved by an agent's own
declaration, under any circumstance.

## The Governing Rule

> An agent must NOT mark a task as fully approved by itself.

Self-review (`03-verification-and-testing.md`) improves the quality of
what reaches a human; it never replaces the human's decision.

## The Agent Report

Once `01`, `02`, and `03` are complete, the agent produces a report in
exactly this structure before requesting human review:

```text
Task ID:
Task name:

Implementation summary:

Files created:

Files modified:

Files deleted:

Dependencies added:

Tests executed:

Test results:

Acceptance criteria:
- [PASS/FAIL] ...
- [PASS/FAIL] ...

Scope check:

Known limitations:

Potential risks:

Questions requiring human decision:
```

Notes on filling this in honestly:

- **Acceptance criteria** — list every criterion from the task file's own
  `Acceptance Criteria` section verbatim, each marked `[PASS]` or `[FAIL]`
  with the evidence that supports the mark (a test name, a command output,
  a specific observation). A criterion with no evidence is not `[PASS]`.
- **Scope check** — explicitly state that nothing in the task's `Out of
  Scope` section was implemented, and that the Mandatory Scope Test
  (`02-task-execution-procedure.md`) was applied to anything added beyond
  the task's literal `Allowed Scope`.
- **Known limitations** — anything the task file itself flagged as an open
  item, deferred decision, or explicit simplification (several EPIC-1 tasks
  have these, e.g., `AUTH-004`'s Verifier-role investigation) gets reported
  here with its answer or its still-open status.
- **Potential risks** — anything the agent noticed that could affect a
  later task, even if out of this task's own scope to fix (e.g., "the
  seed script assumes X; the next task should confirm Y").
- **Questions requiring human decision** — every conflict identified per
  `01-agent-start-procedure.md` Step 6, every "Known documented conflict"
  from `00-execution-overview.md` that the task touched, and anything else
  the agent could not resolve on its own authority. An empty section here
  is only correct if genuinely nothing came up — not a default.

If any task-specific "Expected Agent Report" section exists in the task
file itself (all `.agents/tasks/EPIC-0/` and `.agents/tasks/EPIC-1/` files
have one), its items are additional to, not a replacement for, the
structure above — merge both into a single report.

## What the Human Reviewer Checks

1. Every `[PASS]` acceptance criterion actually has supporting evidence,
   not just a claim.
2. The diff matches the report — no file changed that is not listed, and
   nothing listed as changed is actually unchanged in a way that hides a
   `[FAIL]`.
3. Nothing in `Out of Scope` was touched.
4. No secret, credential, or real `.env` value appears anywhere in the
   diff.
5. `.agents/rules/` compliance (tech stack, coding rules, git workflow,
   testing rules).
6. Any "Questions requiring human decision" are actually answerable by
   this reviewer, or need to go to the Project Manager
   (`06-failure-and-escalation.md`).
7. The task's Definition of Done, as written in the task file, is
   genuinely satisfied — not approximately satisfied.

## Approval

- Only after the human reviewer is satisfied on all points above does the
  task proceed to commit (`05-git-and-commit-procedure.md`).
- Per `.agents/rules/04-git-workflow.md`, this human reviewer must be a
  team member other than whoever (human or agent) implemented the task —
  an agent's own review of its own work does not satisfy the review
  requirement, and a single person cannot be both implementer and sole
  reviewer.
- If the reviewer finds a `[FAIL]` or a gap, the task returns to
  `02-task-execution-procedure.md` (or, if the gap is a genuine scope/
  conflict question, to `06-failure-and-escalation.md`) — it does not get
  partially merged.

## Approval Is Not Merge

Human approval authorizes the commit/PR process
(`05-git-and-commit-procedure.md`); it is a separate, prior step from the
PR-level "at least one reviewer" requirement in
`.agents/rules/04-git-workflow.md`. In practice these are often the same
review, performed once — this file exists to make explicit that the review
must actually happen and actually check the items above, not that it must
happen twice.
