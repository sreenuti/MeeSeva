from __future__ import annotations

import io
import re
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout

from app.intelligence.ocr.base import OcrPage, OcrResult


class LocalOcrProvider:
    """Local text extraction: prefer embedded PDF text; optional Tesseract for images.

    Never sends documents to external services.
    """

    def extract(self, content: bytes, *, mime_type: str, max_pages: int, timeout_seconds: int) -> OcrResult:
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(self._extract_inner, content, mime_type, max_pages)
            try:
                return future.result(timeout=timeout_seconds)
            except FuturesTimeout:
                return OcrResult(errors=["ocr_timeout"])
            except Exception as exc:
                return OcrResult(errors=[f"ocr_failed:{exc.__class__.__name__}"])

    def _extract_inner(self, content: bytes, mime_type: str, max_pages: int) -> OcrResult:
        if mime_type == "application/pdf":
            return self._extract_pdf(content, max_pages=max_pages)
        if mime_type in {"image/jpeg", "image/png", "image/webp"}:
            return self._extract_image(content, mime_type=mime_type)
        return OcrResult(errors=["unsupported_mime"])

    def _extract_pdf(self, content: bytes, *, max_pages: int) -> OcrResult:
        try:
            from pypdf import PdfReader
        except ImportError:
            return OcrResult(errors=["pypdf_missing"])

        try:
            reader = PdfReader(io.BytesIO(content), strict=False)
        except Exception:
            return OcrResult(errors=["malformed_pdf"])

        pages: list[OcrPage] = []
        errors: list[str] = []
        page_count = min(len(reader.pages), max_pages)
        for i in range(page_count):
            try:
                text = (reader.pages[i].extract_text() or "").strip()
            except Exception:
                text = ""
                errors.append(f"page_{i + 1}_text_error")
            method = "embedded_text" if text else "none"
            # Optional OCR for image-only pages when Tesseract is available.
            if not text:
                ocr_text = self._tesseract_pdf_page_fallback(content, i)
                if ocr_text:
                    text = ocr_text
                    method = "tesseract"
            pages.append(OcrPage(page_number=i + 1, text=text, method=method))

        full = "\n".join(p.text for p in pages if p.text).strip()
        if len(reader.pages) > max_pages:
            errors.append("page_limit_reached")
        return OcrResult(pages=pages, full_text=full, page_count=len(reader.pages), errors=errors)

    def _tesseract_pdf_page_fallback(self, _content: bytes, _page_index: int) -> str:
        # Intentionally minimal: rendering PDF pages requires pdf2image/poppler.
        # Keep interface ready; return empty when unavailable.
        return ""

    def _extract_image(self, content: bytes, *, mime_type: str) -> OcrResult:
        # Prefer Tesseract when installed; otherwise fail as unsupported for image OCR.
        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            return OcrResult(
                pages=[OcrPage(page_number=1, text="", method="none", error="tesseract_unavailable")],
                full_text="",
                page_count=1,
                errors=["tesseract_unavailable"],
            )

        try:
            image = Image.open(io.BytesIO(content))
            image.load()
        except Exception:
            return OcrResult(errors=["malformed_image"])

        try:
            text = pytesseract.image_to_string(image) or ""
            text = re.sub(r"[ \t]+\n", "\n", text).strip()
        except Exception as exc:
            return OcrResult(errors=[f"tesseract_error:{exc.__class__.__name__}"])

        return OcrResult(
            pages=[OcrPage(page_number=1, text=text, method="tesseract")],
            full_text=text,
            page_count=1,
        )


def build_ocr_provider(name: str = "local") -> LocalOcrProvider:
    if name != "local":
        raise ValueError(f"Unsupported OCR provider: {name}")
    return LocalOcrProvider()
