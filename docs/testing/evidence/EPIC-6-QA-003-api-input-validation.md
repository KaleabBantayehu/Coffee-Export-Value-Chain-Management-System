# EPIC-6-QA-003 — API and Input Validation Testing

## Task, baseline, and result

- **Task:** EPIC-6-QA-003 — API and Input Validation Testing
- **Branch:** `feature/epic-6-qa-003-api-input-validation`
- **Base develop commit:** `e35b67e6228efdc76029809cc7b4d1ded9251b96`
- **Execution date:** 2026-09-06
- **Environment:** local Windows synthetic-data QA environment; FastAPI,
  PostgreSQL/PostGIS, Python virtual environment, and Newman 6.2.2.
- **Result:** COMPLETED.

This evidence is a new QA-003 execution. It does not relabel upstream
Postman output, prior backend tests, or QA-002 unit/component evidence as a
QA-003 result. It does not execute QA-004 or later QA work.

## API inventory and existing assets

| Area | Implemented API coverage available | Existing upstream asset | New QA-003 execution |
| --- | --- | --- | --- |
| Authentication | Login, authenticated profile/logout, protected boundary | `test_auth_login.py`, `test_auth_session.py` | Login success/invalid/missing/malformed and unauthenticated protected access. |
| Farmer | Create, detail, update, list/search | `test_farmer_api.py`, EPIC-2 collection | Fresh create/update/search, duplicate, and malformed input. |
| Farm/Polygon | Create/list/detail/validate | `test_farm_api.py`, EPIC-2 collection | Fresh polygon and point-radius creation plus invalid geometry, invalid type, and missing Farmer checks. |
| Lot/Trace Event/View | Create lot, append event, read trace | `test_lot_api.py` | Fresh lot, invalid/nonexistent Farm, event, invalid/nonexistent event, trace and missing-Lot checks. |
| QR generation | Generate/reuse and input/lifecycle boundaries | `test_qr_api.py`, EPIC-4 QR-002 collection | Fresh generation/reuse, malformed regenerate value, missing Lot, and response-minimization checks. |
| Public QR verification | Public valid/minimized, tampered, missing/unknown signature/record | `test_qr_api.py`, EPIC-4 QR-003 collection | Fresh public valid/tampered/missing-signature/unknown-record checks. |

Existing upstream collections are retained, not changed:
`docs/testing/postman/EPIC-2.postman_collection.json`,
`EPIC-4-QR-002.postman_collection.json`, and
`EPIC-4-QR-003.postman_collection.json`.

## New QA-003 Postman/Newman execution

- **Collection:** `docs/testing/postman/EPIC-6-QA-003.postman_collection.json`
- **Newman:** 6.2.2
- **Environment method:** existing uncommitted local synthetic environment for
  credentials; collection contains no credential, token, key, or PII value.
  A temporary local server used an ephemeral generated HMAC key and temporary
  public-base URL only for this run, then was stopped.
- **Execution:** 32 requests, 32 test scripts, 32 assertions, 0 failures,
  exit code 0; total duration 9.2 seconds.

The collection creates a run-unique synthetic Farmer identifier at runtime,
then carries its returned IDs only in memory through Farmer, Farm, Lot, Event,
QR, and public-verification requests. It does not export run variables,
responses, credentials, or signatures.

## API and malformed-input matrix

| Area | New QA-003 conditions | Actual result |
| --- | --- | --- |
| Auth | Valid login; invalid credentials; missing password; malformed JSON; unauthenticated protected Farm list | 200, 401, bounded 400, bounded 400, and 401 — PASS |
| Farmer | Valid create/read-update/search; duplicate national ID; missing required fields | 201, 200, 200, 409, and bounded 400 — PASS |
| Farm/Polygon | Valid polygon; valid point plus radius; invalid geometry; nonexistent Farmer; invalid radius type; validate | 201, 201, 400, 404, bounded 400, and 200 — PASS |
| Lot | Valid creation; missing `farm_id`; nonexistent Farm | 201, bounded 400, and 404 — PASS |
| Traceability event | Valid append; missing event type; nonexistent Lot | 201, bounded 400, and 404 — PASS |
| Trace view | Valid trace structure; nonexistent Lot | 200 and 404 — PASS |
| QR generation | First generation; active reuse; malformed `regenerate`; nonexistent Lot; response-minimization check | 201, 200, bounded 400, and 404 — PASS |
| Public QR | Valid unauthenticated verification; tampered signature; missing signature; unknown QR ID; minimized response check | 200, 400, bounded 400, and 404 — PASS |

Malformed body/query validation is intentionally returned as bounded HTTP 400
by the application-level `RequestValidationError` handler. QA-003 therefore
does not incorrectly require HTTP 422 for these requests. The handler returns
the controlled detail `Malformed request body.` rather than field-level
internals. HTTP 422 is not emitted by the implemented API for the exercised
malformed cases; this is an observation, not a defect.

## Focused automated API execution

All commands were run from `backend` with the repository virtual environment.

| Command | Result |
| --- | --- |
| `./.venv/Scripts/python.exe -m unittest discover -s tests -p 'test_auth*.py' -v` | 11/11 PASS |
| `./.venv/Scripts/python.exe -m unittest discover -s tests -p 'test_farmer_api.py'` | 8/8 PASS |
| `./.venv/Scripts/python.exe -m unittest discover -s tests -p 'test_farm_api.py'` | 6/6 PASS |
| `./.venv/Scripts/python.exe -m unittest discover -s tests -p 'test_lot_api.py'` | 7/7 PASS |
| `./.venv/Scripts/python.exe -m unittest discover -s tests -p 'test_qr_api.py'` | 5/5 PASS |

