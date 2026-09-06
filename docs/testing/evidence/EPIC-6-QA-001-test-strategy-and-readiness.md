# EPIC-6-QA-001 — Test Strategy and Environment Readiness

## Task and status

- **Task:** EPIC-6-QA-001 — Test Strategy and Environment
- **Status:** COMPLETED WITH CONDITIONS
- **Prepared branch/base:** `feature/epic-6-qa-001-test-strategy` from `develop` at `c25a50f0a1d2e2ceb7f84f321aa6720cd8c1a946`.
- **Stable baseline inspected:** `main` merge `d2ae1e11da23ca00a3c28585c13551300c04eb44` (`merge: complete EPIC-5 frontend integration`). `develop` is an ancestor of that merge; the merge adds no content change beyond the completed EPIC-5 integration history.
- **Scope:** QA planning, readiness reconciliation, test-asset inventory, fixture policy, and evidence conventions only. This record does not execute QA-002 through QA-010 and does not change application code.

## Authority and scope basis

This strategy follows the Baseline Scope Freeze, Implementation Specification, Design Document, Minimum Project Plan, SRS, Implementation Playbook, the EPIC-6 task package, and `.agents/rules/00-project-authority.md` in that precedence order. The reviewed sources retain the frozen React/JavaScript, FastAPI, PostgreSQL/PostGIS, Leaflet, JWT/RBAC, HMAC QR, and Postman decisions. The bounded acceptance chain is:

`Login → Farmer → Farm/Polygon → Coffee Lot → Traceability Event → QR → Public Verification`.

Only the frozen roles are in scope: Admin, ECTA Officer, Field/Registry Agent, and Verifier. Public QR verification is the intentional unauthenticated exception. QA does not add roles, endpoints, database changes, test frameworks, external integrations, load testing, or stretch-module testing.

## Reconciliation of stale EPIC-6 assumptions

| Earlier conditional assumption | Current evidence and disposition |
| --- | --- |
| EPIC-1 through EPIC-5 implementation state is unknown. | **RESOLVED.** The implementation/evidence lineage is present on `develop`; EPIC-5 was merged to `main` in `d2ae1e1`. Upstream evidence is summarized in the entry matrix below. Independent EPIC-6 execution remains required. |
| GIN format may be unresolved. | **RESOLVED.** PM-approved `PD-003 final decision.md` fixes `ETH-LOT-YYYY-NNNNNN` and `^ETH-LOT-\\d{4}-\\d{6}$`; `backend/tests/test_lot_gin.py` and traceability evidence use it. The older `03-gin-format.md` is historical, not normative. |
| QR payload/public-response details may block assertions. | **RESOLVED.** PD-004 is approved in `04-qr-contract.md`; QR-002 through QR-006 and their evidence consume it. QA QR assertions must use its exact lifecycle, HMAC, public-minimization, and status contract. |
| Router, token, and dashboard behavior may be unspecified. | **RESOLVED for implemented V1.0 behavior.** FE-002/003/004 reconciliation evidence records the existing React auth context/session-expiry handling, protected navigation/logout, and dashboard scope. QA tests the implemented behavior; it does not infer a different router, persistence mechanism, or count endpoint. |
| Core-chain readiness is unknown. | **RESOLVED for readiness.** `EPIC-3-TRACE-007-supplemental-verification.md`, `EPIC-4-QR-006-verification.md`, and `EPIC-5-FE-010-integration-e2e-verification.md` record synthetic Farmer-to-public-QR chain evidence. This is reused for setup/readiness, not relabeled as EPIC-6 execution. |

## Genuine open discrepancies and conditions

