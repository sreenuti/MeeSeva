# Decisions Log

**Status:** M2 approved for synthetic local development; M3 not authorized  
**Last updated:** 2026-10-18

Legend: **APPROVED** · **RECOMMENDATION** · **UNVERIFIED** · **BLOCKER** · **OPEN**

---

## 1. Confirmed product decisions (APPROVED)

| ID | Decision | Direction | Approved by |
|---|---|---|---|
| P1 | Primary customers | Individual Indian citizens | Product owner (M0 brief) |
| P2 | Initial geography | Andhra Pradesh | Product owner |
| P3 | Primary MVP outcome | One complete application-preparation workflow | Product owner |
| P4 | Provisional first workflow | Andhra Pradesh Residence Certificate (General) — assistive worksheet only | Product owner (M3 research brief, 2026-10-18) |
| P5 | Future candidate | Income Certificate. Residence Certificate (Passport) is excluded | Product owner (M3 research brief, 2026-10-18) |
| P6 | Future candidate | Family Member Certificate | Product owner |
| P7 | Dev documents | Synthetic only until compliance approval | Product owner |
| P8 | Business model | Freemium / subscription | Product owner |
| P9 | Delivery | Responsive web app | Product owner |
| P10 | Architecture style | Modular monolith | Product owner |
| P11 | AI approach | AI-assisted, human-controlled | Product owner |
| P12 | Government integration | Not required for MVP | Product owner |
| P13 | Submission | User-controlled download/print/manual | Product owner |
| P14 | Language | English first; multilingual-ready later | Product owner |

Do not reopen unless material feasibility, security, or regulatory blocker.

---

## 2. Architecture decisions

| ID | Decision | Status | Notes |
|---|---|---|---|
| A1 | Next.js + TS + Tailwind frontend | RECOMMENDATION → treat as baseline | Per M0 stack guidance |
| A2 | FastAPI + Pydantic backend | RECOMMENDATION → treat as baseline | Same |
| A3 | PostgreSQL system of record | RECOMMENDATION → treat as baseline | Same |
| A4 | Private encrypted object storage | APPROVED (requirement) | No public document buckets |
| A5 | Managed IdP with MFA | APPROVED (requirement) | Vendor: Amazon Cognito (M1) |
| A6 | Lightweight job worker; Redis only if needed | RECOMMENDATION | Avoid premature infra |
| A7 | Pluggable OCR/LLM providers | APPROVED (direction) | M2 uses local pypdf (+ optional Tesseract); cloud OCR still OPEN (D2) |
| A11 | M2 extraction approach | APPROVED (M2) | Deterministic label parsers for synthetic docs; no generative LLM in M2 |
| A8 | Deterministic PDF packaging | APPROVED (direction) | AI must not invent required values |
| A9 | No microservices/K8s/vector DB/multi-agent for MVP | APPROVED | Complexity deferral |
| A10 | India hosting region for production PII | RECOMMENDATION | Confirm after compliance (D3) |

---

## 3. Open decisions (need product-owner / specialist input)

| ID | Topic | Options / notes | Needed by |
|---|---|---|---|
| D1 | Managed IdP vendor | **Selected: Amazon Cognito** (M1). Pool + MFA still require manual AWS setup — see `M1_COGNITO_SETUP.md` | M1 (config pending) |
| D2 | OCR/extraction provider | **M2 baseline:** local pypdf (+ optional Tesseract). Cloud OCR still OPEN for later | M2 done / cloud later |
| D3 | Production cloud + region | Must support encryption, private storage, residency expectations | Before M6 pilot |
| D4 | Package format for first service | **APPROVED:** assistive worksheet + submission checklist. Not an official government-form facsimile. No government logo, seal, signature, or certificate template | Decided 2026-10-18. Facsimile rights (D11) stay deferred |
| D5 | First official workflow | **APPROVED as provisional:** Residence Certificate (General), service key `ap.revenue.residence_certificate.general`. Passport variant excluded. Income Certificate retained as a future candidate. **Not published and not M3-authorized** while R-GO is BLOCKED | Decided 2026-10-18. Legal availability still **BLOCKER** |
| D6 | Freemium numeric limits | Storage MB, #applications/month, reminder features | M5 (can stub earlier) |
| D7 | Pricing | Amounts, trials, annual vs monthly | Post-M5 / commercial validation |
| D8 | External notification channels | In-app only vs email/SMS for MVP | M5 |
| D9 | Aadhaar handling policy | **APPROVED exclusion:** do not store or extract Aadhaar numbers until legal approval. The official residence form contains an Aadhaar field; the product must not collect it | Before any real docs (**BLOCKER** legal) |
| D10 | Brand / product name | “MeeSeva” is a government brand risk; working name TBD | Anytime pre-pilot |
| D11 | Form template IP/usage rights | License / permission path for reproducing forms | Before M4 official-looking PDFs |

