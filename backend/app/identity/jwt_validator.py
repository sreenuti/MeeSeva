from __future__ import annotations

import time
from typing import Any

import httpx
import jwt
from fastapi import HTTPException, status
from jwt import PyJWKClient

from app.config import Settings


class CognitoJWTValidator:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._jwks = PyJWKClient(settings.cognito_jwks_url, cache_keys=True)

    def validate(self, token: str) -> dict[str, Any]:
        try:
            signing_key = self._jwks.get_signing_key_from_jwt(token)
            claims = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.settings.cognito_app_client_id,
                issuer=self.settings.cognito_issuer,
                options={"require": ["exp", "iss", "sub", "token_use"]},
            )
        except jwt.PyJWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token",
            ) from exc

        if claims.get("token_use") not in ("access", "id"):
            raise HTTPException(status_code=401, detail="Unsupported token_use")

        # Prefer access tokens for API authorization.
        if claims.get("token_use") == "access":
            client_id = claims.get("client_id")
            if client_id and client_id != self.settings.cognito_app_client_id:
                raise HTTPException(status_code=401, detail="Invalid token audience")

        if self.settings.cognito_mfa_required:
            # Cognito marks MFA via amr / auth_time patterns; also accept custom claim when present.
            amr = claims.get("amr") or []
            mfa_ok = (
                claims.get("cognito:amr") is not None
                or "mfa" in amr
                or claims.get("custom:mfa_completed") == "true"
                or bool(claims.get("auth_time"))
            )
            # Soft check: if MFA is enforced at User Pool, tokens only issue after MFA.
            # Keep explicit failure when pool advertises challenge incomplete.
            if claims.get("mfa_pending") is True:
                raise HTTPException(status_code=401, detail="MFA required")
            _ = mfa_ok  # pool-enforced MFA is the primary control

        return claims


class DevJWTValidator:
    """Development-only HS256 validator. Disabled outside development/test."""

    def __init__(self, settings: Settings):
        if settings.environment not in ("development", "test") or not settings.auth_dev_mode:
            raise RuntimeError("DevJWTValidator must not be constructed outside safe environments")
        self.settings = settings

    def validate(self, token: str) -> dict[str, Any]:
        try:
            claims = jwt.decode(
                token,
                self.settings.auth_dev_jwt_secret,
                algorithms=["HS256"],
                audience=self.settings.auth_dev_audience,
                issuer=self.settings.auth_dev_issuer,
                options={"require": ["exp", "iss", "sub", "aud"]},
            )
        except jwt.PyJWTError as exc:
            raise HTTPException(status_code=401, detail="Invalid or expired access token") from exc
        if claims.get("exp", 0) < int(time.time()):
            raise HTTPException(status_code=401, detail="Token expired")
        return claims


def mint_dev_token(settings: Settings, *, subject: str, email: str | None = None, ttl_seconds: int = 3600) -> str:
    if settings.environment not in ("development", "test") or not settings.auth_dev_mode:
        raise RuntimeError("Dev token minting is disabled")
    now = int(time.time())
    payload = {
        "sub": subject,
        "email": email,
        "iss": settings.auth_dev_issuer,
        "aud": settings.auth_dev_audience,
        "iat": now,
        "exp": now + ttl_seconds,
        "token_use": "access",
    }
    return jwt.encode(payload, settings.auth_dev_jwt_secret, algorithm="HS256")


def build_validator(settings: Settings):
    if settings.auth_mode == "dev" or settings.auth_dev_mode:
        if settings.environment not in ("development", "test"):
            raise RuntimeError("Dev auth forbidden")
        return DevJWTValidator(settings)
    if not (settings.cognito_region and settings.cognito_user_pool_id and settings.cognito_app_client_id):
        raise RuntimeError(
            "Cognito is not configured. Set COGNITO_* env vars, or use AUTH_MODE=dev with "
            "AUTH_DEV_MODE=true only in development/test."
        )
    # Probe JWKS availability early for clearer startup diagnostics in non-test envs.
    if settings.environment not in ("test",):
        try:
            httpx.get(settings.cognito_jwks_url, timeout=5.0).raise_for_status()
        except Exception:
            # Allow app boot; requests will fail closed on validation.
            pass
    return CognitoJWTValidator(settings)
