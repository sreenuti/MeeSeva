# M2 — Document Intelligence Pipeline

**Status:** Implemented  
**Last updated:** 2026-10-18

## Flow

1. Document must be owned, not deleted, and malware `scan_status=clean`.
2. `POST /api/v1/documents/{id}/process` enqueues a job (one job per document version).
3. Local OCR/text extraction runs (embedded PDF text preferred; optional Tesseract for images).
4. Rule-based classification → identity / address / income / unknown.
5. Deterministic label:value field extraction (no fabrication).
6. Results remain `extracted_unverified` until the citizen confirms or corrects them.
7. Confirmed values update the citizen profile; conflicts require explicit resolution.

## Supported synthetic formats

Synthetic PDFs with embedded text and labels such as:

- `Full Name:`
- `Date of Birth:` / `Synthetic ID:`
- `Address:` / `Village:` / `District:` / `State:` / `Postal Code:`
- `Income Amount:` / `Income Period:` / `Income Source:` / `Currency:`

Documents must be clearly marked fictional (e.g. `SYNTHETIC IDENTITY DOCUMENT`).

## Source document deletion

Profile fields keep provenance IDs (`source_document_id`, `source_extracted_field_id`). Soft-deleting a source document does not erase confirmed profile values; the source may become unavailable for download. Extraction/process endpoints refuse deleted documents.

## External AI

Not used in M2. Provider interfaces exist for a future approved local/cloud OCR only.
