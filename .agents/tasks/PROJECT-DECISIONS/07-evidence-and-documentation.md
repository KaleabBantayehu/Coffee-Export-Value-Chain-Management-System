# PD-007 - Evidence and Documentation Location Decision

## Objective

Approve repository locations and naming conventions for requirements traceability, QA evidence, defects, reports, manuals, and progress records.

## Why the decision is needed

The task packages require these artifacts, but the current repository does not establish one authoritative location. Without a decision, evidence may be scattered or omitted from review.

## Authoritative sources

- Minimum Project Plan Sections 2.2, 6.4, 7.1-7.2: Test Report, user manual, Postman results, progress reporting, and evidence obligations.
- Implementation Specification EPIC-6: requirements traceability, test documentation, progress reports, user manual, and demo documentation.
- Baseline Section 5: Kidus owns documentation, QA, requirements traceability, progress reports, user manual, and demo documentation.
- Implementation Playbook Sections 9-10: documentation updates and honest status.
- Current repository tree: `docs/testing/` and `docs/progress/` exist as directories in the project context, but no established artifact index is evidenced; exact contents must be checked during execution.

## Current documented position

The documents require the artifact types and owners but do not define a complete canonical path, filename convention, retention policy, or whether sanitized Postman collections belong under `docs/`, `tests/`, or another location.

## Impact

Affects QA-001, QA-003, QA-007, QA-008, QA-009, QA-010, milestone review, client acceptance, and future defect reproduction.

## Options

1. Use `docs/testing/` for strategy, test cases, evidence index, Postman collections/results, Test Report, and manual; `docs/progress/` for progress reports; a documented defect log under `docs/testing/` unless an existing issue tracker is authoritative.
2. Use root `tests/` for executable tests and `docs/testing/` for all human evidence; keep progress under `docs/progress/`.
3. Use the existing GitHub Issues/Projects board for defects and repository docs only for summarized evidence.
4. Defer path choice and let each task select a location.

## Recommended resolution

Recommendation only: choose option 1 or 2 based on the actual current directory contents and the team's GitHub workflow. The project should have one index in `docs/testing/` linking test IDs to artifacts, one traceability matrix, one defect register, one Test Report, and one implemented-scope manual. Do not put secrets, raw tokens, passwords, or real PII in any location.

## Decision status

**UNRESOLVED - Project Manager approval required.** Final canonical locations: `UNRESOLVED`.

## Approval authority

Project Manager Kaleab, with Kidus as documentation owner and Ephratha as QA owner.

## Dependencies

PD-001. This decision is needed before QA evidence collection, but QA strategy planning may proceed with placeholders.

## Acceptance criteria

- Canonical locations for each required artifact type are listed.
- Ownership, naming, sanitization, and review/retention expectations are explicit.
- Existing directories and issue tracker usage are checked before choosing.
- No documentation task invents a source requirement or stores secrets/PII.

## Developer/PM handoff instructions

Evidence collection may be prepared, but **DO NOT FINALIZE ARTIFACT LOCATIONS UNTIL APPROVED**. Use temporary task-local references only with explicit status.
