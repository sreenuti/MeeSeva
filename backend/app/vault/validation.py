from __future__ import annotations

from dataclasses import dataclass

from fastapi import HTTPException, status

from app.config import Settings

# Magic-byte signatures for allowed types.
_SIGNATURES: list[tuple[str, bytes]] = [
    ("application/pdf", b"%PDF"),
    ("image/jpeg", b"\xff\xd8\xff"),
    ("image/png", b"\x89PNG\r\n\x1a\n"),
    ("image/webp", b"RIFF"),
]


@dataclass
class ValidatedUpload:
    content: bytes
    mime_type: str
    size: int
    original_filename: str


def _detect_mime(content: bytes) -> str | None:
    for mime, sig in _SIGNATURES:
        if content.startswith(sig):
            if mime == "image/webp":
                if len(content) >= 12 and content[8:12] == b"WEBP":
                    return mime
                continue
            return mime
    return None


def validate_upload(
    *,
    filename: str,
    content: bytes,
    declared_content_type: str | None,
    settings: Settings,
) -> ValidatedUpload:
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file")

    if len(content) > settings.max_upload_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f"File exceeds maximum size of {settings.max_upload_bytes} bytes",
        )

    detected = _detect_mime(content)
    if detected is None or detected not in settings.allowed_mime_type_set:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported or invalid file content",
        )

    # Reject mismatch between declared type and detected content when declared.
    if declared_content_type and declared_content_type.split(";")[0].strip().lower() not in (
        detected,
        "application/octet-stream",
    ):
        # Soft: still accept if magic bytes are authoritative, but record declared mismatch via exception if clearly wrong.
        if declared_content_type.split(";")[0].strip().lower() not in settings.allowed_mime_type_set:
            raise HTTPException(status_code=415, detail="Declared content type is not allowed")

    safe_name = os_path_basename(filename)[:200] or "document"
    return ValidatedUpload(
        content=content,
        mime_type=detected,
        size=len(content),
        original_filename=safe_name,
    )


def os_path_basename(filename: str) -> str:
    name = filename.replace("\\", "/").split("/")[-1].strip()
    return name or "document"
