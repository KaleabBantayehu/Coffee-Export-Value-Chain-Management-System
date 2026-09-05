# EPIC-5 FE-004 Dashboard and Authenticated Shell Reconciliation

**Task:** EPIC-5-FE-004 — Dashboard and Authenticated Application Shell

**Status:** READY FOR COPILOT BROWSER VERIFICATION

## Reconciliation result

The existing authenticated `/dashboard` route was a protected placeholder, not
an operational entry page. FE-004 replaces that placeholder with a small
dashboard that reuses the existing AuthContext, protected route, navigation,
API helpers, and styling conventions. No backend endpoint, direct database
access, mock production count, router, or UI/state framework was added.

## Approved API contracts used

| Dashboard value | Existing contract | Use |
| --- | --- | --- |
| Registered Farmers | Authenticated `GET /api/v1/farmers` | The documented collection response length is rendered as an aggregate count only. |
| Registered Farms | Authenticated `GET /api/v1/farms` | The documented collection response length is rendered as an aggregate count only. |

Both endpoints are implemented, require authentication, and return collection
responses for all authenticated roles. No individual Farmer or Farm data is
displayed on the dashboard.

## Traceability gap — requires review

No approved Coffee Lot collection or dashboard aggregation endpoint exists.
The inspected Lot contract provides creation, trace retrieval, event append,
and QR generation only. A Coffee Lot count is therefore deliberately omitted;
FE-004 does not infer one from unrelated endpoints or add a backend API.

## Acceptance matrix

| FE-004 criterion | Status | Evidence |
| --- | --- | --- |
| Authenticated users reach a protected dashboard | SOURCE-SUPPORTED | `App.jsx` routes `/dashboard` through the existing `ProtectedRoute`; FE-003 provides the authenticated shell and redirect behavior. |
| Role-appropriate actions use the frozen four-role model | SOURCE-SUPPORTED | `components/navigationItems.js` is the single mapping consumed by both `Navigation.jsx` and `Dashboard.jsx`; dashboard actions exclude the current Dashboard item. |
| Displayed values use approved contracts | SOURCE-SUPPORTED | `Dashboard.jsx` consumes only `searchFarmers('', accessToken)` and `listFarms(accessToken)`. |
| Unsupported dashboard values are omitted/escalated | PASS | Coffee Lot count is omitted and documented above as a traceability gap. |
| Loading, empty, partial-error, unauthorized, and error states are controlled | SOURCE-SUPPORTED | Farmer and Farm requests load independently; each card renders loading, zero-record, or bounded error state. FE-003's `401` redirect and bounded `403` behavior are reused. |
| Responsive, readable operational entry | SOURCE-SUPPORTED | `App.css` adds responsive auto-fit count cards and wrapping role-derived action buttons within the existing shell. Browser visual verification remains required. |
| Frontend lint | PASS | `npm.cmd run lint` completed successfully. |
| Frontend production build | PASS | `npm.cmd run build` completed successfully. |
| Whitespace check | PASS | `git diff --check` completed with no whitespace errors. |

## Files changed

- `frontend/src/pages/Dashboard.jsx`
- `frontend/src/components/navigationItems.js`
- `frontend/src/components/Navigation.jsx`
- `frontend/src/App.jsx`
- `frontend/src/App.css`

## Required browser verification

Codex did not run browser automation. Copilot should verify with synthetic
accounts and data:

1. Login reaches the dashboard and renders the protected shell for each
   applicable role.
2. Dashboard actions match the role and navigate to their existing routes.
3. Farmer/Farm counts render from real API responses, including zero-record
   states.
4. Loading states and a single-widget failure leave the other widget usable.
5. A `401` redirects to login and a `403` remains a bounded error without
   ending a healthy session.
6. The dashboard remains readable at the supported responsive sizes.

No credentials, JWTs, secrets, local environment values, or Farmer PII are
included in this evidence file.
