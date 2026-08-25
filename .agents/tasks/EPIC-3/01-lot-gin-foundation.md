# Task Title

Coffee Lot Data Foundation — GIN Generation & Validation Utility

## Task ID

EPIC-3-TRACE-001

## Epic

EPIC 3 — Traceability Engine

## Owner

Fistum (Backend Developer — Traceability & QR), per Baseline §5 and
Implementation Specification EPIC 3 ownership.

## Status

**Partially blocked.** Collision-handling and validation logic can
proceed. The exact GIN format is not specified anywhere in the
authoritative documents — see "Traceability Gap" below. This task's own
Definition of Done cannot be satisfied until that gap is escalated (not
necessarily resolved, but at minimum escalated).

## Priority

Critical — `TRACE-002` (Coffee Lot creation API) cannot be completed
without a working GIN generator.

## Purpose

Implement the GIN (Global Identification Number) generation and
validation utility that `TRACE-002`'s Lot creation endpoint will call, on
top of the `CoffeeLot` table's `gin_code` column already created by
`EPIC-0-DB-002`.

## Why This Task Exists

Design Document §7.2 fixes `CoffeeLot.gin_code` as unique; nothing yet
generates a GIN value to insert. This mirrors `EPIC-2-FARM-001`'s pattern
of building the identifier-generation utility as its own task, before the
endpoint that will call it, and before it is needed by any other task.

## Authoritative Sources

- SRS, Module 06 (FR-TRACE): FR-TRACE-001/002 do not state a GIN format.
- SRS, Appendix C ("Cryptographic e-Waybill Verification Layout"):
  illustrative example `BATCH GIN : ETH-LOT-2026-G1-00392` — not a
  normative requirement statement, and tied to the e-Waybill (stretch,
  EPIC 7) context, embedding a grade code not present in V1.0's simplified
  lot model.