| Item | Status | QA handling and rationale |
| --- | --- | --- |
| Minimum Project Plan wording referring to an “Exporter” versus the frozen four-role model | **OPEN — NON-BLOCKING** | Test only the four frozen roles. Do not create or test an Exporter role. Record the source discrepancy in QA-008/009; the Baseline/current-decision record controls V1.0 operation. |
| Historical Abel ownership wording | **RESOLVED operationally / OPEN — NON-BLOCKING historically** | PD-005 approves Biniyam as frontend lead and Abel as support. Do not silently rewrite the older source wording; QA ownership remains Ephratha/Kidus as task-defined. |
| Schedule/document wording differences | **OPEN — NON-BLOCKING** | Use the current repository documents for timing evidence and report discrepancies; schedule wording does not change functional QA criteria. |
| QA-005/QA-006 dependency sequence | **OPEN — BLOCKING for final sequencing only** | PD-006 remains unresolved. QA-001 can plan, and QA-002/003/004 can be planned independently. Before scheduling/closing QA-005 and QA-006, PM must approve a non-circular sequence. |
| Canonical project-wide evidence locations | **OPEN — BLOCKING for final canonicalization only** | PD-007 remains unresolved. This task-local record uses the established `docs/testing/evidence/` pattern but does not declare it the project-wide canonical location. PM must resolve PD-007 before QA-008/009/010 final evidence organization. |
| QR-configured live environment | **OPEN — NON-BLOCKING readiness condition** | Existing QR evidence distinguishes a default local configuration error from the configured synthetic verification path. QA QR execution requires local, uncommitted `QR_HMAC_SECRET_KEY` and `PUBLIC_QR_BASE_URL`; absence is not automatically a product defect. |

## Upstream entry readiness matrix

“Tested” and “Verified” below refer to committed upstream evidence. “Ready” means ready to be independently exercised by the named EPIC-6 task, not already QA-approved.

| Area | Specified | Implemented | Tested | Verified | Approved | Merged | Ready for QA execution | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Authentication/RBAC | Yes | Yes | Yes | Yes | Yes | Yes | Yes — QA-002/003/004 | Auth/RBAC tests in `backend/tests/test_auth_login.py`, `test_auth_session.py`, `test_rbac.py`, `test_security.py`; FE-002/003 evidence; frozen four-role record in current decisions. |
| Farmer Registry | Yes | Yes | Yes | Yes | Yes | Yes | Yes — QA-002/003/005/006 | `test_farmer_api.py`, `test_farmer_fin.py`; `EPIC-2-verification.md`; FE-005 evidence. |
| Farm/Polygon | Yes | Yes | Yes | Yes | Yes | Yes | Yes — QA-002/003/005/006 | `test_farm_api.py`, `test_db_schema.py`; `EPIC-2-verification.md`; FE-006 evidence. |
| Area/EUDR demonstration logic | Yes | Yes | Yes | Yes | Yes | Yes | Yes — QA-002/003/005/006 | Farm tests and `EPIC-2-verification.md` record polygon/point-radius area and demonstration state; FE-006 evidence. |
| Coffee Lot | Yes | Yes | Yes | Yes | Yes | Yes | Yes — QA-002/003/005/006 | `test_lot_api.py`, `test_lot_gin.py`; `EPIC-3-TRACE-007-supplemental-verification.md`; FE-007 evidence. |
| Traceability Events | Yes | Yes | Yes | Yes | Yes | Yes | Yes — QA-002/003/004/005/006 | `test_lot_api.py`, `test_rbac.py`; TRACE-007 supplemental; FE-008 evidence. |
| Trace view | Yes | Yes | Yes | Yes | Yes | Yes | Yes — QA-003/005/006 | TRACE-007 supplemental and FE-008 evidence record origin hierarchy, ordered events, bounded missing-Lot handling. |
| QR generation | Yes | Yes | Yes | Yes | Yes | Yes | Yes — QA-002/003/004/005/006, with configured QR environment | PD-004; `test_qr_api.py`; `EPIC-4-QR-006-verification.md`; FE-009 evidence. |
| Public QR verification | Yes | Yes | Yes | Yes | Yes | Yes | Yes — QA-003/004/005/006, with configured QR environment | PD-004; `test_qr_api.py`; QR-006 verification; FE-009 evidence. |
| EPIC-5 integrated frontend | Yes | Yes | Lint/build and browser evidence | Yes | Yes | Yes | Yes — QA-006 | FE-001 through FE-010 reconciliation evidence, especially `EPIC-5-FE-010-integration-e2e-verification.md`; main merge `d2ae1e1`. |

## Existing test-asset inventory

### Backend

- **Runner:** Python `unittest` discovery; `backend/.venv/Scripts/python.exe -m unittest discover -s backend/tests -v` is the supported regression command.
- **Static inventory:** 14 `test_*.py` files and 74 `def test_...` cases currently discovered by source inventory. QA-001 did not rerun them.
- **Coverage areas:** configuration/security; authentication/login/session; users/RBAC; seed/idempotency; Farmer FIN/API; Farm/polygon/API/schema; Coffee Lot/GIN/API; QR/API; database schema.
- **Existing focused files:** `test_auth_login.py`, `test_auth_session.py`, `test_config.py`, `test_db_schema.py`, `test_farm_api.py`, `test_farmer_api.py`, `test_farmer_fin.py`, `test_lot_api.py`, `test_lot_gin.py`, `test_qr_api.py`, `test_rbac.py`, `test_security.py`, `test_seed.py`, `test_user_management.py`.

