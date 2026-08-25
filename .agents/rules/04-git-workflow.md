# Rule 04 — Git Workflow

## Purpose

Defines the branching, review, and commit conventions for CEVCMS V1.0.
Source of authority: Implementation Specification (EPIC 0 tasks); Baseline
§5 (team ownership); Implementation Playbook §9 (per-feature workflow).

## Branch model

- **`main`** — the stable baseline. Nothing is committed to `main` directly.
  `main` only receives merges from `develop` at agreed checkpoints (e.g., at
  a milestone).
- **`develop`** — the active integration branch. All completed, reviewed
  feature work merges here first.
- **`feature/<short-description>`** — one branch per task. Created from
  `develop`, named after the task (e.g., `feature/auth-login`,
  `feature/farmer-registration`), and merged back into `develop` only.

No individual development happens directly on `main` or `develop`.

## Pull request requirement

- Every feature branch is merged via a pull request into `develop`, never by
  direct push.
- **At least one reviewer** (a team member other than the author) must
  review and approve before merge. An AI agent's own review of its own work
  does not satisfy this requirement — a human teammate must review.
- The PR description states: which task file it implements (by Task ID),
  what was implemented, and what was explicitly left out (if anything),
  mirroring the task file's `Out of Scope` section.

## Commit messages

Use meaningful, conventional-style commit messages, per Implementation
Playbook §9:

```text
feat(auth): implement JWT login
fix(farmer): validate FIN uniqueness
test(farm): add polygon validation tests
docs(traceability): update requirements traceability entry
```

- Prefix: `feat`, `fix`, `test`, `docs`, `chore`, or `refactor`.
- Scope in parentheses: the module the change touches (`auth`, `farmer`,
  `farm`, `lot`, `traceability`, `qr`, `db`, `infra`).
- Reference the Task ID in the commit body when applicable (e.g.,
  `Refs: EPIC-0-BE-001`).

## Per-feature workflow (from Implementation Playbook §9)

Every feature, without exception, follows these steps in order:

1. **Requirement** — trace it: SRS requirement -> Design Document section ->
   backlog/task item. If any link is missing, stop and classify it
   (`06-change-control.md`) before writing code.
2. **Design** — confirm database, API, business logic, frontend,
   permissions, and validation against the Design Document before
   implementing.
3. **Implement** — create a feature branch from `develop`.
4. **Test** — happy path, invalid input, unauthorized access, wrong role,
   database behavior, API response (see `05-testing-rules.md`).
5. **Review** — a teammate reviews before merge.
6. **Merge** — into `develop`, never directly into `main`.
7. **Integration test** — confirm nothing existing broke.
8. **Commit** — meaningful, conventional messages (see above).
9. **Update documentation** — the requirements-traceability entry and test
   documentation are updated (owned by Kidus) so the docs stay honest about
   what is actually built.
10. **Move to the next backlog item** — in dependency order
    (`01-scope-boundaries.md`), not whichever task looks most interesting.

## What an AI agent must never do in git

- Push directly to `main` or `develop`.
- Force-push over another contributor's branch.
- Merge its own pull request.
- Rewrite history on a shared branch.
- Commit generated secrets, `.env` files with real values, or credentials of
  any kind.