---

## 4. Assumptions (UNVERIFIED)

| ID | Assumption | Impact if wrong |
|---|---|---|
| U1 | Citizens will pay for application preparation convenience | Business model weakens |
| U2 | Online-first AP services still benefit from offline/assistive packages | Package value proposition changes; still useful as checklist |
| U3 | Synthetic documents suffice to build extraction quality until pilot | Accuracy risk at pilot |
| U4 | Managed IdP MFA satisfies initial security bar | May need additional device binding |
| U5 | Single modular monolith scales to controlled pilot | Revisit only if proven bottleneck |

---

## 5. Decisions recorded on 2026-10-18 (M3 research brief)

These are product decisions. They do not clear the legal or schema gate for implementation.

| ID | Decision | Status |
|---|---|---|
| M2 | M2 is approved for synthetic local development | APPROVED |
| D5 | Provisional first workflow is Residence Certificate (General) | APPROVED as provisional |
| — | Residence Certificate (Passport) | EXCLUDED |
| P5 | Income Certificate | Retained as a future candidate; not the first workflow |
| D4 | First output is an assistive worksheet and submission checklist | APPROVED |
| P12 / P13 | No government API integration and no direct submission | APPROVED (unchanged) |
| D9 | No Aadhaar number storage or extraction | EXCLUDED pending legal approval |
| R-GO | G.O.Ms.No.592 legal effect | **BLOCKED** — no government-hosted copy obtained |
| M3 | Service catalog, application engine, and PDF generator | **NOT AUTHORIZED** |

## 6. Product-owner decisions still required

1. Accept that R-GO stays BLOCKED, and that the worksheet must not tell citizens the General Residence Certificate is currently authorized for unrestricted purposes.  
2. Approve or reject the draft service specification `ap.revenue.residence_certificate.general` version `0.1-draft` in `M3_SERVICE_SCHEMA_RESEARCH.md`. Approval of the draft is not approval to implement M3.  
3. Confirm the worksheet may omit Aadhaar even though the official form prints an Aadhaar line.  
4. Decide whether to keep this provisional pilot, or pause it until an official copy of G.O.Ms.No.592 and any later September 2026 clarification is filed.  
5. Do **not** start M3 implementation until that choice is explicit. The recommendation in `M3_READINESS_REPORT.md` is to withhold implementation.  
6. Cognito pool/MFA setup remains outstanding for non-dev auth (D1 config).  
7. Confirm D10 naming caution (avoid government trademark confusion).  
8. D11 remains open only if a future decision reverses D4 and seeks an official-form facsimile.

### M2 closure note

M2 is approved for synthetic local development only. Income Certificate field mapping remains incomplete and is no longer the first workflow. The Residence Certificate Telugu form was visually reviewed; see `M3_SERVICE_SCHEMA_RESEARCH.md`. **M3 is not cleared.**

---

## 7. Superseded prior framing

Earlier alignment (`Product_Idea_Alignment.docx`) emphasized partner document-request APIs and vault+reminders as MVP. **Superseded by APPROVED M0 decisions:** MVP centers on one application-preparation workflow; partner APIs are future scope.
