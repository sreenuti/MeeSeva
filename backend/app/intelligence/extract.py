from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class FieldCandidate:
    field_key: str
    raw_value: str
    normalized_value: str | None
    data_type: str
    confidence: str
    validation_result: str
    source_page: int | None
    source_text_snippet: str | None


_LABEL_LINE = re.compile(
    r"(?im)^\s*(full name|name|date of birth|dob|synthetic id|synthetic identifier|"
    r"address line(?:\s*1)?|address|city|village|district|state|postal code|pincode|"
    r"income amount|gross annual income|income period|income source|currency)\s*[:\-]\s*(.+?)\s*$"
)


def _snippet(line: str) -> str:
    return line.strip()[:240]


def _norm_name(value: str) -> str | None:
    cleaned = re.sub(r"\s+", " ", value).strip()
    if not cleaned or "SYNTHETIC" in cleaned.upper() and len(cleaned) < 3:
        return None
    # Reject if looks empty after cleanup
    return cleaned.title() if cleaned.isupper() else cleaned


def _norm_date(value: str) -> str | None:
    value = value.strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", value)
    if m:
        return value
    m = re.match(r"^(\d{2})[/-](\d{2})[/-](\d{4})$", value)
    if m:
        d, mo, y = m.groups()
        return f"{y}-{mo}-{d}"
    return None


def _norm_amount(value: str) -> str | None:
    digits = re.sub(r"[^\d.]", "", value)
    if not digits:
        return None
    try:
        amount = float(digits)
    except ValueError:
        return None
    if amount < 0:
        return None
    return f"{amount:.2f}"


def _norm_postal(value: str) -> str | None:
    digits = re.sub(r"\D", "", value)
    return digits if len(digits) == 6 else None


def extract_fields(text: str, category: str, pages: list[tuple[int, str]] | None = None) -> list[FieldCandidate]:
    """Deterministic label:value extraction for synthetic documents. Never fabricates missing fields."""
    if not text.strip():
        return []

    page_for_line: dict[str, int] = {}
    if pages:
        for page_no, page_text in pages:
            for line in page_text.splitlines():
                page_for_line[line.strip()] = page_no

    found: dict[str, FieldCandidate] = {}
    for line in text.splitlines():
        m = _LABEL_LINE.match(line)
        if not m:
            continue
        label = m.group(1).lower().strip()
        raw = m.group(2).strip()
        if not raw:
            continue
        page = page_for_line.get(line.strip())

        mapping = _map_label(label, category)
        if not mapping:
            continue
        field_key, data_type, normalizer = mapping
        normalized = normalizer(raw) if normalizer else raw.strip()
        validation = "valid" if normalized else "invalid"
        confidence = "medium" if normalized else "low"
        # Do not overwrite an already-found field (first wins).
        if field_key in found:
            continue
        found[field_key] = FieldCandidate(
            field_key=field_key,
            raw_value=raw,
            normalized_value=normalized,
            data_type=data_type,
            confidence=confidence,
            validation_result=validation,
            source_page=page,
            source_text_snippet=_snippet(line),
        )

    return list(found.values())


def _map_label(label: str, category: str):
    common_name = ("full_name", "string", _norm_name)
    identity = {
        "full name": common_name,
        "name": common_name,
        "date of birth": ("date_of_birth", "date", _norm_date),
        "dob": ("date_of_birth", "date", _norm_date),
        "synthetic id": ("synthetic_identifier", "string", lambda v: v.strip().upper() or None),
        "synthetic identifier": ("synthetic_identifier", "string", lambda v: v.strip().upper() or None),
    }
    address = {
        "full name": common_name,
        "name": common_name,
        "address line": ("address_line", "string", lambda v: v.strip() or None),
        "address line 1": ("address_line", "string", lambda v: v.strip() or None),
        "address": ("address_line", "string", lambda v: v.strip() or None),
        "city": ("city", "string", lambda v: v.strip() or None),
        "village": ("village", "string", lambda v: v.strip() or None),
        "district": ("district", "string", lambda v: v.strip() or None),
        "state": ("state", "string", lambda v: v.strip() or None),
        "postal code": ("postal_code", "string", _norm_postal),
        "pincode": ("postal_code", "string", _norm_postal),
    }
    income = {
        "full name": common_name,
        "name": common_name,
        "income amount": ("income_amount", "number", _norm_amount),
        "gross annual income": ("income_amount", "number", _norm_amount),
        "income period": ("income_period", "string", lambda v: v.strip() or None),
        "income source": ("income_source", "string", lambda v: v.strip() or None),
        "currency": ("currency", "string", lambda v: v.strip().upper() or None),
    }

    if category == "identity_proof":
        return identity.get(label)
    if category == "address_proof":
        return address.get(label)
    if category == "income_proof":
        return income.get(label)
    # Unknown: try all maps conservatively
    return identity.get(label) or address.get(label) or income.get(label)


def normalize_for_compare(field_key: str, value: str | None) -> str | None:
    if value is None:
        return None
    v = value.strip()
    if not v:
        return None
    if field_key in {"full_name"}:
        return re.sub(r"\s+", " ", v).casefold()
    if field_key == "date_of_birth":
        return _norm_date(v) or v
    if field_key == "postal_code":
        return _norm_postal(v) or v
    if field_key == "income_amount":
        return _norm_amount(v) or v
    if field_key in {"state", "district", "city", "village", "currency"}:
        return v.casefold()
    return re.sub(r"\s+", " ", v).casefold()
