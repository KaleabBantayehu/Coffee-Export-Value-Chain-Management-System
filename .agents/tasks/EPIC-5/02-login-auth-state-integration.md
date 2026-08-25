# EPIC-5-FE-002 - Login UI and Authentication-State Integration

## Objective

Integrate the documented login UI with EPIC-1's login/me/logout contract and JWT auth state using the existing React application.

## Scope

Render username/email and password inputs, submit the documented login request, handle success/failure, update the established auth state from the documented response, retrieve/use the documented current-user state where required, and route the user to the approved protected entry point.

## Out of Scope

Backend auth changes, new token/session systems, MFA, refresh tokens, OAuth/OIDC, password reset, new roles, or inventing request/response fields.

## Preconditions

FE-001 complete; EPIC-1-AUTH-002/003/006 actual login and auth-state contracts are implemented, tested, verified, and approved.

## Dependencies

FE-001; EPIC-1-AUTH-002, AUTH-003, AUTH-006. If the actual response differs from the task contract, stop and escalate.

## Inputs

EPIC-1 API response/request shape, auth-state interface, role model, approved login design, and synthetic credentials.

## Expected Outputs

Working login page integrated with existing auth state and documented post-login navigation, with controlled validation and error states.

## Relevant Files / Modules

Existing `frontend/src` auth/page/API/route files identified in FE-001 and EPIC-1-AUTH-006. No backend files.

## Backend Responsibilities

None; consume `POST /api/v1/auth/login` and any documented `/auth/me` behavior as-is.

## Frontend Responsibilities

Form, submission, auth-state update, loading/error state, safe redirect, and no duplicate token logic.

## Database Responsibilities

None.

## API Requirements

Use exactly the inspected EPIC-1 login/me contract. Do not send client-derived role/user identity or invent status handling.

## UI / UX Requirements

Provide clear required-field and generic authentication-error feedback; preserve accessible form behavior and approved login screen layout.

## Security Requirements

Never log/render password or JWT; use the existing EPIC-1 token handling; do not store secrets in source; do not reveal whether a username or password alone was incorrect.

## Validation / Error Handling

Validate required fields client-side while relying on backend validation; display structured 4xx/network errors without stack traces; prevent duplicate submits while loading.

## Acceptance Criteria

- Login sends the documented request fields and handles the documented success response.
- Successful login updates the existing auth state and reaches the approved protected entry point.
- Invalid credentials and validation/network failures produce controlled feedback.
- No password, token, or new auth mechanism is exposed or invented.

## Testing Requirements

Test/manual evidence for valid login, invalid/missing input, failed authentication, loading state, and auth-state update; run frontend build/lint and EPIC-1 regression tests where available.

## Traceability

SRS FR-AUTH-001/002 narrowed by V1.0; Design Document Sections 4.1, 8, 9.1, 10, 13; Implementation Specification EPIC-1 frontend tasks and EPIC-5 Login screen; Minimum Project Plan Section 7.1 login/navigation WBS; Baseline Sections 2 and 4; EPIC-1-AUTH-002/003/006.

## Ownership, Git, and Change Control

Primary: Biniyam; Abel support. Verification: Ephratha and independent reviewer; Kidus documentation. Branch `feature/EPIC-5-FE-002-login-auth-state`; commit `feat(frontend): integrate login authentication state`; PR to `develop`. Any token persistence or API deviation not established by EPIC-1 is escalated.

## Blockers / Stop Conditions

Stop if login/me response, token handling, or post-login route is not implemented and approved upstream. Do not create a substitute auth flow.
