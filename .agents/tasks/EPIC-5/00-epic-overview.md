# EPIC-5 - Frontend Integration

## EPIC objective

Deliver the integrated React/JavaScript frontend for the CEVCMS V1.0 core workflow: login -> role-appropriate protected UI -> farmer -> farm/polygon -> coffee lot -> traceability -> QR -> public verification. EPIC-5 consumes the API contracts from EPIC-1 through EPIC-4 and makes the working increment demonstrable; it does not redesign backend APIs or reimplement upstream domain logic.

## Business purpose

Provide one connected browser workflow for ECTA staff and the public verification audience. The frontend must make the approved core chain usable with synthetic/demo data while respecting the four-role model, protected versus public screens, rural/intermittent-connectivity context without adding offline functionality, and V1.0's bounded scope.

## Authoritative scope

The Implementation Specification names EPIC 5 “Frontend Integration,” owned by Biniyam (Lead) / Abel (Support), with screens: Login; Dashboard; Farmer Registration/List; Farm/Polygon Registration/Details; Coffee Lot Creation; Traceability View; QR Generation & Verification. The Design Document Sections 9.1-9.4 define the corresponding screens and the connected flow. The Baseline Sections 2-4 fix React/JavaScript, the core workflow, and the public verification boundary. The Minimum Project Plan schedules frontend integration in Week 4 and maps client acceptance to M5 and closure to M6.

## Scope boundaries

In scope: shared application shell; API client integration; login/auth state; protected routing; role-aware navigation; logout/session cleanup; dashboard counts using documented APIs; farmer and farm/polygon screens; lot and traceability screens; QR generation and public verification screens; validation, loading/error states, and end-to-end frontend verification.

Out of scope: backend/API/database changes; new endpoints or request/response contracts; new frameworks or state-management libraries; TypeScript; Redux/React Query/Tailwind/Material UI unless later explicitly frozen; MFA, refresh tokens, OAuth/OIDC, HSM, ABAC, offline queues/native mobile, SMS/USSD, stretch modules, real external integrations, production infrastructure, and any public PII exposure. EPIC-5 does not duplicate EPIC-1 through EPIC-4 implementation.

## Upstream dependency status rule

Task-file existence is not evidence that earlier work is implemented, tested, verified, approved, or merged. Before each task, confirm the exact upstream task and API contract is available on `develop` and record status as specified / implemented / tested / verified / approved. A missing or unresolved contract blocks the affected integration; do not invent a substitute.

- **EPIC-1:** `AUTH-006`/`AUTH-007` provide login/auth state/protected routing; `AUTH-008` must provide verification evidence. Four roles are Admin, ECTA Officer, Field/Registry Agent, Verifier.
- **EPIC-2:** `FARM-005`/`FARM-006` provide farmer/farm/polygon UI/API shapes and Leaflet/React-Leaflet mapping. The documented mapping conflict remains governed operationally by the frozen Leaflet decision; do not introduce Mapbox.
- **EPIC-3:** `TRACE-005`/`TRACE-006` provide lot and trace screens/contracts; `TRACE-007` must verify the chain. Do not duplicate lot/event/trace logic.
- **EPIC-4:** `QR-001` must be approved before QR UI work; `QR-004`/`QR-005` provide generation/public verification contracts. Payload, `qrId`, library, and public response gaps remain blocked until approved.

## Task inventory

| ID            | File                                          | Deliverable                                                        | Owner                                                                   |
| ------------- | --------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| EPIC-5-FE-001 | `01-frontend-foundation-shell.md`             | Shared React shell and integration prerequisites                   | Biniyam lead; Abel support                                              |
| EPIC-5-FE-002 | `02-login-auth-state-integration.md`          | Login form and JWT auth-state integration                          | Biniyam; Abel support                                                   |
| EPIC-5-FE-003 | `03-protected-routes-role-navigation.md`      | Protected routes, role navigation, logout/session handling         | Biniyam; Abel support                                                   |
| EPIC-5-FE-004 | `04-dashboard-authenticated-shell.md`         | Authenticated dashboard and shell entry                            | Biniyam; Abel support                                                   |
| EPIC-5-FE-005 | `05-farmer-registration-list-detail.md`       | Farmer registration, list, and detail integration                  | Biniyam; Abel support                                                   |
| EPIC-5-FE-006 | `06-farm-polygon-registration-details.md`     | Farm/polygon capture and detail integration                        | Biniyam; Abel support; Yedenekachew contract support                    |
| EPIC-5-FE-007 | `07-coffee-lot-creation.md`                   | Coffee Lot creation integration                                    | Biniyam; Abel support                                                   |
| EPIC-5-FE-008 | `08-traceability-history-lot-detail.md`       | Protected traceability history/detail integration                  | Biniyam; Abel support                                                   |
| EPIC-5-FE-009 | `09-qr-generation-verification.md`            | QR generation and public verification integration                  | Biniyam lead; Abel QR UI support subject to recorded ownership decision |
| EPIC-5-FE-010 | `10-frontend-integration-e2e-verification.md` | Full frontend integration, regression, and acceptance verification | Biniyam implementation; Ephratha QA; Kidus evidence                     |

