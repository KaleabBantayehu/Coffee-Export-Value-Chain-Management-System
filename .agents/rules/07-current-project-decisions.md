# CEVCMS V1.0 — Current Project Decisions

**Project:** Coffee Export Value Chain Management System (CEVCMS)  
**Version:** V1.0  
**Document Type:** Internal AI-Agent and Development Control Record  
**Location:** `.agents/rules/07-current-project-decisions.md`  
**Status:** Active for the current V1.0 implementation period

* * *

## 1\. Purpose

This document records the project decisions that have been explicitly settled for the CEVCMS V1.0 implementation.

It exists to prevent developers, AI agents, and project members from independently interpreting earlier documents when a decision has already been resolved.

This document does **not** replace the:

-   Assignment Description
-   Software Requirements Specification (SRS)
-   Minimum Project Plan
-   Design Document
-   V1.0 Baseline & Scope Freeze
-   Implementation Specification & Development Backlog

It is an implementation-control document that records the current agreed interpretation of those sources.

If a future change is required, it must follow the project's change-control procedure in:

`.agents/rules/06-change-control.md`

No AI agent may treat this document as permission to expand V1.0 scope.

* * *

# 2\. Project Authority

The following documents are the primary project sources:

1.  **V1.0 Baseline & Scope Freeze**
2.  **Implementation Specification & Development Backlog**
3.  **Design Document V1.0**
4.  **Minimum Project Plan V1.0**
5.  **Software Requirements Specification V2.1**
6.  **Assignment Description V1.0**
7.  Phase 1 Discovery / User Research Report

For implementation decisions, the latest explicitly agreed V1.0 decisions recorded in the Baseline, Implementation Specification, and Design Document must be followed.

If an AI agent encounters a contradiction that is not explicitly resolved here:

**STOP → report the conflict → do not choose unilaterally.**

The Project Manager must decide whether the issue is:

-   Required
-   Defect Fix
-   Stretch
-   Out of Scope

according to the project's change-control rules.

* * *

# 3\. V1.0 Version Freeze

The project version is:

**CEVCMS V1.0**

Do not change the project version to:

-   V1.1
-   V2.0
-   V2.1
-   or any other implementation version

unless explicitly authorized by the Project Manager and required by the university/project process.

The SRS may remain referenced as V2.1 because it is the requirements document version.

The software implementation itself remains:

**CEVCMS V1.0**

* * *

# 4\. Frozen Technology Stack

The following technologies are frozen for V1.0.

| Layer | Decision |
| --- | --- |
| Frontend | React + JavaScript |
| Backend | Python + FastAPI |
| Database | PostgreSQL + PostGIS |
| Mapping | Leaflet / React-Leaflet |
| Authentication | JWT + password hashing |
| QR | QR generation + HMAC signing |
| API Testing | Postman |
| Version Control | Git + GitHub |
| UI/UX | Figma |

### Explicit technology restrictions

Do NOT introduce the following without Project Manager approval and change classification:

-   Angular
-   Vue
-   Node.js/Express as the backend
-   MongoDB
-   MySQL as a replacement database
-   Mapbox as a replacement for Leaflet
-   Redis
-   Kubernetes
-   microservices
-   message queues
-   blockchain
-   AI/ML services
-   native Android applications
-   external production authentication platforms

The V1.0 implementation uses a **modular monolithic backend**.

Do not redesign it as a microservice architecture.

* * *

# 5\. Frozen V1.0 Core Scope

The following are mandatory V1.0 functionality:

1.  Authentication and RBAC
2.  Farmer registration
3.  Farm registration
4.  Farm polygon mapping
5.  Coffee lot registration
6.  Traceability events
7.  Dynamic QR generation
8.  Public QR verification

The primary acceptance workflow is:

```
Login
  ↓
Register Farmer
  ↓
Register Farm
  ↓
Draw / Save Farm Polygon
  ↓
Create Coffee Lot
  ↓
Create Traceability Record / Event
  ↓
Generate QR
  ↓
Scan / Open QR
  ↓
Public Verification Page
  ↓
Display Traceability / Origin Information
```

This workflow is the primary V1.0 acceptance path.

A feature is not more important than completing this workflow.

* * *

# 6\. Stretch Scope

Stretch functionality may be implemented only after the complete core workflow is operational and tested.

The stretch scope is:

-   Quality grading
-   Digital waybill
-   Export licensing
-   Forex-related functionality

Stretch work must never:

-   delay the core workflow;
-   replace unfinished core work;
-   cause technology expansion;
-   become a prerequisite for demonstrating the core MVP.

If time runs short, stretch functionality is dropped before core functionality.

* * *

# 7\. Explicitly Out of Scope for V1.0

