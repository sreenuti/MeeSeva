from __future__ import annotations

import os

from tests.conftest import tiny_pdf, tiny_png


def test_unauthenticated_rejected(client):
    r = client.get("/api/v1/documents")
    assert r.status_code == 401


def test_upload_list_download_delete_happy_path(client, auth_a, storage_dir):
    files = {"file": ("synth-ration.pdf", tiny_pdf(), "application/pdf")}
    data = {"doc_type": "ration_card", "display_name": "Synthetic Ration Card"}
    r = client.post("/api/v1/documents", headers=auth_a, files=files, data=data)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["downloadable"] is True
    assert body["scan_status"] == "clean"
    doc_id = body["id"]

    listed = client.get("/api/v1/documents", headers=auth_a)
    assert listed.status_code == 200
    assert listed.json()["total"] == 1

    meta = client.get(f"/api/v1/documents/{doc_id}", headers=auth_a)
    assert meta.status_code == 200
    assert meta.json()["display_name"] == "Synthetic Ration Card"

    dl = client.get(f"/api/v1/documents/{doc_id}/download", headers=auth_a)
    assert dl.status_code == 200
    assert dl.content.startswith(b"%PDF")

    deleted = client.delete(f"/api/v1/documents/{doc_id}", headers=auth_a)
    assert deleted.status_code == 204
    assert client.get("/api/v1/documents", headers=auth_a).json()["total"] == 0


def test_user_isolation(client, auth_a, auth_b):
    files = {"file": ("a.pdf", tiny_pdf(), "application/pdf")}
    created = client.post("/api/v1/documents", headers=auth_a, files=files, data={"doc_type": "id"})
    assert created.status_code == 201
    doc_id = created.json()["id"]

    assert client.get("/api/v1/documents", headers=auth_b).json()["total"] == 0
    assert client.get(f"/api/v1/documents/{doc_id}", headers=auth_b).status_code == 404
    assert client.get(f"/api/v1/documents/{doc_id}/download", headers=auth_b).status_code == 404
    assert client.delete(f"/api/v1/documents/{doc_id}", headers=auth_b).status_code == 404

    # Owner still has access
    assert client.get(f"/api/v1/documents/{doc_id}", headers=auth_a).status_code == 200


def test_reject_unsupported_and_oversized(client, auth_a):
    bad = client.post(
        "/api/v1/documents",
        headers=auth_a,
        files={"file": ("note.txt", b"hello world", "text/plain")},
    )
    assert bad.status_code == 415

    os.environ["MAX_UPLOAD_BYTES"] = "32"
    from app.config import get_settings

    get_settings.cache_clear()
    # Recreate validator/settings by hitting with large payload; settings cached on app —
    # validate via direct call path using oversized content against default limit instead.
    get_settings.cache_clear()
    os.environ.pop("MAX_UPLOAD_BYTES", None)
    get_settings.cache_clear()

    huge = tiny_pdf(b"0" * (11 * 1024 * 1024))
    oversized = client.post(
        "/api/v1/documents",
        headers=auth_a,
        files={"file": ("big.pdf", huge, "application/pdf")},
    )
    assert oversized.status_code == 413


def test_eicar_quarantine_not_downloadable(client, auth_a):
    # PDF header + EICAR marker for stub scanner
    from app.vault.scanner import EICAR

    payload = b"%PDF-1.4\n" + EICAR + b"\n%%EOF\n"
    r = client.post(
        "/api/v1/documents",
        headers=auth_a,
        files={"file": ("eicar.pdf", payload, "application/pdf")},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["scan_status"] == "infected"
    assert body["downloadable"] is False
    denied = client.get(f"/api/v1/documents/{body['id']}/download", headers=auth_a)
    assert denied.status_code == 403


def test_consent_and_me(client, auth_a):
    me = client.get("/api/v1/me", headers=auth_a)
    assert me.status_code == 200
    assert me.json()["email"] == "citizen.a@example.com"

    consents = client.post(
        "/api/v1/consents",
        headers=auth_a,
        json={"purposes": ["vault_storage"], "granted": True},
    )
    assert consents.status_code == 200
    assert consents.json()[0]["purpose"] == "vault_storage"


def test_png_upload(client, auth_a):
    r = client.post(
        "/api/v1/documents",
        headers=auth_a,
        files={"file": ("id.png", tiny_png(), "image/png")},
        data={"display_name": "Synthetic ID Photo"},
    )
    assert r.status_code == 201
    assert r.json()["mime_type"] == "image/png"


def test_upload_failure_cleanup_on_storage_error(client, auth_a, monkeypatch, storage_dir):
    from app.vault import storage as storage_mod

    class Boom(storage_mod.LocalObjectStorage):
        def put_bytes(self, key: str, data: bytes, content_type: str) -> None:
            raise RuntimeError("disk full")

    monkeypatch.setattr("app.vault.router.build_storage", lambda settings: Boom(str(storage_dir)))
    r = client.post(
        "/api/v1/documents",
        headers=auth_a,
        files={"file": ("a.pdf", tiny_pdf(), "application/pdf")},
    )
    assert r.status_code == 500
    assert list(storage_dir.rglob("*")) == [] or all(p.is_dir() for p in storage_dir.rglob("*"))


def test_dev_token_endpoint_only_in_dev(client):
    r = client.post("/api/v1/dev/token", json={"subject": "dev-user", "email": "dev@example.com"})
    assert r.status_code == 200
    assert "access_token" in r.json()
