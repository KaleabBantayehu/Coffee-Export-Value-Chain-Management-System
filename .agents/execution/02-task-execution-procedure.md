# 02 — Task Execution Procedure

## Purpose

Defines what an agent may and may not do while actually implementing an
already-started task (i.e., after `01-agent-start-procedure.md` has been
completed with no blocking gap or conflict).

## What an Agent May Do

- Modify files explicitly within the task's own `Allowed Scope` and
  `Files/Directories in Scope` (or "...Potentially Affected") sections.
- Create files required by the task, in locations consistent with the
  **existing** repository structure discovered in Step 4 of
  `01-agent-start-procedure.md` — not a structure invented from a task
  file's "indicative path" if the real repository already does it
  differently. Indicative paths in task files are illustrative; the actual
  repository layout, once inspected, is authoritative for where new files
  go.
- Modify existing code when the task explicitly requires it (e.g.,
  extending a shared dependency created by a prior task, as several
  EPIC-1 tasks do with `AUTH-001`'s hashing utility).
- Add tests required by the task, per `.agents/rules/05-testing-rules.md`
  and the task's own `Testing Requirements`.
- Update documentation explicitly called for by the task's own
  `Documentation Requirements` section.
- Add a narrowly-scoped library that fulfills an already-approved
  requirement, under the specific allowance in
  `.agents/rules/02-tech-stack.md` — recording the choice in the agent
  report, not silently.

## What an Agent May NOT Do

- Implement another task, even a small piece of it, "while already in the
  area." Each task file is executed on its own; a task that seems to
  naturally lead into the next one still stops at its own boundary.
- Refactor unrelated code. A task fixes or builds what it says it does; it
  does not "clean up" adjacent code as a side effect, even if the agent
  believes the cleanup is objectively good — that is a separate,
  classifiable change (`.agents/rules/06-change-control.md`), not part of
  this task.
- Redesign architecture. The modular-monolith structure, layer separation,
  and module boundaries are fixed by the Design Document and
  `.agents/rules/03-coding-rules.md`.
- Add future or stretch features ahead of schedule, per
  `.agents/rules/01-scope-boundaries.md`.
- Change approved technologies, per `.agents/rules/02-tech-stack.md` — this
  includes not "upgrading" a library, not swapping an equivalent library,
  and not introducing Mapbox GL in place of Leaflet/React-Leaflet (see the
  known conflict recorded in `00-execution-overview.md` — until resolved,
  Leaflet/React-Leaflet remains the only approved mapping library).
- Modify frozen project documents: the Assignment Description, SRS,
  Minimum Project Plan, Baseline Scope Freeze, or Design Document. These
  are Level 1–3 documents; nothing this execution procedure does can touch
  them.
- Modify `.agents/rules/` or any file in `.agents/tasks/` (including the
  task file currently being executed) — if a rule or task file itself
  needs to change, that is change control, decided by the Project Manager,
  not an in-flight edit by the agent doing the implementation.
- Modify unrelated directories — if the task is backend, do not touch
  `frontend/` "for consistency," and vice versa, unless the task file
  explicitly says otherwise (as some EPIC-1 tasks do, by design, when
  frontend and backend must agree on a contract).
- Install unnecessary packages, per `.agents/rules/02-tech-stack.md` and
  the current-state instruction not to reinstall or expand the existing,
  already-approved backend/frontend environments.
- Rewrite working code merely for stylistic preference. If existing code in
  the task's allowed scope already satisfies `.agents/rules/03-coding-rules.md`,
  leave it as-is; only change what the task requires.
- Recreate anything already completed in EPIC 0: the Git repository, `main`
  or `develop` branches, the Python virtual environment, already-installed
  backend dependencies, the React/Vite frontend scaffold, or the base
  repository directory structure. EPIC-0 is complete; treat it as a fixed
  starting point unless a verification task explicitly identifies a
  defect in it.

## The Mandatory Scope Test

Before implementing anything not explicitly and unambiguously named in the
task file's `Allowed Scope`, the agent runs this test:

```text
Question 1 — Is this required by the assigned task?
Question 2 — Is it inside the frozen V1.0 scope
              (.agents/rules/01-scope-boundaries.md)?
Question 3 — Is it supported by the approved requirements/design
              (SRS / Design Document / task file)?
Question 4 — Is it necessary to satisfy the task's acceptance criteria?
```

- If the answer to **any** question is "no," the agent does not implement
  it.
- If implementation genuinely appears necessary despite a "no," the agent
  does not implement it either — it routes through
  `.agents/rules/06-change-control.md` and
  `06-failure-and-escalation.md` instead. "It seems necessary" is a report,
  not an authorization.

## The Dependency Rule

> **Never install or recreate something before inspecting whether it
> already exists.**

For every dependency or infrastructure requirement a task seems to need:

```text
Inspect
   |
   v
Verify
   |
   v
Reuse if present
   |
   v
Add only if genuinely required
```

This is especially important because EPIC 0 is already complete. Repeating
any of the following is prohibited unless a task specifically identifies
an existing defect requiring correction:

- repository initialization
- Git branch creation
- Python environment creation
- dependency installation (backend or frontend)
- React/Vite scaffolding
- database setup

If a genuinely new dependency is required by an approved task (this should
be rare, given the frozen stack), the agent must, in order:

1. Verify the dependency is not already installed (check `pip freeze` /
   `package.json`, not memory).
2. Verify the dependency is actually required — not merely convenient.
3. Explain, in the eventual agent report, why it is necessary.
4. Confirm it is compatible with the approved technology stack
   (`.agents/rules/02-tech-stack.md`) — a dependency that quietly pulls in
   an unapproved framework or infrastructure component is not compatible
   even if it "just works."
5. Update the appropriate dependency file (`requirements.txt`/
   `pyproject.toml` equivalent for backend, `package.json` for frontend) —
   do not leave an undeclared dependency.
6. Test the change.

## Implementation Order Within a Task

Follow the task file's own `Implementation Steps` in the order given. If a
task file's steps imply an order that conflicts with what Step 4 of
`01-agent-start-procedure.md` found in the actual repository (e.g., a step
assumes something is missing that inspection showed already exists), stop
and report per `06-failure-and-escalation.md` rather than silently
reordering or skipping steps on your own judgment.

## Exit Condition for This Procedure

Implementation is "done" for the purpose of moving to the next stage only
when every applicable step in the task file's own `Implementation Steps`
has been carried out within the boundaries above. The next stage is
`03-verification-and-testing.md` — testing is not optional and is not
folded into this stage.
