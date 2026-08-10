# Rule 03 — Coding Rules

## Purpose

Practical, non-bureaucratic coding rules for a seven-person team with roughly
one month remaining. These rules favor a working, honestly-scoped modular
monolith over a "more correct" but unfinished system. They apply to human
developers and AI coding agents equally.

Source of authority: Design Document §1.4 ("Design Principles" — Traceable,
Bounded, Simple over clever, Demonstrable, Honest about limits) and §3
(System Architecture); Implementation Playbook §8.

## Architecture discipline

- The backend is a **modular monolith**, not microservices. Each module
  (Authentication/RBAC, Farmer & Polygon Registry, Traceability & QR, and —
  once reached — the stretch modules) is a distinct set of routes,
  controllers, and business-logic functions inside the one FastAPI
  application, per Design Document §3 and Playbook §8.
- Do not extract a module into a separate service, process, or deployable
  unit. Do not introduce inter-service communication, message queues, or an
  API gateway.
- Preserve module boundaries in code structure (e.g., separate routers,
  service files, and schema modules per domain area) so a future extraction
  remains possible without redesigning the data model — but do not build the
  extraction now.

## Code quality expectations

- **Maintainable, modular code.** One module's code lives in its own
  file(s)/folder; do not scatter one module's logic across unrelated files.
- **Clear naming.** Names describe what something is or does (e.g.,
  `farmer_service.py`, `create_farmer`), not abbreviations invented for
  convenience.
- **Separation of concerns**, matching the layered structure implied by the
  Design Document: API/route layer, business-logic/service layer, data-access
  layer (models via SQLAlchemy), and request/response schema layer (Pydantic)
  are kept distinct. Route handlers should not embed raw SQL or heavy
  business logic directly.
- **Validation.** Every write endpoint validates its input server-side
  (required fields, type/range/format checks) per Design Document §8. Do not
  rely on frontend validation alone.
- **Error handling.** Return structured, predictable error responses (HTTP
  400 for validation errors, 401/403 for auth/authorization failures, 404 for
  missing resources), consistent with Design Document §8. Do not let
  unhandled exceptions leak stack traces or internal detail to the client.
- **No unnecessary abstraction.** Do not build generic plugin systems,
  configurable rule engines, or abstract base classes for extensibility that
  no current task requires. Solve the task in front of you.
- **No speculative enterprise architecture.** Do not add caching layers,
  background job queues, event buses, feature flags, multi-tenancy, or
  horizontal-scaling scaffolding "for later." That later is explicitly out of
  scope (`01-scope-boundaries.md`).
- **No duplicate functionality.** Before adding a new utility, model, or
  endpoint, check whether an equivalent already exists in the codebase from a
  prior task. Reuse it; do not fork a near-identical copy.
- **No unnecessary dependency changes.** See `02-tech-stack.md`. If a task
  can be completed with what is already installed, do not add a package.

## Secrets and configuration

- No credentials, API keys, signing secrets, or connection strings are ever
  committed to the repository. Configuration is environment-variable based,
  with a `.env.example` documenting required variables without real values
  (Implementation Specification, EPIC 0 Definition of Done).
- The QR HMAC signing key and the JWT signing secret are read from
  environment variables, per Design Document §5.3 and §10 — never hard-coded.

## Honesty in implementation

- Where V1.0 deliberately simplifies an SRS enterprise requirement (e.g., a
  demonstration-scale EUDR flag instead of a real satellite forest-canopy
  check, per Design Document §4.2), the simplification must be clearly
  labeled in code comments and, where user-facing, in the UI — never
  implemented in a way that implies it is the production-grade version.
- Do not simulate an out-of-scope integration (e.g., a "fake NBE call") in a
  way that could be mistaken for a real one. If a stub is needed to satisfy a
  dependency, it must be obviously and explicitly a stub.
