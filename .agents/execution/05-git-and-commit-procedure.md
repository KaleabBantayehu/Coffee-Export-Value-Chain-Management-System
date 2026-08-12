# 05 — Git and Commit Procedure

## Purpose

Defines the exact git sequence a task follows once human approval
(`04-human-review-and-approval.md`) has been given. This file restates
`.agents/rules/04-git-workflow.md` in execution-sequence form; where
anything here and that rule file appear to differ, the rule file governs
and the difference is a defect in this file to be reported.

## The Governing Rule

> Never commit directly to `main`.

`main` is the stable baseline. `develop` is the active integration branch,
already pushed to GitHub. All task work happens on a feature branch created
from `develop` and merges back into `develop` only.

## Sequence

```text
develop
   |
   v
feature branch          (created fresh from the current develop tip —
   |                      do not branch from an older commit or from
   |                      another feature branch)
   v
implementation           (02-task-execution-procedure.md)
   |
   v
testing                  (03-verification-and-testing.md)
   |
   v
human review              (04-human-review-and-approval.md)
   |
   v
commit                   (on the feature branch, only after approval)
   |
   v
push                     (the feature branch, to GitHub)
   |
   v
merge/integration into develop   (via pull request, per
                                   .agents/rules/04-git-workflow.md:
                                   at least one reviewer other than
                                   the implementer approves)
```

Nothing in this sequence merges directly into `main`. `main` only receives
`develop` at agreed project checkpoints, decided by the Project Manager —
not by any individual task's completion.

## Branch Naming

One feature branch per task, named after the Task ID and a short
description:

```text
feature/EPIC-1-AUTH-001-password-foundation
feature/EPIC-1-AUTH-002-login-jwt
feature/EPIC-1-AUTH-006-frontend-login-auth-state
```

This is slightly more specific than the illustrative branch names already
given inside individual EPIC-0/EPIC-1 task files (e.g.,
`feature/auth-login-jwt`) — **both forms are acceptable**; including the
Task ID in the branch name is recommended going forward for easier
traceability between a branch and its task file, but this execution
procedure does not require renaming or re-branching work already in
progress under the shorter naming style already used in existing task
files.

Do not create a branch for trivial, documentation-only changes (e.g., a
single traceability-matrix update) unless `.agents/rules/04-git-workflow.md`
already requires one for that kind of change — check that rule file rather
than defaulting to "always branch."

## Commit Messages

Per `.agents/rules/04-git-workflow.md`:

```text
feat(auth): implement JWT login
fix(farmer): validate FIN uniqueness
test(auth): verify EPIC 1 acceptance criteria end-to-end
docs(auth): update requirements traceability for EPIC 1
```

- Prefix: `feat`, `fix`, `test`, `docs`, `chore`, or `refactor`.
- Scope: the module the change touches.
- Reference the Task ID in the commit body (e.g., `Refs: EPIC-1-AUTH-002`).

## What Happens at Commit Time

- Commit only what was reviewed and approved in
  `04-human-review-and-approval.md` — if anything changed since the
  report was written (e.g., a last-minute fix), the report must be updated
  and re-reviewed before commit, not committed silently alongside the
  approved diff.
- The PR description references the Task ID and states, explicitly,
  whether anything from the task's `Out of Scope` section was touched
  (it should not have been) and whether any "Questions requiring human
  decision" from the report remain open.

## Push and Merge

- Push the feature branch to GitHub.
- Open a pull request into `develop`.
- At least one reviewer other than the implementer approves, per
  `.agents/rules/04-git-workflow.md`. An agent does not merge its own pull
  request under any circumstance, even after "approval" in
  `04-human-review-and-approval.md` — that approval authorizes opening the
  PR and requesting merge-level review; it is not itself the merge-level
  review.
- After merge, confirm the existing test suite still passes on `develop`
  (regression check, per `03-verification-and-testing.md`) before treating
  the task as fully closed.

## What an Agent Must Never Do in Git (restated from the rules for this sequence)

- Push directly to `main` or `develop`.
- Force-push over another contributor's branch.
- Merge its own pull request.
- Rewrite history on a shared branch.
- Commit generated secrets, `.env` files with real values, or credentials
  of any kind.
- Reinitialize the repository, recreate `main`/`develop`, or otherwise
  touch git structure already established in EPIC 0.
