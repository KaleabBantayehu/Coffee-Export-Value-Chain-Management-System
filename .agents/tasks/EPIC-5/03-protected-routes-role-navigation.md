# EPIC-5-FE-003 - Protected Routes, Role-Aware Navigation, Logout, and Session Handling

## Objective

Connect the authenticated application routes and navigation to EPIC-1's protected-route and four-role semantics.

## Scope

Gate protected screens on existing auth state, render role-appropriate navigation for Admin, ECTA Officer, Field/Registry Agent, and Verifier, provide documented logout behavior, clear auth state on logout/invalid session, and handle unauthorized responses consistently.

## Out of Scope

Backend RBAC changes, new permissions/roles, frontend-only security claims that contradict backend permissions, refresh tokens, session revocation infrastructure, MFA, or redesign of EPIC-1 auth.

## Preconditions

FE-001 and FE-002 complete; EPIC-1-AUTH-004/006/007/008 are implemented, tested, verified, and approved; actual role/navigation contract inspected.

## Dependencies

FE-002; EPIC-1-AUTH-004, AUTH-006, AUTH-007, AUTH-008.

## Inputs

Existing auth context/state, route mechanism, frozen role model, endpoint permissions, and approved screen list.

## Expected Outputs

Protected route behavior, role-aware navigation, logout/session cleanup, and controlled 401/403 handling.

## Relevant Files / Modules

Existing route/navigation/auth files under `frontend/src` identified in FE-001/002. No backend or prior task edits.

## Backend Responsibilities

None; consume EPIC-1 behavior.

## Frontend Responsibilities

Route guards, menu visibility/action availability, logout, auth cleanup, and unauthorized error presentation.

## Database Responsibilities

None.

## API Requirements

Use only documented `/auth/me` and `/auth/logout` behavior if required. Do not invent a client-side permission endpoint.

## UI / UX Requirements

Users see only role-appropriate actions; unauthenticated users are redirected to login; unauthorized actions have a clear controlled state rather than a blank screen.

## Security Requirements

Protected route checks are not the sole security boundary; backend enforcement remains authoritative. Logout removes the existing client auth state. Public QR verification remains accessible without login.

## Validation / Error Handling

Handle missing/expired/invalid JWT and 401/403 responses without loops, stale protected data, or raw server detail.

## Acceptance Criteria

- Unauthenticated protected-route access reaches login.
- Navigation reflects exactly the four frozen roles and documented screen permissions.
- Logout clears auth state and makes protected screens inaccessible.
- 401/403 responses are handled clearly and do not expose server internals.
- Public verification is not accidentally gated by protected routing.

## Testing Requirements

Test/manual evidence for each role's navigation, unauthenticated redirect, logout cleanup, 401, 403, and public-route access; run build/lint and EPIC-1 regression tests.

## Traceability

Design Document Sections 4.1, 8, 9.1-9.4, 10, 13; Implementation Specification EPIC-1 frontend tasks, EPIC-5 screen list and roles; Minimum Project Plan Section 7.1; Baseline Sections 3-5; EPIC-1-AUTH-004/006/007/008. The Plan's conflicting “Exporter” test role remains excluded under the frozen four-role model.

## Ownership, Git, and Change Control

Primary: Biniyam; Abel support. Verification: Ephratha; Kidus records evidence. Branch `feature/EPIC-5-FE-003-protected-routes`; commit `feat(frontend): add protected routes and role navigation`; PR to `develop`. Any role/permission change requires PM decision.

## Blockers / Stop Conditions

Stop if role semantics or auth state are unavailable or conflict with the frozen four-role model. Do not add a role or second authorization mechanism.
