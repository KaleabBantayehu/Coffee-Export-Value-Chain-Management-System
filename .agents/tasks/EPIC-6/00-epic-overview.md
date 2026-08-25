# EPIC-6 - Testing & QA

## Purpose

EPIC-6 is the independent quality gate for CEVCMS V1.0. It prepares, executes, records, and reviews evidence for the implemented core system: Authentication/RBAC -> Farmer Registry -> Farm/Polygon -> EUDR demonstration logic -> Coffee Lot -> Traceability Events -> QR generation -> public QR verification, including the integrated EPIC-5 frontend.

The epic tests what is actually implemented. Task-file existence is never treated as implementation completion. Every upstream dependency is classified as specified, implemented, tested, verified, approved, and merged before execution is claimed.

## Scope

- QA strategy, environment readiness, fixtures, test matrix, and evidence conventions.
- Backend unit and component tests for implemented business logic.
- Postman/API, malformed-input, and response/error testing for implemented endpoints.
- Four-role authentication/RBAC and security-boundary testing.
- Cross-module database/API integration and the complete core-chain test.
- EPIC-5 frontend functional and UI verification.
- Defect tracking, regression decisions, requirements traceability, test evidence, Test Report, and implemented-work user manual.
- Final M6 QA gate and explicit readiness recommendation.

## Explicit out of scope

No application implementation, defect fixes, schema/API changes, test-driven redesign, new testing framework unless authorized by existing project decisions, stretch-module implementation/testing as a core prerequisite, real external integrations, native offline/mobile testing, load testing including 5,000 TPS, formal penetration testing, or enterprise security validation. EPIC-7 Quality Grading/Waybill and EPIC-8 Export/Forex remain downstream and blocked until the core is operational and tested.

## Authoritative sources

- `docs/project-baseline/CEVCMS_V1_0_Baseline_Scope_Freeze.docx`, Sections 2-6: frozen V1.0, core chain, ownership, change control.
- `docs/project-baseline/CEVCMS_V1.0_Implementation_Specification.docx`: EPIC-6 Testing & QA, ownership, core-chain acceptance, test/report deliverables, Week 4 delivery.
- `docs/design/CEVCMS_Design_Document_V1.0.docx`, Sections 4.1-5.3, 7-10, 13-14, 17-20: architecture, data/API/security/UI behavior and scope reductions.
- `docs/project-baseline/CEVCMS_Minimum_Project_Plan_V1.0.docx`, Sections 2.1, 4.3, 6.4, 7.1-7.2: QA plan, risk register, WBS, M4/M5/M6 schedule.
- `docs/requirements/SOFTWARE REQUIREMENTS SPECIFICATION (SRS).pdf`: in-scope FR-AUTH, FR-FARM, FR-TRACE and security detail, narrowed by higher-authority V1.0 design/baseline.
- `docs/CEVCMS_V1.0_Implementation_Playbook.md`: per-feature testing, review, regression, documentation workflow.
- `.agents/rules/`, `.agents/execution/`, and EPIC-0 through EPIC-5 task packages.

## Task inventory

| ID            | File                                                | Deliverable                                                       | Owner                                     |
| ------------- | --------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------- |
| EPIC-6-QA-001 | `01-test-strategy-and-environment.md`               | Approved QA strategy, environment, fixtures, and readiness matrix | Ephratha; Kidus documentation             |
| EPIC-6-QA-002 | `02-unit-and-component-testing.md`                  | Backend unit and available frontend component test execution      | Ephratha; Biniyam support                 |
| EPIC-6-QA-003 | `03-api-and-input-validation-testing.md`            | Postman/API and malformed-input evidence                          | Ephratha                                  |
| EPIC-6-QA-004 | `04-authentication-and-rbac-security-testing.md`    | Four-role auth/RBAC/security verification                         | Ephratha                                  |
| EPIC-6-QA-005 | `05-integration-and-core-chain-testing.md`          | API/database/core workflow integration evidence                   | Ephratha; Kidus walkthrough evidence      |
| EPIC-6-QA-006 | `06-frontend-functional-and-ui-verification.md`     | EPIC-5 screen and browser verification                            | Ephratha; Biniyam support; Kidus evidence |
| EPIC-6-QA-007 | `07-defect-tracking-and-regression.md`              | Defect lifecycle, fixes, and regression evidence                  | Ephratha; Kidus log/documentation         |
| EPIC-6-QA-008 | `08-requirements-traceability-and-test-evidence.md` | Requirement-to-test-to-evidence matrix                            | Kidus; Ephratha results                   |
| EPIC-6-QA-009 | `09-test-report-and-user-manual.md`                 | Formal Test Report and implemented-scope user manual              | Kidus; Ephratha technical input           |
| EPIC-6-QA-010 | `10-final-qa-gate-and-m6-readiness.md`              | Final QA sign-off and M6 readiness recommendation                 | Ephratha + Kidus                          |