The following are not to be implemented as real production integrations:

-   Real NBE integration
-   Real commercial bank integration
-   Real customs integration
-   Real Ethio Telecom integration
-   Real Safaricom Ethiopia USSD/SMS gateway
-   Native offline Android application
-   GPS / IoT hardware integrations
-   Blockchain smart contracts
-   AI/ML defect analysis
-   Satellite yield estimation
-   Kubernetes production infrastructure
-   National-scale deployment
-   5,000 TPS load testing
-   Real farmer personal data
-   Real financial data
-   Real customs/trade data

Demonstration data must be synthetic, seeded, or otherwise safe for the university project.

* * *

# 8\. Frozen Authentication and RBAC Model

The V1.0 application uses these four roles:

1.  **Admin**
2.  **ECTA Officer**
3.  **Field/Registry Agent**
4.  **Verifier**

Do not create an additional V1.0 application role such as:

-   Exporter
-   Farmer
-   Coop Manager
-   Bank Officer
-   Customs Officer

unless the Project Manager explicitly approves a scope change.

Stakeholders described in the Discovery Report are not automatically application roles.

The public QR verification endpoint is intentionally unauthenticated.

All other protected application routes must use the common authentication and RBAC mechanism.

* * *

# 9\. Mapping Decision

The V1.0 mapping implementation is:

**Leaflet / React-Leaflet**

Farm polygon data must use:

**PostgreSQL + PostGIS geometry**

Do not introduce Mapbox GL or another mapping platform simply because it appears as an alternative in an earlier planning document.

The purpose of the V1.0 map is to support the bounded farm/polygon registration workflow and demonstration.

* * *

# 10\. Team Responsibility Decisions

Current implementation ownership is:

| Member | Current V1.0 Responsibility |
| --- | --- |
| Kaleab Bantayehu | Project Manager + Backend/Auth Lead |
| Yedenekachew Fantahun | Database + Farmer/Farm/Polygon Backend |
| Fistum Adisu | Traceability + Dynamic QR Backend |
| Biniyam Abel | Frontend Lead |
| Abel Debalke | Frontend / Full-Stack Support |
| Ephratha Samuel | Backend + QA |
| Kidus Ergetachew | Documentation + QA + Communication |

### Abel Debalke

For the current core implementation, Abel is assigned as:

**Frontend / Full-Stack Support**

He supports Biniyam with:

-   reusable React components;
-   form validation;
-   API integration;
-   frontend implementation;
-   core UI support.

Abel may take stretch-module frontend or backend work only:

1.  after the core chain is functional;
2.  if the work is still within V1.0 stretch scope;
3.  with Project Manager approval.

No AI agent may automatically assign Abel to a stretch backend module simply because an older document lists him there.

* * *

# 11\. Kidus Ergetachew Responsibility

Kidus owns documentation, QA support, and project communication tasks including:

-   requirements traceability;
-   test documentation;
-   defect tracking documentation;
-   progress reports;
-   user manual;
-   demonstration documentation;
-   project-document consistency.

Kidus does not need to be assigned complex core backend implementation merely to increase development capacity.

* * *

# 12\. Database Decision

The V1.0 database is:

**PostgreSQL + PostGIS**

The core data chain is:

```
User / Role
     ↓
Farmer
     ↓
Farm
     ↓
CoffeeLot
     ↓
TraceabilityEvent
     ↓
QRRecord
```

Farm polygons must use spatial/PostGIS geometry rather than plain text latitude/longitude fields.

The database must support the end-to-end acceptance workflow.

Do not add enterprise-scale database infrastructure.

* * *

# 13\. Backend Architecture Decision

The backend architecture is:

**Modular Monolith**

The backend must preserve logical module boundaries while remaining a single deployable FastAPI application.

Expected core module boundaries include:

```
Authentication / RBAC
Farmer & Polygon Registry
Traceability
QR
Common / Shared
```

Do not convert the project to:

```
microservices
message queues
service mesh
distributed event architecture
```

unless explicitly approved through change control.

* * *

# 14\. API Decision

The API uses:

**REST / JSON**

API routes use the V1 API namespace:

```
/api/v1/
```

Core authentication routes include:

```
POST /api/v1/auth/login
GET  /api/v1/auth/me
POST /api/v1/auth/logout
```

Protected application routes require JWT authentication and appropriate RBAC authorization.

The public QR verification route is intentionally unauthenticated.

* * *

# 15\. Security Decisions

V1.0 must implement:

-   password hashing;
-   JWT authentication;
-   RBAC;
-   protected routes;
-   input validation;
-   authorization checks;
-   HMAC-signed QR payloads;
-   audit logging where specified by the design;
-   environment-based secrets;
-   no plaintext passwords;
-   no committed production secrets.

