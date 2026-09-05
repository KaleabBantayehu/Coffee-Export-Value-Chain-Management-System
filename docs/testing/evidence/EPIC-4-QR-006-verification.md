# EPIC-4 QR-006 Verification and Handoff Evidence

**Task:** EPIC-4-QR-006 — EPIC Verification and Core-Chain Sign-off
**Verification date:** 2026-09-05
**Status:** COMPLETED

## Scope and contract

The approved V1.0 QR contract is [PD-004](../../../.agents/tasks/PROJECT-DECISIONS/04-qr-contract.md), committed in `70c8d6d`. It fixes the HMAC-SHA256 canonical payload, separate `QR_HMAC_SECRET_KEY`, public QR identifier, active-record lifecycle, verification URL, and minimized public response.

| Requirement / gate | Status | Evidence |
| --- | --- | --- |
| QR-001 contract approved | PASS | PD-004 status is APPROVED; commit `70c8d6d`. |
| QR-002 signed generation/lifecycle | PASS | Commit `0ff936e`; current `test_qr_api` coverage verifies restricted generation, HMAC canonicalization, PNG/SVG output, reuse, regeneration, and one active record. |
| QR-003 public verification | PASS | Commit `e48f65f`; current tests verify unauthenticated valid/minimized output plus tampered/malformed/unknown/inactive handling. Prior supplied Newman evidence: Newman 6.2.2, 3 requests, 3 assertions, 0 failures. |
| QR-004 generation UI | PASS (prior browser evidence) | Copilot evidence supplied for authenticated Admin access, protected route, generation, QR/PNG display, print action, Verifier denial, and bounded nonexistent-Lot error. |
| QR-005 public UI | PASS (prior browser evidence) | Copilot evidence supplied for logged-out/logged-in valid verification, tampered/unknown/inactive/malformed states, and data minimization. QR-005 commit `c112728`. |
| EPIC-3 handoff | PASS | `docs/testing/evidence/EPIC-3-TRACE-007-supplemental-verification.md`, committed in `a195c79`, closes the historical verification limitation with synthetic UI and database evidence. |

## Current automated checks

| Check | Result | Evidence |
| --- | --- | --- |
| Backend regression | PASS | `backend/.venv/Scripts/python.exe -m unittest discover -s tests` completed with exit status 0. The discovered suite contains 74 tests. |
| Alembic state | PASS | `0003_qr_record_lifecycle (head)`. |
| Frontend lint | PASS | `npm.cmd run lint`. |
| Frontend production build | PASS | `npm.cmd run build` completed successfully with Vite. |
| Git whitespace check | PASS | `git diff --check` returned no whitespace errors. |
| Newman availability | PASS | `newman.cmd --version` returned `6.2.2`. The existing sanitized QR-003 collection is retained at `docs/testing/postman/EPIC-4-QR-003.postman_collection.json`; its prior successful synthetic-data execution is recorded above. |

## Database evidence

A read-only local query selected a complete, non-PII chain:

```text
CoffeeLot 110 (ETH-LOT-2026-288293)
  -> Farm 222
  -> Farmer 283
  -> 1 TraceabilityEvent
  -> 2 QRRecords, exactly 1 active
  -> 0 orphan QRRecords in the database
```

This confirms persisted linkage and lifecycle state. It does not by itself establish that this particular QR-bearing Lot was created through the UI.

## PD-004 security and minimization review

- The QR service signs/recomputes the canonical payload with HMAC-SHA256 using `QR_HMAC_SECRET_KEY`; it does not use a JWT-secret fallback.
- `qr_id` is distinct from the Lot GIN, and the public URL uses `/verify/{qrId}?sig={signature}`.
- Generation is limited to Admin and Field/Registry Agent; the public verification router has no authentication dependency and is read-only.
- Regeneration deactivates the prior active record, with the database partial-unique index preserving one active record per Lot.
- Public verification returns only `status`, `gin_code`, nullable `origin_region`, and nullable `grade`; tests assert the absence of farmer PII and signing material.
- Unknown/inactive records return generic `404`; malformed/tampered signatures return generic `400`; PNG and SVG generation are covered by automated tests.

No credential, JWT, HMAC secret, signature, password, local environment value, farmer name, national ID, phone number, farm geometry, or coordinate is included in this artifact.

## Remaining browser-only completion evidence

The QR-004 and QR-005 Copilot checks establish their individual UI contracts. QR-006 additionally requires one explicit, unbroken synthetic workflow. It remains to be recorded by Copilot:

1. Log in and use the UI to select/create the synthetic Lot from the existing Farmer/Farm/Polygon chain.
2. Observe its initial `lot_created` event, append a traceability event, and view its protected trace.
3. Generate a QR for that same UI-originated Lot.
4. Open its generated public URL while logged out and confirm the valid minimized result.
5. Run a read-only database query for that same Lot, demonstrating Farmer -> Farm -> CoffeeLot -> TraceabilityEvent -> QRRecord.

Do not record the task or EPIC as complete until that evidence is supplied and an independent human reviewer approves the final handoff.

## Supplemental same-Lot browser and database verification

**Verification date:** 2026-09-05
**Synthetic role:** Admin

The remaining browser-only evidence was completed as one unbroken workflow using the same UI-originated Coffee Lot:

- Logged in successfully as the synthetic Admin role.
- Selected Farm 326 through the Coffee Lot UI and created **Lot 254**.
- The UI displayed GIN **ETH-LOT-2026-205909** and status `created`.
- The protected trace view showed the Farmer -> Farm -> Coffee Lot chain and the automatically created `lot_created` event.
- Appended `quality_inspection` with synthetic notes through the protected traceability UI; the new event appeared after `lot_created`.
- Generated the QR from the same Lot trace view. The UI rendered the QR image, displayed **QR ID 113**, and displayed its verification URL.
- Logged out completely and opened the exact generated verification URL. The public route did not redirect to login and displayed `Status: Valid`, the matching GIN `ETH-LOT-2026-205909`, and safely unavailable origin information only. No private or cryptographic fields were rendered.

A read-only database query for Lot 254 confirmed:

```text
CoffeeLot 254 (ETH-LOT-2026-205909)
  -> Farm 326
  -> Farmer 411
  -> 2 TraceabilityEvents: lot_created, quality_inspection
  -> QRRecord 113
  -> exactly 1 active QRRecord
```

The browser and database evidence refer to the same Lot, GIN, traceability events, and active QR record. No database state was modified by the cross-check.

**Browser verification:** PASS
**Same-Lot database cross-check:** PASS
**Exactly-one-active-QR check:** PASS
