# EPIC-6-QA-004 — Authentication, RBAC, and Security Evidence

## Status

**COMPLETED — APPROVED FOR INTEGRATION under PD-011.**

## Scope and environment

- Branch: `feature/epic-6-qa-004-auth-rbac-security`
- Local target: PostgreSQL `cevcm_db` on `localhost` (`::1`), confirmed reachable as the repository's configured local development database.
- No production or shared remote host was contacted.
- The frozen roles tested were exactly **Admin**, **ECTA Officer**, **Field/Registry Agent**, and **Verifier**. The obsolete Exporter wording was not used.
- No frontend code or application authorization code was changed. Browser/UI verification remains QA-006 scope.

## Controlled local fixture preparation

The initially configured local bootstrap Admin could not authenticate against the current local database. Under the explicit local-fixture authorization, four non-personal `qa.*` accounts were prepared only in the local database:

| Account identifier | Database role | Login result | Role confirmed |
| --- | --- | --- | --- |
| `qa.admin` | Admin | 200 | Yes |
| `qa.ecta` | ECTA Officer | 200 | Yes |
| `qa.field` | Field/Registry Agent | 200 | Yes |
| `qa.verifier` | Verifier | 200 | Yes |

Provisioning used a narrow one-off local invocation of the application's existing `User`, `Role`, SQLAlchemy session, and `hash_password` utility. It created the four previously absent allowlisted `qa.*` identities, then reset only those same synthetic fixture passwords for the live run. No real identity was inspected, changed, elevated, or removed. Passwords were generated in process memory, supplied to Newman only as runtime variables, and not written to a file, collection, evidence, Git history, or terminal report.

Fixture sanity checks through the normal API were PASS:

- Admin `GET /api/v1/users`: 200.
- ECTA Officer `GET /api/v1/users`: 403.

## Live API security matrix

Executed against a temporary local Uvicorn instance at `127.0.0.1:8002`. A fresh in-process `QR_HMAC_SECRET_KEY` and local public base URL were supplied only to that temporary process. The server was stopped after execution.

| Area | Expected | Result |
| --- | --- | --- |
| Authentication failures | Generic invalid credentials 401; missing/malformed body 400 | PASS |
| Four role login and `/auth/me` | 200 and exact database-backed role for each fixture | PASS |
| Missing, malformed/invalid, expired JWT | Protected endpoint returns 401 | PASS |
| Admin user administration | Admin `GET /users` returns 200 | PASS |
| Lower-role administration | ECTA Officer, Field Agent, and Verifier receive 403 | PASS |
| Escalation resistance | Field Agent cannot create an Admin user: 403 | PASS |
| Farmer boundary | Field Agent creates synthetic Farmer: 201; Officer and Verifier denied: 403 | PASS |
| Farm boundary | Admin creates Farm: 201; Officer denied: 403 | PASS |
| Lot boundary | Field Agent creates Lot: 201; Officer and Verifier denied: 403 | PASS |
| Server-controlled lot fields | Client `created_by`, GIN, and status are not accepted as authority; response has the authenticated Field Agent ID, generated GIN, and `created` status | PASS |
| Trace behavior | ECTA Officer appends an event: 201 with server-recorded actor; Verifier reads authenticated trace: 200 | PASS |
| QR boundary | Admin generates: 201; Field Agent reuses: 200; Officer and Verifier denied: 403 | PASS |
| Public QR boundary | Verification without Authorization: 200; public response excludes national ID, phone, polygon geometry, QR internals, payload hash, and signature fields | PASS |
| QR tampering | Modified signature rejected: 400 | PASS |

## Automated execution

Sanitized collection: `docs/testing/postman/EPIC-6-QA-004.postman_collection.json`.

The collection stores blank runtime credential/token variables only. It contains no passwords, tokens, JWT signing key, HMAC key, QR signature, or personal data.