The following enterprise security features are not V1.0 requirements:

-   HSM infrastructure;
-   OAuth2/OIDC federation;
-   full ABAC;
-   enterprise key-management infrastructure;
-   formal enterprise penetration testing.

Do not claim these features are implemented when they are not.

* * *

# 16\. AI-Agent Rules

Every AI agent working on CEVCMS must:

1.  Read this file.
2.  Read `.agents/rules/00-project-authority.md`.
3.  Read `.agents/rules/01-scope-boundaries.md`.
4.  Read `.agents/rules/02-tech-stack.md`.
5.  Read `.agents/rules/03-coding-rules.md`.
6.  Read `.agents/rules/04-git-workflow.md`.
7.  Read `.agents/rules/05-testing-rules.md`.
8.  Read `.agents/rules/06-change-control.md`.
9.  Read the specific task file before changing code.
10.  Trace the task to the SRS, Design Document, Implementation Specification, and applicable Project Plan section.

An agent must not begin implementation when a requirement or architectural decision is unclear.

It must report the ambiguity instead.

* * *

# 17\. Existing Work Must Not Be Recreated

The following project infrastructure already exists and must not be recreated as part of later tasks:

-   Git repository
-   `main` branch
-   `develop` branch
-   backend virtual environment
-   installed backend dependencies
-   frontend React/Vite project
-   repository folder structure
-   baseline documentation
-   `.agents/` rules
-   EPIC-0 task definitions
-   EPIC-1 task definitions
-   execution procedures

Future agents must inspect the repository before installing, initializing, or recreating infrastructure.

Do not reinstall packages simply because an execution task mentions environment setup.

Do not recreate the GitHub repository.

Do not recreate the virtual environment.

* * *

# 18\. Git Decision

The working development branch is:

```
develop
```

Feature work must use feature branches.

Example:

```
git switch -c feature/auth-login
```

Do not develop directly on `main`.

Do not merge directly into `main`.

Changes must be reviewed before integration according to the project's Git workflow.

* * *

# 19\. Change-Control Decision

Any proposed change must first be classified:

### Required

Necessary to satisfy an existing approved requirement.

### Defect Fix

Fixes already-approved functionality without adding new capability.

### Stretch

Belongs to the approved stretch scope and occurs only after the core chain works.

### Out of Scope

Introduces functionality outside the approved V1.0 boundary.

If an AI agent believes a change is necessary but cannot determine its classification:

**STOP and ask the Project Manager.**

An agent must never silently expand scope.

* * *

# 20\. Documentation Consistency

The implemented system and project documentation must remain consistent.

If implementation differs from the approved design because of an approved decision:

1.  Record the decision.
2.  Update the affected documentation.
3.  Update requirements traceability.
4.  Update relevant tests.
5.  Do not silently leave contradictory documentation.

The goal is that the repository accurately describes what V1.0 actually does.

* * *

# 21\. Four-Week Priority Rule

The project has a one-month implementation period.

Priority order is:

```
CORE FUNCTIONALITY
       ↓
CORE INTEGRATION
       ↓
CORE TESTING
       ↓
END-TO-END DEMONSTRATION
       ↓
DOCUMENTATION / HARDENING
       ↓
STRETCH FUNCTIONALITY
```

If schedule pressure occurs:

**Remove or reduce stretch before reducing core functionality.**

The core workflow is always the primary priority.

* * *

# 22\. Final Decision Rule

When an AI agent encounters conflicting information:

```
Is the decision explicitly settled here?
        │
       YES
        ↓
Follow it.
        │
       NO
        ↓
Check the authoritative project documents.
        │
        ↓
Is the conflict explicitly resolved?
        │
    ┌───┴───┐
   YES      NO
    ↓        ↓
 Follow   STOP + escalate
```

The AI agent is an implementation assistant.

It is not authorized to redefine:

-   project scope;
-   architecture;
-   technology;
-   team ownership;
-   project version;
-   acceptance criteria;
-   core workflow.

Only the Project Manager and approved project-control process may authorize such changes.

* * *

## 23\. Current Implementation Objective

The immediate development objective is to implement the frozen V1.0 core workflow:

**Authentication → Farmer → Farm/Polygon → Coffee Lot → Traceability → Dynamic QR → Public Verification**

All development decisions should be evaluated against whether they help the team complete, integrate, test, and demonstrate this workflow within the one-month implementation period.

**End of Current Project Decisions**

This is deliberately **not another 40-page document**. It is a compact control file that agents can load quickly.

The key decisions are supported by the Baseline: React is frozen rather than Angular, the core scope is explicitly defined, and the four application roles are established. The Design Document also explicitly confirms the four-role RBAC model and public QR verification design.