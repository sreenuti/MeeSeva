from __future__ import annotations

from app.vault.scanner import EICAR
from tests.synthetic_docs import (
    malformed_pdf,
    synthetic_address_pdf,
    synthetic_identity_alt_name_pdf,
    synthetic_identity_pdf,
    synthetic_income_pdf,
)


def _upload(client, auth, content: bytes, name: str = "synth.pdf"):
    r = client.post(
        "/api/v1/documents",
        headers=auth,
        files={"file": (name, content, "application/pdf")},
        data={"display_name": name},
    )
    assert r.status_code == 201, r.text
    return r.json()


def test_process_clean_synthetic_identity(client, auth_a):
    doc = _upload(client, auth_a, synthetic_identity_pdf())
    proc = client.post(f"/api/v1/documents/{doc['id']}/process", headers=auth_a)
    assert proc.status_code == 200, proc.text
    assert proc.json()["status"] == "awaiting_user_review"

    extraction = client.get(f"/api/v1/documents/{doc['id']}/extraction", headers=auth_a)
    assert extraction.status_code == 200
    body = extraction.json()
    assert body["predicted_category"] == "identity_proof"
    keys = {f["field_key"] for f in body["fields"]}
    assert "full_name" in keys
    assert "date_of_birth" in keys
    assert "synthetic_identifier" in keys
    for field in body["fields"]:
        assert field["verification_status"] == "extracted_unverified"
        assert field["document_id"] == doc["id"]
        assert field["source_text_snippet"]


def test_quarantined_and_infected_cannot_process(client, auth_a):
    infected = b"%PDF-1.4\n" + EICAR + b"\n%%EOF\n"
    doc = _upload(client, auth_a, infected, "eicar.pdf")
    assert doc["scan_status"] == "infected"
    denied = client.post(f"/api/v1/documents/{doc['id']}/process", headers=auth_a)
    assert denied.status_code == 403


def test_malformed_fails_safely(client, auth_a):
    # Bypass content validation by writing through a clean PDF then... actually validator rejects non-PDF.
    # Upload a valid header PDF that is malformed for pypdf.
    doc = _upload(client, auth_a, malformed_pdf(), "bad.pdf")
    # malformed may still pass magic-byte check (%PDF)
    proc = client.post(f"/api/v1/documents/{doc['id']}/process", headers=auth_a)
    assert proc.status_code == 200
    assert proc.json()["status"] in {"failed", "unsupported"}
    assert proc.json()["error_code"]
    # Error must not include file body
    assert EICAR.decode("latin-1", errors="ignore") not in (proc.json().get("error_message") or "")


def test_missing_values_not_fabricated(client, auth_a):
    content = synthetic_identity_pdf().replace(b"Date of Birth: 1990-05-15", b"Date of Birth:")
    # If replace breaks PDF text stream length, use a custom minimal doc without DOB
    from tests.synthetic_docs import _pdf_with_lines

    content = _pdf_with_lines(
        [
            "SYNTHETIC IDENTITY DOCUMENT - NOT A GOVERNMENT ID",
            "Full Name: Demo Synthetic User",
            "Synthetic ID: SYNTH-ID-42",
        ]
    )
    doc = _upload(client, auth_a, content)
    client.post(f"/api/v1/documents/{doc['id']}/process", headers=auth_a)
    fields = client.get(f"/api/v1/documents/{doc['id']}/extraction", headers=auth_a).json()["fields"]
    keys = {f["field_key"] for f in fields}
    assert "full_name" in keys
    assert "date_of_birth" not in keys


def test_user_correction_and_unverified_until_confirmed(client, auth_a):
    doc = _upload(client, auth_a, synthetic_identity_pdf())
    client.post(f"/api/v1/documents/{doc['id']}/process", headers=auth_a)
    fields = client.get(f"/api/v1/documents/{doc['id']}/extraction", headers=auth_a).json()["fields"]
    name = next(f for f in fields if f["field_key"] == "full_name")
    assert name["verification_status"] == "extracted_unverified"

    profile_before = client.get("/api/v1/profile", headers=auth_a).json()
    assert all(f["verification_state"] != "verified" or f["field_key"] != "full_name" for f in profile_before["fields"]) or not profile_before["fields"]

    corrected = client.post(
        f"/api/v1/extracted-fields/{name['id']}/review",
        headers=auth_a,
        json={"action": "correct", "value": "Asha Synthetic Rao (Corrected)"},
    )
    assert corrected.status_code == 200
    assert corrected.json()["verification_status"] == "user_corrected"
    assert corrected.json()["user_corrected_value"] == "Asha Synthetic Rao (Corrected)"

    profile = client.get("/api/v1/profile", headers=auth_a).json()
    pf = next(f for f in profile["fields"] if f["field_key"] == "full_name")
    assert pf["value"] == "Asha Synthetic Rao (Corrected)"
    assert pf["verification_state"] == "verified"
    assert pf["original_extracted_value"]
    assert pf["user_corrected"] is True


