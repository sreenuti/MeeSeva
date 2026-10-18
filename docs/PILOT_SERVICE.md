# Pilot Service Validation

**Status:** Income Certificate — **BLOCKED** for M3 form-mapping · Residence Certificate — **conditionally better form artifact**, still not M3-ready  
**Last researched:** 2026-10-18 (M2 closure / M3 readiness review)  
**Preferred pilot (product baseline):** AP Income Certificate (Revenue) — provisional  
**Recommended next pilot decision:** See §12  

Do **not** use the EWS Income & Asset Certificate form as a substitute for the regular Income Certificate.

---

## 1. Decision matrix (what can be established authoritatively?)

| Requirement | Regular Income Certificate | Residence Certificate (General / Passport) |
|---|---|---|
| Service exists officially | **VERIFIED** | **VERIFIED** |
| Responsible department / authority | **VERIFIED** — Revenue; Tahsildar / Deputy Tahsildar | **VERIFIED** — Revenue; Tahsildar/MRO (district pages) |
| Supporting-document checklist | **VERIFIED (high level)** | **VERIFIED (high level)** via district `.ap.gov.in` pages |
| Complete application field schema | **MISSING** — not published as regular blank form; online schema not captured | **PARTIAL** — official Telugu blank form exists; English field list not authoritatively translated in this review |
| Official blank form / digital field schema | **MISSING** on MeeSeva Application Forms index for *regular* Income Certificate | **VERIFIED artifact** — MeeSeva Revenue Residence Telugu PDF |
| Permitted use / reproduction of form template | **UNVERIFIED** | **UNVERIFIED** |
| Submission / package acceptance | **PARTIALLY VERIFIED** — primary path is online APSEVA/VSWS; offline package acceptance not verified | **PARTIALLY VERIFIED** — MeeSeva centre / portal; offline facsimile acceptance not verified |

---

## 2. Andhra Pradesh Income Certificate (preferred baseline)

### 2.1 Verification summary

| Item | Status | Notes |
|---|---|---|
| Service exists officially | VERIFIED | APSEVA SOP; GSWS CSP manual; district service lists |
| Responsible department | VERIFIED | Revenue Department |
| Competent authority | VERIFIED | Tahsildar / Deputy Tahsildar |
| SLA | VERIFIED | 7 days |
| Fee | VERIFIED | ₹12 (APSEVA Ease of Living SOP) |
| Supporting documents | VERIFIED (checklist only) | Application form; IT returns / pay slips / other income proof; Ration Card / EPIC / Aadhaar |
| Official online channel | VERIFIED | APSEVA / VSWS citizen login |
| Complete field-level schema | **UNVERIFIED / MISSING** | No authoritative English field list for regular Income Certificate |
| Official blank form | **MISSING** | Not listed on MeeSeva Application Forms (Revenue) page reviewed 2026-10-18 |
| Form usage permissions | UNVERIFIED | |
| Package = official submission artifact | UNVERIFIED / LIKELY CONSTRAINED | Online-first submission |
| Individual vs parent income | PARTIALLY VERIFIED | CSP manual mentions both; fields not captured |
| Undertaking / signature | PARTIALLY VERIFIED | SOP: citizen may give undertaking |

**Implementation readiness for deterministic M3 mapping:** **BLOCKED** (B1–B4).

### 2.2 Official sources

| # | Source | URL | Accessed | Confirmed |
|---|---|---|---|---|
| S1 | APSEVA Ease of Living SOP — Income Certificate | https://apseva.ap.gov.in/assets/User-Manuals/EoDB%20SOP%20final.pdf | 2026-10-18 | Authority, SLA, docs, fee ₹12, procedure, submission URL |
| S2 | GSWS CSP User Manual | https://apseva.ap.gov.in/assets/User-Manuals/CSP-User-Manual.pdf | 2026-10-18 | Service listing, workflow, docs, individual/parent income |
| S3 | VSWS / APSEVA entry | https://vswsonline.ap.gov.in/#/home | 2026-10-18 | Cited submission channel |
| S4 | MeeSeva Application Forms index (Revenue) | http://ap.meeseva.gov.in/DeptPortal/Meeseva-Applications.html | 2026-10-18 | Lists EWS + Agricultural Income forms; **no regular Income Certificate blank form listed** |
| S5 | MeeSeva EWS form (**different service**) | https://ap.meeseva.gov.in/DeptPortal/Application%20Forms%20New/Revenue-pdf/Issuance%20of%20Income%20%20Asset%20Certificate%20%20for%20%20Economically%20Weaker%20Sections(EWS)ApplicationForm.pdf | 2026-10-18 | Full EWS fields — **must not substitute** |
| S6 | Kadapa district G.O. notice | https://kadapa.ap.gov.in/te/notice/issue-of-income-certificate-by-the-revenue-authorities-revised-orders-issued-date-04-07-2017-1214-2/ | 2026-10-18 | Revised orders exist; PDF not fully extracted this pass |

**Not used as authoritative field sources:** third-party aggregators (IndiaFilings, etc.).

### 2.3 Verified supporting documents (only)

1. Application form  
2. Copy of IT Returns / Pay Slips (or any other income-proof documents)  
3. Ration Card / EPIC Card / Aadhaar Card  

### 2.4 Explicit non-substitutes

| Artifact | Why not usable as Income Certificate schema |
|---|---|
| EWS Income & Asset Certificate form (S5) | Separate service; caste/asset declarations specific to EWS |
| Agriculture Income Certificate form | Separate service in MeeSeva/CSP catalogs |

