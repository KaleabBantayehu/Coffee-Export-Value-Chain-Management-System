# PROJECT-DECISION-07 — EPIC-2 Verification Evidence Location

**Status:** APPROVED

## Decision

The canonical locations for EPIC-2 verification artifacts are approved as:

```text
docs/testing/postman/EPIC-2.postman_collection.json
docs/testing/evidence/EPIC-2-verification.md
```

## Rationale

This structure:

* Matches the existing project documentation structure.
* Separates executable API verification artifacts from human-readable verification evidence.
* Provides a deterministic canonical location for EPIC-2 verification outputs.
* Allows FARM-007 to create and maintain sanitized verification artifacts without inventing additional documentation locations.

## Scope

The approved locations may be used for:

* Sanitized Postman collections.
* API verification requests and workflows.
* Manual UI walkthrough evidence.
* Automated test summaries.
* Database/PostGIS verification summaries.
* EPIC-level verification and traceability evidence.

Secrets, credentials, tokens, private connection strings, and other sensitive values must not be committed to these artifacts.

## Effect on FARM-007

This decision resolves the evidence-location blocker identified under PD-007.

FARM-007 may now:

1. Create the EPIC-2 Postman collection.
2. Execute the collection against the project environment.
3. Record sanitized results.
4. Complete the required UI walkthrough.
5. Record database/PostGIS verification evidence.
6. Update the EPIC-2 verification record in the approved evidence location.
7. Perform final EPIC-2 verification and sign-off checks.

**Decision authority:** Project Manager
**Decision status:** Approved
