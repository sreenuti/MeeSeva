import pytest
from pydantic import ValidationError


def test_dev_auth_forbidden_in_production(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("AUTH_MODE", "dev")
    monkeypatch.setenv("AUTH_DEV_MODE", "true")
    monkeypatch.setenv("COGNITO_REGION", "ap-south-1")
    monkeypatch.setenv("COGNITO_USER_POOL_ID", "ap-south-1_example")
    monkeypatch.setenv("COGNITO_APP_CLIENT_ID", "exampleclient")
    from app.config import Settings

    with pytest.raises(ValidationError):
        Settings()
