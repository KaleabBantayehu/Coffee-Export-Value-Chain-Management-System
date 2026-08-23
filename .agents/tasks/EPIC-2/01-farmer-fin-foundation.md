# Task Title

Farmer Data Foundation — FIN Generation & Validation Utility

## Task ID

EPIC-2-FARM-001

## Epic

EPIC 2 — Farmer & Polygon Registry

## Owner

Yedenekachew (Database Lead & Backend Developer), per Baseline §5 and
Implementation Specification EPIC 2 ownership.

## Status

**Partially blocked.** The uniqueness/collision-handling and validation
logic described below can proceed. The exact FIN numeric format cannot be
finalized without escalation — see "Blocking Ambiguity" below. This task's
own Definition of Done cannot be satisfied until that escalation is
resolved.

## Priority

Critical — `FARM-002` (Farmer registration API) cannot be completed
without a working FIN generator.

## Objective

Implement the FIN (Farmer Identification Number) generation and validation
utility that `FARM-002`'s registration endpoint will call, on top of the
`Farmer` table's `fin_code` column already created by `EPIC-0-DB-002`.

## Why This Task Exists

Design Document §4.2 states the system "generates a unique Farmer
Identification Number (FIN) on save, per FR-FARM-001; FIN uniqueness is
enforced at the database level." That database-level uniqueness constraint
already exists (`EPIC-0-DB-002`); nothing yet generates a FIN value to
insert. Building this as its own task, before the registration endpoint,
mirrors `EPIC-1-AUTH-001`'s pattern of building a shared utility before the
endpoint that will call it.

## Authoritative Sources

- SRS, Module 02 (FR-FARM), FR-FARM-001: *"Outputs: Unique Farmer
  Identification Number (FIN - Format: ETH-FAR-XXXX-XXXXXX). Validation
  Rules: FIN must be unique nationwide."*
- SRS, Use Case UC-01 ("Register Smallholder Farmer"), Main Success
  Scenario step 5: *"System generates FIN (ETH-FAR-XXX-XXXXXX), signs
  transaction cryptographically, and outputs digital registration
  confirmation."*
