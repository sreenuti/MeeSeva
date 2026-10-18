from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class OcrPage:
    page_number: int
    text: str
    method: str  # embedded_text | tesseract | none
    error: str | None = None


@dataclass
class OcrResult:
    pages: list[OcrPage] = field(default_factory=list)
    full_text: str = ""
    page_count: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def has_text(self) -> bool:
        return bool(self.full_text.strip())


class OcrProvider(Protocol):
    def extract(self, content: bytes, *, mime_type: str, max_pages: int, timeout_seconds: int) -> OcrResult: ...
