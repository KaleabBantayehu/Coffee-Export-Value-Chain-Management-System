# EPIC-6-QA-007 - Defect Tracking and Regression

## Objective

Operate the defect lifecycle and prove that approved fixes do not regress the CEVCMS V1.0 core.

## Scope

Create and triage defects; maintain severity/priority/owner/status; link defects to requirements/upstream tasks/evidence; coordinate retest; run targeted and full regression for auth/RBAC, Farmer, Farm/Polygon, traceability, QR, frontend navigation, and the complete core workflow.

## Out of Scope

Fixing defects, changing requirements, closing defects without retest, stretch QA, load testing, formal penetration testing, or modifying prior task files.

## Preconditions

QA-001 strategy and QA-002 through QA-006 result inputs available as applicable; a fix has an owner and reviewed branch/PR before regression.

## Dependencies

All QA execution tasks and any owning implementation task/defect-fix branch; existing regression suites; EPIC-1 through EPIC-5 gates.

## Inputs

Test failures, screenshots/output, reproduction environments, requirement matrix, code/PR references, and prior regression baseline.

## Expected Outputs

Defect log, triage decisions, retest results, regression matrix, reopened/closed statuses, and release-blocker summary.

## Relevant Files / Modules

Defect log, test evidence, Postman results, backend/frontend test outputs, PR/task references, and progress documentation. No application source changes.

## Backend Responsibilities

Coordinate backend defect retests and API regression; owning developer implements fixes in their task scope.

## Frontend Responsibilities

Coordinate frontend navigation/UI retests and regression; Biniyam supports diagnosis.

## Database Responsibilities

Verify data-integrity regressions through read-only checks where applicable; do not repair data directly.

## API Requirements

Retest only documented endpoints and preserve baseline status/response expectations. A changed contract is a change-control issue, not an automatic test update.

## UI / UX Requirements

Confirm fixes preserve navigation, role behavior, validation, error states, and public/private boundaries.

## Security Requirements

Security failures, secret exposure, unauthorized access, or public PII exposure are release-blocking until fixed and retested.

## Validation / Error Handling

Every defect record includes: ID, severity, priority, affected requirement/task, environment, reproduction steps, expected, actual, evidence, owner, status, fix reference, and regression result.

## Acceptance Criteria

- Every observed failure has a unique complete defect record or documented non-defect rationale.
- Core/security defects are not closed without successful retest.
- Targeted and full regression results are recorded after approved fixes.
- No regression in auth, RBAC, Farmer, Farm/Polygon, traceability, QR, frontend navigation, or core chain remains unclassified.
- Open blockers are visible to QA-009/010.

## Testing Requirements

Run targeted tests for each fix and the full available suite before recommending merge/release, per rules 05 and execution 03. Manual regression is required where automation is unavailable.

## Evidence Requirements

Defect records, before/after outputs, retest result, PR/task reference, sanitized screenshots/logs, and regression command output.

## Traceability

Implementation Specification EPIC-6 defect tracking/regression; Minimum Project Plan Sections 4.3, 6.4, 7.1; `.agents/rules/04-git-workflow.md`, `05-testing-rules.md`, `06-change-control.md`; all upstream EPIC task acceptance criteria.

## Ownership, Git, and Change Control

Primary: Ephratha. Kidus owns defect-log documentation; owning developer fixes; independent reviewer approves. Branch `feature/EPIC-6-QA-007-defects-regression`; commit `test(qa): record defects and regression evidence`; PR to `develop`. Scope/contract changes require PM authorization.

## Blockers / Stop Conditions

Stop closure if reproduction/evidence is insufficient, a fix is unreviewed, regression fails, or a defect changes scope/architecture. Do not patch source from this task.
