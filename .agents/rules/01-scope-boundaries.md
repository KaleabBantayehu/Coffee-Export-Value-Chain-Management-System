# Rule 01 — Scope Boundaries

## Purpose

CEVCMS V1.0 is a deliberately bounded subset of a much larger enterprise
system described in the SRS. This rule states exactly what is in scope, what
is stretch, and what is out of scope, and what an agent must do when a task
seems to require something outside these boundaries.

Source of authority: Project Baseline & Scope Freeze §3; Implementation
Specification §1; Implementation Playbook §4.

## Core scope (must-have — V1.0 is not done without these)

- Authentication and RBAC
- Farmer registration
- Farm registration
- Farm polygon mapping
- Coffee lot registration
- Traceability events
- Dynamic QR generation
- Public QR verification

## The core-chain acceptance workflow

All core scope items exist to make this single sequence work end to end.
This is the primary path V1.0 is judged against:

```text
Login
  -> Register Farmer
  -> Register Farm
  -> Draw / Save Farm Polygon
  -> Create Coffee Lot
  -> Create Traceability Record / Event
  -> Generate QR
  -> Scan / Open QR
  -> Public Verification Page
  -> Display permitted Traceability / Origin Information
```

A task that does not move the system toward this sequence being true is
either stretch or out of scope — it is not core, regardless of how useful it
seems.

## Core-chain dependency rule

The core scope has a fixed build order (Implementation Specification §4,
Playbook §5):

```text
Authentication & RBAC
   -> Farmer Registry
   -> Farm + Polygon Registry
   -> Traceability + Coffee Lot
   -> Dynamic QR Generation
   -> Public QR Verification
```

An agent must not begin work on a downstream module (e.g., Traceability) if
the module(s) it depends on (e.g., Farmer Registry) are not yet functional,
even if asked to. If asked to do so, flag the dependency gap instead of
proceeding out of order.

## Stretch scope (only after the core chain is fully operational)

- Quality grading
- Digital waybill
- Export licensing
- Forex-related functionality (simulated / non-live only)

Stretch work must **never** displace or delay core work. No stretch task file
exists yet in `tasks/`; none should be started, by human or agent, before the
core chain above is demonstrably working end to end. If asked to begin
stretch work early, refuse and point to this rule.

## Out of scope for V1.0 — do not implement, even partially

- Real NBE (National Bank of Ethiopia) integration
- Real commercial bank integration
- Real customs (Ethiopian Customs Commission / ASYCUDA) integration
- Real Ethio Telecom / Safaricom USSD or SMS gateway
- Native offline Android application
- GPS / IoT hardware integrations
- Blockchain smart contracts
- AI/ML defect analysis
- Satellite yield estimation
- Kubernetes or other national-scale production infrastructure
- 5,000 TPS (or any) load testing at national scale
- Use of real farmer personal data
- Use of real financial data

Where the SRS describes an enterprise-grade version of something in core
scope (e.g., HSM-backed key custody instead of an environment-variable
secret, OAuth2/OIDC instead of simple JWT, multi-region PostgreSQL instead of
a single instance), the **simplified V1.0 version already specified in the
Design Document** is what gets built. The SRS's enterprise version is design
context, not a V1.0 target.

## The stop-rather-than-invent rule

If, while implementing a task, an agent identifies something that seems
necessary but is not written in the task file, the Design Document, or the
SRS for that module:

1. **Stop before implementing it.**
2. Check whether it is genuinely required to satisfy an already-documented
   requirement (in which case it may be "Required" — see
   `06-change-control.md`), or whether it is a convenience, an assumption, or
   scope creep.
3. If in doubt, do not implement it. Report the gap in the task's `Expected
   Agent Report` section instead, so a human can classify it.

Agents and developers must never expand scope to make a task "more complete"
or "more production-ready" than what the task file and source documents
define. A course-scale prototype that honestly does less is preferred over
one that silently does more than agreed.
