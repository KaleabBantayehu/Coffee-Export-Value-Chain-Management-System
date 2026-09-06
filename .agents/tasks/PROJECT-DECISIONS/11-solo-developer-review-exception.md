# PD-011 — Solo-Developer Review and Merge Exception

## Decision

**APPROVED BY PROJECT MANAGER.**

For the current CEVCMS V1.0 project, which has one human developer/project
owner and no second human team member available, the Project Manager approves
a documented solo-developer self-review exception to the independent-review
requirement in `.agents/rules/04-git-workflow.md`.

## Context

The standard workflow requires a reviewer who is a team member other than the
author. That remains the correct control for multi-person development, but it
cannot be satisfied when a project has only one human developer. The exception
preserves review discipline without creating an impossible procedural blocker.

## Approved workflow

### Multi-person projects

The existing standard remains unchanged: at least one human reviewer other
than the author must review and approve each feature branch before merge.

### Genuine single-developer projects

While no second human team member is available, the project owner/developer
may perform a documented self-review before merge. The record must include:

- branch and task;
- author;
- why the single-developer exception applies;
- files and exact diff reviewed;
- task-required automated, static, test, and branch-safety checks executed;
- check results;
- unresolved risks or blockers;
- explicit Project Manager/project-owner approval; and
- merge commit or pull-request reference, where applicable.

AI assistants and tools may support the review, but they must not be described
as an independent human reviewer. If another human contributor or reviewer
becomes available, the standard independent-review rule resumes for applicable
future merges.

## Safeguards retained

This exception does **not** waive:

- task acceptance criteria;
- automated/static/test checks;
- security review or sanitization;
- evidence and documentation requirements;
- branch safety, pull-request, or protected-branch requirements;
- required governance decisions; or
- blocking-condition escalation.

It does not authorize direct, unreviewed pushes to protected branches and does
not automatically approve an application task merely because the exception
exists.

## QA-001 effect

`feature/epic-6-qa-001-test-strategy` and commit
`2e400eb81ab4a14dc3e41b23cafe8e180a01d9d7` remain unmerged under this
decision. They must be re-reviewed and explicitly approved using the
solo-developer record in a separate integration task. This decision does not
retroactively claim QA-001 complied with the former rule.

## Authority and status

- **Classification:** Controlled governance-process amendment; it changes no
  application scope, architecture, technology, or security contract.
- **Approval authority:** Project Manager Kaleab.
- **Status:** APPROVED.
- **Recorded approval:** The Project Manager instruction establishing this
  decision and authorizing the narrowly scoped Rule 04 amendment.