## Dependency graph

```text
EPIC-1..EPIC-5 task packages and implementation state inspection
                              |
                              v
                  QA-001 strategy/environment
                              |
          +-------------------+-------------------+
          v                   v                   v
      QA-002              QA-003              QA-004
   unit/component       API/validation       auth/RBAC/security
          |                   |                   |
          +-------------------+-------------------+
                              v
                  QA-005 integration/core chain
                              |
                              v
                  QA-006 frontend functional/UI
                              |
          +-------------------+-------------------+
          v                                       v
      QA-007 defects/regression              QA-008 traceability/evidence
          |                                       |
          +-------------------+-------------------+
                              v
                     QA-009 report/manual
                              |
                              v
                     QA-010 final QA/M6 gate
```

QA-001 can prepare the plan, matrix, environment checklist, and fixtures before all upstream implementation is complete. QA-002, QA-003, and QA-004 may prepare test cases in parallel after QA-001; execution of each area is conditional on the corresponding upstream implementation. QA-005 requires the implemented backend chain and stable database. QA-006 requires EPIC-5 screens and upstream APIs. QA-007 and QA-008 can begin evidence/log structure in parallel with execution but require results to close. QA-009 consumes QA-007/008 outputs. QA-010 is strictly last.

## Recommended execution order

1. QA-001 establishes scope, environment, fixture policy, and readiness statuses.
2. QA-002-004 prepare and execute unit, API/validation, and security tests as their dependencies become available.
3. QA-005 verifies cross-module integration and the complete core chain.
4. QA-006 verifies all implemented EPIC-5 screens and public/private UI boundaries.
5. QA-007 manages every defect and reruns targeted/full regression after fixes.
6. QA-008 maps requirements to implementation task, test case, evidence, result, and defect.
7. QA-009 produces the formal Test Report and implemented-only user manual.
8. QA-010 performs the independent final QA gate and M6 recommendation.

## Entry criteria

QA-001 may begin against the repository and task contracts. Execution-dependent tasks require: the relevant upstream task is implemented on `develop`, its tests exist and pass, its verification task has evidence, required human approval/merge is recorded, the local environment is runnable, and synthetic fixtures are available. Missing evidence is a blocker, not an assumption.

## Exit criteria

EPIC-6 is complete only when all applicable core tests have objective evidence, defects are dispositioned or explicitly block release, regression is green, the full core workflow has been manually and technically verified, public data minimization and four-role security checks pass, requirements/test evidence and Test Report/manual are updated, an independent human reviews the result, and QA-010 issues a documented GO for M6. No stretch work is required for core sign-off.

## Core V1.0 test strategy

Backend unit tests cover password hashing, seed/idempotency, FIN/GIN generation, area/EUDR logic, lot creation, append-only event behavior, and QR/HMAC behavior where implemented. API testing uses Postman plus existing automated tests for auth, Farmer, Farm/Polygon, Lot, Traceability, QR, and public verification. Validation covers malformed credentials, farmer/farm/polygon/lot/event/QR inputs. Security uses Admin, ECTA Officer, Field/Registry Agent, and Verifier only. Integration verifies Login -> Farmer -> Farm -> Polygon -> Area/EUDR -> Lot -> Event -> Trace -> QR -> public verification. Frontend verification covers actual EPIC-5 screens with automation only where the repository provides it; otherwise manual browser evidence is required.

## Defect lifecycle

Every defect receives a unique ID, severity, priority, affected requirement/task, environment, reproduction steps, expected and actual result, evidence, owner, status, fix reference, and regression result. Ephratha owns the defect log and triage. Kidus maintains documentation and traceability. A defect remains open until retested; any failed core/security/regression criterion blocks the relevant gate. Scope changes, architecture changes, or invented requirements follow PM change control rather than defect handling.