These are API/component tests, not merely utility tests. They independently
exercise HTTP status behavior, database-backed response contracts, malformed
and missing inputs, and the applicable authorization boundaries.

## HTTP status and bounded-error consistency

| Status | QA-003 result |
| --- | --- |
| 200 | PASS — login, reads/updates, validation, trace, QR reuse, and valid public verification. |
| 201 | PASS — Farmer, Farm, Lot, Event, and initial QR generation. |
| 400 | PASS — malformed request bodies/types, invalid geometry, tampered or absent QR signature. |
| 401 | PASS — invalid credentials and unauthenticated protected endpoint. |
| 403 | PASS in the focused QR API tests for ECTA Officer and Verifier QR-generation attempts. The current local read-only Postman token was expired/invalid and returned 401, so it was not retained as a QA-003 collection assertion; full role-matrix execution remains QA-004. |
| 404 | PASS — nonexistent Farmer/Farm/Lot/QR resources and unknown QR ID where applicable. |
| 409 | PASS — duplicate Farmer national-ID constraint. |
| 422 | OBSERVATION — the custom validation handler normalizes exercised validation failures to 400. |

No internal stack trace was accepted as an API result. Controlled JSON error
responses contained bounded `detail` values only.

## Security and data minimization

- **PASS:** QR-generation checks assert that response JSON excludes
  `payload_hash` and `hmac_signature`.
- **PASS:** Public QR checks assert that response JSON has only the approved
  status, GIN, origin-region, and grade shape; national ID, phone number, and
  HMAC-signature data are absent.
- **PASS:** Login and protected-boundary checks use structured, bounded errors;
  no stack trace, password, password hash, JWT secret, HMAC key, token, raw
  signature, or Farmer PII is recorded in this evidence or collection.
- **Scope note:** this is API response validation, not formal penetration or
  timing-security testing.

## Observations and defects

1. **OBSERVATION — upstream EPIC-2 collection fixture drift.** Its fixed
   synthetic national ID already existed locally, producing a duplicate 409 and
   cascading missing-variable failures. QA-003 did not change it; the separate
   run-unique collection above passed.
2. **OBSERVATION — running local API lacked QR runtime configuration.** It
   returned controlled 500 QR configuration errors. QA-003 used an ephemeral
   synthetic HMAC/base-URL configuration in a temporary local server to execute
   QR API behavior successfully. This is an environment-preparation condition,
   not an implemented QR defect.
3. **OBSERVATION — local read-only Postman token expired/invalid.** Its 401
   response is not treated as a 403 authorization result. Existing focused API
   tests demonstrate the QR-generation 403 boundary; QA-004 owns full
   four-role live verification.
4. **Coverage note:** no update/delete Event endpoint exists in the approved
   route inventory. QA-003 does not invent one; append-only/RBAC boundary depth
   remains QA-004 and integration verification.
5. **Non-failing test-run warnings:** `python-dotenv` parse warnings and the
   SQLAlchemy `datetime.utcnow()` deprecation warning appeared during tests.
   They caused no failure, skip, or error and are not QA-003 defects.

- **Defects found:** none.
- **Blocking defects:** none.

## Requirements traceability

| Requirement/task family | QA-003 evidence |
| --- | --- |
| FR-AUTH-001/002; EPIC-1 Auth/RBAC | Login success/failure, malformed requests, protected boundary, session/API tests. |
| FR-FARM-001/002; EPIC-2 Farmer/Farm/Polygon | Fresh Farmer, FIN-bearing API behavior, Farm geometry/area validation, constraints, and structured errors. |
| FR-TRACE-001; EPIC-3 Traceability | Lot creation, append event, trace response, missing-resource and malformed-input behavior. |
| FR-TRACE-002; EPIC-4 Dynamic QR | QR lifecycle, invalid inputs, public verification, tamper rejection, and public-data minimization. |

## Solo-review record — QA-003 feature branch

- **Task/branch:** EPIC-6-QA-003 /
  `feature/epic-6-qa-003-api-input-validation`.
- **Author/reviewer:** Kaleab Bantayehu, Project Manager/project owner.
- **Reason exception applies:** no second human team member is available;
  PD-011 governs the documented solo-developer review path.
- **Exact diff reviewed:** this QA-003 collection and evidence record only; no
  application source, local environment, credential, or upstream collection is
  changed.
- **Checks reviewed:** Newman 32/32 pass, focused API tests Auth 11/11,
  Farmer 8/8, Farm 6/6, Lot/Trace 7/7, QR 5/5; sanitization and diff checks are
  pending final artifact review.
- **Risks/blockers:** none unresolved. The observations above remain visible;
  QA-004 retains role-matrix depth and PD-006/PD-007 remain later-task
  governance conditions.
- **Approval state:** pending Project Manager owner approval before feature
  branch integration. No AI assistant or tool is represented as an independent
  human reviewer.

## Final QA-003 result

**COMPLETED.** Applicable API and malformed-input behavior was independently
executed and recorded with a passing sanitized Newman matrix and focused
backend API tests. No blocking API or security defect remains.