### API and input-validation assets

- `docs/testing/postman/EPIC-2.postman_collection.json` with `EPIC-2.local.postman_environment.json` (local-only; never publish values).
- `docs/testing/postman/EPIC-4-QR-002-generation.postman_collection.json` and `EPIC-4-QR-003-public-verification.postman_collection.json`.
- Existing evidence records EPIC-2 Newman execution with 11 requests/assertions and zero failures, plus QR/trace API results in their task evidence. Re-run results are not claimed by QA-001.
- Endpoint-specific automated coverage is provided primarily by the backend test files above; QA-003 will execute only documented endpoint contracts and malformed-input cases.

### Frontend assets

- `frontend/package.json` provides `dev`, `build`, `lint`, and `preview`; it provides **no frontend test script or approved frontend test runner**.
- Recorded upstream browser/manual evidence exists for FE-001 through FE-010, lot/trace (`TRACE-007`), and QR (`QR-006`).
- QA-006 must collect independent functional/manual evidence using the existing supported browser path where available; QA-001 does not add Playwright, Cypress, Jest, Vitest, or another framework.

### Database and integration assets

- Alembic migrations are `0001_initial_core_schema.py`, `0002_make_farm_derived_fields_nullable.py`, and `0003_qr_record_lifecycle.py`.
- TRACE-007 supplemental records a synthetic read-only Lot → Farm → Farmer → TraceabilityEvent relationship check. QR-006 records the QR lifecycle/public verification chain and one-active-QR check. FE-010 records the integrated frontend flow.
- QA-005 must independently verify its required relationship/core-chain evidence with read-only database inspection only; it must not insert data through SQL.

## Approved QA environment and tooling

Only the following observed/project-supported tools are planned:

| Tooling | Observed version/status | QA use |
| --- | --- | --- |
| Backend Python | Python 3.13.3 | `unittest` execution and API service. |
| Alembic | 1.19.1 | Migration/current-state checks. |
| Node.js | v22.15.0 | Frontend tooling. |
| npm | 11.11.0 | Existing frontend scripts only; do not install packages. |
| React/Vite | Repository-pinned in `frontend/package.json` (React 19.2.8; Vite 8.2.0) | Existing app lint/build/manual path. |
| PostgreSQL client | `psql.exe` is installed locally; server/PostGIS version is not asserted by QA-001 | Read-only QA-005 verification against a configured synthetic database. |
| Postman/Newman | Project-approved Postman collections exist; `newman.cmd` is locally discoverable | Sanitized API runs when configured; no credentials in artifacts. |
| Browser/manual path | Existing EPIC-5 browser evidence path | Manual/UI evidence only; no new automation infrastructure. |

The QA environment must use a locally configured backend, database, and frontend; synthetic role accounts; an existing synthetic Farmer/Farm/Lot chain; and QR environment values only in noncommitted local configuration. QA-001 records no environment values, credentials, tokens, or secrets.

## Synthetic fixture policy

1. Use seeded or newly created **synthetic/anonymized** records only; no real farmer PII, live financial data, or production integration data.
2. Use exactly four accounts: Admin, ECTA Officer, Field/Registry Agent, and Verifier. Store passwords and JWTs only in local runtime/Postman environments, never in committed evidence.
3. Reuse existing safe fixtures where possible. Create task-scoped synthetic records only through the supported UI/API workflow needed for the QA case.
4. Use the approved FIN decision and PD-003 GIN shape; consume PD-004 QR behavior without constructing an alternative payload, QR identifier, or verification response.
5. Maintain a usable chain: Farmer → Farm (polygon or permitted representation) → Coffee Lot → initial and appended Traceability Events → active QR → public verification.
6. Record fixture aliases/IDs only when non-sensitive and useful for repeatability. Redact or omit payload signatures, signing keys, passwords, JWTs, national IDs, phone numbers, coordinates, and raw PII.

## EPIC-6 execution matrix (prepared, not executed)

