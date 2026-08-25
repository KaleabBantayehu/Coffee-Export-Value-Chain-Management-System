# EPIC 4 - Dynamic QR Engine

## EPIC identity

- **Epic ID:** EPIC-4
- **Official name:** Dynamic QR Engine
- **Primary owner:** Fistum, Traceability and QR, per Baseline Scope Freeze Section 5 and Implementation Specification EPIC 4.
- **Supporting frontend owner:** Biniyam, Frontend Lead. The Implementation Specification also names Abel for reusable QR UI components and API integration; this ownership overlap is recorded as an open decision below because the Baseline and Minimum Project Plan describe Abel differently.
- **Verification owners:** Ephratha for API, unit, input-validation, RBAC, and integration testing; Kidus for traceability matrix, test evidence, Test Report, and walkthrough documentation.

## Objective and business purpose

Implement the V1.0 QR leg of the core chain: generate a server-created QR for an existing traceable Coffee Lot, sign its payload with the frozen HMAC mechanism, persist the QR record, expose a public read-only verification endpoint, and provide the authenticated generation and public verification web experiences. This completes the acceptance path from Farmer -> Farm -> Polygon -> Lot -> Traceability -> QR -> public verification.

The business purpose is digitally verifiable farm-to-lot origin information for the university demonstration and ECTA workflow. The public result must contain only the non-sensitive summary approved by the Design Document.

## Scope

- QR payload schema and encoding contract, subject to Project Manager review where the authoritative documents are silent.
- HMAC-SHA256 signing and verification using the environment-provided QR signing key.
- QR record persistence related to an existing CoffeeLot.
- `POST /api/v1/lots/{id}/qr` for authenticated QR generation.
- `GET /api/v1/verify/{qrId}` as an unauthenticated, read-only public verification endpoint.
- QR image generation in the representations explicitly named by the Design Document: PNG/SVG, once the allowed library is confirmed.
- Authenticated QR generation UI and unauthenticated public verification page.

## Out of scope

No QR work may add MFA, refresh tokens, HSM, RS256, ABAC, Redis, microservices, blockchain, offline sync/mobile application, new databases, real external integrations, production-scale infrastructure, or real personal/financial/trade data. No lot splitting/merging, enterprise DAG lineage, quality grading, waybills, export licensing, or forex functionality. Do not expose farmer national ID, phone number, exact polygon coordinates, credentials, signing secrets, or internal database details in the public response.

## Authoritative sources

1. `docs/project-baseline/CEVCMS_V1_0_Baseline_Scope_Freeze.docx` - Sections 2-5: frozen V1.0 scope, technology, core workflow, ownership.
2. `docs/project-baseline/CEVCMS_V1.0_Implementation_Specification.docx` - EPIC 4 task list, API flow, Definition of Done, and four-week order.
3. `docs/design/CEVCMS_Design_Document_V1.0.docx` - Sections 5.3, 7.2, 8, 9.3-9.4, 10, 11, 13, 14, 16, 17, 20.
4. `docs/project-baseline/CEVCMS_Minimum_Project_Plan_V1.0.docx` - Sections 2.1, 4.1, 4.3, 6.4, 7.1-7.2: core module, risks, testing, WBS, M4 schedule.
5. `docs/requirements/SOFTWARE REQUIREMENTS SPECIFICATION (SRS).pdf` - Module 06, FR-TRACE-002, SEC-02/SEC-03 context, and Appendix C illustrative material.
6. `docs/CEVCMS_V1.0_Implementation_Playbook.md` - frozen workflow and traceability requirements.
7. `.agents/rules/00-project-authority.md`, `01-scope-boundaries.md`, `02-tech-stack.md`, `05-testing-rules.md`, and `06-change-control.md`.
8. `.agents/tasks/EPIC-3/` - the preceding Lot and Traceability task contract and handoff requirements.

## EPIC-3 dependency and completion status

EPIC-4 depends on EPIC-3 being **specified, implemented, tested, verified, and approved**, not merely having task files. Required handoff evidence is at least one persisted CoffeeLot with a valid GIN, Farm origin, and TraceabilityEvent chain reachable through the protected trace endpoint. `EPIC-3-TRACE-007` must confirm the chain and report whether its GIN-format gap was resolved or formally accepted as non-blocking. If any of those states is missing, EPIC-4 tasks that consume lot data are blocked and must not build substitute Lot/Traceability work.

EPIC-0, EPIC-1, and EPIC-2 are also prerequisites through the EPIC-3 handoff. Their task-file existence is not evidence of implementation or approval. Each execution must verify the actual merged, tested state and record it.

