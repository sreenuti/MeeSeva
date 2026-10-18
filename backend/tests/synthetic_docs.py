"""Helpers to build clearly fictional synthetic PDFs with embedded text."""

from __future__ import annotations


def _pdf_with_lines(lines: list[str]) -> bytes:
    # Minimal PDF with Helvetica text that pypdf can extract.
    escaped = []
    for line in lines:
        safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        escaped.append(safe)

    content_lines = ["BT", "/F1 11 Tf", "50 750 Td"]
    for i, line in enumerate(escaped):
        if i == 0:
            content_lines.append(f"({line}) Tj")
        else:
            content_lines.append("0 -16 Td")
            content_lines.append(f"({line}) Tj")
    content_lines.append("ET")
    stream = "\n".join(content_lines).encode("latin-1", errors="replace")

    objects = []
    objects.append(b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n")
    objects.append(b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n")
    objects.append(
        b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources<< /Font<< /F1 5 0 R >> >> >>endobj\n"
    )
    objects.append(
        f"4 0 obj<< /Length {len(stream)} >>stream\n".encode("ascii") + stream + b"\nendstream\nendobj\n"
    )
    objects.append(b"5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(out))
        out.extend(obj)
    xref_pos = len(out)
    out.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    out.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode("ascii"))
    out.extend(
        f"trailer<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii")
    )
    return bytes(out)


def synthetic_identity_pdf() -> bytes:
    return _pdf_with_lines(
        [
            "SYNTHETIC IDENTITY DOCUMENT - NOT A GOVERNMENT ID",
            "Full Name: Asha Synthetic Rao",
            "Date of Birth: 1990-05-15",
            "Synthetic ID: SYNTH-ID-000123",
            "This document is fictional and for software testing only.",
        ]
    )


def synthetic_address_pdf() -> bytes:
    return _pdf_with_lines(
        [
            "SYNTHETIC ADDRESS PROOF - NOT AN OFFICIAL CERTIFICATE",
            "Full Name: Asha Synthetic Rao",
            "Address: 12 Demo Street, Example Nagar",
            "Village: Samplepur",
            "District: Demo District",
            "State: Andhra Pradesh",
            "Postal Code: 520001",
        ]
    )


def synthetic_income_pdf() -> bytes:
    return _pdf_with_lines(
        [
            "SYNTHETIC INCOME PROOF - NOT A REAL PAYSLIP OR ITR",
            "Full Name: Asha Synthetic Rao",
            "Income Amount: INR 180000",
            "Income Period: FY 2024-25",
            "Income Source: Synthetic Employer Pvt Ltd",
            "Currency: INR",
        ]
    )


def synthetic_identity_alt_name_pdf() -> bytes:
    return _pdf_with_lines(
        [
            "SYNTHETIC IDENTITY DOCUMENT - NOT A GOVERNMENT ID",
            "Full Name: Asha S. Rao",
            "Date of Birth: 1990-05-15",
            "Synthetic ID: SYNTH-ID-000999",
        ]
    )


def malformed_pdf() -> bytes:
    return b"%PDF-1.4\nthis is not a valid pdf structure<<<<"