## Dependency graph

```text
EPIC-1 AUTH-006/007 + EPIC-0 React scaffold
                         |
                         v
              FE-001 foundation/shell
                         |
              +----------+----------+
              v                     v
       FE-002 login/auth      FE-005 farmer screen
              |                     |
              v                     |
       FE-003 routes/nav             |
              |                     |
              v                     |
       FE-004 dashboard              |
              |                     |
              +----------+----------+
                         v
       FE-006 farm/polygon screen
                         |
              +----------+----------+
              v                     v
       FE-007 lot creation    FE-008 traceability
              |                     |
              +----------+----------+
                         v
              FE-009 QR integration
                         |
                         v
              FE-010 full verification
```

FE-005 may begin after FE-001 and the verified EPIC-2 farmer contract; it does not require FE-006. FE-006 requires the verified farm/polygon API and Leaflet contract. FE-007 requires EPIC-3 lot API plus a usable authenticated shell. FE-008 requires EPIC-3 trace APIs and FE-007 navigation/lot identity. FE-009 requires approved EPIC-4 QR contracts and both QR API/UI upstream tasks. FE-010 waits for all screens and all upstream verification gates.

## Recommended execution order and parallelization

1. FE-001, after the existing React scaffold and upstream auth/UI foundations are verified.
2. FE-002, then FE-003, then FE-004 as the shell/auth path.
3. FE-005 can run in parallel with FE-002/003 once FE-001 and the Farmer API contract are available, but integration to protected navigation waits for FE-003.
4. FE-006 can run in parallel with FE-005 after the Farm/Polygon API contract is verified.
5. FE-007 and FE-008 can run in parallel only when their respective EPIC-3 contracts are merged and FE-001/003 are available; FE-008 needs an existing Lot ID fixture or FE-007's navigation contract.
6. FE-009 follows approved EPIC-4 QR contracts and can integrate generation and public verification subflows in parallel only if QR-004 and QR-005 contracts are independently stable.
7. FE-010 is strictly last.

Mocked/stubbed API responses may be used only for isolated UI development when they mirror an already documented and inspected contract, are clearly test fixtures, and are replaced/validated against the real API before task completion. They must not conceal a missing upstream contract.

## Critical path

EPIC-1 auth foundation -> FE-001 -> FE-002 -> FE-003 -> FE-004 -> FE-005/006 -> EPIC-3 lot/trace integrations FE-007/008 -> approved EPIC-4 QR contracts and APIs -> FE-009 -> FE-010 -> M5/M6 evidence. The exact screen branch may be parallelized, but the final acceptance workflow cannot bypass any link.

## Ownership

Biniyam is the EPIC-5 lead and owns React UI/API integration. Abel supports reusable React components, API integrations, form validation, traceability UI, and QR UI components as documented by the Implementation Specification. The existing Abel role conflict in `.agents/execution/00-execution-overview.md` remains recorded; it must not be silently reinterpreted. Ephratha owns API/RBAC/input-validation/integration QA; Kidus owns requirements traceability, test evidence, Test Report, user/demo documentation. Yedenekachew supports the farm/polygon contract seam where required by EPIC-2 ownership.

## Frontend architecture summary

Use the existing React/Vite JavaScript app and its current project structure. Maintain clear boundaries for shared shell/auth, API clients, pages, and reusable form/map/result components. Reuse the existing EPIC-1 auth and EPIC-2/3/4 components where available. Do not introduce a new state framework, router, styling framework, backend service, or frontend scaffold. The public verification route must be intentionally separate from protected application routes.

## API integration summary

Consume, without redesign: EPIC-1 login/me/logout/auth behavior; EPIC-2 farmer/farm/polygon contracts; EPIC-3 lot/event/trace contracts; EPIC-4 approved QR generation and verification contracts. Each task must inspect the actual merged response shape before implementation. Any missing field, endpoint, status behavior, QR payload detail, or public response detail is **Traceability gap - requires review** and blocks the affected integration.