## Boundary conflict decision

The sources contain a documented organizational conflict, not a resolved technical contradiction:

- Implementation Specification EPIC 3 is “Traceability Engine” and EPIC 4 is “Dynamic QR Engine,” with separate task lists and Definitions of Done.
- Baseline Section 4 presents separate sequential workflow steps: “Create Traceability Record / Event,” “Generate QR,” and “Public Verification Page.”
- Minimum Project Plan Section 4.1 groups them as one core module, “Traceability & QR Engine,” and schedules that module by M4.

The higher-authority Baseline and Implementation Specification support a distinct QR backlog following EPIC-3; the plan's phrase describes a combined delivery/module grouping and does not define different endpoints or requirements. EPIC-4 therefore proceeds as QR-specific functionality after EPIC-3, while retaining the conflict in this record. No EPIC-3 file is modified.

## Documented gaps - review required

The authoritative material defines the mechanism and high-level flow but does not define all implementation details. Each gap is a controlled input to `EPIC-4-QR-001`; no task may silently choose a value:

- **Traceability gap - requires review:** exact QR payload field set, field names, canonical serialization, and version marker are not specified. The Design Document states only a verification URL and lot ID plus HMAC over the payload.
- **Traceability gap - requires review:** QR identifier (`qrId`) format, uniqueness/lifecycle rules, and whether it is the database ID or a separate public identifier are not specified.
- **Traceability gap - requires review:** QR generation library is not named. A narrowly scoped QR library is allowed only after the task records the choice and confirms it does not change the frozen stack.
- **Traceability gap - requires review:** exact public verification response schema and precise “coarse origin” fields are not specified. The response must remain non-PII and non-sensitive until approved.
- **Inherited traceability gap:** EPIC-3 GIN format remains open until `EPIC-3-TRACE-007` reports a Project Manager decision or formal non-blocking acceptance.

These gaps block implementation decisions that depend on the missing contract. They do not block source inspection, contract review, test-fixture planning, or a decision record.

## Task inventory

| ID            | File                                      | Deliverable                                                         | Owner                                               |
| ------------- | ----------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------- |
| EPIC-4-QR-001 | `01-qr-contract-and-security-decision.md` | Approved payload, identifier, encoding, response, and HMAC contract | Fistum; PM decision; Ephratha/Kidus review          |
| EPIC-4-QR-002 | `02-qr-record-and-generation-api.md`      | QR persistence and authenticated generation endpoint                | Fistum                                              |
| EPIC-4-QR-003 | `03-public-qr-verification-api.md`        | Public signature verification and non-sensitive summary endpoint    | Fistum                                              |
| EPIC-4-QR-004 | `04-frontend-qr-generation.md`            | Authenticated QR generation/display/download UI                     | Biniyam; Abel support subject to ownership decision |
| EPIC-4-QR-005 | `05-frontend-public-verification.md`      | Unauthenticated verification page and result states                 | Biniyam; Abel support subject to ownership decision |
| EPIC-4-QR-006 | `06-epic4-verification-and-handoff.md`    | End-to-end QR verification, evidence, and core-chain sign-off       | Ephratha + Kidus                                    |

## Dependency graph and sequence

```text
EPIC-3-TRACE-007 approved handoff
        |
        v
EPIC-4-QR-001  [critical decision gate]
        |
        +--------------------------+
        v                          v
EPIC-4-QR-002                EPIC-4-QR-003
record + generate API        public verify API
        |                          |
        +-------------+------------+
                      v
        EPIC-4-QR-004 and EPIC-4-QR-005
        generation UI / public page
                      |
                      v
             EPIC-4-QR-006 final gate
```

`QR-002` and `QR-003` can proceed in parallel only after `QR-001` is approved and the shared contract is stable. `QR-004` requires `QR-002`'s actual response and image representation. `QR-005` requires `QR-003`'s actual public response and verification URL/identifier contract. Frontend tasks can run in parallel with each other after their respective APIs are merged. Testing of isolated API logic runs within each task; final end-to-end testing cannot proceed until all preceding tasks are merged and a seeded Lot exists.

## Critical path

EPIC-3 verified handoff -> QR-001 contract/security decision -> QR-002 generation API -> QR-003 public verification API -> QR-005 public page and QR-004 generation UI (parallel after their API prerequisites) -> QR-006 end-to-end gate. The public verification path is the acceptance-critical branch; generation UI is also required for the complete human workflow.

## Milestone/week mapping

