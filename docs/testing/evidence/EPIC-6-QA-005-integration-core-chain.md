# EPIC-6-QA-005 — Integration and Core-Chain Evidence

## Status

**COMPLETED — APPROVED FOR INTEGRATION under PD-011.**

## Scope, baseline, and environment

- Branch: `feature/epic-6-qa-005-integration-core-chain`.
- Base `develop`: `32a9a39dcc1906c1951cc498ce58619c2cb86787`.
- PD-006 is active: this activity verifies the backend/API/database core chain only. QA-006 independently owns all frontend and browser verification.
- PD-007 is not a QA-005 execution blocker and was not progressed.
- Local target: the configured local PostgreSQL development database and a temporary local Uvicorn process at `127.0.0.1:8002`.
- A fresh, in-process QR signing setting and local public base URL were supplied only to the temporary server. They were not written to the collection, evidence, Git history, or terminal evidence.
- The normal API authenticated the approved local synthetic `qa.admin` account and confirmed the **Admin** role. The generated password and resulting bearer token remained runtime-only.

## New synthetic QA-005 core chain

This is a new run, not a substitution for TRACE-007, QR-006, FE-010, QA-003, or QA-004 evidence. All identifiers below are synthetic IDs from the same run.

| Step | Sanitized observed result | Result |
| --- | --- | --- |
| Authentication | `POST /api/v1/auth/login` and authenticated role check succeeded for the synthetic Admin fixture. | PASS |
| Farmer | New Farmer **959**, FIN `ETH-FAR-7935-485320`, was created through the approved API. | PASS |
| Farm/polygon | New Farm **789** links to Farmer 959; read-only DB inspection reported `POLYGON`, SRID 4326, calculated area **486.4474 ha**, and implemented demonstration review/EUDR flag `true`. This is demonstration logic, not formal EUDR compliance. | PASS |
| Coffee Lot | New Lot **359**, GIN `ETH-LOT-2026-948082`, links to Farm 789. Its API result showed server-controlled `created` status and authenticated creator ID **888**. | PASS |
| Automatic event | Initial Event **449**, type `lot_created`, links to Lot 359 with server-recorded actor 888. | PASS |
| Appended event | New Event **450**, type `qa005_trace_appended`, links to Lot 359 with server-recorded actor 888. The initial event remained intact. | PASS |
| Protected trace | The authenticated trace response linked the same Farmer 959 → Farm 789 → Lot 359 / GIN and returned the ordered event sequence `lot_created`, then `qa005_trace_appended`. | PASS |
| QR generation | New active QR **212** links to Lot 359. Generation returned the same GIN, a public QR ID, verification URL, SVG data URI, and PNG data URL; it exposed no raw canonical payload, payload hash, or signature field. | PASS |
| Public verification | The public API was invoked without an Authorization header for this QR. It returned a valid minimized result for the same GIN and did not expose Farmer contact data, credentials, tokens, or cryptographic internals. | PASS |

## Database relationship and consistency evidence

Read-only SQLAlchemy/PostGIS inspection after API creation observed:

```text
Farmer 959
  -> Farm 789 (POLYGON, SRID 4326, 486.4474 ha, demo flag true)
  -> Lot 359 / ETH-LOT-2026-948082 (created; creator 888)
  -> Events 449 lot_created, 450 qa005_trace_appended (both Lot 359; actor 888)
  -> QR 212 (Lot 359; active true)
```

- DB Farmer → Farm: PASS.
- DB Farm → Lot: PASS.
- DB Lot → Events: PASS; both expected events are present, ordered, and linked to the same Lot.
- DB Lot → QR: PASS; exactly the observed generated QR belongs to the same Lot and is active.
- Database/API identifier comparison: PASS; all API-captured IDs match the read-only relationships above.
- Transaction consistency: PASS. The API-created Lot and automatic `lot_created` event were both present and correctly linked. Existing lot API transaction coverage is supporting evidence; no destructive rollback simulation was invented for this run.

## API collection and execution

Sanitized dynamic collection: `docs/testing/postman/EPIC-6-QA-005.postman_collection.json`.

The collection uses blank runtime-only credentials/tokens and captures the run's Farmer, Farm, Lot, GIN, event IDs, QR ID, and verification data only in Newman runtime variables. It contains no credential, JWT, signing key, HMAC secret, signature, local environment value, or real PII.

