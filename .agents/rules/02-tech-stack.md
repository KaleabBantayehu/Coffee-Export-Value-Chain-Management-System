# Rule 02 — Frozen Technology Stack

## Purpose

The technology stack for CEVCMS V1.0 is frozen. This rule records it exactly
and prohibits unauthorized substitution, no matter how reasonable an
alternative might seem in isolation.

Source of authority: Project Baseline & Scope Freeze §2; Implementation
Specification (Technical Stack Freeze table); Implementation Playbook §3.

## The frozen stack

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

## One already-resolved conflict

The Design Document left the frontend framework open between Angular and
React. The Implementation Specification and Baseline have since fixed this to
**React + JavaScript**. Angular is not to be introduced, discussed as a live
choice, or partially adopted.

## Confirmed local backend environment

As reported by the team and recorded in the Implementation Playbook §3.
Re-verify with `pip freeze` / `python --version` if there is ever doubt,
rather than trusting this table blindly — but do not reinstall or reprovision
based on a mismatch without first understanding why it differs.

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

These are already installed. **Do not reinstall them.** If a dependency issue
comes up, fix the specific problem; do not re-provision the environment or
swap a library for a similar one without going through
`06-change-control.md`.

## What is explicitly prohibited

- Introducing a different frontend framework, meta-framework, or state
  library (e.g., Vue, Svelte, Next.js, Redux) without a controlled scope
  change signed off by the Project Manager.
- Introducing a different backend framework (e.g., Django, Flask, Express)
  under any circumstance — FastAPI is fixed.
- Introducing a different database or a caching/queueing layer not already
  named above (e.g., MongoDB, Redis, Kafka, RabbitMQ) — even if the SRS
  mentions such technology for the full enterprise system. The SRS's Redis
  reference (SRS §2.4, enterprise operating environment) is enterprise-scope,
  not V1.0-scope.
- Adding an ORM, migration tool, or auth library not already implied by the
  confirmed environment above (SQLAlchemy is the ORM; no other ORM is
  introduced) without going through change control.
- Upgrading or downgrading any dependency version listed above "for safety"
  or "for a bug fix" without documenting the specific problem being solved
  and getting it logged as a controlled change.
- Adding infrastructure technology (containers beyond what already exists,
  orchestration, service mesh, CDN, message queues) — Design Document §16
  explicitly states no additional technology is introduced because none is
  required to demonstrate core scope.
- Replacing HMAC-signed QR with any other signing scheme, or JWT with any
  other session mechanism (e.g., server-side sessions, OAuth2/OIDC) — these
  are the Design Document's deliberate simplifications of the SRS's
  enterprise security design (SEC-02) and are frozen for V1.0.

## What is allowed without a change-control step

- Adding a well-established, narrowly-scoped library that implements a
  capability already required by an approved task (e.g., a QR-code image
  generation library to satisfy FR-TRACE-002) is allowed **if** the task file
  does not already name one, the library serves only that requirement, and
  the choice is recorded in the `Expected Agent Report`. This is not a stack
  change; it is fulfilling an already-approved requirement.
- Standard testing libraries (e.g., `pytest`) needed to satisfy
  `05-testing-rules.md` are allowed under the same condition.

When genuinely uncertain whether something counts as "the frozen stack" or
"a new technology," treat it as a new technology and route it through
`06-change-control.md`.