## Security considerations

JWT handling uses the existing EPIC-1 mechanism; no frontend secret or signing key is stored. Protected routes and actions require existing auth state and role semantics. Logout clears client auth state and makes protected routes inaccessible. Unauthorized responses show controlled errors and do not leak server detail. Public QR verification requires no login and displays only the EPIC-4-approved non-sensitive result; it must not fall back to protected trace data or expose PII, exact coordinates, credentials, payload/signature internals, or secrets. User input is validated and rendered safely; API failures do not become injection or stack-trace disclosure.

## Testing strategy

Every task has observable acceptance criteria and frontend tests or manual evidence consistent with the existing repository. The current frontend package exposes `build` and `lint` scripts but no frontend test runner; no new test framework is authorized by this backlog. Use the existing available validation path, add tests only where the approved project setup supports them, and record manual browser walkthrough evidence where automation is unavailable. FE-010 runs the full backend/frontend regression suites, API checks, role checks, public-data inspection, and the unbroken acceptance workflow. No load or formal penetration testing.

## Schedule

The Minimum Project Plan places frontend integration in Week 4, with M4 at the end of Week 3 as the working core increment, M5 as Client Acceptance Review mid-Week 4, and M6 as Project Closure at the end of Week 4. EPIC-5 must hand EPIC-6 a runnable, documented core frontend, stable screen-to-API mapping, seeded demo walkthrough, regression evidence, known-defect disposition, and updated traceability/test documentation. EPIC-5 must not claim completion if an upstream contract or core workflow step remains blocked.

## Handoff into EPIC-6

EPIC-5 hands EPIC-6 a runnable React frontend covering the complete approved core workflow, the verified screen-to-API contract map, role and public-route behavior, synthetic demo walkthrough, responsive/manual evidence, regression results, known-defect disposition, and updated traceability/Test Report material. EPIC-6 may consume this handoff only when FE-010 and the upstream EPIC-1 through EPIC-4 verification gates are approved; no unresolved contract or security blocker may be hidden in the handoff.

## Known ambiguities and unresolved decisions

- EPIC-4 QR-001 controls unresolved payload, identifier, library, image, and public response details. FE-009 is blocked on those decisions and must not guess.
- EPIC-3 GIN format may still be open; screens must consume the actual Lot response rather than validate an invented format.
- Abel's role wording conflicts across Level-3 sources; Biniyam remains lead and PM clarification is required if Abel's assignment affects ownership.
- The Minimum Project Plan groups Traceability and QR as one module while the Implementation Specification separates EPIC-3 and EPIC-4; EPIC-5 integrates both as documented without changing either backlog.
- The source documents do not define a complete dashboard-count endpoint contract. FE-004 must use an existing documented API or record **Traceability gap - requires review**; it may not invent an endpoint.
- The source documents do not define a precise frontend router/library or browser token storage mechanism. FE-001/002 must preserve any already-established implementation; if none exists, the choice is an explicit PM/design decision rather than silent technology invention.

## Consistency audit