## Evidence strategy

Collect reproducible test output, Postman request/result exports without secrets, API status/response samples with synthetic data, screenshots for frontend/manual states, database read-only verification where relationship/integrity matters, logs only when sanitized and necessary, and end-to-end walkthrough evidence. Never include credentials, JWTs, signing keys, farmer PII, or real data. Evidence must identify test case, build/branch, environment, date, result, and defect reference where applicable.

## Requirements traceability strategy

Kidus maintains the matrix: requirement ID -> narrowed V1.0 interpretation -> implementation task(s) -> test case(s) -> evidence artifact -> result -> defect/fix if applicable. Use actual IDs only: FR-AUTH-001/002, FR-FARM-001/002, FR-TRACE-001/002, and applicable SEC/NFR IDs supported by the documents. Record unimplemented enterprise requirements as narrowed/out of scope rather than claiming coverage.

## Handoff from EPIC-5

EPIC-5 must hand over a runnable frontend, verified screen-to-API map, role/public-route behavior, synthetic walkthrough, responsive/manual evidence, regression results, and known-defect disposition. If FE-010 or upstream EPIC-1 through EPIC-4 verification is not approved, QA-006/QA-010 must mark the affected scope blocked.

## Handoff to EPIC-7

EPIC-7 may begin only after QA-010 confirms the frozen V1.0 core is operational and tested, with no blocking core/security defects and PM-approved disposition of known gaps. QA-010 does not authorize EPIC-7 implementation; it records the gate state. Stretch testing is not a prerequisite for core completion.

## Known blockers

Upstream implementation state is unknown until verified at task start; all execution tasks are conditional. Missing QA tooling, missing upstream evidence, and failed core/security criteria block the relevant gate.

## Known conflicts/gaps

- Upstream implementation state is unknown until verified at task start; all execution tasks are conditional.
- EPIC-2 FIN format and EPIC-3 GIN format gaps may affect fixtures and expected values; do not invent formats.
- EPIC-4 QR payload, identifier, library, and public-response contract gaps block QR-specific assertions until QR-001 is approved.
- Dashboard count API, frontend router/token persistence details may be unspecified; test only approved behavior and mark gaps.
- Abel's ownership descriptions conflict across authoritative Level-3 sources; assignment is not silently changed.
- The Minimum Project Plan's testing table mentions “Exporter,” conflicting with the frozen four-role model; QA uses only four roles and reports the discrepancy.
- Minimum Project Plan/document availability and schedule wording may differ from older governance notes; the actual current document is used and discrepancies are reported.

## Assumptions

- Assumption allowed for preparation only: test data is synthetic/anonymized and the existing local test tooling is used. Assumptions cannot turn into pass results without evidence.

## Ownership matrix

| Area                                              | Primary          | Supporting/verification                           |
| ------------------------------------------------- | ---------------- | ------------------------------------------------- |
| QA strategy, API/unit/validation/RBAC/integration | Ephratha         | Relevant module owner; independent human reviewer |
| Test cases, traceability, evidence archive        | Kidus            | Ephratha results                                  |
| Frontend functional support                       | Biniyam          | Ephratha/Kidus evidence                           |
| Defect triage                                     | Ephratha         | Kidus log; owning developer fixes                 |
| Test Report/user manual/progress evidence         | Kidus            | Ephratha technical results                        |
| Final QA recommendation                           | Ephratha + Kidus | PM/human approval                                 |

## Schedule

Minimum Project Plan Section 7.2 places core completion/testing in Week 3 M4, frontend integration and stabilization in Week 4, M5 client acceptance mid-Week 4, and M6 closure at Week 4 end. QA preparation starts incrementally; QA-010 is the M6 readiness gate. No schedule pressure authorizes bypassing tests, review, or unresolved decisions.

## Consistency audit