Minimum Project Plan Section 7.2 places completion of “Traceability & QR Engine,” integration, and unit/integration tests in **Week 3, Milestone M4 (Working Increment Delivered)**. Implementation Specification's Week 3 core integration order likewise reaches Lot -> Traceability -> QR -> Verification. QR-001 must not consume the entire M4 window without escalation because it is a prerequisite decision gate. Week 4 is for remaining integration evidence, documentation, and stabilization, not permission to expand scope.

## Team ownership

Fistum owns QR backend and the Dynamic QR Engine. Biniyam owns the React UI and API integration. The Implementation Specification names Abel for reusable QR UI components, API integrations, form validation, and QR UI components, while the Baseline/Minimum Project Plan contain an Abel role/module discrepancy documented in the execution procedures. PM assignment is required if it changes primary ownership. Ephratha owns automated/API/RBAC/security testing; Kidus owns traceability, test evidence, Test Report, user/demo documentation. Human review must be by someone other than the implementer.

## Testing strategy

Each new business function gets success and failure unit tests. Each endpoint gets automated tests, invalid-input tests, authentication/authorization tests where protected, and a Postman request. QR tests must cover valid signatures, tampered payloads, malformed/unknown/inactive identifiers, nonexistent Lots, public data minimization, and absence of secrets. Frontend tests or documented manual walkthroughs cover generation success/error and public valid/invalid states. No load testing or formal penetration testing is in scope. The full regression suite and an unbroken UI walkthrough are required in QR-006.

## Security considerations

Use the frozen JWT/password/RBAC model for protected generation and an intentionally unauthenticated, read-only verification endpoint. Keep the QR HMAC key in environment configuration; never return or log it. Sign a canonical approved payload and verify the exact same representation. Reject malformed, tampered, unknown, inactive, or deleted records using structured responses without leaking internal detail. The public response must contain only the approved non-sensitive origin summary and must not expose PII, exact polygon coordinates, credentials, signing material, database IDs unless explicitly approved, or stack traces. Use ORM/parameterized access and validate all path/body input.

## Cross-EPIC issues / required follow-up

- **EPIC-3 GIN format:** `EPIC-3-TRACE-001` records “Traceability gap - requires review.” QR-001 must not freeze a payload field or test fixture that assumes an unresolved GIN format. Impact: QR-002/003 and UI tests may be blocked until resolved or formally accepted as non-blocking.
- **Traceability/QR grouping:** the Minimum Project Plan's combined module wording remains a documentation conflict with the Implementation Specification's separate EPICs. EPIC-4 proceeds on the explicit separate backlog, pending PM acknowledgement; no prior task is changed.
- **Abel ownership:** Baseline and Minimum Project Plan role descriptions conflict with the Implementation Specification's QR UI support assignment. Escalate before assigning a primary owner if it affects delivery.
- **Earlier EPIC completion:** EPIC-0 through EPIC-3 task files do not prove implementation, testing, verification, or approval. QR-002/003/006 must record concrete evidence and stop on missing handoff prerequisites.

## Definition of EPIC completion

EPIC-4 is complete only when QR-001's decisions are recorded/approved, QR-002 through QR-005 meet their criteria and are merged to `develop`, QR-006 passes the full core workflow with synthetic data, valid and invalid QR cases, public data-minimization checks, regression tests, human review, requirements traceability, and a clear handoff/report. Any unresolved required decision, failed acceptance criterion, missing EPIC-3 handoff, or unauthorized scope change blocks completion.

## Consistency audit