### 2.5 Income Certificate blockers (before M3)

| ID | Blocker | Owner |
|---|---|---|
| B1 | Authoritative field-level schema for regular Income Certificate (portal capture or official blank form) | Product + research |
| B2 | Package format: official facsimile vs assistive worksheet + portal checklist | Product owner |
| B3 | Form reproduction / usage permissions | Legal / product |
| B4 | Whether any offline package is accepted officially, or online-assist only | Product |
| B5 | Versioned `ServiceDefinition` from verified evidence only | Engineering after B1–B4 |

---

## 3. Fallback — Andhra Pradesh Residence Certificate

### 3.1 Why reconsider

Compared with regular Income Certificate, Residence Certificate has a **published official blank application PDF** on MeeSeva Revenue forms and **consistent supporting-document checklists** on multiple district government sites.

It is **not** fully M3-ready: English field schema still needs authoritative bilingual confirmation; template rights and package acceptance remain open.

### 3.2 Verified / partial findings

| Item | Status | Evidence |
|---|---|---|
| Service types | VERIFIED | General and Passport — e.g. https://visakhapatnam.ap.gov.in/service/residence-certificate/ |
| Supporting documents | VERIFIED (district pages) | Application form; Ration/EPIC/Aadhaar; House tax / telephone / electricity bill; Photo mandatory for Passport type |
| Official blank form | VERIFIED (artifact exists) | https://ap.meeseva.gov.in/DeptPortal/Application%20Forms%20New/Revenue-pdf/REVENUE%20-%20RESIDENCE-Telugu.pdf |
| English field schema | PARTIAL / UNVERIFIED | Telugu form exists; this review did not produce a counsel/official English field mapping |
| Form usage permissions | UNVERIFIED | |
| Package acceptance | UNVERIFIED | MeeSeva centre / portal paths described; facsimile acceptance unknown |
| Fee / SLA | UNVERIFIED for a single statewide figure in this pass | Third-party figures discarded; need charter/SOP confirmation |

### 3.3 Indicative Telugu form labels (UNVERIFIED English gloss — do not implement from this alone)

The official PDF appears to collect applicant identity/address/purpose/residence-duration and ID numbers, plus declaration/signature and supporting-doc checklist. **Treat any English rendering below as ASSUMPTION until bilingual official confirmation:**

ASSUMED labels pending verification: applicant name; father/husband name; door no.; street/locality; village/town; mandal; date of birth; purpose; years of residence; ration card no.; Aadhaar no.; voter ID no.; declaration; signature; enclosures (application, ration/EPIC/Aadhaar, utility/house-tax proof).

### 3.4 Residence blockers (if selected)

| ID | Blocker |
|---|---|
| R1 | Authoritative English (or bilingual) field schema from official form / portal |
| R2 | Package format decision (same as B2) |
| R3 | Form reproduction permissions (same as B3) |
| R4 | Confirm General vs Passport scope for MVP (recommend **General only**) |
| R5 | Confirm fee/SLA from authoritative charter/SOP |

---

## 4. Assumptions (explicit)

| ID | Assumption | Impact if wrong |
|---|---|---|
| A1 | Online-first AP services still benefit from an assistive preparation package | Package value changes; worksheet may still help |
| A2 | District supporting-doc lists for Residence match current MeeSeva practice statewide | May need portal confirmation |
| A3 | Regular Income Certificate field capture is possible via authenticated portal walkthrough | If not, Income remains blocked indefinitely for form mapping |

---

## 5. Product implications for package generation

Until B2/R2 and acceptance are decided:

- Do **not** claim a generated PDF is the official government form.  
- Prefer framing: **assistive application worksheet + supporting-document pack + portal/MeeSeva step checklist**.  
- Deterministic mapping to an “official form facsimile” remains blocked without schema + rights.

---

## 6. Change detection (RECOMMENDATION)

1. Re-check MeeSeva Application Forms index and APSEVA SOP/user manuals quarterly.  
2. Capture portal field schemas with dated screenshots/hashes into `ServiceDefinition` changelog.  
3. Never silently mutate published service definition versions.

---

## 7. Synthetic development policy

Synthetic identities/documents only until compliance approval. No real Aadhaar, PAN, passport, or citizen income documents to external AI.

---

## 8. Recommended pilot choice (M2 closure)

| Option | Recommendation |
|---|---|
| **Stay on Income Certificate** | Only if product owner accepts **assistive worksheet + checklist** (clears B2 as non-facsimile) **and** commits to B1 portal field capture before any “official form” claims |
| **Switch preferred pilot to Residence Certificate (General)** | **RECOMMENDED for faster form-artifact progress** — official blank PDF exists; supporting docs verified on district sites; still requires R1–R5 before full M3 |
| Implement both | **Rejected** for MVP |

**Engineering recommendation:** Ask product owner to **select Residence Certificate (General)** as the first official workflow **or** explicitly approve Income Certificate assistive-only package scope. Until that decision + field schema evidence, **M3 service-catalog / application-engine implementation must not proceed**.

---

## 9. Can M3 proceed?

| M3 workstream | Allowed now? |
|---|---|
| Full service definition with official field mapping + form template claims | **No** — BLOCKED |
| Application engine / PDF package generator for official facsimile | **No** — BLOCKED |
| Scaffolding against a *provisional* assistive worksheet after PO decision on pilot + B2/R2 | **Only after explicit product-owner approval** (not started in this task) |
| Continue Income Certificate research / Residence bilingual field capture | **Yes** (research only) |
