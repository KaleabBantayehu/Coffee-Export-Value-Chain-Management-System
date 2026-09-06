# EPIC-5 FE-003 Protected Routes, Role Navigation, and Session Reconciliation

**Task:** EPIC-5-FE-003 — Protected Routes, Role-Aware Navigation, Logout,
and Session Handling

**Status:** COMPLETED

## Ownership resolution

[PD-005](../../../.agents/tasks/PROJECT-DECISIONS/05-frontend-ownership.md)
is approved. Biniyam is the EPIC-5 frontend lead and Abel provides support.
`AUTH-007` remains historically complete; FE-003 owns the current shared
frontend shell's protected-route, role-navigation, logout/session-cleanup,
and invalid-session integration behavior. Backend authentication and RBAC
remain authoritative.

## Defect found and corrected

Protected API clients previously converted every non-success response into a
page-level error. A protected API `401` therefore left the in-memory
`accessToken` and `role` intact, allowing stale protected UI to remain visible.

The correction reuses the existing architecture:

- `AuthContext` registers one session-expiry callback that clears `accessToken`
  and `role`, then uses the existing `navigate('/login')` helper.
- Farmer, Farm, and Lot helpers (which include trace/event and QR-generation
  requests) use one shared protected-request error helper.
- A `401` invokes the registered callback and returns the bounded message
  `Your session has expired. Please sign in again.`
- A `403` does not expire the session and returns the bounded authorization
  message `You are not authorized to perform this action.`
- Explicit logout remains unchanged: it clears state in its `finally` block.
- The public `api/verification.js` client is not changed and remains
  unauthenticated.

No persistence, refresh token, second auth context, router, or backend change
was introduced.

## Acceptance matrix

| FE-003 criterion | Status | Evidence |
| --- | --- | --- |
| Unauthenticated protected access reaches login | SOURCE-SUPPORTED | `App.jsx` redirects any unauthenticated non-login, non-`/verify/...` path; prior synthetic trace evidence recorded this behavior. Browser recheck remains listed below. |
| Navigation reflects the four frozen roles | SOURCE-SUPPORTED | `Navigation.jsx` maps Admin, ECTA Officer, Field/Registry Agent, and Verifier explicitly; no additional role is introduced. |
| Logout clears auth state and protected screens become inaccessible | SOURCE-SUPPORTED | `AuthContext.jsx` clears state in `signOut`'s `finally`; `App.jsx`/`ProtectedRoute.jsx` gate protected UI. Browser verification remains required. |
| Invalid/expired `401` removes stale protected access | SOURCE-SUPPORTED | `api/authenticatedRequest.js` calls the AuthContext-registered expiry handler; it clears state and navigates to `/login`. Browser verification remains required. |
| `403` remains controlled and distinct from expiry | SOURCE-SUPPORTED | The shared protected helper returns a bounded authorization error without invoking session expiry. Browser verification remains required. |
| Public verification is not protected | SOURCE-SUPPORTED | `App.jsx` handles `/verify/...` before protected routes; `api/verification.js` remains unchanged and has no Authorization header. Browser recheck remains required. |
| Frontend lint | PASS | `npm.cmd run lint` completed successfully. |
| Frontend production build | PASS | `npm.cmd run build` completed successfully. |
| Focused EPIC-1 backend auth/RBAC regression | PASS | `tests.test_auth_login`, `tests.test_auth_session`, and `tests.test_rbac`: 15 tests completed successfully. |
| Whitespace check | PASS | `git diff --check` completed with no whitespace errors. |

## Files changed

- `frontend/src/context/AuthContext.jsx`
- `frontend/src/api/sessionExpiry.js`
- `frontend/src/api/authenticatedRequest.js`
- `frontend/src/api/farmers.js`
- `frontend/src/api/farms.js`
- `frontend/src/api/lots.js`

## Browser verification scope

Codex did not run browser automation. Copilot completed the required
synthetic-account browser checks, recorded below:

1. Admin navigation.
2. ECTA Officer navigation.
3. Field/Registry Agent navigation.
4. Verifier navigation.
5. Explicit logout.
6. Back-navigation after logout remains protected.
7. A protected API `401` clears auth state and redirects to `/login`.
8. A protected API `403` remains controlled authorization feedback without
   logging the user out.
9. Public `/verify/...` remains accessible without login.

No password, JWT, credential, signing secret, or synthetic personal data is
recorded in this evidence file.

## Supplemental browser verification

**Verification date:** 2026-09-05

- **Admin navigation:** PASS. Login reached `/dashboard`; the authenticated shell exposed Dashboard, Farmers, Coffee Lots, User management, and Log out.
- **ECTA Officer navigation:** PASS. The authenticated shell exposed Dashboard, Farmers, QR verification, and Log out, with no Admin-only management actions.
- **Field/Registry Agent navigation:** PASS. The authenticated shell exposed Dashboard, Farmers, Farm registration, Coffee Lots, and Log out.
- **Verifier navigation:** PASS. The authenticated shell exposed Dashboard, Farmers, and Log out, with no creation or management actions.
- **Logout:** PASS. Explicit logout cleared the session and returned to `/login`.
- **Protected back-navigation:** PASS. Browser Back after logout remained on the logged-out state; the protected page did not become usable again.
- **401 expired-session cleanup:** PASS. A controlled protected API response of HTTP 401 cleared the authenticated state and navigated to `/login`; no stale protected shell or raw backend detail remained.
- **403 retained-session handling:** PASS. A controlled protected API response of HTTP 403 displayed the bounded authorization message `You are not authorized to perform this action.`, remained on the protected page, and kept the authenticated Field/Registry Agent shell available.
- **Public verification:** PASS. Logged out, `/verify/113` with its valid synthetic signature loaded publicly and displayed only the approved Valid status, GIN, and unavailable origin; no login redirect or protected trace data appeared.
- **Security/error exposure:** PASS. No password, JWT, secret, stack trace, or raw backend internals appeared in the UI. The public route remained independent of authenticated state.

**Browser verification:** PASS
**Source changes:** None