| Audit item                         | Result  | Explanation                                                                                                                                                        |
| ---------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1. Scope                           | PASS    | Limited to Dynamic QR generation and public verification in frozen V1.0 core scope.                                                                                |
| 2. Requirements traceability       | PASS    | Each task cites SRS, Design, Implementation Specification, Minimum Project Plan, Baseline, and EPIC-3 sources where applicable; silent details are marked as gaps. |
| 3. Architecture                    | PASS    | Uses the existing modular monolith and separates contract, service/API, UI, and verification concerns.                                                             |
| 4. Technology                      | PASS    | Retains React/JavaScript, FastAPI/Python, PostgreSQL/PostGIS, JWT, HMAC, Git, and Postman; no unapproved technology is introduced.                                 |
| 5. Database                        | PARTIAL | QRRecord relationship and constraints are required, but exact schema/lifecycle details await QR-001 review because the sources do not fully specify them.          |
| 6. API architecture                | PASS    | Uses the two documented endpoints and requires a shared approved contract before implementation.                                                                   |
| 7. Frontend architecture           | PASS    | Separates authenticated generation UI from the public verification page and reuses existing app/auth patterns.                                                     |
| 8. Authentication/RBAC             | PASS    | Generation is protected by existing V1.0 auth/RBAC; verification is intentionally public and read-only.                                                            |
| 9. EPIC-3 dependency               | PARTIAL | Handoff requirements are explicit, but actual implementation/test/approval status must be verified by QR-002/003/006.                                              |
| 10. QR/Traceability boundary       | PASS    | Separate EPIC-4 QR backlog follows the higher-authority Baseline/Implementation Specification framing; the plan grouping conflict is recorded, not hidden.         |
| 11. Task ordering                  | PASS    | Contract gate precedes APIs; APIs precede their respective UI; final verification is last.                                                                         |
| 12. Parallelization                | PASS    | QR-002 and QR-003 parallelize after QR-001; QR-004 and QR-005 parallelize after their individual APIs.                                                             |
| 13. Critical path                  | PASS    | EPIC-3 handoff -> QR-001 -> generation/verification API path -> both UI branches -> QR-006 is identified.                                                          |
| 14. Testing                        | PASS    | Unit, endpoint, Postman, frontend/manual, regression, database, invalid-input, and security checks are assigned without load/penetration scope.                    |
| 15. Security                       | PASS    | HMAC secret handling, tampering, malformed/unknown/inactive records, RBAC, injection-safe input, and public minimization are covered.                              |
| 16. Git workflow                   | PASS    | Every implementation task names a feature branch, conventional commit, PR to `develop`, and independent review.                                                    |
| 17. Change control                 | PASS    | Missing requirements and deviations stop at QR-001/escalation; no task authorizes silent invention.                                                                |
| 18. Team ownership                 | PARTIAL | Fistum/Biniyam/Ephratha/Kidus ownership is sourced; Abel's conflicting role is explicitly awaiting PM clarification.                                               |
| 19. Minimum Project Plan schedule  | PASS    | Week 3/M4 alignment is recorded, with Week 4 limited to evidence/stabilization.                                                                                    |
| 20. V1.0 scope freeze              | PASS    | Out-of-scope enterprise security, infrastructure, integrations, data, and stretch modules are explicitly excluded.                                                 |
| 21. No duplicate earlier-EPIC work | PASS    | Tasks consume EPIC-3 Lot/Traceability contracts and explicitly prohibit reimplementing them.                                                                       |

## Final delivery report

**A. File tree created**

```text
.agents/tasks/EPIC-4/
├── 00-epic-overview.md
├── 01-qr-contract-and-security-decision.md
├── 02-qr-record-and-generation-api.md
├── 03-public-qr-verification-api.md
├── 04-frontend-qr-generation.md
├── 05-frontend-public-verification.md
└── 06-epic4-verification-and-handoff.md
```

**B. Task descriptions**

- QR-001: establish the approved QR payload, identifier, encoding, public response, and HMAC contract.
- QR-002: persist signed QR records and expose authenticated QR generation.
- QR-003: verify QR signatures publicly and return the approved non-sensitive summary.
- QR-004: provide authenticated QR generation/display/download UI.
- QR-005: provide the unauthenticated public verification page and result states.
- QR-006: run the complete API/UI/database/security/regression gate and issue the handoff.

**C. Dependency order:** EPIC-3-TRACE-007 -> QR-001 -> QR-002/QR-003 -> QR-004/QR-005 -> QR-006.

**D. Parallelizable tasks:** QR-002 and QR-003 after QR-001; QR-004 and QR-005 after their corresponding APIs. Final testing waits for all.

**E. Critical path:** the order in C, with both API branches and both UI branches required before QR-006.

**F. Traceability summary:** FR-TRACE-002 is implemented through the Design Document QR/HMAC/API/UI sections, the EPIC-4 Implementation Specification backlog and DoD, the M4 WBS, and Baseline core workflow. Exact payload, identifier, library, and public response details are explicit review gaps.

**G. Open decisions/conflicts:** QR contract gaps; EPIC-3 GIN format; Traceability/QR module grouping; Abel ownership wording.

**H. Cross-EPIC issues:** EPIC-3 handoff status must be evidenced, and EPIC-3's documented gaps must be resolved or formally accepted before QR implementation proceeds.

**I. Consistency audit:** reported above; 17 PASS and 4 PARTIAL items, with no FAIL. PARTIAL items are controlled prerequisites, not silently resolved assumptions.

**J. Safety confirmation:** EPIC-0 untouched; EPIC-1 untouched; EPIC-2 untouched; EPIC-3 untouched; rules untouched; execution files untouched; no application source code modified; no requirements invented; no conflict silently resolved.