- Design Document §4.2 ("the system generates a unique Farmer
  Identification Number (FIN) on save, per FR-FARM-001; FIN uniqueness is
  enforced at the database level")
- Design Document §7.2 (`Farmer.fin_code` — unique, already created by
  `EPIC-0-DB-002`)

## Requirements Traceability

```text
SRS:
- FR-FARM-001 (Module 02) — states the FIN format as ETH-FAR-XXXX-XXXXXX.
- UC-01 — states the FIN format as ETH-FAR-XXX-XXXXXX.
  These two statements conflict on the digit count of the first numeric
  segment (four digits vs. three digits). Neither statement is more
  "official" than the other within the SRS document itself — FR-FARM-001
  is the functional-requirement specification for Module 02; UC-01 is a
  representative use-case walkthrough. Both are SRS-authoritative text.

Design Document:
- Section 4.2 confirms a FIN is generated and is unique, but does not
  restate or resolve a specific format — it defers entirely to
  "FR-FARM-001," which is itself one of the two conflicting sources.
- Section 7.2 fixes the column as `fin_code` (unique), with no format
  constraint (e.g., no fixed-length `CHAR`, no format-validating check
  constraint) specified at the schema level from EPIC-0-DB-002.

Implementation Specification:
- EPIC 2, Backend Tasks: "Farmer model, FIN generation..." — confirms FIN
  generation is EPIC-2 backend scope, without specifying format.

Minimum Project Plan:
- No FIN-format detail found; the Minimum Project Plan does not restate
  requirement-level detail already covered by the SRS/Design Document.

Baseline Scope Freeze:
- Section 3.1, "Farmer registration" (core scope item; format not
  specified here either).
```

## Dependencies

`EPIC-0-DB-002` (the `Farmer` table and its `fin_code` unique constraint).
No dependency on any EPIC-1 task — this is a pure data-generation utility,
not an endpoint.

## Preconditions

- Confirm the `Farmer` table exists with a `fin_code` column carrying a
  database-level uniqueness constraint (re-run `EPIC-0-DB-002`'s
  verification method if any doubt exists).

## Blocking Ambiguity — Escalate Before Finalizing the Format

Per this request's explicit instruction ("If the documents do not define
enough information to implement it safely: DO NOT guess. Record the
ambiguity explicitly and route it through the project's change-control
process"), this task must not resolve the FR-FARM-001-vs-UC-01 format
conflict on its own authority. Before writing the final digit-count logic,
raise this via `.agents/execution/06-failure-and-escalation.md`'s report
format:

```text
Issue: The SRS states two different FIN formats in two different
sections: FR-FARM-001 specifies ETH-FAR-XXXX-XXXXXX (4-digit segment);
UC-01 specifies ETH-FAR-XXX-XXXXXX (3-digit segment). Neither the Design
Document nor the Implementation Specification restates or resolves a
specific format.

Evidence: SRS Module 02, FR-FARM-001, "Outputs" line; SRS Use Case UC-01,
Main Success Scenario, step 5.

Affected documents: SRS (Level 2) — both conflicting statements are
within the same document, so the authority hierarchy in
.agents/execution/00-execution-overview.md does not resolve this; a
same-document internal inconsistency requires a decision, not a
precedence rule.

Why it blocks implementation: A FIN generator must produce a specific,
fixed-width numeric format to be useful (e.g., for zero-padding,
uniqueness-collision retry logic, and any future display/validation
regex). Implementing one guessed format risks generating FINs that must
later be regenerated or reformatted if the "wrong" one was chosen,
which would break any Farm/Lot records already created against them by
that point.

Possible options:
  1. Adopt FR-FARM-001's format (ETH-FAR-XXXX-XXXXXX) since it is the
     formal functional-requirement statement rather than an illustrative
     use-case walkthrough.
  2. Adopt UC-01's format (ETH-FAR-XXX-XXXXXX).
  3. Adopt a project-decided format independent of either literal SRS
     string, documented as a deliberate V1.0 simplification (similar to
     how Design Document §4.1 narrows FR-AUTH-001's MFA requirement).

Recommended action: Option 1 is a reasonable recommendation, since
functional requirements are typically the controlling specification and
use-case text is illustrative — but this is a recommendation for the
Project Manager, not a decision this task is authorized to make.
```

**This task's remaining work (below) proceeds without depending on the
exact digit count**, so it is not fully blocked — only the final format
constant is. Structure the implementation so the digit-count/format string
is a single, isolated, easily-changed value once the Project Manager
decides, rather than hard-coded in multiple places.

## Allowed Scope

- A FIN generation function producing a unique value in the general shape
  `ETH-FAR-<N digits>-<6 digits>` (with `<N digits>` left as an explicit,
  isolated, not-yet-finalized parameter pending escalation, per above).
- Collision-handling logic: if a generated FIN happens to collide with an
  existing one (checked against the database's uniqueness constraint), the
  utility retries with a new value rather than failing the whole
  registration outright.
- A FIN validation/format-check function, usable to confirm an existing
  value matches the (eventually finalized) expected shape.
- Unit tests for generation, collision retry, and format validation,
  written against the placeholder digit-count so they are trivially
  updated once the format is finalized.

## Out of Scope

- The Farmer registration endpoint itself (`FARM-002`).
- Any other Farmer field (name, national ID, gender, phone, cooperative) —
  this task is the FIN utility only.
- SMS OTP verification of the phone number (SRS FR-FARM-001's validation
  rule; not part of Design Document §4.2's narrowed V1.0 scope — see
  `00-epic-overview.md`'s Out-of-Scope list).
- Cryptographic per-transaction signing (SRS UC-01's "signs transaction
  cryptographically" step) — not part of Design Document §4.2's V1.0
  design; Design Document §5.3's HMAC signing is scoped to QR payloads
  (EPIC 4), not farmer registration.
- Deciding the FIN format — that decision belongs to the Project Manager,
  per the Blocking Ambiguity section above.

## Files/Directories Potentially Affected

Indicative paths, to be matched against the actual backend layout
established in `EPIC-0-BE-001` and used by `EPIC-1`:

- `backend/app/core/identifiers.py` (or equivalent existing "core"/"utils"
  location, matching wherever `EPIC-1-AUTH-001`'s hashing utility was
  placed) — the FIN generation/validation functions.
- `backend/tests/` — unit tests for the utility.

## Implementation Requirements

- The FIN's constant prefix `ETH-FAR-` is not in dispute between the two
  SRS sources and may be implemented immediately.
- The digit-count of the first numeric segment is implemented as a single
  named constant/parameter, not repeated inline, so resolving the
  escalation is a one-line change, not a re-implementation.
- The trailing 6-digit segment is consistent between both SRS sources
  (`XXXXXX`) and may be implemented immediately as a 6-digit, zero-padded
  numeric value.
- Generation must be deterministically collision-checked against the
  database (query for existing `fin_code` before returning, or rely on the
  database's uniqueness constraint plus a retry loop on insert failure —
  record which approach was chosen in the `Expected Agent Report`).
- No SMS OTP, cryptographic signing, or offline queuing logic is included
  (see Out of Scope).

## Acceptance Criteria

- Calling the generation function returns a value matching
  `ETH-FAR-<N digits>-<6 digits>` with the currently-placeholder digit
  count clearly documented as pending Project Manager decision.
- Calling the generation function twice in immediate succession returns
  two different values.
- If a collision is simulated (e.g., by pre-inserting a FIN the generator
  would produce, in a test), the utility retries and returns a different,
  non-colliding value rather than raising an unhandled database error.
- The validation function correctly accepts a value matching the expected
  shape and rejects a value that does not (wrong prefix, wrong segment
  lengths, non-numeric characters in the numeric segments).
- The escalation report (per "Blocking Ambiguity") has been produced and
  submitted, regardless of whether a Project Manager decision has been
  received yet — this task's own Definition of Done requires the
  escalation to exist, not necessarily to already be resolved.

## Testing Requirements

Per `.agents/rules/05-testing-rules.md` and
`.agents/execution/03-verification-and-testing.md`:

- Unit test: generation produces a correctly-shaped value.
- Unit test: two successive generations differ.
- Unit test: collision triggers a retry and ultimately succeeds with a
  different value.
- Unit test: validation function accepts valid shapes and rejects at least
  three distinct kinds of invalid input (wrong prefix, wrong length, non-
  numeric characters).

## Security Requirements

- The FIN is not a secret and is not treated as one — no hashing/encryption
  is applied to it (it is a public-style identifier, not a credential),
  consistent with Design Document §5.3's distinction between identifiers
  and signed/secret payloads.
- No farmer personal data (name, national ID) is referenced by this task —
  it operates purely on the identifier value.

## Error Handling Requirements

- A collision-retry loop has a bounded maximum number of attempts and
  raises a clear, structured error if exhausted (rather than looping
  indefinitely) — this should be effectively unreachable in practice given
  the identifier space, but must not be able to hang.

## Documentation Requirements

- Kidus records the FIN-format escalation in the project's
  requirements-traceability documentation as an open item against
  FR-FARM-001, referencing this task's Blocking Ambiguity section, so it
  is visible outside this task file too.

## Commit Guidance

- Branch: `feature/EPIC-2-FARM-001-fin-foundation`, from `develop`, per
  `.agents/execution/05-git-and-commit-procedure.md`.
- Commit message pattern: `feat(farmer): add FIN generation and validation utility`.
- PR references Task ID `EPIC-2-FARM-001` and explicitly states the FIN
  format is pending Project Manager decision, linking the escalation
  report.
- Merge target: `develop`.

## Verification Requirements

Per `.agents/execution/03-verification-and-testing.md`: self-review
against this task's own Acceptance Criteria before requesting human
review; confirm the digit-count constant is isolated to one location
before requesting review, so the reviewer can independently verify the
"one-line change" claim.

## Escalation / Change-Control Conditions

- The FIN-format conflict (above) is escalated per
  `.agents/execution/06-failure-and-escalation.md` as part of this task's
  normal execution, not as a failure of the task.
- If, during implementation, any other Farmer-identifier requirement in
  the SRS is found to conflict with the Design Document's narrowed V1.0
  scope, escalate the same way rather than choosing.

## Expected Agent Report

Use the standard format from
`.agents/execution/04-human-review-and-approval.md`, plus:

1. The full escalation report for the FIN-format conflict, submitted
   verbatim.
2. Confirmation that the digit-count is isolated to a single named
   constant/parameter.
3. Which collision-handling approach was implemented (pre-check query vs.
   insert-failure retry) and why.
4. Test results.