| Item                                | Result  | Explanation and action                                                                                                                                                     |
| ----------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Scope                            | PASS    | Only V1.0 core frontend integration is included; stretch and enterprise features are excluded.                                                                             |
| 2. Requirements traceability        | PASS    | Tasks trace to source sections and upstream EPIC contracts; gaps are named explicitly.                                                                                     |
| 3. Architecture                     | PASS    | Existing React app and modular backend boundaries are preserved.                                                                                                           |
| 4. Technology stack                 | PASS    | React/JavaScript and Leaflet/React-Leaflet are used; no new framework is authorized.                                                                                       |
| 5. Frontend architecture            | PASS    | Shared shell, API clients, pages, public route, and reusable components are separated.                                                                                     |
| 6. Backend API dependencies         | PARTIAL | Upstream contracts are specified but must be verified as implemented/tested/approved at task start. Action: block affected task on missing contract.                       |
| 7. Authentication/RBAC dependencies | PARTIAL | EPIC-1 contracts and four roles are specified; actual completion status is not assumed. Action: verify AUTH-006/007/008.                                                   |
| 8. Database dependencies            | PASS    | Frontend reads API data and introduces no schema or direct database responsibility.                                                                                        |
| 9. Traceability chain               | PASS    | Farmer -> Farm/Polygon -> Lot -> Traceability -> QR -> public verification is mapped.                                                                                      |
| 10. QR integration                  | PARTIAL | EPIC-4 contract gates and public-data boundary are preserved; unresolved details block FE-009.                                                                             |
| 11. Security                        | PASS    | JWT reuse, route protection, logout, public minimization, safe input, and no secrets are covered.                                                                          |
| 12. Testing                         | PARTIAL | Required verification is defined, but no frontend test runner exists in the current scaffold. Action: use available lint/build/manual evidence and record any tooling gap. |
| 13. Git workflow                    | PASS    | Each task requires a feature branch from `develop`, PR, independent review, and traceable commit.                                                                          |
| 14. Change control                  | PASS    | Missing contracts and technology/scope deviations stop and escalate.                                                                                                       |
| 15. Team ownership                  | PARTIAL | Biniyam/Abel ownership is sourced; Abel's known project-level conflict remains for PM review.                                                                              |
| 16. Minimum Project Plan schedule   | PASS    | Week 4, M4 predecessor, M5 acceptance, and M6 closure are recorded.                                                                                                        |
| 17. V1.0 scope freeze               | PASS    | No offline/mobile, stretch, external integration, or enterprise security scope is added.                                                                                   |
| 18. No duplicate EPIC-0 work        | PASS    | Existing React/Vite scaffold is reused; no reinitialization or database work.                                                                                              |
| 19. No duplicate EPIC-1 work        | PASS    | Auth state and route mechanisms are consumed, not recreated.                                                                                                               |
| 20. No duplicate EPIC-2 work        | PASS    | Farmer/farm/polygon APIs and components are consumed, not reimplemented.                                                                                                   |
| 21. No duplicate EPIC-3 work        | PASS    | Lot/trace APIs and screens are integrated, not duplicated.                                                                                                                 |
| 22. No duplicate EPIC-4 work        | PASS    | QR backend/contract decisions and QR screens are consumed; FE-009 is integration only.                                                                                     |

## Final delivery report

**A. File tree created**

```text
.agents/tasks/EPIC-5/
├── 00-epic-overview.md
├── 01-frontend-foundation-shell.md
├── 02-login-auth-state-integration.md
├── 03-protected-routes-role-navigation.md
├── 04-dashboard-authenticated-shell.md
├── 05-farmer-registration-list-detail.md
├── 06-farm-polygon-registration-details.md
├── 07-coffee-lot-creation.md
├── 08-traceability-history-lot-detail.md
├── 09-qr-generation-verification.md
└── 10-frontend-integration-e2e-verification.md
```

**B. Tasks:** FE-001 foundation shell; FE-002 login/auth state; FE-003 protected routes/navigation/logout; FE-004 dashboard shell; FE-005 farmer screens; FE-006 farm/polygon screens; FE-007 lot creation; FE-008 traceability view; FE-009 QR generation/public verification; FE-010 final integration and verification.

**C. Dependency order:** FE-001 -> FE-002 -> FE-003 -> FE-004; FE-005/006 after FE-001 and their APIs; FE-007/008 after their EPIC-3 APIs and usable auth shell; FE-009 after approved EPIC-4 contracts/APIs; FE-010 last.

**D. Parallelizable tasks:** FE-005 and FE-006 can run in parallel after their separate upstream contracts; FE-007 and FE-008 can run in parallel when their separate contracts and shell prerequisites exist; QR generation and public verification subflows can run in parallel only after their EPIC-4 contracts are stable.

**E. Critical path:** auth shell -> farmer/farm -> lot/trace -> QR -> final acceptance verification.

**F. Requirements traceability:** FR-AUTH-001/002, FR-FARM-001/002, FR-TRACE-001/002, Design Document Sections 4.1, 4.2, 5.3, 8, 9.1-9.4, 13, 17-20, Implementation Specification EPIC-5 and core-chain DoD, Minimum Project Plan Sections 6.4, 7.1-7.2, Baseline Sections 2-4, plus upstream EPIC task contracts.

**G. Open conflicts/decisions:** QR-001 contract gaps; EPIC-3 GIN gap; Abel ownership conflict; Traceability/QR grouping; dashboard endpoint and router/token-storage details where sources are silent.

**H. Cross-EPIC dependencies:** EPIC-1 auth; EPIC-2 farmer/farm/polygon; EPIC-3 lot/trace; EPIC-4 QR; all must be verified beyond task-file existence.

**I. Audit:** 17 PASS and 5 PARTIAL items; no FAIL. Every PARTIAL has an explicit verification/blocking action above.

**J. Safety:** This package creates only `.agents/tasks/EPIC-5/`; it must not modify EPIC-0 through EPIC-4, rules, execution procedures, backend, frontend, database, or docs. No requirements are invented and no unresolved contract is silently resolved.
