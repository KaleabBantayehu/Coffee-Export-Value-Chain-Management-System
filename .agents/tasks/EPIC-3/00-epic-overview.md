# EPIC 3 — Traceability Engine (Coffee Lot & Traceability Events): Overview

## Epic ID

EPIC-3

## Epic Name

Traceability Engine — Coffee Lot Creation & Traceability Events

**Naming note:** the Implementation Specification titles this backlog item
"EPIC 3 — Traceability Engine" and treats QR generation as a separate item,
"EPIC 4 — Dynamic QR Engine." Other documents use different groupings —
see "Open Decisions / Conflicts, Item 1" below before assuming this
boundary is uncontested.

## Implementation Status of Prior Work (do not assume completion)

Per this request's explicit instruction, task-file existence is not
evidence of implementation. As of this writing:

- **EPIC-0**: task specifications exist (`.agents/tasks/EPIC-0/`). The
  current project state supplied in earlier turns states EPIC-0 is
  complete, including the database schema from `EPIC-0-DB-002` (which
  already defines the `CoffeeLot` and `TraceabilityEvent` tables this epic
  builds on). This epic's tasks treat that schema as existing, per that
  stated project state — but no independent verification evidence (test
  output, migration log) has been inspected in the course of writing this
  task package. If that assumption is wrong, `EPIC-3-TRACE-001`'s own
  Preconditions step will surface it.
- **EPIC-1**: task specifications exist. Whether Authentication & RBAC is
  actually implemented, merged, and passing `EPIC-1-AUTH-008`'s
  verification is **not confirmed by this task package** and must be
  checked at the start of `EPIC-3-TRACE-002` (the first task requiring a
  real JWT and RBAC enforcement), per
  `.agents/execution/01-agent-start-procedure.md` Step 4/5.
- **EPIC-2**: task specifications exist, including `EPIC-2-FARM-007`
  (end-to-end verification). Whether Farmer & Polygon Registry is actually
  implemented and verified is **not confirmed by this task package** and
  must be checked at the start of `EPIC-3-TRACE-002`, which requires a
  real, persisted Farm (with computed area and EUDR flag from
  `EPIC-2-FARM-004`) to attach a Coffee Lot to.

**This task package does not implement, duplicate, or re-verify any
EPIC-1 or EPIC-2 work.** Every EPIC-3 task that needs EPIC-1/EPIC-2
functionality names the exact task it depends on and requires that
dependency's actual, verified state to be confirmed before proceeding —
not assumed from the existence of a task file.

## Objective

Implement the Traceability Engine: Coffee Lot creation against an existing
Farm, append-only Traceability Event logging, and protected retrieval of a
Lot's full traceability chain — completing the fourth link in the V1.0
core chain and producing the traceable Lot record that EPIC 4 (QR) will
attach a QR code to.

## Business / Project Purpose

Per Baseline §4, "Create Coffee Lot" and "Create Traceability Record /
Event" are the fifth and sixth steps of the primary acceptance workflow,
immediately after Farm/Polygon registration and before QR generation. Per
the Assignment Description (Objectives O1/O2) and the Minimum Project
Plan §2.1, farm-to-lot origin traceability is one of the two core
objectives the whole project exists to demonstrate — this epic is where
that traceability link is actually created, not merely designed.

## Bounded V1.0 Scope

In scope, per Implementation Specification EPIC 3 and Design Document §5:

**Backend:**
- Coffee Lot creation against a mandatory, existing Farm (on top of the
  `CoffeeLot` table already created by `EPIC-0-DB-002`).
- GIN (Global Identification Number) generation — **see the flagged
  traceability gap below.**
- Append-only Traceability Event logging (on top of the
  `TraceabilityEvent` table already created by `EPIC-0-DB-002`).
- Protected (authenticated) retrieval of a Lot's full traceability chain,
  including farmer contact fields, per Design Document §5.3's public-vs-
  protected data distinction.

**Frontend:**
- Lot registration form (select an existing Farm, create a Lot).
- Traceability event log view/entry for a Lot.

