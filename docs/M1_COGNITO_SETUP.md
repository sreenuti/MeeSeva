# M1 — Amazon Cognito Setup

**Status:** Prerequisites checklist  
**Decision:** Cognito selected as managed IdP for M1 (`DECISIONS.md` D1)

---

## Required AWS resources

1. Cognito **User Pool** in an approved region (India region preferred for production PII; confirm with compliance).
2. App client (public SPA/web client) **without** client secret.
3. Callback / logout URLs for the web origin (e.g. `http://localhost:3000`).
4. Hosted UI optional; Amplify SDK auth is used by the web app.

## MFA configuration (required)

| Setting | Required value |
|---|---|
| MFA | **ON — Required** (not optional) for staging/production |
| MFA methods | TOTP and/or SMS per compliance preference |
| Password policy | Strong policy (min 12 recommended) |
| Account recovery | Email (or phone) via Cognito |

The API validates JWT `iss`, signature (JWKS), audience/client, expiration, and `token_use`. Pool-enforced MFA is the primary control so tokens are only issued after MFA challenge completion.

## Environment variables

Backend:

- `AUTH_MODE=cognito`
- `AUTH_DEV_MODE=false`
- `COGNITO_REGION`
- `COGNITO_USER_POOL_ID`
- `COGNITO_APP_CLIENT_ID`
- `COGNITO_MFA_REQUIRED=true`
- `ENVIRONMENT=development|staging|production`

Frontend:

- `NEXT_PUBLIC_AUTH_MODE=cognito`
- `NEXT_PUBLIC_COGNITO_REGION`
- `NEXT_PUBLIC_COGNITO_USER_POOL_ID`
- `NEXT_PUBLIC_COGNITO_APP_CLIENT_ID`

## Unresolved setup items (manual)

| Item | Owner | Notes |
|---|---|---|
| Create User Pool + app client | Ops / engineer | Not provisioned by this repo |
| Choose region for residency | Product + legal | Open decision D3 |
| Enable required MFA | Ops | Must be Required before pilot |
| SES/SMS for Cognito messages | Ops | Needed for real email/SMS delivery |
| Custom domain / Hosted UI branding | Optional | Not required for M1 |
| Production secrets in secret manager | Ops | Do not commit `.env` |

## Development-safe path (no Cognito credentials)

When Cognito is unavailable locally:

```
ENVIRONMENT=development
AUTH_MODE=dev
AUTH_DEV_MODE=true
NEXT_PUBLIC_AUTH_MODE=dev
```

- Backend exposes `POST /api/v1/dev/token` **only** when `ENVIRONMENT` is `development` or `test` **and** `AUTH_DEV_MODE=true`.
- Settings validation **refuses to start** if `AUTH_MODE=dev` or `AUTH_DEV_MODE=true` when `ENVIRONMENT` is `staging` or `production`.
- Never enable the development bypass in deployed environments.

## Verification checklist

- [ ] User can register and confirm email
- [ ] MFA challenge required on login
- [ ] Access token accepted by API
- [ ] Expired/wrong-audience tokens rejected
- [ ] Dev token endpoint returns 404 when Cognito mode is active / non-dev environment