```text
newman 6.2.2
newman run docs/testing/postman/EPIC-6-QA-005.postman_collection.json \
  --env-var baseUrl=http://127.0.0.1:8002 \
  --env-var <synthetic-runtime-credential>

Result: 10 requests, 10 assertions, 0 failures, exit 0
```

The run exercised login; role confirmation; Farmer; polygon Farm; Lot; initial trace; appended trace; protected trace; QR generation; and public verification in one dependent chain.

## Automated regression

The full current backend suite contains 74 discovered tests. It was executed in bounded, sequential test-file groups against the same local test environment to avoid the command runner's single-process window and shared-database concurrency. Every group exited 0; the 15 user-management tests were additionally observed as three passing subsets (4 + 6 + 5).

```text
.venv\Scripts\python.exe -m unittest discover -s tests -p <test_file> -q

Result: PASS — 74/74 current backend tests across all 14 test files.
```

Focused API/integration coverage in that execution includes Farmer, Farm/polygon, Coffee Lot/GIN, traceability, QR, RBAC, auth/session, schema, seed, and user-management modules.

The existing local dotenv parser emits a line-14 warning before test startup. It did not expose a value, affect the temporary API run, or cause a test failure; it remains a non-blocking local-environment observation.

## Requirements traceability

| Requirement/task area | QA-005 evidence |
| --- | --- |
| FR-AUTH-001/002; AUTH-008 | Normal synthetic login, authenticated protected trace, and unauthenticated public QR boundary. |
| FR-FARM-001/002; FARM-007 | Same-run Farmer and polygon Farm, persisted relationship, calculated area, and implemented demonstration flag. |
| FR-TRACE-001/002; TRACE-007 | Same-run Lot, generated GIN, automatic initial event, append-only follow-on event, and ordered protected trace. |
| QR-006 / approved QR contract | Same-Lot QR generation, QRRecord linkage/lifecycle, and anonymous minimized public verification. |
| PD-006 | API/database-only verification; no browser or UI claim. |

## Security and scope review

- PASS: only local synthetic fixtures and runtime credentials were used.
- PASS: no secrets, passwords, tokens, hashes, signatures, database connection data, or real Farmer PII are stored in this evidence or collection. The collection contains only a deterministic synthetic polygon test fixture, not a real farm location.
- PASS: no application source, schema, API contract, frontend, or environment file changed.
- PASS: no browser, Copilot, or UI verification was used or claimed; QA-006 remains unstarted.
- PASS: QA-007 through QA-010 and EPIC-7/EPIC-8 remain unstarted.

## Defects, blockers, and observations

No QA-005 integration defect candidate or blocking core-chain failure was found.

The only environment observation is the pre-existing local dotenv parser warning noted above. It is not an API/database integration defect and was not changed.

## PD-011 solo-review record

- **Task/branch:** EPIC-6-QA-005 / `feature/epic-6-qa-005-integration-core-chain`.
- **Author:** Kaleab Bantayehu, Project Manager/project owner.
- **Reason the documented solo-review path applies:** this is a genuine single-developer project with no separate human reviewer available; PD-011 governs owner review and integration.
- **Exact reviewed delta:** QA-005 commit `293d6bd29dbac41ca25230cdd88e8ba71037469a` contains only this evidence record and the sanitized QA-005 Newman collection. No application source, local credential/environment file, database dump, protected prompt, or later QA task is in scope.
- **Task-contract review:** PASS. A new same-run API/database chain completed from authenticated Farmer creation through anonymous public QR verification; database links, automatic and appended events, trace ordering, QR lifecycle, sanitization, and automated regression were verified. Browser verification was intentionally deferred to QA-006 under PD-006.
- **Execution evidence reviewed:** 10 Newman requests / 10 assertions / 0 failures; read-only relationship chain; 74/74 backend regression; collection JSON validation; and `git diff --check` before commit.
- **Defects/blockers:** none found. The local dotenv parser warning is non-blocking and unchanged.
- **Approval state:** **APPROVED FOR INTEGRATION** by the Project Manager/project owner under PD-011 on 2026-09-06. No AI assistant or tool is represented as an independent human reviewer.

## Final status

**COMPLETED — APPROVED FOR INTEGRATION.** The QA-005 API/database core-chain exit criteria are satisfied. QA-006 is the next approved sequencing step and is not started by this task.