| Future task | Scope | Implementation dependency | Upstream evidence reused for readiness | Independent EPIC-6 execution still required | Blocking condition | Intended evidence |
| --- | --- | --- | --- | --- | --- | --- |
| QA-002 | Backend unit/component coverage; available frontend component path | Implemented backend and existing frontend scripts | 74-test inventory and upstream regression evidence | Yes: run/record targeted and full applicable tests; document absent frontend runner honestly | None for backend; no approved frontend component runner means frontend component execution is not applicable unless an existing supported runner is found | Sanitized command output and test-case mapping |
| QA-003 | Documented APIs and malformed input | Running local backend, synthetic fixtures, documented endpoints | Existing Postman collections and endpoint tests | Yes: execute selected API/validation matrix | Local service, synthetic credentials, and applicable QR config needed | Sanitized Postman/Newman/API results |
| QA-004 | Authentication, four-role RBAC, public/private security boundaries | Seeded four-role accounts and local backend | Auth/RBAC tests, FE-003, QR-006 public/private evidence | Yes: independently exercise allowed/denied/unauthenticated cases | All four synthetic roles must be available | Sanitized status/result matrix |
| QA-005 | Cross-module API/database integration and core chain | Stable database, backend, fixtures, QR config | EPIC-2, TRACE-007, QR-006, FE-010 chain evidence | Yes: one QA-owned core-chain run and read-only relationship check | PD-006 must be resolved before final QA-005/QA-006 sequencing/closure; QR config required for QR leg | API output, read-only DB query output, sanitized walkthrough record |
| QA-006 | EPIC-5 screens, UI states, role/public-route behavior | Runnable frontend/backend and seeded fixtures | FE-001–010, TRACE-007, QR-006 browser evidence | Yes: independent UI/manual verification | PD-006 sequencing decision; supported browser/manual environment; QR config for QR happy path | Screenshots/manual checklist, lint/build results |

## Evidence convention

Each new EPIC-6 artifact must include, where applicable:

- QA test-case ID and requirement/task mapping;
- branch, commit/build, environment description, and execution date;
- test result (`PASS`, `FAIL`, `BLOCKED`, or `NOT RUN`);
- sanitized evidence source/command/request identifier; and
- linked defect ID and regression result when failed.

Do not include passwords, JWTs, HMAC keys, environment-secret values, raw QR signatures/payload internals, real farmer PII, or exact sensitive coordinates. Evidence records must distinguish **upstream evidence reused for readiness** from **EPIC-6 execution evidence**.

## Defect readiness

QA-001 creates no defects. If later QA identifies a reproducible product defect under the approved environment, the QA-007 record must include: unique defect ID; severity; priority; affected requirement/task; environment; reproduction steps; expected result; actual result; sanitized evidence; owner; status; fix reference; and regression result. A missing local secret, unavailable browser path, or other documented environment limitation is not a product defect unless it reproduces as a product failure under the approved configured environment.

## Requirements-traceability preparation

QA-008 will maintain the following structure without inventing IDs:

| Requirement family | Narrowed V1.0 interpretation | Expected implementation/test references |
| --- | --- | --- |
| FR-AUTH-001/002 | JWT authentication, protected behavior, and frozen four-role RBAC | AUTH implementation/tasks; QA-002/003/004/005/006 evidence |
| FR-FARM-001/002 | Synthetic Farmer and Farm/Polygon registry, FIN, spatial/area demonstration state | FARM implementation/tasks; QA-002/003/005/006 evidence |
| FR-TRACE-001/002 | Coffee Lot/GIN, append-only traceability, approved QR generation/public verification boundary | TRACE and QR implementation/tasks; QA-002/003/004/005/006 evidence |
| Applicable SEC/NFR wording | Only source-supported security, privacy, validation, and demo-scale constraints | QA-003/004/005/006 evidence, with enterprise requirements recorded as narrowed/out of scope |

The matrix must show requirement ID → V1.0 interpretation → implementation task(s) → QA case(s) → evidence → result → defect/fix. Enterprise-only requirements are recorded as narrowed/out of scope, never as passed.

## QA-001 outcome

QA-001 is complete as a planning/readiness task. It does not certify the system for M6, does not declare QA-002 through QA-010 complete, and does not authorize EPIC-7 or EPIC-8. The two governance conditions (PD-006 and PD-007) are explicitly preserved for PM resolution before their affected later-stage closures.
