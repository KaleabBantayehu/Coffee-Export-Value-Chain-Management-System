# EPIC-6-QA-005 - Integration and Core-Chain Testing

## Objective

Verify the cross-module API/database integration and the complete V1.0 core chain using actual implemented services and synthetic data.

## Scope

Exercise Login -> Farmer registration -> Farm registration -> polygon capture -> area/EUDR status -> Coffee Lot -> Traceability Event -> trace retrieval -> QR generation -> public QR verification. Confirm persisted relationships, transaction outcomes, API handoffs, and no manual database intervention for workflow creation.

## Out of Scope

Implementing/fixing modules, direct insertion of acceptance records, schema/API redesign, stretch modules, load testing, formal penetration testing, and enterprise DAG/offline workflows.

## Preconditions

QA-001 complete; EPIC-1 through EPIC-5 completion/verification gates are implemented and approved; backend/frontend/database run; synthetic users/data and approved QR contract exist. Missing upstream gate blocks the relevant chain segment.

## Dependencies

EPIC-1-AUTH-008, EPIC-2-FARM-007, EPIC-3-TRACE-007, EPIC-4-QR-006, EPIC-5-FE-010; QA-002 through QA-004 results as applicable.

## Inputs

Approved endpoint/UI contracts, Postman collection, test fixtures, database read-only query plan, and core acceptance script.

## Expected Outputs

Integration test results, database relationship evidence, full-chain API evidence, failed-step/defect list, and explicit blocked/ready status.

## Relevant Files / Modules

Backend/API integration tests, Postman collection, frontend workflow, database read-only query location, and QA evidence files. Do not modify application source.

## Backend Responsibilities

Verify service-to-database/API joins and transaction integrity through public interfaces and read-only checks.

## Frontend Responsibilities

Coordinate with QA-006 for browser-created records; confirm actual UI calls the documented APIs.

## Database Responsibilities

Confirm Farmer -> Farm -> polygon/area/EUDR -> CoffeeLot -> TraceabilityEvent -> QRRecord links, using read-only queries after UI/API creation.

## API Requirements

Use only upstream documented endpoints and approved QR contract. Do not invent a dashboard or QR route. Record exact observed responses without secrets/PII.

## UI / UX Requirements

The complete workflow must be executable through the connected web application, with controlled transitions and errors.

## Security Requirements

Use synthetic data; verify auth boundaries and public QR minimization; no direct DB mutation to make the chain pass.

## Validation / Error Handling

Include invalid Farm/Lot/event/QR cases at integration boundaries and verify rollback/structured errors where documented. File defects instead of adapting.

## Acceptance Criteria

- A complete core chain is created and exercised through the approved UI/API path.
- Database evidence confirms correct persisted relationships and no orphaned records.
- Each handoff uses the actual upstream contract.
- Failure of any core link is reported as BLOCKED with an owning task and reproduction detail.
- No stretch functionality is required or used as a prerequisite.

## Testing Requirements

Run integrated Postman/API workflow, relevant automated suites, read-only database verification, and coordinate the manual browser chain with QA-006. Rerun after fixes via QA-007.

## Evidence Requirements

Timestamped workflow output, sanitized API results, screenshots/manual steps, read-only query output with synthetic IDs, and defect links.

## Traceability

Assignment Description acceptance workflow; SRS FR-AUTH/FR-FARM/FR-TRACE narrowed V1.0; Design Document Sections 4.1-5.3, 7-10, 13, 17; Implementation Specification core-chain and EPIC-6 integration testing; Minimum Project Plan Sections 4.1, 6.4, 7.1-7.2; upstream verification gates.

## Ownership, Git, and Change Control

Primary: Ephratha. Kidus owns walkthrough/evidence; module owners support diagnosis. Branch `feature/EPIC-6-QA-005-core-chain-integration`; commit `test(qa): verify CEVCMS core chain integration`; PR to `develop`. No fixes are made in this task.

## Blockers / Stop Conditions

Block immediately if any upstream gate is only specified, not implemented/verified/approved, or if a required contract is unresolved. Do not insert data directly or begin EPIC-7/8.
