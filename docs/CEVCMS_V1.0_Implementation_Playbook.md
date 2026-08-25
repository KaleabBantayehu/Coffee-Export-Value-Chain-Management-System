# CEVCMS V1.0 — Implementation Playbook

**Reference:** ECTA-CEVCMS-PLAYBOOK-V1.0
**Status:** Working control document for the development phase
**Authority:** This playbook does not introduce new scope, technology, or requirements. It restates decisions already frozen in the Baseline & Scope Freeze (`ECTA-CEVCMS-BASELINE-V1.0`), the Design Document (`ECTA-CEVCMS-DD-V1.0`), and the Implementation Specification, and adds only the day-to-day execution mechanics (git workflow, per-feature checklist) needed to run development without re-litigating settled decisions.

---

## 0. Purpose

Once the Baseline is approved, the technology stack, core scope, and critical workflow are **frozen**. This playbook is the single document the team (and any AI coding assistant) opens before touching code, so that:

- nobody reinstalls or swaps tooling that's already decided,
- nobody adds a feature that isn't traceable to an approved document,
- everyone builds in the dependency order the Implementation Specification already defines, and
- "what we've built" and "what the docs say" never quietly drift apart.

---

## 1. Document Precedence

```text
                    ECTA DISCOVERY REPORT
                            |
                            v
                         SRS V2.1
                            |
                            v
                 ASSIGNMENT DESCRIPTION V1.0
                            |
                            v
                 MINIMUM PROJECT PLAN V1.0
                            |
                            v
                  DESIGN DOCUMENT V1.0
                            |
                            v
        IMPLEMENTATION SPECIFICATION + BACKLOG
                            |
                            v
             BASELINE / SCOPE FREEZE V1.0
                            |
                            v
                    ACTUAL DEVELOPMENT   <-- this playbook governs this step only
```

This mirrors the precedence already stated in the Design Document: the Minimum Project Plan controls the one-month scope, the SRS controls requirement detail, the Discovery Report controls stakeholder/interface context, and Appendix 1 controls documentation methodology. This playbook does not sit above any of those documents — it sits *below* the Baseline, translating it into day-to-day execution steps.

---

## 2. The One Rule

Before implementing anything, ask:

> **Where is this requirement documented?**

If the answer isn't the SRS, the Assignment Description, the Design Document, the Implementation Specification, or the approved Baseline — **it doesn't get added**, no matter how small it seems.

Every proposed feature or change is classified first:

| Classification | Meaning | Action |
|---|---|---|
| **Required** | Needed for an existing documented requirement | Implement in current or next sprint |
| **Defect Fix** | Fixes existing functionality that doesn't match its spec | Implement immediately, log it |
| **Stretch** | Approved stretch feature, only after core is operational | Queue behind core scope |
| **Out of Scope** | Not part of V1.0 per the Baseline | Reject; do not implement |

This is what protects a one-month, seven-person project from scope creep — it is the single biggest risk called out across the Minimum Project Plan's risk register and the Baseline's change-control section.

---

## 3. Frozen Technology Stack

| Layer | Decision |
|---|---|
| Frontend | React + JavaScript |
| Backend | Python + FastAPI |
| Database | PostgreSQL + PostGIS |
| Mapping | Leaflet / React-Leaflet |
| Authentication | JWT + password hashing |
| QR | QR generation + HMAC signing |
| API Testing | Postman |
| Version Control | Git + GitHub |
| UI/UX | Figma |

**Do not reinstall, replace, or add to this list** without going through Section 2's classification and getting it logged as a controlled scope change by the Project Manager (Kaleab).

### Confirmed local backend environment

*As reported by the team from the current dev machine — re-verify with `pip freeze` / `python --version` if there's ever doubt, rather than trusting this table blindly:*

```text
Python          3.13.3
FastAPI         0.141.1
SQLAlchemy      2.0.51
psycopg2-binary 2.9.12
Pydantic        2.13.4
JWT             python-jose
Password        passlib + bcrypt
Uvicorn         0.52.1
```

These are already installed. **Do not reinstall them** — if a dependency issue comes up, fix the specific problem, don't re-provision the environment.

---

## 4. Frozen Core Scope

**Must-have (V1.0 is not done without these):**

- Authentication & RBAC
- Farmer registration
- Farm registration
- Farm polygon mapping
- Coffee lot registration
- Traceability events
- Dynamic QR generation
- Public QR verification

**Stretch — only after the core chain above is fully operational:**

- Quality grading
- Digital waybill
- Export licensing
- Forex-related cross-validation (simulated, non-live)

Stretch work never displaces or delays core work. If Week 3 ends and core isn't fully working end to end, stretch does not start.

---

## 5. Development Order

The Implementation Specification already fixes this dependency graph — it is not re-derived here:

```text
Authentication & RBAC
        |
        v
Farmer Registry
        |
        v
Farm + Polygon Registry
        |
        v
Traceability + Coffee Lot
        |
        v
Dynamic QR Generation
        |
        v
Public QR Verification
        |
        v
      CORE COMPLETE
        |
  +-----+-----+
  v           v
Quality     Export + Forex
Grading     Cross-Validation
Waybill     (STRETCH)
(STRETCH)
```

