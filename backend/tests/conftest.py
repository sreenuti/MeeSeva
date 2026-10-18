from __future__ import annotations

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Configure safe test environment before importing app modules.
os.environ["ENVIRONMENT"] = "test"
os.environ["AUTH_MODE"] = "dev"
os.environ["AUTH_DEV_MODE"] = "true"
os.environ["AUTH_DEV_JWT_SECRET"] = "test-secret-not-for-production-32b"
os.environ["STORAGE_BACKEND"] = "local"
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["MALWARE_SCANNER"] = "stub"

from app.config import get_settings
from app.db import Base, get_db
from app.identity.jwt_validator import mint_dev_token
from app.main import create_app
from app import models as _models  # noqa: F401 — register metadata

get_settings.cache_clear()


@pytest.fixture()
def storage_dir(tmp_path: Path):
    path = tmp_path / "vault"
    path.mkdir()
    os.environ["LOCAL_STORAGE_PATH"] = str(path)
    get_settings.cache_clear()
    return path


@pytest.fixture()
def client(storage_dir: Path):
    get_settings.cache_clear()
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

    app = create_app()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    # Reset validator singleton between tests
    import app.identity.deps as deps

    deps._validator = None

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)
    get_settings.cache_clear()


@pytest.fixture()
def token_a():
    settings = get_settings()
    return mint_dev_token(settings, subject="user-a-subject", email="citizen.a@example.com")


@pytest.fixture()
def token_b():
    settings = get_settings()
    return mint_dev_token(settings, subject="user-b-subject", email="citizen.b@example.com")


@pytest.fixture()
def auth_a(token_a):
    return {"Authorization": f"Bearer {token_a}"}


@pytest.fixture()
def auth_b(token_b):
    return {"Authorization": f"Bearer {token_b}"}


def tiny_pdf(extra: bytes = b"") -> bytes:
    # Minimal PDF recognized by magic-byte validator.
    return b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n" + extra


def tiny_png() -> bytes:
    return (
        b"\x89PNG\r\n\x1a\n"
        b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde"
        b"\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
    )