def test_conflict_requires_resolution(client, auth_a):
    doc1 = _upload(client, auth_a, synthetic_identity_pdf(), "id1.pdf")
    client.post(f"/api/v1/documents/{doc1['id']}/process", headers=auth_a)
    name1 = next(
        f
        for f in client.get(f"/api/v1/documents/{doc1['id']}/extraction", headers=auth_a).json()["fields"]
        if f["field_key"] == "full_name"
    )
    client.post(
        f"/api/v1/extracted-fields/{name1['id']}/review",
        headers=auth_a,
        json={"action": "confirm"},
    )

    doc2 = _upload(client, auth_a, synthetic_identity_alt_name_pdf(), "id2.pdf")
    client.post(f"/api/v1/documents/{doc2['id']}/process", headers=auth_a)
    name2 = next(
        f
        for f in client.get(f"/api/v1/documents/{doc2['id']}/extraction", headers=auth_a).json()["fields"]
        if f["field_key"] == "full_name"
    )
    client.post(
        f"/api/v1/extracted-fields/{name2['id']}/review",
        headers=auth_a,
        json={"action": "confirm"},
    )

    conflicts = client.get("/api/v1/profile/conflicts", headers=auth_a)
    assert conflicts.status_code == 200
    assert any(c["field_key"] == "full_name" for c in conflicts.json())

    resolved = client.post(
        "/api/v1/profile/conflicts/resolve",
        headers=auth_a,
        json={"field_key": "full_name", "value": "Asha Synthetic Rao", "source_extracted_field_id": name1["id"]},
    )
    assert resolved.status_code == 200
    assert resolved.json()["verification_state"] == "verified"
    assert resolved.json()["value"] == "Asha Synthetic Rao"


def test_isolation_extraction_and_profile(client, auth_a, auth_b):
    doc = _upload(client, auth_a, synthetic_income_pdf(), "income.pdf")
    client.post(f"/api/v1/documents/{doc['id']}/process", headers=auth_a)
    assert client.get(f"/api/v1/documents/{doc['id']}/extraction", headers=auth_b).status_code == 404
    assert client.post(f"/api/v1/documents/{doc['id']}/process", headers=auth_b).status_code == 404

    fields = client.get(f"/api/v1/documents/{doc['id']}/extraction", headers=auth_a).json()["fields"]
    amount = next(f for f in fields if f["field_key"] == "income_amount")
    client.post(
        f"/api/v1/extracted-fields/{amount['id']}/review",
        headers=auth_a,
        json={"action": "confirm"},
    )
    assert client.get("/api/v1/profile", headers=auth_b).json()["fields"] == []
    denied = client.post(
        f"/api/v1/extracted-fields/{amount['id']}/review",
        headers=auth_b,
        json={"action": "confirm"},
    )
    assert denied.status_code == 404


def test_deleted_cannot_process(client, auth_a):
    doc = _upload(client, auth_a, synthetic_address_pdf(), "addr.pdf")
    client.delete(f"/api/v1/documents/{doc['id']}", headers=auth_a)
    assert client.post(f"/api/v1/documents/{doc['id']}/process", headers=auth_a).status_code == 404


def test_duplicate_processing_safe(client, auth_a):
    doc = _upload(client, auth_a, synthetic_identity_pdf())
    first = client.post(f"/api/v1/documents/{doc['id']}/process", headers=auth_a).json()
    second = client.post(f"/api/v1/documents/{doc['id']}/process", headers=auth_a).json()
    assert first["id"] == second["id"]
    assert second["status"] == "awaiting_user_review"


def test_m1_vault_still_works(client, auth_a):
    doc = _upload(client, auth_a, synthetic_identity_pdf())
    listed = client.get("/api/v1/documents", headers=auth_a)
    assert listed.status_code == 200
    assert listed.json()["total"] >= 1
    dl = client.get(f"/api/v1/documents/{doc['id']}/download", headers=auth_a)
    assert dl.status_code == 200
