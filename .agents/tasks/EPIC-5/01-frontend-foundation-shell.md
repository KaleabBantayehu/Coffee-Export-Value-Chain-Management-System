# EPIC-5-FE-001 - Frontend Foundation, Application Shell, and Shared Integration Prerequisites

## Objective

Establish the shared React/JavaScript application shell and integration conventions required by the EPIC-5 screens, using the existing Vite project without scaffolding or technology expansion.

## Scope

Inspect and preserve the current frontend structure; establish shared page/layout/navigation mounting points, API base configuration pattern, reusable request/error/loading/form primitives only where needed by later screens, and route/component integration seams. Register no new backend contract.

## Out of Scope

New framework, router/state/styling library, TypeScript, backend/database work, auth redesign, screen-specific business workflows, offline support, or replacing existing upstream components.

## Preconditions

Existing React/Vite scaffold is present; EPIC-0 is verified; EPIC-1 frontend/auth implementation shape is inspected. Task-file existence alone is insufficient.

## Dependencies

EPIC-0 frontend scaffold; EPIC-1-AUTH-006/007 actual implementation status. Missing scaffold or unresolved auth integration is a blocker.

## Inputs

Current `frontend/package.json`, `src/`, existing EPIC-1 through EPIC-4 frontend contracts/components, approved design/wireframes, and API base configuration.

## Expected Outputs

A documented shared shell/integration structure that later tasks can extend without duplicate utilities, plus any narrowly scoped shared components required by approved screens.

## Relevant Files / Modules

`frontend/package.json`, `frontend/src/main.jsx`, `frontend/src/App.jsx`, existing `frontend/src/` components/pages/api/config locations. Confirm paths before editing during execution.

## Backend Responsibilities

None. Consume existing APIs only.

## Frontend Responsibilities

Create the shared mounting/layout/integration seams, preserve React/JavaScript, and expose stable extension points for auth, pages, forms, map, trace, and QR screens.

## Database Responsibilities

None.

## API Requirements

No new endpoint. Preserve the configured backend base URL and existing API request conventions. If no approved configuration convention exists, record **Traceability gap - requires review** rather than inventing an API contract.

## UI / UX Requirements

Use the approved Figma/design conventions where available; provide coherent navigation and responsive structure without adding unapproved screens or explanatory product copy.

## Security Requirements

Do not place secrets in source; do not create token handling separate from EPIC-1; do not make public routes protected or protected routes public by accident.

## Validation / Error Handling

Shared request/error/loading behavior must preserve structured backend errors and avoid rendering raw stack traces. Validate configuration presence without exposing values.

## Acceptance Criteria

- Existing React/Vite app is reused and builds without a new framework or scaffold.
- Shared shell seams exist for the documented screens and do not duplicate upstream components.
- API base/configuration behavior is traceable to an existing convention or explicitly escalated.
- No secret, backend, database, or upstream EPIC file is modified.

## Testing Requirements

Run the existing frontend `build` and `lint` scripts; manually inspect the shell at desktop/mobile-sized viewports; record any absence of frontend test tooling as a project gap, not a reason to add a framework.

## Traceability

Implementation Specification EPIC-5 Frontend Integration and screen list; Design Document Sections 3, 8, 9.1-9.4, 16; Minimum Project Plan Sections 7.1-7.2 Week 4/M5/M6; Baseline Sections 2-4; EPIC-0 scaffold and EPIC-1 frontend contracts. Missing shell/router/API configuration detail is **Traceability gap - requires review**.

## Ownership, Git, and Change Control

Primary: Biniyam. Support: Abel for reusable components. Verification: Ephratha plus independent reviewer; Kidus updates traceability. Branch `feature/EPIC-5-FE-001-frontend-foundation`; conventional commit `feat(frontend): establish integration shell`; PR to `develop`. Any new dependency or architecture change requires PM change control.

## Blockers / Stop Conditions

Stop if the scaffold is absent, EPIC-1 frontend shape is not implemented/verified, or a router/state/API convention must be invented. Do not modify upstream tasks or source documents.