| Area                            | Result  | Explanation and action                                                                                                  |
| ------------------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------- |
| Scope                           | PASS    | Core QA only; stretch remains downstream.                                                                               |
| Requirements traceability       | PASS    | Matrix task explicitly maps requirement -> test -> evidence -> result -> defect.                                        |
| Architecture consistency        | PASS    | Tests existing modular monolith boundaries without redesign.                                                            |
| Technology consistency          | PASS    | Uses existing Python/FastAPI/PostgreSQL/PostGIS/React/Leaflet/Postman stack.                                            |
| Database consistency            | PASS    | Uses read-only verification and existing DB tests; no schema changes.                                                   |
| API consistency                 | PASS    | Tests documented upstream endpoints only; missing contracts block assertions.                                           |
| Frontend consistency            | PASS    | Tests actual EPIC-5 screens and existing tooling/manual path.                                                           |
| Authentication/RBAC consistency | PASS    | Uses exactly four frozen roles and public QR exception.                                                                 |
| Testing completeness            | PARTIAL | Completion depends on which upstream tasks are actually implemented; QA-001 tracks conditional gaps.                    |
| Security                        | PASS    | Covers auth, tampering, PII minimization, secrets, and structured errors; no penetration test claimed.                  |
| Evidence requirements           | PASS    | Evidence types are realistic: output, Postman, screenshots, sanitized logs, DB checks.                                  |
| Defect management               | PASS    | Lifecycle and required fields are defined in QA-007.                                                                    |
| Git workflow                    | PASS    | QA changes use feature branches/PRs and independent review; no direct develop/main work.                                |
| Change control                  | PASS    | Conflicts and missing requirements stop/escalate; no silent fixes.                                                      |
| Ownership                       | PARTIAL | Ephratha/Kidus ownership is clear, but Abel's existing conflict remains open. Action: report, do not reassign silently. |
| Schedule                        | PASS    | Week 3 M4 and Week 4 M5/M6 alignment is explicit.                                                                       |
| V1.0 scope freeze               | PASS    | No enterprise, offline, external, load, or stretch requirement is added.                                                |
| EPIC dependencies               | PARTIAL | EPIC-1 through EPIC-5 completion cannot be assumed. Action: verify gates before execution.                              |
| No duplicate EPIC-0 work        | PASS    | Existing environment/scaffold is consumed, not recreated.                                                               |
| No duplicate EPIC-1 work        | PASS    | Auth implementation is tested, not rewritten.                                                                           |
| No duplicate EPIC-2 work        | PASS    | Farmer/Farm/Polygon behavior is tested, not reimplemented.                                                              |
| No duplicate EPIC-3 work        | PASS    | Lot/Traceability behavior is tested, not duplicated.                                                                    |
| No duplicate EPIC-4 work        | PASS    | QR behavior is tested against approved contract, not implemented.                                                       |
| No duplicate EPIC-5 work        | PASS    | Frontend screens are verified, not rebuilt.                                                                             |
| No premature EPIC-7/EPIC-8 work | PASS    | QA-010 gates stretch start; no stretch implementation/testing prerequisite is created.                                  |

## Final delivery report

**A. File tree:** `00-epic-overview.md` plus `01` through `10` task files listed above.

**B. Task titles:** QA-001 strategy/environment; QA-002 unit/component; QA-003 API/validation; QA-004 auth/RBAC/security; QA-005 integration/core chain; QA-006 frontend/UI; QA-007 defects/regression; QA-008 traceability/evidence; QA-009 report/manual; QA-010 final gate/M6 readiness.

**C. Dependency order:** QA-001 -> QA-002/003/004 -> QA-005 -> QA-006 -> QA-007/008 -> QA-009 -> QA-010, with preparation parallelism documented above.

**D. Parallelizable tasks:** QA-002, QA-003, and QA-004 preparation/execution by independent scope after QA-001; QA-007 and QA-008 evidence structures can run alongside execution. Integration/final gates wait for prerequisites.

**E. Critical path:** QA-001 -> implemented upstream gates -> QA-005 -> QA-006 -> QA-007 -> QA-008 -> QA-009 -> QA-010.

**F. Traceability:** FR-AUTH, FR-FARM, FR-TRACE, approved security/design sections, EPIC task contracts, M4/M5/M6 WBS, and Assignment acceptance workflow are mapped per task.

**G. Open gaps:** implementation status, FIN/GIN/QR contract details, dashboard contract, Abel ownership, four-versus-five role test wording, and any schedule/document discrepancy.

**H. Cross-EPIC dependencies:** EPIC-1 through EPIC-5 implementation and verification handoffs are required; no task-file existence is sufficient.

**I. Audit:** 21 PASS, 3 PARTIAL, 0 FAIL; each PARTIAL has an action above.

**J. Safety:** this package is documentation only; no application source, earlier EPIC, rules, execution file, or authoritative document is modified.
