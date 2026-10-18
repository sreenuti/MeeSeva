from functools import lru_cache
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Citizen Services API"
    environment: Literal["development", "test", "staging", "production"] = "development"
    api_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:3000"

    database_url: str = "postgresql+psycopg://citizen:citizen@localhost:5432/citizen_services"

    # Auth
    auth_mode: Literal["cognito", "dev"] = "cognito"
    cognito_region: str = ""
    cognito_user_pool_id: str = ""
    cognito_app_client_id: str = ""
    cognito_mfa_required: bool = True
    # Dev-only JWT (never enabled when environment is production/staging)
    auth_dev_mode: bool = False
    auth_dev_jwt_secret: str = "dev-only-change-me-use-32b-min"
    auth_dev_issuer: str = "https://dev.local/citizen-services"
    auth_dev_audience: str = "citizen-services-dev"

    # Storage
    storage_backend: Literal["local", "s3"] = "local"
    local_storage_path: str = "./data/vault"
    s3_bucket: str = ""
    s3_region: str = ""
    s3_endpoint_url: str | None = None
    s3_kms_key_id: str | None = None
    download_url_ttl_seconds: int = 60

    # Upload limits
    max_upload_bytes: int = 10 * 1024 * 1024
    allowed_mime_types: str = "application/pdf,image/jpeg,image/png,image/webp"

    # Malware scanning
    malware_scanner: Literal["stub", "clamav"] = "stub"
    clamav_host: str = "localhost"
    clamav_port: int = 3310
    fail_closed_on_scan_error: bool = True

    soft_delete_grace_days: int = 30
    consent_policy_version: str = "2026-10-18"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def allowed_mime_type_set(self) -> set[str]:
        return {m.strip() for m in self.allowed_mime_types.split(",") if m.strip()}

    @property
    def cognito_issuer(self) -> str:
        return f"https://cognito-idp.{self.cognito_region}.amazonaws.com/{self.cognito_user_pool_id}"

    @property
    def cognito_jwks_url(self) -> str:
        return f"{self.cognito_issuer}/.well-known/jwks.json"

    @model_validator(mode="after")
    def reject_dev_auth_outside_development(self) -> "Settings":
        if self.environment in ("production", "staging") and (
            self.auth_mode == "dev" or self.auth_dev_mode
        ):
            raise ValueError(
                "Dev authentication is forbidden when ENVIRONMENT is production or staging."
            )
        if self.auth_mode == "cognito" and self.environment not in ("development", "test"):
            if not (self.cognito_region and self.cognito_user_pool_id and self.cognito_app_client_id):
                raise ValueError("Cognito configuration is required outside development/test.")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
