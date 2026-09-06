# PROJECT-DECISIONS - CEVCMS V1.0 Governance Decision Package

## Purpose

This package records project-level decisions required before assigning the full EPIC-0 through EPIC-6 implementation chain. It is a governance artifact only. It does not change any existing task, rule, execution procedure, source document, or application code.

## Decision inventory

| ID     | File                               | Decision                                                               | Current status |
| ------ | ---------------------------------- | ---------------------------------------------------------------------- | -------------- |
| PD-001 | `01-authority-hierarchy.md`        | Authority hierarchy and conflict resolution                            | UNRESOLVED     |
| PD-002 | `02-fin-format.md`                 | FIN format                                                             | UNRESOLVED     |
| PD-003 | `PD-003 final decision.md`         | GIN format                                                             | APPROVED       |
| PD-004 | `04-qr-contract.md`                | QR payload, identifier, storage, signing, and public response contract | APPROVED       |
| PD-005 | `05-frontend-ownership.md`         | Feature frontend versus EPIC-5 integration ownership                   | APPROVED       |
| PD-006 | `06-qa-sequencing.md`              | EPIC-6 QA-005/QA-006 sequence                                          | UNRESOLVED     |
| PD-007 | `07-evidence-and-documentation.md` | Locations for QA/evidence/documentation artifacts                      | UNRESOLVED     |
| PD-008 | `08-epic-readiness-gate.md`        | Gate for assigning an EPIC to implementation                           | UNRESOLVED     |
| PD-009 | `09-epic3-epic-boundary.md`        | EPIC 3 Traceability versus EPIC 4 Dynamic QR backlog boundary          | RESOLVED       |
| PD-010 | `10-epic3-trace007-evidence-limitation.md` | EPIC-3 TRACE-007 verification-evidence limitation | CLOSED BY SUPPLEMENTAL VERIFICATION |

## Decision dependency order

```text
PD-001 authority hierarchy
       |
       +--> PD-002 FIN format
       +--> PD-003 GIN format
       +--> PD-004 QR contract
       +--> PD-005 frontend ownership
       +--> PD-006 QA sequencing
       +--> PD-007 evidence/documentation locations
                    |
                    v
             PD-008 EPIC readiness gate
                    |
                    v
             developer assignment

PD-009 records the approved EPIC-3/EPIC-4 backlog boundary and is required
before EPIC 3 can be signed off for handoff to EPIC 4.
```

PD-001 should be approved first because it governs how all later conflicts are interpreted. PD-002 and PD-003 should be resolved before identifier-dependent implementation. PD-004 must be resolved before QR implementation or QR-specific assertions. PD-005 and PD-006 must be resolved before assigning overlapping frontend or QA work. PD-007 should be approved before QA evidence is produced. PD-008 is the final gate that consumes the preceding decisions and verified dependencies.

## Decisions that block implementation

- PD-001 blocks authoritative conflict resolution across the project.
- PD-002 blocks final FIN generation/validation and stable Farmer fixtures.
- PD-003 blocks final GIN generation/validation and stable Lot/QR fixtures.
- PD-004 blocks EPIC-4 QR implementation and EPIC-5 QR integration.
- PD-005 is approved for EPIC-5 shared-shell integration; changes outside
  its recorded ownership scope still require Project Manager approval.
- PD-006 blocks final QA ordering and can create a circular dependency.
- PD-007 blocks consistent evidence/report storage, though QA planning can proceed.
- PD-008 blocks formal declaration that downstream EPICs are ready for assignment.

## Decisions that can be deferred

Evidence locations (PD-007) can be deferred only for planning; they should be decided before evidence collection. Some UI composition details, test fixture values, and implementation-level choices can be decided during approved tasks if they do not alter a contract or scope. No FIN/GIN/QR contract detail may be deferred past the task that consumes it.

## Recommended Project Manager approval sequence

1. Approve the governing authority hierarchy.
2. Resolve FIN and GIN formats together, preserving V1.0 identifiers.
3. Approve the complete QR contract and privacy boundary.
4. Decide feature-frontend versus EPIC-5 ownership and remove duplicate assignment.
5. Approve the QA sequence and remove the QA-005/QA-006 circularity.
6. Approve repository locations for evidence and documentation.
7. Approve the EPIC readiness gate and only then assign implementation work.

## Cross-EPIC impact summary

PD-001 affects every conflict. PD-002 affects EPIC-2, EPIC-3, EPIC-4, and QA fixtures. PD-003 affects EPIC-3, EPIC-4, EPIC-5, and QA fixtures. PD-004 affects EPIC-4, EPIC-5, and EPIC-6. PD-005 affects EPIC-1 through EPIC-5 frontend assignments. PD-006 affects EPIC-5/EPIC-6 handoff. PD-007 affects EPIC-6 and milestone reporting. PD-008 controls assignment readiness for all epics.

## Package safety

Only this new directory may be created. Existing EPIC-0 through EPIC-6 files, rules, execution procedures, docs, backend, and frontend remain outside this package's scope. No decision is final until explicitly approved by the Project Manager (Kaleab) and recorded in the appropriate project decision record.
