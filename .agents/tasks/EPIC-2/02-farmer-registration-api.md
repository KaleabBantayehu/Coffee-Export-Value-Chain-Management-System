# Task Title

Farmer Registration & Retrieval API

## Task ID

EPIC-2-FARM-002

## Epic

EPIC 2 — Farmer & Polygon Registry

## Owner

Yedenekachew (Database Lead & Backend Developer)

## Status

Not started.

## Priority

Critical — the primary acceptance path's "Register Farmer" step; also the
precondition for `FARM-003` (a Farm cannot exist without a real Farmer).

## Objective

Implement `POST /api/v1/farmers`, `GET /api/v1/farmers/{id}`,
`PUT /api/v1/farmers/{id}`, and `GET /api/v1/farmers?search=`, using the
FIN utility from `FARM-001` and the authentication/RBAC mechanism from
`EPIC-1-AUTH-003`/`EPIC-1-AUTH-004`.

## Why This Task Exists

Baseline §4 lists "Register Farmer" as the second step of the primary
acceptance workflow. Design Document §8 fully specifies this API's
contract; this task implements it.

## Authoritative Sources

- Design Document §4.2 ("A Field/Registry Agent (web role) enters: full
  name, national ID, gender, phone number, and an optional cooperative
  reference... A lightweight Cooperative lookup table is included... purely
  so a farmer record can reference the cooperative it is affiliated with")
- Design Document §7.2 (`Farmer` entity: `farmer_id`, `fin_code` (unique),
  `full_name`, `national_id` (unique), `gender`, `phone_number`,
  `cooperative_id` (FK, nullable), `created_at` — already created by
  `EPIC-0-DB-002`)
- Design Document §8 (API Design — Farmers table):
  - `POST /api/v1/farmers` — "Register a farmer, generate FIN" — Auth:
    "JWT + Field/Registry Agent or Admin" — "Validates required fields;
    rejects duplicate national_id."
  - `GET /api/v1/farmers/{id}` — "Retrieve a farmer profile" — Auth: "JWT"
    — "Returns farmer + linked farms summary."
  - `PUT /api/v1/farmers/{id}` — "Update a farmer profile" — Auth: "JWT +
    Field/Registry Agent or Admin" — "Writes an AuditLog entry (old/new
    values)."
  - `GET /api/v1/farmers?search=` — "List/search farmers" — Auth: "JWT" —
    "Search by FIN, name, or cooperative."
- Design Document §10 (Security Design — AuditLog covers Farmer record
  mutations)
- Design Document §13, Sequence 2 (Register Farmer and Farm)

## Requirements Traceability

```text
SRS:
- FR-FARM-001 (Module 02) — Farmer Master Profiling. The SRS's full input
  list ("Full Name, National ID / Kebele ID, Gender, Household size,
  Primary Cooperative ID, Phone Number, Bank/Telebirr Account Number")
  and its SMS-OTP validation rule are narrowed by Design Document §4.2 to
  exactly: full name, national ID, gender, phone number, optional
  cooperative reference. This task implements the Design Document's
  narrowed field list, not the SRS's fuller enterprise list — the omitted
  fields (household size, bank/Telebirr account, SMS OTP) are recorded as
  out of scope in 00-epic-overview.md, not silently dropped without
  record.

Design Document:
- Section 4.2 (narrowed field list; Cooperative lookup)
- Section 7.2 (Farmer entity, from EPIC-0-DB-002)
- Section 8 (Farmers API table, quoted above)
- Section 10 (AuditLog on Farmer mutations)
- Section 13, Sequence 2

Implementation Specification:
- EPIC 2, Backend Tasks: "Farmer model, FIN generation, registration,
  retrieval, validation"

Minimum Project Plan:
- Week 2 Key Activities: "begin Authentication & RBAC and Farmer &
  Polygon Registry (backend + frontend)"; Section 7.3 Task Dependencies
  confirms Farmer & Polygon Registry API follows Authentication & RBAC API.

Baseline Scope Freeze:
- Section 3.1, "Farmer registration"
- Section 4, Critical Workflow — "Register Farmer" (second step)
```

## Dependencies

`EPIC-2-FARM-001` (FIN generation utility — required by `POST /farmers`)
and `EPIC-1-AUTH-003`/`EPIC-1-AUTH-004` (authentication dependency and RBAC
authorization mechanism — this task does not build a new one).

## Preconditions

- `FARM-001` merged, with its FIN utility's digit-count either finalized
  or still pending — if still pending, this task proceeds using the same
  isolated placeholder constant `FARM-001` established, and its own report
  restates that the FIN format is not yet finalized.
- `EPIC-1-AUTH-003`/`EPIC-1-AUTH-004` merged and usable without
  modification.
- The `Farmer` and `Cooperative` tables exist per `EPIC-0-DB-002`.

## Allowed Scope

- The four Farmer endpoints listed in "Objective," using `FARM-001`'s FIN
  utility and `EPIC-1`'s authentication/RBAC dependencies exactly as they
  exist.
- Request/response schemas for these four endpoints.
- Server-side validation of required fields and of `national_id`
  uniqueness (per Design Document §8's "rejects duplicate national_id").
- An `AuditLog` write on `PUT /api/v1/farmers/{id}`, recording old/new
  values, reusing the same pattern `EPIC-1-AUTH-005` already established
  for `User` role changes (same `AuditLog` table, same old/new-value
  convention) rather than inventing a new audit pattern.

## Out of Scope

- Farm registration or polygon capture (`FARM-003`).
- Building a new authorization check instead of reusing
  `EPIC-1-AUTH-004`'s mechanism.
- Household size, bank/Telebirr account number, SMS OTP verification,
  National ID photo capture, or cryptographic per-transaction signing (see
  `00-epic-overview.md`'s Out-of-Scope list).
- Full Cooperative & Processing Management (SRS Module 04) — only a
  foreign-key reference to the existing lightweight `Cooperative` lookup
  table is used; no Cooperative CRUD is built here.
- Deleting a Farmer record — Design Document §8 defines no `DELETE`
  endpoint for Farmers; none is added.

## Files/Directories Potentially Affected

Indicative paths, matched against the layout already established by
`EPIC-0-BE-001` and used by `EPIC-1`:

- `backend/app/api/v1/farmers.py` (or equivalent, matching the existing
  router-per-domain pattern used for `backend/app/api/v1/auth.py` and
  `backend/app/api/v1/users.py`).
- `backend/app/schemas/farmer.py` (or equivalent).
- `backend/app/services/farmer_service.py` (or equivalent) — validation,
  uniqueness checks, FIN generation call, AuditLog write.
- `backend/tests/` — tests for all four endpoints.

## Implementation Requirements

- `POST /api/v1/farmers` requires `Field/Registry Agent or Admin`, per
  Design Document §8, enforced via `EPIC-1-AUTH-004`'s mechanism — not a
  bespoke check.
- Request body accepts exactly: full name, national ID, gender, phone
  number, optional cooperative reference — no more, no fewer fields.
- `national_id` uniqueness is validated before insert, returning a
  structured `400`/`409` on duplicate, not a raw database exception.
- On success, the endpoint calls `FARM-001`'s FIN generation utility,
  persists the new `Farmer` row, and returns the farmer profile including
  the generated FIN.
- `GET /api/v1/farmers/{id}` requires only authentication (any of the four
  roles), per Design Document §8, and returns "farmer + linked farms
  summary" — since no Farm exists yet at this point in the epic
  (`FARM-003` has not run), the "linked farms" portion of the response may
  correctly be an empty list; this is not a defect, it reflects that no
  Farm has been created yet.
- `PUT /api/v1/farmers/{id}` requires `Field/Registry Agent or Admin` and
  writes an `AuditLog` entry with old/new values, matching
  `EPIC-1-AUTH-005`'s established audit pattern.
- `GET /api/v1/farmers?search=` requires only authentication and searches
  by FIN, name, or cooperative, per Design Document §8.

## Acceptance Criteria

- An authenticated Field/Registry Agent can register a farmer via
  `POST /api/v1/farmers` with valid data and receives `200`/`201` with the
  generated FIN in the response.
- The same request from an authenticated user whose role is not
  Field/Registry Agent or Admin (e.g., Verifier) is rejected with `403`.
- An unauthenticated request is rejected with `401`.
- Registering a farmer with a `national_id` that already exists is
  rejected with a structured `400`/`409`, not a raw database error.
- `GET /api/v1/farmers/{id}` for an existing farmer returns `200` with the
  correct profile.
- `GET /api/v1/farmers/{id}` for a non-existent ID returns `404`.
- `PUT /api/v1/farmers/{id}` by an authorized role successfully updates the
  record and writes a correctly-populated `AuditLog` row.
- `GET /api/v1/farmers?search=` correctly returns matching results when
  searching by FIN, by name, and by cooperative, tested separately.
- Submitting a request missing a required field is rejected with a
  structured `400`.

## Testing Requirements

Per `.agents/rules/05-testing-rules.md`:

- Test: successful registration returns the expected shape including a
  generated FIN.
- Test: role-based rejection (non-Field/Registry Agent, non-Admin) on
  `POST`/`PUT` returns `403`; unauthenticated returns `401`.
- Test: duplicate `national_id` is rejected cleanly.
- Test: missing required field is rejected cleanly.
- Test: retrieval by ID succeeds for an existing record and returns `404`
  for a missing one.
- Test: update writes a correct `AuditLog` entry.
- Test: search by each of the three supported criteria (FIN, name,
  cooperative) returns correct results.
- Regression: `EPIC-1`'s existing auth/RBAC test suite still passes
  unchanged after this task's routes are added.

## Security Requirements

- `national_id` and `phone_number` are not logged in plaintext in
  application logs beyond what is operationally necessary; no farmer PII
  appears in error messages returned to unauthorized callers.
- RBAC enforcement is via `EPIC-1-AUTH-004`'s mechanism only.

## Error Handling Requirements

- Missing required field -> structured `400`.
- Duplicate `national_id` -> structured `400`/`409`.
- Non-existent farmer ID on retrieval/update -> structured `404`.
- Unauthorized role -> `403`; unauthenticated -> `401`.

## Documentation Requirements

- Kidus updates the requirements-traceability entry for FR-FARM-001 to
  "registration/retrieval implemented per Design Document §4.2's narrowed
  field list; household size, bank/Telebirr, SMS OTP, ID photo, and
  cryptographic signing not implemented in V1.0."

## Commit Guidance

- Branch: `feature/EPIC-2-FARM-002-farmer-api`, from `develop`.
- Commit message pattern: `feat(farmer): implement farmer registration and retrieval API`.
- PR references Task ID `EPIC-2-FARM-002`.
- Merge target: `develop`.

## Verification Requirements

Self-review per `.agents/execution/03-verification-and-testing.md`;
confirm no field outside the Design Document §4.2 list was added to the
request schema.

## Escalation / Change-Control Conditions

- If `FARM-001`'s FIN format is still unresolved when this task begins,
  proceed using the placeholder constant and restate the open escalation
  in this task's own report — do not block this entire task on that
  single unresolved digit count, since the rest of the Farmer API does not
  depend on it.
- Any other conflict discovered follows
  `.agents/execution/06-failure-and-escalation.md`.

## Expected Agent Report

Standard format from `.agents/execution/04-human-review-and-approval.md`,
plus:

1. Confirmation that the request/response schema matches Design Document
   §4.2's field list exactly (no extra, no missing fields).
2. Confirmation of how `national_id` uniqueness is enforced (application
   check, database constraint, or both).
3. Whether `FARM-001`'s FIN format was finalized or still pending at the
   time this task was executed.
4. Test results.
