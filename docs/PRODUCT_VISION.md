# Product Vision

**Status:** M0 baseline  
**Last updated:** 2026-10-18  
**Working name:** India AI Citizen Services Platform (repository: MeeSeva)

---

## Vision

Help Indian citizens securely manage personal documents and use the information in those documents to prepare government and administrative applications—with the citizen always in control.

**Guiding principle:** Don't just store documents. Use documents to help citizens get things done.

---

## Problem statement

Citizens in Andhra Pradesh often struggle to complete government applications because:

- Personal documents are scattered (phone photos, PDFs, physical copies).
- The same identity and income details are re-entered for every application.
- Official forms and supporting-document rules are hard to interpret.
- Many citizens rely on service centers, relatives, or intermediaries.
- Document expiry and renewals are easy to miss.

DigiLocker and similar services address storage, issued-document access, sharing, and verification. They do not, on currently documented capabilities, provide a reusable structured citizen profile with AI-assisted extraction, deterministic service-specific form mapping, missing/conflict detection, and downloadable application-package preparation under human review.

---

## Target customers

| Role | Description |
|---|---|
| Primary | Individual Indian citizens in Andhra Pradesh who need help completing government applications |
| Characteristics | Often smartphone-first; may have limited technical experience; documents as photos/PDFs; may need future Telugu/other language support |
| Out of MVP | Family accounts, authorized partners, enterprise/B2B portals, multi-state catalogs |

---

## Positioning

Differentiated value versus document storage alone:

1. Reusable structured citizen profile with provenance
2. AI-assisted classification and extraction (human-verified)
3. Service-specific application guidance
4. Automatic identification of required information
5. Detection of missing or inconsistent information
6. Deterministic form-field mapping
7. Automatic supporting-document selection
8. Human-in-the-loop application review
9. Completed application package generation
10. Field-level source traceability

**Commercial hypothesis (unvalidated):** Citizens may pay for convenience and application preparation rather than storage alone. Requires customer validation.

**Competitive note:** DigiLocker (MeitY) provides secure storage, issued documents, sharing, and verification. Do not claim DigiLocker lacks a feature without checking current official documentation.

---

## Confirmed decisions (APPROVED)

| Decision | Direction |
|---|---|
| Primary customers | Individual Indian citizens |
| Initial geography | Andhra Pradesh |
| Primary MVP outcome | One complete application-preparation workflow |
| Pilot service | AP Income Certificate (provisional until official validation) |
| Alternative service | Residence Certificate |
| Future candidate | Family Member Certificate |
| Development documents | Synthetic documents only until compliance approval |
| Business model | Freemium / subscription (pricing unapproved) |
| Initial delivery | Responsive web application |
| Architecture | Modular monolith |
| AI approach | AI-assisted, human-controlled |
| Government integration | Not required for MVP |
| Submission | User-controlled download/print/manual submission |
| Language | English initially; multilingual architecture for later |

---

## MVP boundaries

**In MVP**

- Secure account (managed IdP + MFA)
- Private document vault
- OCR/classification/extraction with user verification
- Verified citizen profile with provenance
- One validated service definition (Income Certificate if unblocked; else Residence Certificate)
- Application draft → review → approval → PDF package
- Expiry metadata + basic dashboard
- Grounded AI guidance from approved knowledge base
- Freemium entitlement model (no payment gateway)

**Out of MVP**

- Direct government API submission
- DigiLocker issuer/partner integrations
- Multi-state catalog
- Multilingual UI
- Family/partner accounts
- Payment/billing integrations
- Multi-agent AI systems
- Microservices / Kubernetes

---

## Future roadmap (not MVP)

Additional states and services; Telugu and other languages; family accounts; authorized partners; renewals automation; government integrations where legally permitted; mobile apps; voice interaction.

---

## Commercial hypotheses (UNVERIFIED)

1. Freemium conversion is driven by application-preparation usage and storage limits.
2. Citizens will trust a private vault enough to upload identity/income documents after clear consent UX.
3. Time saved versus manual/intermediary preparation is large enough to justify Premium.
4. Online-first AP services still benefit from offline package preparation (assistive fill + document pack).

Pricing and exact entitlement limits remain product-owner decisions.

---

## Prior artifacts reused

| Artifact | Role |
|---|---|
| `Product Idea - Sree Kanth Nuti.pdf` / `extracted_pdf_rest.txt` | Original product concept and V1 feature list |
| `Product_Idea_Alignment.docx` | Earlier alignment framing (vault + partners); superseded where it conflicts with confirmed M0 decisions |

Partner document-request APIs and B2B sharing are deferred beyond MVP per confirmed scope.
