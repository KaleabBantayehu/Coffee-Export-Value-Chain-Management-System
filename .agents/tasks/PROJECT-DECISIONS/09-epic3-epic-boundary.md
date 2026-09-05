# PD-009 — EPIC 3 / EPIC 4 Boundary Acknowledgement

## Decision

Traceability and Dynamic QR are separate implementation epics in the CEVCMS
V1.0 backlog.

## Context

The Minimum Project Plan groups "Traceability & QR Engine" as a combined
higher-level module, while the implementation backlog separates EPIC 3 —
Traceability Engine and EPIC 4 — Dynamic QR Engine. This record resolves the
backlog-management interpretation of that difference.

## Approved implementation boundary

- **EPIC 3 — Traceability Engine:** Coffee Lot GIN generation, Farm-to-Lot
  relationship, append-only Traceability Events, traceability history, and the
  Farmer → Farm → Polygon → Coffee Lot → Traceability Event chain.
- **EPIC 4 — Dynamic QR Engine:** QR payload contract, QR generation, HMAC
  signing, QR record storage, verification, invalid-QR handling, and public
  verification.

The Minimum Project Plan's combined wording remains a higher-level module
grouping; it does not require EPIC 3 and EPIC 4 to be delivered as one backlog
epic.

## Dependency and scope guard

EPIC 4 remains dependent on successful completion and verification of EPIC 3's
traceability chain. This acknowledgement authorizes no functionality beyond
the separately approved EPIC 4 scope.

## Status

**RESOLVED / ACKNOWLEDGED BY PROJECT MANAGER**

## Approval authority

Project Manager Kaleab
