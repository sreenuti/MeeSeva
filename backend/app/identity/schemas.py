from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class TokenClaims(BaseModel):
    sub: str
    email: str | None = None
    token_use: str | None = None
    aud: str | list[str] | None = None
    iss: str | None = None
    exp: int | None = None
    auth_time: int | None = None
    cognito_mfa: bool | None = None


class UserOut(BaseModel):
    id: UUID
    email: str | None
    locale: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ConsentIn(BaseModel):
    purposes: list[str] = Field(min_length=1)
    granted: bool = True


class ConsentOut(BaseModel):
    purpose: str
    policy_version: str
    granted: bool
    granted_at: datetime

    model_config = {"from_attributes": True}


class DevTokenRequest(BaseModel):
    subject: str = Field(min_length=3, max_length=128)
    email: EmailStr | None = None
