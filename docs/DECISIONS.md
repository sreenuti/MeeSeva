# Decisions Log

**Status:** M0 baseline  
**Last updated:** 2026-10-18

Legend: **APPROVED** · **RECOMMENDATION** · **UNVERIFIED** · **BLOCKER** · **OPEN**

---

## 1. Confirmed product decisions (APPROVED)

| ID | Decision | Direction | Approved by |
|---|---|---|---|
| P1 | Primary customers | Individual Indian citizens | Product owner (M0 brief) |
| P2 | Initial geography | Andhra Pradesh | Product owner |
| P3 | Primary MVP outcome | One complete application-preparation workflow | Product owner |
| P4 | Pilot service | AP Income Certificate (provisional) | Product owner |
| P5 | Alternative service | Residence Certificate | Product owner |
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
| D4 | Package format for first service | Official-form facsimile vs **assistive worksheet + portal/MeeSeva checklist** (recommended default until rights/schema clear) | Before M3 (**BLOCKER**) |
| D5 | First official workflow | **Income Certificate remains product baseline but BLOCKED for field mapping.** Research (2026-10-18): no regular Income blank form on MeeSeva forms index; EWS must not substitute. **Residence Certificate (General)** has official Telugu blank form + district supporting-doc lists — **RECOMMENDED switch** pending PO approval; still needs English field confirmation (R1–R5 in `PILOT_SERVICE.md`) | Before M3 (**BLOCKER**) |
| D6 | Freemium numeric limits | Storage MB, #applications/month, reminder features | M5 (can stub earlier) |
| D7 | Pricing | Amounts, trials, annual vs monthly | Post-M5 / commercial validation |
| D8 | External notification channels | In-app only vs email/SMS for MVP | M5 |
| D9 | Aadhaar handling policy | Collect/store/extract vs prohibit until legal sign-off | Before any real docs (**BLOCKER** legal) |
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

## 5. Product-owner approvals required next

1. Accept M2 closure (local-dev conditional approval already noted).  
2. **Decide D5:** keep Income Certificate (assistive-only until B1) **or switch to Residence Certificate (General)**.  
3. **Decide D4:** package format (recommend assistive worksheet + checklist; no official-form claim).  
4. Confirm D11 before any official-form facsimile work.  
5. Do **not** authorize full M3 (catalog/engine/PDF package) until D4/D5 (+ schema evidence) clear.  
6. Cognito pool/MFA setup remains outstanding for non-dev auth (D1 config).  
7. Confirm D10 naming caution (avoid government trademark confusion).

### M2 closure research note (2026-10-18)

- **VERIFIED:** Income Certificate service metadata + supporting-doc checklist (APSEVA/GSWS).  
- **MISSING:** Regular Income Certificate blank form / field schema (MeeSeva forms index lists EWS & Agricultural Income, not regular Income).  
- **VERIFIED artifact:** Residence Certificate Telugu application PDF on MeeSeva.  
- **M3 status:** **Not cleared** for implementation.

---

## 6. Superseded prior framing

Earlier alignment (`Product_Idea_Alignment.docx`) emphasized partner document-request APIs and vault+reminders as MVP. **Superseded by APPROVED M0 decisions:** MVP centers on one application-preparation workflow; partner APIs are future scope.
