# 01 — Agent Start Procedure

## Purpose

Defines exactly what an agent (or a human developer following the same
discipline) must do **before modifying any code**, for every task, every
time — no exceptions for "simple" tasks.

## Step 1 — Identify the Task

Read the single task file being executed:

```text
.agents/tasks/<EPIC>/<TASK>.md
```

Do not read ahead into other tasks and start implementing pieces of them
"since you're already in that area." One task file, one execution pass.
Confirm the Task ID at the top of the file matches the Task ID you were
asked to execute — if you were asked to execute `EPIC-1-AUTH-003` and the
file's own header says something else, stop; you have the wrong file.

## Step 2 — Read Applicable Rules

Read, at minimum, every file in `.agents/rules/`:

- `00-project-authority.md` — document precedence and conflict handling
  (this execution directory's own hierarchy in `00-execution-overview.md`
  is the same hierarchy restated with two more documents now available;
  where they overlap they must agree — if they do not, that is itself a
  conflict to report).
- `01-scope-boundaries.md` — core / stretch / out-of-scope, and the
  stop-rather-than-invent rule.
- `02-tech-stack.md` — the frozen technology stack.
- `03-coding-rules.md` — code quality and architecture rules.
- `04-git-workflow.md` — branching, PR, review rules.
- `05-testing-rules.md` — testing expectations.
- `06-change-control.md` — classification and escalation.
- `07-current-project-decisions.md` — the latest agreed CEVCMS V1.0 project
  decisions for schedule, ownership, and implementation interpretation.

Then read this `.agents/execution/` directory's remaining files
(`02` through `07`) if not already familiar with them — they define _how_
to carry out what the rules require.

## Step 3 — Read Relevant Project Documentation

Read only what the task file's own `Authoritative Sources` and
`Requirements Traceability` sections cite — do not re-read entire
documents from scratch for every task. The task file has already done the
work of identifying which sections matter. If, while implementing, a
question arises that the cited sections do not answer, that is a trigger
for Step 6 (conflict/gap check), not a license to read broadly and decide
on your own.

The full authoritative source set, per `00-execution-overview.md`'s
hierarchy, is: Assignment Description, SRS, Minimum Project Plan V1.0,
Baseline Scope Freeze, Design Document V1.0, Implementation Specification,
Implementation Playbook, and the Development Backlog/EPIC task
specifications themselves.

## Step 4 — Inspect the Repository

**This step is critical and must not be skipped, guessed at, or assumed.**

Before deciding what to create, look at what already exists:

```bash
git status
git branch
git log --oneline --decorate -10
```

Then inspect the actual directory relevant to the task (e.g., `backend/`,
`frontend/`) rather than assuming its layout from a task file's
"indicative paths." Per the current confirmed project state:

- `main` and `develop` already exist; `develop` is already pushed to
  GitHub.
- `backend/.venv/` already exists with dependencies installed.
- `frontend/` already exists as a React/Vite project with `node_modules/`,
  `src/`, `package.json`, etc.
- The repository root already contains `backend/`, `frontend/`, `docs/`,
  `tests/`, `.agents/`, `.env.example`, `.gitignore`, `README.md`.
- EPIC-0 is complete.

**Do not assume something described in a task file is missing just
because the task file says to implement it.** A task file was written
before this specific execution pass; the repository may already partially
satisfy it (e.g., a previous, interrupted attempt; a teammate's parallel
work already merged). Check first. If the task's objective already appears
satisfied, do not re-implement it — report that finding instead (see
`06-failure-and-escalation.md`) so a human can confirm and close the task
without redundant work.

## Step 5 — Verify Preconditions

Using the task file's own `Preconditions` and `Dependencies` sections,
confirm, concretely (not by assumption):

- The files/modules the task depends on actually exist and are on
  `develop`.
- Any dependency the task needs is already installed (`pip freeze` /
  `package.json` — do not reinstall to "make sure").
- The database is in the expected state, if relevant (query it; do not
  assume the last migration ran).
- Existing tests relevant to the dependency area currently pass (a
  regression baseline before you add more).
- The specific prior task(s) listed as dependencies are actually marked
  complete, per `07-task-completion-checklist.md`'s definition — not just
  "someone said it's done."

If any precondition does not hold, **stop here**. Do not work around a
missing precondition by building a substitute for it — that is scope
creep into someone else's task. Report it per
`06-failure-and-escalation.md`.

## Step 6 — Check for Conflicts

Before writing any code, explicitly ask: does anything found in Steps 1–5
conflict with anything else found in Steps 1–5? In particular, check
against the task specification, the SRS, the Design Document, the
Implementation Specification, the Minimum Project Plan, the Baseline, and
the actual existing implementation.

Also check the "Known documented conflicts" list in
`00-execution-overview.md` — if the task touches one of those areas (team
ownership, the four-role RBAC model, or the mapping library), treat it as
already flagged; do not re-decide it, and do not proceed past the affected
part of the task without escalating per `06-failure-and-escalation.md`.

If a **new** conflict is found (not already on that list), the agent must
**stop and report it rather than silently choosing.** See
`06-failure-and-escalation.md` for the exact report format. Do not
implement "the version that seems more likely to be right" and move on —
an unreported guess here is exactly the failure mode this entire
`.agents/` system exists to prevent.

## Exit Condition for This Procedure

Only once Steps 1–6 are complete, with no unresolved precondition failure
and no unreported conflict, does the agent proceed to
`02-task-execution-procedure.md`.