- Design Document §5.2 ("Lot GIN — a unique code assigned to a Coffee Lot
  at creation, in the spirit of SRS's Global Identification Number, scoped
  to Version 1.0's simplified lot model (one lot, one origin farm).")
- Design Document §7.2 (`CoffeeLot.gin_code` — unique, already created by
  `EPIC-0-DB-002`)

## Requirements Traceability

```text
SRS:
- FR-TRACE-001/002 (Module 06) — no GIN format specified in either
  requirement statement.
- Appendix C — one illustrative, non-authoritative example
  (ETH-LOT-2026-G1-00392), not applicable as-is because it embeds a
  stretch-scope grade code V1.0's core-only lot model does not have.

Design Document:
- Section 5.2 confirms a GIN is generated and unique, "in the spirit of"
  the SRS's GIN concept, without restating or resolving a specific format.
- Section 7.2 fixes the column as `gin_code` (unique), with no format
  constraint specified at the schema level from EPIC-0-DB-002.

Implementation Specification:
- EPIC 3, Tasks: "CoffeeLot model & Lot/GIN generation logic" — confirms
  GIN generation is EPIC-3 backend scope, without specifying format.

Minimum Project Plan:
- No GIN-format detail found in the WBS or elsewhere.

Baseline Scope Freeze:
- Section 3.1, "Coffee lot registration" (core scope item; format not
  specified here either).
```

## Prerequisites

- Confirm the `CoffeeLot` table exists with a `gin_code` column carrying a
  database-level uniqueness constraint (re-run `EPIC-0-DB-002`'s
  verification method if any doubt exists).

## Dependencies

`EPIC-0-DB-002` (the `CoffeeLot` table and its `gin_code` unique
constraint) only. No dependency on any EPIC-1 or EPIC-2 task — this is a
pure data-generation utility, not an endpoint.

## Traceability Gap — Escalate Before Finalizing the Format

Per this request's Section 10 ("If a requirement cannot be mapped,
explicitly mark: 'Traceability gap — requires review.'"): **Traceability
gap — requires review.** No SRS or Design Document text specifies a GIN
format for V1.0. Raise this via
`.agents/execution/06-failure-and-escalation.md`'s report format:

```text
Issue: No authoritative source specifies a GIN (Global Identification
Number) format for Version 1.0 Coffee Lots. FR-TRACE-001/002 give no
format string. Design Document §5.2 describes the GIN conceptually
without a format. The only concrete example in the SRS is in Appendix C
(ETH-LOT-2026-G1-00392), illustrating a stretch-scope e-Waybill layout
that embeds a grade code not applicable to V1.0's simplified lot model.

Evidence: SRS Module 06 (FR-TRACE-001, FR-TRACE-002); SRS Appendix C;
Design Document Section 5.2.

Affected documents: SRS (Level 2), Design Document (Level 3) — neither
resolves this; it is an absence of specification, not a conflict between
two stated positions (contrast with EPIC-2-FARM-001's FIN format, which
has two actively conflicting SRS statements).

Why it blocks implementation: A GIN generator must produce a specific,
consistent format to be useful for display, lookup, and (in EPIC 4) QR
payload encoding. Implementing an arbitrary format risks needing to
regenerate already-created Lot records if the team later adopts a
different convention.

Possible options:
  1. Adapt the Appendix C illustrative pattern, dropping its
     stretch-scope grade segment, e.g. ETH-LOT-<year>-<sequence>.
  2. Adopt a format structurally parallel to FIN's eventual resolution
     (ETH-LOT-<N digits>-<M digits>), for consistency across the two
     identifier types.
  3. Adopt any other project-decided format, documented as a deliberate
     V1.0 decision.

Recommended action: This is a recommendation for the Project Manager, not
a decision this task is authorized to make. Given FARM-001's FIN format
is itself still pending Project Manager decision, resolving both
identifier formats in the same decision session may be efficient.
```

**This task's remaining work (below) proceeds without depending on the
exact format string**, so it is not fully blocked — only the final format
constant is. Structure the implementation so the format is a single,
isolated, easily-changed value, exactly as `EPIC-2-FARM-001` did for FIN.

## Scope

### Allowed Scope

- A GIN generation function producing a unique value in an isolated,
  clearly-marked-as-placeholder format pending Project Manager decision.
- Collision-handling logic: retry on collision against the database's
  uniqueness constraint, mirroring `EPIC-2-FARM-001`'s approach.
- A GIN validation/format-check function.
- Unit tests for generation, collision retry, and format validation,
  written against the placeholder format so they are trivially updated
  once finalized.

### Out of Scope

- The Coffee Lot creation endpoint itself (`TRACE-002`).
- Any other Lot field (`farm_id`, `created_by`, `status`) — this task is
  the GIN utility only.
- Deciding the GIN format — that decision belongs to the Project Manager.
- QR payload encoding of the GIN — that is EPIC 4's concern; this task
  only guarantees the GIN value itself is generated and unique.

## Backend/Frontend/Database Responsibilities

Backend only. No frontend or database-schema work (the schema already
exists per `EPIC-0-DB-002`).

## Files/Modules Likely Affected

Indicative paths, matched against the layout already established in
`EPIC-0-BE-001` and used by `EPIC-1`/`EPIC-2`:

- `backend/app/core/identifiers.py` (or wherever `EPIC-2-FARM-001`'s FIN
  utility was placed — if that file already exists and is generically
  named, this task may extend it with a GIN function alongside the FIN
  function rather than creating a new file; confirm against the actual
  repository structure per
  `.agents/execution/01-agent-start-procedure.md` Step 4).
- `backend/tests/` — unit tests for the utility.

## Implementation Requirements

- The format's structure (prefix, segment lengths) is implemented as a
  single named constant/parameter, not repeated inline.
- Generation is deterministically collision-checked against the database
  (query for existing `gin_code` before returning, or rely on the
  database's uniqueness constraint plus a retry loop on insert failure —
  record which approach was chosen).
- No QR-related logic (HMAC signing, payload construction) is included —
  that is EPIC 4.

## Acceptance Criteria

- Calling the generation function returns a value matching the
  currently-placeholder format, clearly documented as pending Project
  Manager decision.
- Calling the generation function twice in immediate succession returns
  two different values.
- If a collision is simulated, the utility retries and returns a
  different, non-colliding value rather than raising an unhandled
  database error.
- The validation function correctly accepts a value matching the expected
  shape and rejects at least three distinct kinds of invalid input.
- The escalation report (per "Traceability Gap") has been produced and
  submitted, regardless of whether a Project Manager decision has been
  received yet.

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- Unit test: generation produces a correctly-shaped value.
- Unit test: two successive generations differ.
- Unit test: collision triggers a retry and ultimately succeeds with a
  different value.
- Unit test: validation function accepts valid shapes and rejects at
  least three distinct kinds of invalid input.

## Security Considerations

- The GIN is not a secret and is not treated as one — consistent with
  Design Document §5.3's distinction between identifiers and signed/secret
  QR payloads (which are EPIC 4's concern, not this task's).
- No farmer or farm data is referenced by this task — it operates purely
  on the identifier value.

## Expected Outputs / Deliverables

- A tested, reusable GIN generation and validation utility.
- A submitted escalation report for the GIN-format traceability gap.

## Definition of Done

- All items in "Acceptance Criteria" are true and independently
  verifiable.
- All items in "Testing Requirements" pass.
- Reviewed and approved by at least one other team member.
- Merged into `develop`.
- Requirements-traceability entry updated (Kidus), recording the GIN
  format as an open item against FR-TRACE-001/002.

## Change-Control Conditions

- The GIN-format gap is escalated per
  `.agents/execution/06-failure-and-escalation.md` as part of this task's
  normal execution, not as a failure of the task.
- If any other Lot-identifier requirement is found to conflict with the
  Design Document's narrowed V1.0 scope during implementation, escalate
  the same way rather than choosing.

## Git/Branch Expectations

- Branch: `feature/EPIC-3-TRACE-001-gin-foundation`, from `develop`, per
  `.agents/execution/05-git-and-commit-procedure.md`.
- Commit message pattern: `feat(traceability): add GIN generation and validation utility`.
- PR references Task ID `EPIC-3-TRACE-001` and explicitly states the GIN
  format is pending Project Manager decision, linking the escalation
  report.
- Merge target: `develop`.

## Expected Agent Report

Use the standard format from
`.agents/execution/04-human-review-and-approval.md`, plus:

1. The full escalation report for the GIN-format gap, submitted verbatim.
2. Confirmation that the format string is isolated to a single named
   constant/parameter.
3. Which collision-handling approach was implemented and why.
4. Test results.
