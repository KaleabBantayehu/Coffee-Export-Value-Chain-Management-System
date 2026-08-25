# EPIC-6-QA-002 - Unit and Component Testing

## Objective

Execute and document unit tests for implemented backend business logic and available frontend component tests without adding application behavior.

## Scope

Cover password hashing, seed/idempotency, FIN/GIN generation, area/EUDR logic, lot creation, append-only events, QR/HMAC behavior where implemented, and frontend components where an existing test setup supports them. Record unavailable or unimplemented areas as blocked.

## Out of Scope

Implementing missing logic, choosing FIN/GIN/QR formats, installing an unapproved test framework, full API/integration tests, UI redesign, stretch modules, load testing, and formal penetration testing.

## Preconditions

QA-001 complete; relevant upstream task is implemented, tests are present or approved test placement is known, and the selected environment is runnable.

## Dependencies

EPIC-1 through EPIC-5 implementation state; QA-001. Each test area depends on its owning upstream task being implemented and merged.

## Inputs

Existing source/tests, approved requirements/design, test matrix, synthetic fixtures, and actual configured test commands.

## Expected Outputs

Executed unit/component test results, coverage limited to evidenced tests, failure/blocked list, and sanitized test artifacts.

## Relevant Files / Modules

`backend/tests/`, backend business-logic modules, `frontend/src/` and any existing frontend tests/config. Do not modify source or upstream task files.

## Backend Responsibilities

Ephratha runs and evaluates backend unit tests; module owners clarify expected behavior without changing requirements.

## Frontend Responsibilities

Run existing component tests if present; otherwise record manual verification as QA-006, not as fabricated automated coverage.

## Database Responsibilities

Use mocks/fixtures or test DB only according to existing setup; verify seed/idempotency against an appropriate isolated environment without changing schema.

## API Requirements

None directly; unit expectations must derive from implemented API/domain contracts.

## UI / UX Requirements

Component assertions may cover documented rendering and states only where an existing runner supports them.

## Security Requirements

Confirm hashing is not plaintext and HMAC/JWT secrets do not appear in test output or fixtures. Do not test enterprise mechanisms excluded from V1.0.

## Validation / Error Handling

Each business function requires success and known failure/edge coverage per testing rules; unresolved formats or behavior are blocked, not guessed.

## Acceptance Criteria

- Each implemented required business function has at least one success and one failure/edge test or an explicit documented blocker.
- Seed/idempotency, identifier, area/EUDR, lot/event, and QR/HMAC tests are separately reported.
- Existing frontend component tests are run if available; absent tooling is recorded.
- No application source or requirements are modified.
- Results identify exact command, environment, and pass/fail/blocked status.

## Testing Requirements

Run the configured backend suite and available frontend suite; rerun relevant tests after any defect fix through QA-007. Do not claim coverage percentages unsupported by evidence.

## Evidence Requirements

Test output, test-case IDs, fixture identifiers without PII/secrets, failure traces sanitized of credentials, and blocked-area explanations.

## Traceability

Rules 05 and execution 03; Implementation Specification EPIC-6 unit testing; Minimum Project Plan Section 7.1 unit-testing row; Design Document Sections 4.1-4.2, 5.1-5.3, 10, 14; upstream EPIC-1 through EPIC-4 business-task contracts.

## Ownership, Git, and Change Control

Primary: Ephratha; Biniyam supports frontend interpretation; Kidus records evidence. Branch `feature/EPIC-6-QA-002-unit-component-tests`; commit `test(qa): execute unit and component test matrix`; PR to `develop`. Test-tool or expected-behavior changes require escalation.

## Blockers / Stop Conditions

Block a test if its code/contract is not implemented, its expected format is unresolved, or tooling is absent. Do not fill a gap with a new implementation.