This is deliberately **not** expanded to: QR code generation or the public
verification endpoint (EPIC 4), the SRS's full enterprise DAG lineage
engine (lot splitting/merging across multiple farms, wet-mill batch
aggregation, bag serialization), quality grading, waybill issuance, export
licensing, forex validation, or any stretch module — all of these are
later epics or explicitly out of V1.0 scope
(`.agents/rules/01-scope-boundaries.md`).

## Owner (from authoritative sources)

Per Baseline §5 ("Fistum | Traceability and QR. Owns the CoffeeLot and
TraceabilityEvent models, the append-only event chain, and the Dynamic QR
Engine...") and Implementation Specification EPIC 3 ("Owner: Fistum"):

- **Fistum** — primary owner of all backend EPIC-3 tasks (`TRACE-001`
  through `TRACE-004`): GIN generation, Lot creation, Traceability Event
  logging, and trace retrieval.
- **Yedenekachew** — joint responsibility specifically at the Farm-to-Lot
  integration seam, per the Minimum Project Plan's WBS ("Integrate
  Farmer/Polygon module with Traceability module... Fistum Adisu,
  Yedenekachew Fantahun"). This is narrower than Fistum's overall
  ownership: Yedenekachew's involvement is specifically about confirming
  `EPIC-2-FARM-003`/`FARM-004`'s Farm contract is correctly consumed by
  `TRACE-002`, not general co-ownership of the epic.
- **Biniyam** — owns the frontend tasks (`TRACE-005`, `TRACE-006`), per
  Baseline §5's general frontend-lead ownership and the Minimum Project
  Plan's WBS ("Build traceability lineage view + QR display/download...
  Biniyam Abel").
- **Ephratha** — owns integration/API/RBAC testing for `TRACE-007`, per
  Baseline §5 and the Minimum Project Plan's WBS ("Integration tests for
  module APIs (Postman)... Ephratha Samuel"; "Role-permission and
  input-validation test pass... Ephratha Samuel").
- **Kidus** — owns the functional/system walkthrough and Test Report
  draft specifically for the traceability use case within `TRACE-007`, per
  the Minimum Project Plan's WBS ("Functional/system walkthrough of full
  traceability use case... Kidus Ergetachew | Test Report (draft)"). This
  is a **more precise split than `EPIC-1-AUTH-008`/`EPIC-2-FARM-007` used**
  (which named Ephratha as sole verification owner with Kidus limited to
  documentation) — see "Cross-EPIC Issues / Required Follow-up" below.

## Dependencies

- `EPIC-1` (Authentication & RBAC) — task specifications exist; actual
  implementation/verification status must be confirmed at the start of
  `TRACE-002`. `TRACE-002`/`TRACE-003`/`TRACE-004` consume
  `EPIC-1-AUTH-003`'s authentication dependency and `EPIC-1-AUTH-004`'s
  RBAC authorization mechanism as-is. **EPIC 3 does not create a second
  authorization system.**
- `EPIC-2` (Farmer & Polygon Registry), specifically `EPIC-2-FARM-003` and
  `EPIC-2-FARM-004` — task specifications exist; actual implementation/
  verification status must be confirmed at the start of `TRACE-002`, since
  a Coffee Lot requires a real, persisted Farm with a computed area and
  EUDR flag to attach to.
- `EPIC-0-DB-002` (initial schema) — the `CoffeeLot` and
  `TraceabilityEvent` tables, including `CoffeeLot.gin_code`'s uniqueness
  constraint and the mandatory `farm_id` foreign key, already exist. EPIC 3
  does not alter this schema; if a genuine schema gap is found, that is
  change control (`.agents/rules/06-change-control.md`), not a silent
  migration.

## Preconditions

- `develop` reflects EPIC 0's schema work and, per this epic's own
  dependency checks (not assumed), a functioning EPIC-1 auth/RBAC layer
  and a functioning EPIC-2 Farmer/Farm/polygon/area/EUDR chain.
- The `CoffeeLot` and `TraceabilityEvent` tables are reachable via the
  database connection configured in `EPIC-0-DB-001`.

## Task Inventory

| Task ID | File | Title | Owner |
|---|---|---|---|
| EPIC-3-TRACE-001 | `01-lot-gin-foundation.md` | Coffee Lot Data Foundation — GIN Generation & Validation Utility | Fistum |
| EPIC-3-TRACE-002 | `02-coffee-lot-creation-api.md` | Coffee Lot Creation API (Farm -> Lot) | Fistum (+ Yedenekachew at the Farm/Lot boundary) |
| EPIC-3-TRACE-003 | `03-traceability-event-api.md` | Append-Only Traceability Event Logging API | Fistum |
| EPIC-3-TRACE-004 | `04-lot-trace-retrieval-api.md` | Lot Traceability Chain Retrieval API | Fistum |
| EPIC-3-TRACE-005 | `05-frontend-lot-registration.md` | Frontend Lot Registration Form | Biniyam |
| EPIC-3-TRACE-006 | `06-frontend-traceability-view.md` | Frontend Traceability Event Log View & Entry | Biniyam |
| EPIC-3-TRACE-007 | `07-epic3-verification.md` | EPIC 3 End-to-End Verification & EPIC 4 Handoff Readiness | Ephratha (integration/RBAC) + Kidus (functional walkthrough, Test Report) |

## Dependency Graph

```text
EPIC-1 (Auth/RBAC — status to be confirmed, not assumed)
EPIC-2-FARM-003/004 (Farm + area + EUDR — status to be confirmed)
   |
   v
EPIC-3-TRACE-001  (GIN generation utility + validation foundation;
   |                also depends on EPIC-0-DB-002 schema only —
   |                no dependency on EPIC-1/EPIC-2)
   v
EPIC-3-TRACE-002  (Coffee Lot creation API; depends on TRACE-001's
   |                GIN utility, a real Farm from EPIC-2, and
   |                EPIC-1's auth/RBAC mechanism)
   |
   +----------------------------+
   v                            v
EPIC-3-TRACE-003              EPIC-3-TRACE-004
(Traceability event            (Lot trace retrieval;
logging; depends only          depends only on TRACE-002 —
on TRACE-002)                  a Lot with at least its
                                auto-created initial event
                                is enough to build/test
                                against, though richer
                                once TRACE-003 exists)
   |                            |
   +-------------+--------------+
                 |
   +-------------+--------------+
   v                            v
EPIC-3-TRACE-005              EPIC-3-TRACE-006
(Frontend: Lot registration    (Frontend: Traceability event
form; depends only on          log view/entry; depends on
TRACE-002's API contract —     TRACE-003 AND TRACE-004's
can start once TRACE-002       API contracts)
merges, in parallel with
TRACE-003/004 backend work)
   |                            |
   +-------------+--------------+
                 v
         EPIC-3-TRACE-007
   (End-to-end verification;
    depends on TRACE-001 through TRACE-006)
```

## Parallelization Opportunities

- `EPIC-3-TRACE-003` (event logging) and `EPIC-3-TRACE-004` (trace
  retrieval) both depend only on `TRACE-002`, not on each other — they may
  proceed **in parallel** once `TRACE-002` merges. This is a genuine
  addition to the parallelization pattern already used in `EPIC-2`
  (where the equivalent backend chain was strictly sequential); here, two
  backend tasks can run side by side because one only writes events and
  the other only reads the lot+events, with no shared mutable state
  between them beyond the already-created Lot.
- `EPIC-3-TRACE-005` (frontend Lot registration) depends only on
  `TRACE-002`'s API contract and may proceed in parallel with
  `TRACE-003`/`TRACE-004`, mirroring `EPIC-2-FARM-005`'s pattern.
- `EPIC-3-TRACE-006` (frontend traceability view) cannot start
  meaningfully before both `TRACE-003` and `TRACE-004` merge, since it
  both displays retrieved events (`TRACE-004`'s contract) and creates new
  ones (`TRACE-003`'s contract).

## Milestone / Week Mapping

Per Minimum Project Plan §7.2 (Week-by-week schedule): *"Week 3 | Core
module completion and integration; stretch scope begins if ahead of plan |
Complete Traceability & QR Engine; integrate Auth, Farmer Registry, and
Traceability into one working chain; run unit and integration tests as
each piece lands... | M4 — Working Increment Delivered (end of Week 3)."*
EPIC 3 is therefore Week-3 work, and `TRACE-007`'s successful completion is
one of the conditions for Milestone M4. This is consistent with
Implementation Specification's own four-week schedule ("Week 3 — Core
Integration: Connect Login -> Farmer -> Farm -> Polygon -> Lot ->
Traceability -> QR -> Verification. Achieve Working Increment Target
(M4)."). Both documents agree on the timing; see "Open Decisions /
Conflicts, Item 1" for where they disagree (module grouping, not timing).

## Team / Ownership Considerations

See "Owner" above. In addition:

- **Required skill for `TRACE-002`/`TRACE-003`/`TRACE-004`**: familiarity
  with the existing FastAPI/SQLAlchemy patterns already established by
  `EPIC-1`/`EPIC-2` (router-per-domain, service-layer validation, shared
  auth/RBAC dependencies) — these tasks extend that pattern, not invent a
  new one.
- **Possible parallel owner for `TRACE-003`/`TRACE-004`**: since both are
  independent once `TRACE-002` exists, if Fistum is time-constrained, a
  second backend-capable team member (e.g., Ephratha, who has general
  backend capability per Baseline §5) could take one of the two in
  parallel — this is offered as an option for the Project Manager to
  decide, not a task-file assignment, since Baseline §5 names Fistum as
  the epic's backend owner and any reassignment is a Project Manager
  decision per `.agents/rules/06-change-control.md`.
- **Verification responsibility**: split between Ephratha (integration/
  API/RBAC testing) and Kidus (functional walkthrough, Test Report draft),
  per the Minimum Project Plan's explicit WBS split — see `TRACE-007`.

## Testing Strategy

Consistent with `.agents/execution/03-verification-and-testing.md` and the
Minimum Project Plan §7.1 Quality Plan (Unit testing by module owner
alongside the code; Integration/API testing via Postman, owned by
Ephratha; Functional/system walkthroughs against Assignment Description
§12's acceptance criteria, using seeded demonstration data). Each backend
task specifies its own unit/API tests; `TRACE-007` performs the
integration-level and functional-walkthrough-level testing across the
whole epic.

## Known Risks

Carried forward from the Minimum Project Plan's risk register (§4.3),
restated here because they specifically name this epic's integration
point:

- **RSK-03** — *"Integration problems when merging Auth, Farmer Registry,
  and Traceability modules."* Probability: Medium; Impact: Medium.
  Mitigation (as stated in the Minimum Project Plan): *"Shared API
  contracts and DB schema agreed at design time (M3); integration
  attempted incrementally from Week 2, not left to Week 4."* This is the
  specific reason `TRACE-002` requires confirming EPIC-1/EPIC-2's actual
  implementation status rather than assuming it, and the specific reason
  `TRACE-007` exists as a dedicated integration-verification task rather
  than treating each `TRACE-0xx` task's own tests as sufficient proof the
  whole chain works.
- **RSK-06** — *"Testing delayed to the last days of the project."*
  Mitigation: testing is continuous, not deferred — reflected in every
  `TRACE-0xx` task's own `Testing Requirements` section, not only in
  `TRACE-007`.

## Open Decisions / Conflicts

### 1. Whether "Traceability" and "QR" are one module or two — genuinely conflicting, not resolved here

**Conflicting statements:**
- Implementation Specification: separates *"EPIC 3 — Traceability
  Engine"* (Owner: Fistum; CoffeeLot/TraceabilityEvent scope) from
  *"EPIC 4 — Dynamic QR Engine"* (Owner: Fistum; QR payload/HMAC/
  verification scope) as two distinct backlog items with two distinct
  Definitions of Done.
- Baseline Scope Freeze §4 (Critical Workflow): lists *"Create Coffee
  Lot"*, then *"Create Traceability Record / Event"*, then *"Generate
  QR"* as three separate, sequential steps — consistent with treating
  Traceability and QR as separate concerns, though the Baseline does not
  use the word "epic" at all.
- Minimum Project Plan §4.1 (Core Scope): *"Deliver the three core-scope
  modules (Authentication & RBAC, Farmer & Polygon Registry, Traceability
  & QR Engine) fully functional and tested by Milestone M4."* This treats
  "Traceability & QR Engine" as **one** combined core-scope module —
  three modules total, not four.

**Affected task(s):** the entire EPIC-3 boundary — whether QR generation
belongs inside this task package or is genuinely a separate, later one.

**Impact:** If "Traceability & QR Engine" is truly one module, this task
package (EPIC-3, Traceability only) is an incomplete slice of it, and a
future "EPIC-4" task package would need to be understood as completing
the same module rather than starting a new one. If they are two modules
(Implementation Specification's framing), this task package is complete
and self-contained, and EPIC-4 is a genuinely separate epic.

**Whether implementation can proceed safely:** **Yes.** Both readings
agree on every functional and technical requirement inside this task
package (Lot creation, event logging, trace retrieval) — the disagreement
is purely about backlog/epic bookkeeping (one epic or two), not about
scope content, RBAC rules, data model, or API contract. No `TRACE-0xx`
task's implementation requirements change under either reading.

**Recommended authority/escalation path:** This task package proceeds
treating EPIC-3 as Traceability only (Lot + Event; no QR), for continuity
with the dependency-chain diagrams already established and delivered in
`EPIC-0`, `EPIC-1`, and `EPIC-2`'s own overview files (all of which show
"Traceability + Coffee Lot" and "Dynamic QR" as two separate steps in the
core chain) and with the Implementation Specification's explicit epic
split. The Minimum Project Plan's three-module framing is recorded here,
unresolved, for the Project Manager's awareness; if the Project Manager
confirms "Traceability & QR Engine" should be tracked as one epic, that is
a documentation/backlog-organization decision for Kidus to reconcile
across `EPIC-3`'s and the future QR task package's overview files — it
does not require reopening any `TRACE-0xx` task's technical content.

### 2. GIN format — a traceability gap, not a two-way conflict like FIN's

Unlike `EPIC-2-FARM-001`'s FIN format (where two SRS statements actively
contradict each other), no SRS or Design Document text specifies a GIN
format for V1.0 at all. FR-TRACE-001/002 give no format string. Design
Document §5.2 says only that the GIN is "a unique code... in the spirit of
SRS's Global Identification Number," without specifying one. The only
concrete example anywhere in the SRS is in **Appendix C**, illustrating a
stretch-scope (EPIC 7, out of current scope) e-Waybill layout:
`ETH-LOT-2026-G1-00392` — and this example embeds a grade code (`G1`)
that V1.0's simplified, stretch-free lot model has no data for, so it
cannot be safely reproduced as-is either. Per this request's Section 10
("If a requirement cannot be mapped, explicitly mark: 'Traceability gap —
requires review.'"): **Traceability gap — requires review.**
`EPIC-3-TRACE-001` implements the GIN utility with the same
isolated-placeholder-plus-escalation pattern `EPIC-2-FARM-001` established
for FIN, and escalates per `.agents/execution/06-failure-and-escalation.md`.

### 3. "Any authenticated role" may append a Traceability Event — confirmed, not ambiguous, but worth flagging

Design Document §8 states `POST /api/v1/lots/{id}/events`'s Auth
requirement as simply *"JWT"* — with no role qualifier, unlike
`POST /api/v1/lots` (*"JWT + Field/Registry Agent or Admin"*). Read
literally and consistently with how `EPIC-1`/`EPIC-2` have applied Design
Document §8's Auth column elsewhere (treating its exact wording as
authoritative rather than inferring a stricter rule it doesn't state),
this means **any authenticated role — including Verifier — may append a
Traceability Event.** This is not ambiguous (the text is clear), but it
may not be the team's actual intent, since Verifier is otherwise framed as
a read-only, public-verification-oriented role
(`.agents/execution/00-execution-overview.md`'s Role Model note on
Verifier). `EPIC-3-TRACE-003` implements this literally as documented and
flags it for the Project Manager's awareness rather than silently
tightening it — tightening it without authorization would itself be an
unauthorized scope/behavior change.

## Explicit Out-of-Scope Items for EPIC 3

Per `.agents/rules/01-scope-boundaries.md` and Design Document §5.1/§19:

- QR code generation, HMAC signing, or the public verification endpoint —
  EPIC 4 (see Open Decision #1 on the boundary question itself).
- The SRS's full enterprise DAG traceability engine (FR-TRACE-001's lot
  splitting/merging, wet-mill batch aggregation, bag serialization,
  cooperative-intake blending) — Design Document §5.1 explicitly narrows
  V1.0 to a single-origin, non-splitting/merging lot model. UC-22 ("Split
  Coffee Processing Lot") and UC-23 ("Merge Green Coffee Lots") are not
  implemented.
- Any Lot update or deletion endpoint — Design Document §8 defines no such
  endpoint; Lots and Events are both effectively append-only/immutable
  once created (Events explicitly so: "no update/delete route exposed").
- Quality grading, waybill issuance, export licensing, or forex
  cross-validation stretch modules, even though Design Document §5.1
  mentions "quality certificate attached" / "waybill issued" as example
  future `TraceabilityEvent` types — those event types are not generated
  by anything in this epic, since the modules that would generate them
  (EPIC 7, EPIC 8) are not built.
- Cherry collection/batch intake (SRS Module 03) — not part of V1.0's
  Farm-to-Lot chain at all; a Coffee Lot in this epic's scope is created
  directly against a Farm, not against a collection batch.

## Handoff Requirements to EPIC 4

For Dynamic QR (EPIC 4) to begin, EPIC 3 must leave behind:

- At least one real, persisted `CoffeeLot` record with a valid GIN (once
  the GIN traceability gap is resolved) linked to a real Farm, reachable
  via `GET /api/v1/lots/{id}/trace`.
- At least one real, persisted `TraceabilityEvent` row against that Lot
  (at minimum, the auto-created "lot created" event from `TRACE-002`).
- A stable, documented API contract for Lot creation and retrieval that
  EPIC 4's QR generation endpoint (`POST /api/v1/lots/{id}/qr`, per Design
  Document §8) can reference by `lot_id`.
- Confirmation, from `TRACE-007`, that no defect remains open against Lot
  creation, event logging, or trace retrieval that would block QR
  generation from correctly resolving its target lot.

## Cross-EPIC Issues / Required Follow-up

Recorded here rather than fixed in the earlier task files, per this
request's explicit instruction not to modify `EPIC-0`/`EPIC-1`/`EPIC-2`:

1. **Verification-task ownership pattern inconsistency.** `EPIC-1-AUTH-008`
   and `EPIC-2-FARM-007` both name Ephratha as the sole verification-task
   owner, with Kidus limited to documentation updates. The Minimum Project
   Plan's WBS, now available, more precisely splits this: Ephratha owns
   integration/API/RBAC testing specifically, while Kidus owns the
   functional/system walkthrough and Test Report draft specifically. This
   task package's `TRACE-007` uses the more precise split. **Follow-up:**
   Kidus/the Project Manager should decide whether to retroactively note
   this refinement against `EPIC-1-AUTH-008`/`EPIC-2-FARM-007` in the
   requirements-traceability documentation (not by editing those task
   files) so the ownership model is consistent across all three epics'
   actual execution.
2. **Week 1 vs. Week 2 schema-implementation timing** (identified during
   `EPIC-2`'s creation, restated here since the Minimum Project Plan's WBS
   confirms it again at line-item level): the Implementation
   Specification's four-week schedule places initial schema and even
   Auth/RBAC backend work in "Week 1," while the Minimum Project Plan's
   WBS treats Week 1 as design-only and schedules schema *implementation*
   (including the `CoffeeLot`/`TraceabilityEvent` schema this epic depends
   on) under a later block consistent with Week 2. Since EPIC-0 is stated
   complete regardless of which week it was actually done in, this does
   not block EPIC-3, but it remains an unreconciled schedule-documentation
   inconsistency worth Kidus's attention.

## Change-Control Rules

Identical to those already governing `EPIC-1`/`EPIC-2`, per
`.agents/rules/06-change-control.md` and
`.agents/execution/06-failure-and-escalation.md`: every proposed deviation
is classified (Required / Defect Fix / Stretch / Out of Scope) before any
work begins; only the Project Manager authorizes a scope, architecture, or
technology change; conflicts are reported using the standard Issue/
Evidence/Affected documents/Why it blocks/Options/Recommendation format,
not silently resolved. This applies in full to both Open Decisions above.

## Definition of EPIC Completion

EPIC 3 is not complete, and EPIC 4 must not begin, until **all** of the
following hold (mirroring `.agents/execution/07-task-completion-checklist.md`'s
EPIC-level sign-off and the pattern already used by `EPIC-2`'s completion
gate):

- All seven tasks (`TRACE-001`–`TRACE-007`) report Definition of Done
  satisfied and are merged to `develop`.
- `TRACE-007`'s end-to-end verification passes every criterion in its own
  Acceptance Criteria, exercising: **Authenticated user -> select an
  existing Farm -> Create Coffee Lot -> observe auto-created initial
  Traceability Event -> append at least one additional Traceability Event
  -> retrieve the full traceability chain and confirm it correctly traces
  back to the originating Farm and Farmer.**
- The GIN traceability gap flagged under `TRACE-001` has been resolved by
  the Project Manager, or explicitly, formally accepted as a documented
  open item that does not block the demo.
- Open Decision #1 (epic boundary) has been acknowledged by the Project
  Manager, even if not formally reconciled in documentation before EPIC 4
  begins — EPIC 4 must not begin under a silently different understanding
  of what it covers.
- No item from any task's `Out of Scope` section was implemented.
- At least one complete Farmer -> Farm -> Lot -> Traceability Event chain
  exists in the local/demo database, created through the actual UI, proving
  the chain works end to end for a human, not just for automated tests.

## Traceability Summary

```text
SRS
  Module 06: Traceability & Dynamic QR Engine (FR-TRACE)
    FR-TRACE-001 DAG Traceability Engine (narrowed for V1.0)
    FR-TRACE-002 Cryptographic QR Code Generation (EPIC 4, not this epic)
        |
        v
Design Document V1.0
    Section 5.1 Traceability Chain (narrows FR-TRACE-001 to a
      single-origin, non-splitting/merging model)
    Section 5.2 Identifiers (GIN — format not specified; see Open
      Decision #2)
    Section 7.1/7.2 ERD and Entity Descriptions (CoffeeLot,
      TraceabilityEvent — already built by EPIC-0-DB-002)
    Section 8 API Design — Traceability (POST /lots,
      POST /lots/{id}/events, GET /lots/{id}/trace)
    Section 9.3 Traceability / Operations UI
    Section 13 Sequence 4 (Create Traceable Coffee Lot)
        |
        v
Implementation Specification
    EPIC 3 — Traceability Engine (backend task list, Definition of Done)
        |
        v
Minimum Project Plan V1.0
    Week 3 Key Activities: "Complete Traceability & QR Engine; integrate
      Auth, Farmer Registry, and Traceability into one working chain"
    Milestone M4 (Working Increment Delivered, end of Week 3)
    Section 7.1 WBS: schema, API, UI, integration, and testing rows for
      Traceability (Fistum Adisu; joint with Yedenekachew at the
      Farm/Lot integration seam; Ephratha and Kidus for testing)
        |
        v
EPIC-3 tasks (TRACE-001 through TRACE-007)
```