```text
newman.cmd run docs/testing/postman/EPIC-6-QA-004.postman_collection.json \
  --env-var baseUrl=http://127.0.0.1:8002 \
  --env-var <synthetic-runtime-credential-or-token-variable>

Result: 34 requests, 34 test scripts, 34 assertions, 0 failures (exit 0)
```

The expired-token assertion used the project's existing `create_jwt_token` helper with a negative expiration interval and the locally configured runtime signing setting. No token was persisted or displayed.

Focused backend regression evidence available during this QA activity:

| Suite | Result |
| --- | --- |
| `unittest discover -s tests -p 'test_auth*.py'` | PASS (exit 0) |
| `unittest discover -s tests -p 'test_rbac.py'` | PASS |
| QA-002 evidence: auth/security/seed component coverage | 14/14 PASS |

The local dotenv parser emits a pre-existing line-14 warning before test startup. It does not expose a secret, did not affect the temporary API or live matrix, and is recorded here as an environment observation rather than a security defect.

## Security and sanitization review

- No credentials, tokens, signatures, password hashes, JWT/HMAC secrets, exact geometry, or non-synthetic PII were committed or recorded.
- Public verification was exercised without a bearer token and was checked for minimized output.
- Protected operational endpoints returned 401 without/with invalid/expired tokens and 403 for authenticated insufficient roles.
- No unauthorized access, role confusion, privilege escalation, or sensitive public-field exposure was observed.

## Defects and follow-up

No QA-004 security defect candidate was found.

The only environment observation is the pre-existing dotenv parser warning noted above. It is not a QA-004 authorization failure and was not changed.

## Git and review state

- Only this evidence file and its sanitized QA-004 collection are QA-004 deliverables.
- `.agents/execution/IMPLEMENT-TASK-PROMPT.md` is a protected pre-existing local modification and must remain unstaged/uncommitted.
- No QA-005, QA-006, EPIC-7, or EPIC-8 work was started.
- The Project Manager/project owner approved this evidence for integration
  under the documented PD-011 solo-review exception.

## PD-011 solo-review record

- **Task/branch:** EPIC-6-QA-004 / `feature/epic-6-qa-004-auth-rbac-security`.
- **Author/reviewer:** Kaleab Bantayehu, Project Manager/project owner.
- **Reason the exception applies:** this is a genuine single-developer project
  with no second human team member available; PD-011 governs the documented
  owner self-review process.
- **Exact diff and task contract reviewed:** QA-004 commit
  `1cf7e9e9f6c0061cdcf63b04dda453af5bc7881c` contains only this evidence
  record and `docs/testing/postman/EPIC-6-QA-004.postman_collection.json`.
  The EPIC-6-QA-004 task contract was reviewed against the complete delta; no
  application source, local credential file, or unrelated QA task is changed.
- **Checks reviewed:** local QA target confirmation; independent four-role API
  execution; 401 missing/invalid/expired-token behavior; 403 insufficient-role
  behavior; generic login failure; privileged Farmer/Farm/Lot/QR boundaries;
  server-controlled identity fields; public QR minimization and tamper
  rejection; supported expired-token generation; Newman 34 requests/34
  assertions/0 failures; collection JSON validation; empty sensitive runtime
  variables; and feature-delta `git diff --check`.
- **Fixture classification:** **APPROVED LOCAL QA FIXTURE PREPARATION**. The
  localhost-only synthetic `qa.*` accounts used existing User/Role models and
  password hashing, introduced no bootstrap/backdoor endpoint, changed no real
  account, and are not a product change.
- **Security/sanitization review:** PASS. No plaintext password, bearer/JWT,
  signing key, HMAC key, QR signature, local environment file, real Farmer
  PII, or application source is included in the reviewed delta.
- **Unresolved risks/blockers:** none. The pre-existing dotenv parser warning
  remains a non-blocking local environment observation. PD-006 and PD-007
  remain deferred governance items for later QA tasks.
- **Approval state:** **APPROVED FOR INTEGRATION** by the Project
  Manager/project owner under PD-011 on 2026-09-06. No AI assistant or tool is
  represented as an independent human reviewer.