---

## 6. Four-Week Schedule

```text
WEEK 1 — Foundation
  Repository -> React setup -> FastAPI foundation -> PostgreSQL/PostGIS
    -> Database schema -> Authentication/RBAC -> Initial Farmer module

WEEK 2 — Core Modules
  Authentication -> Farmer -> Farm -> Polygon -> EUDR demonstration flag
    -> Leaflet frontend -> Start traceability

WEEK 3 — Integration
  Login -> Farmer -> Farm -> Polygon -> Lot -> Traceability -> QR -> Verification

WEEK 4 — Stabilization
  Bug fixing -> Integration testing -> RBAC testing -> Validation
    -> Demo data -> Test Report -> User Manual -> UI cleanup
    -> Stretch (if time allows) -> Demo rehearsal
```

This is the same order already set out in the Implementation Specification and Minimum Project Plan — it is restated here, not reinvented.

---

## 7. Definition of "Working Increment" (the north star)

> A registered user can log into CEVCMS, register a farmer and farm, capture and save a farm polygon, create a traceable coffee lot linked to that farm, generate a digitally signed QR code for the lot, and allow an unauthenticated user to scan/verify that QR code and view the permitted origin/traceability information.

Every core-scope task exists to make this single sequence true. A feature that doesn't move the system closer to this sentence being demonstrably true is either stretch or out of scope.

---

## 8. Backend Architecture

Per the Design Document: a **modular monolith**, not microservices — a distributed-systems architecture would add operational overhead a seven-person, four-week team cannot absorb.

```text
FastAPI
   |
   +-- Authentication / RBAC
   |
   +-- Farmer Registry
   |
   +-- Farm / Polygon Registry
   |
   +-- Coffee Lot
   |
   +-- Traceability
   |
   +-- QR Generation / Verification
        |
        v
 PostgreSQL + PostGIS
```

Polygon data is stored as **PostGIS geometry**, never plain latitude/longitude fields — this is a Design Document requirement, not a style preference.

---

## 9. Per-Feature Development Workflow

Every feature, without exception, goes through these ten steps:

1. **Requirement** — trace it: `SRS requirement → Design Document section → Backlog task`. If any link is missing, stop and classify it (Section 2) before writing code.
2. **Design** — confirm database, API, business logic, frontend, permissions, and validation before implementing, using the Design Document as the source, not improvised on the spot.
3. **Implement** — create a feature branch:
   ```bash
   git switch -c feature/auth-login
   ```
4. **Test** — happy path, invalid input, unauthorized access, wrong role, database behavior, API response.
5. **Review** — another team member reviews before merge.
6. **Merge** — into `develop`, never directly into `main`.
7. **Integration test** — confirm nothing existing broke.
8. **Commit** — meaningful, conventional messages:
   ```text
   feat(auth): implement JWT login
   fix(farmer): validate FIN uniqueness
   ```
9. **Update documentation** — Kidus updates the relevant requirements-traceability entry and test documentation so the docs stay honest about what's actually built.
10. **Move to the next backlog item** — in dependency order (Section 5), not whichever task looks most interesting.

---

## 10. Current Status

*Team-reported status — treat as a snapshot to verify (Section 12), not as a completed audit:*

| Item | Status |
|---|---|
| Discovery Report | Done |
| SRS | Done |
| Assignment Description | Done |
| Minimum Project Plan | Done |
| Design Document | Done |
| Implementation Specification | Done |
| Baseline / Scope Freeze | Done |
| Git repository | Created |
| `main` branch (stable baseline) | Created |
| `develop` branch (active implementation) | Created, pushed to GitHub |
| Python virtual environment | Set up |
| Backend dependencies | Installed |

Planning is complete. Implementation is the remaining work — this playbook governs it.

---

## 11. Working Rule for AI-Assisted Development

AI coding assistants (Claude, Gemini, ChatGPT, or an agentic tool like Antigravity) are useful for generating boilerplate, explaining code, writing tests, and finding bugs. They do **not** decide architecture, scope, or requirements — those are already fixed by the documents in Section 1.

In practice: before asking an AI assistant to implement something, point it at the specific SRS requirement, Design Document section, and backlog task (Section 9, Step 1). An assistant that isn't given that context will happily generate something plausible-looking that doesn't match what's actually documented — and if two different AI tools are used across sessions without shared, current context, that's exactly how "SRS says one thing, the code says another, and the docs go stale" happens on a project this size.

---

## 12. Immediate Next Steps

Before writing any more code, establish a clean checkpoint:

```bash
git status
git branch
git log --oneline --decorate -5
```

Review the output against Section 10 before proceeding. Then continue in dependency order (Section 5): **Backend Foundation → Database Configuration → PostgreSQL/PostGIS connection → first database migration/schema** — per the Design Document and Implementation Specification, not a newly improvised structure.

---

*End of Playbook — ECTA-CEVCMS-PLAYBOOK-V1.0*
