# EPIC-6-QA-001 - Test Strategy and Environment

## Objective

Define the executable QA strategy, environment readiness, fixture policy, test matrix, and evidence conventions for the implemented CEVCMS V1.0 core.

## Scope

Inspect actual implementation/verification status for EPIC-1 through EPIC-5; classify each dependency; identify available backend/frontend runners; define unit/API/RBAC/integration/frontend/manual/regression coverage; prepare synthetic fixtures and a readiness matrix; document blocked tests.

## Out of Scope

Application changes, new test framework installation, fixing defects, implementing missing upstream tasks, real data/integrations, load testing, formal penetration testing, and stretch-module QA gates.

## Preconditions

Repository and authoritative documents are available; EPIC-6 directory is created. Actual upstream state may be incomplete and must be recorded honestly.

## Dependencies

EPIC-0 through EPIC-5 task packages and current `develop` state; `.agents/rules/05-testing-rules.md`; Minimum Project Plan Section 6.4/7.1. No implementation dependency is required for planning.

## Inputs

Source documents, task contracts, branch/status history, test manifests, environment configuration, synthetic-data policy, and upstream completion evidence.

## Expected Outputs

QA strategy, scope/test matrix, environment checklist, fixture plan, evidence naming convention, dependency status table, and blocked-test register.

## Relevant Files / Modules

`.agents/tasks/`, `backend/tests/`, `frontend/`, `frontend/package.json`, Postman collection location if present, `docs/testing/` or current test documentation. Do not modify protected files.

## Backend Responsibilities

Inventory backend test commands and API environments; no code changes.

## Frontend Responsibilities

Inventory existing frontend build/lint/test/manual capabilities; explicitly record absence of a test runner if still true.

## Database Responsibilities

Define read-only verification queries and seeded-data requirements; do not alter schema or insert acceptance records directly.

## API Requirements

Inventory only documented upstream endpoints and required auth/error cases; missing contracts are blocked and marked `Traceability gap - requires review`.

## UI / UX Requirements

Define manual evidence for implemented screens, responsive checks, loading/error states, and public/private data boundaries without prescribing an unapproved framework.

## Security Requirements

Use four roles only; synthetic/anonymized data; never store credentials, JWTs, HMAC keys, or PII in evidence.

## Validation / Error Handling

Define expected invalid-input categories per actual contract; do not invent status codes or response fields.

## Acceptance Criteria

- Every EPIC-1 through EPIC-5 dependency is classified specified/implemented/tested/verified/approved/merged.
- Core and out-of-scope test boundaries are explicit.
- Environment and available tooling are verified, not assumed.
- Every blocked test names its dependency, evidence needed, and unblock condition.
- Evidence and synthetic-fixture rules are usable by QA owners.

## Testing Requirements

Run repository-available discovery checks and existing test-list commands where possible; do not claim feature tests pass from planning evidence.

## Evidence Requirements

Strategy document, dependency matrix, command/tool inventory, sanitized fixture inventory, and blocked-test register.

## Traceability

Implementation Specification EPIC-6 Testing & QA; Design Document Sections 14, 17, 20; Minimum Project Plan Sections 6.4, 7.1-7.2; Baseline Sections 3-5; rules 00, 01, 02, 05, 06; upstream EPIC handoffs.

## Ownership, Git, and Change Control

Primary: Ephratha. Documentation: Kidus. Independent reviewer required. Branch `feature/EPIC-6-QA-001-test-strategy`; commit `docs(qa): define EPIC 6 test strategy and environment`; PR to `develop`. Any new tool, fixture requirement, or scope change follows PM change control.

## Blockers / Stop Conditions

Stop planning only if authoritative scope cannot be identified. Mark execution areas blocked when upstream implementation/evidence/tooling is absent; never substitute invented behavior.
