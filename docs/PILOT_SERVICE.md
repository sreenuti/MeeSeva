# Pilot Service — Andhra Pradesh Income Certificate

**Status:** BLOCKED for implementation (partially verified)  
**Last researched:** 2026-10-18  
**Preferred pilot:** AP Income Certificate (Revenue)  
**Fallback:** AP Residence Certificate (documented below; not selected for dual MVP)

---

## 1. Verification summary

| Item | Status | Notes |
|---|---|---|
| Service exists officially | VERIFIED | Listed in AP GSWS/APSEVA materials |
| Responsible department | VERIFIED | Revenue Department |
| Competent authority | VERIFIED | Tahsildar / Deputy Tahsildar |
| SLA | VERIFIED | 7 days (official SOP/user manual) |
| Fee | VERIFIED | ₹12 (official SOP) |
| Supporting documents (checklist) | VERIFIED (high level) | Application form; IT returns/pay slips/other income proof; Ration Card / EPIC / Aadhaar |
| Official online submission channel | VERIFIED | APSEVA / VSWS online citizen login |
| Complete field-level form schema (regular Income Certificate) | UNVERIFIED / MISSING | No authoritative English field list captured for the current online service application form |
| Downloadable official blank form suitable for offline package | UNVERIFIED / MISSING | EWS form found; regular Income Certificate field form not verified as equivalent |
| Form reproduction / usage permissions | UNVERIFIED | Rights to regenerate official form layout unknown |
| Generated package usable as official submission artifact | UNVERIFIED / LIKELY CONSTRAINED | Primary channel is online portal upload/payment; offline print package may be assistive only |
| Applicant scenarios (individual vs parent income) | PARTIALLY VERIFIED | CSP manual: “Individual as well as based on Parent income” — field details not captured |
| Signature / undertaking requirements | PARTIALLY VERIFIED | SOP notes citizen may give an undertaking; wet-ink signature rules for offline path unclear |
| Change-detection process for requirements | RECOMMENDATION only | See §8 |

**Implementation readiness:** BLOCKED until blockers in §9 are cleared or product owner switches to fallback service and validates that path.

---

## 2. Official sources consulted

| # | Source | URL | Accessed | What it confirmed |
|---|---|---|---|---|
| S1 | APSEVA Ease of Living SOP (Income Certificate section) | https://apseva.ap.gov.in/assets/User-Manuals/EoDB%20SOP%20final.pdf | 2026-10-18 | Authority, SLA 7 days, docs checklist, procedure, fee ₹12, submission URL |
| S2 | GSWS CSP User Manual | https://apseva.ap.gov.in/assets/User-Manuals/CSP-User-Manual.pdf | 2026-10-18 | Service listed; SLA; approval flow DA→VRO→RI→Deputy Tahsildar/Tahsildar; docs checklist; purpose (loans/fee reimbursement); individual/parent income |
| S3 | APSEVA / VSWS submission entry | https://vswsonline.ap.gov.in/#/home | 2026-10-18 | Cited in SOP as form submission channel |
| S4 | MeeSeva EWS Income & Asset Certificate form (related, not same service) | https://ap.meeseva.gov.in/DeptPortal/Application%20Forms%20New/Revenue-pdf/Issuance%20of%20Income%20%20Asset%20Certificate%20%20for%20%20Economically%20Weaker%20Sections(EWS)ApplicationForm.pdf | 2026-10-18 | Full EWS field list — **do not treat as Income Certificate schema** |
| S5 | Kadapa district notice (revised orders) | https://kadapa.ap.gov.in/te/notice/issue-of-income-certificate-by-the-revenue-authorities-revised-orders-issued-date-04-07-2017-1214-2/ | 2026-10-18 | Confirms existence of revised government orders; PDF content not fully extracted in this research pass |

**Not used as authoritative field sources:** third-party form aggregators.

---

## 3. Verified service definition (high level)

| Attribute | Value | Source |
|---|---|---|
| Service name | Income Certificate | S1, S2 |
| State / jurisdiction | Andhra Pradesh | S1, S2 |
| Department | Revenue | S1, S2 |
| Competent authority | Tahsildar / Deputy Tahsildar | S1, S2 |
| Purpose (descriptive) | Certificate of income for individual or based on parent income; used for loans and fee reimbursements | S2 |
| Applicability | Anyone who wants an Income Certificate | S1 |
| SLA | 7 days | S1, S2 |
| Fee | ₹12 | S1 |
| Category (GSWS) | B | S2 |
| Workflow (portal) | Citizen/DA application → VRO verify (field visit if needed) → RI reverify → Tahsildar/Deputy Tahsildar approve | S1, S2 |

### Verified supporting documents

From S1/S2 checklist:

1. Application form  
2. Copy of IT Returns / Pay Slips (or any other income-proof documents)  
3. Ration Card / EPIC Card / Aadhaar Card  

**Do not invent** additional mandatory documents for MVP mapping until confirmed.

---

## 4. Official procedure (citizen path)

From S1:

1. Citizen logs into APSEVA portal.  
2. Selects Income Certificate service and fills online application.  
3. Uploads documents, pays online, submits.  
4. May give an undertaking.  
5. VRO → RI → Tahsildar/Deputy Tahsildar processing.  
6. Citizen tracks by application number; downloads/prints certificate when approved.

**Product implication:** The official happy path is **online submission**, not primarily an offline wet-ink form drop-off. Our MVP package is therefore best framed as an **application-preparation aid** (structured draft + supporting pack + instructions) unless offline acceptance is separately verified.

---

## 5. Field / template status

### Regular Income Certificate (pilot target)

| Artifact | Status |
|---|---|
| Online service application field list | NOT CAPTURED from authoritative walkthrough of current portal screens |
| Offline blank PDF matching current service | NOT VERIFIED |
| Mapping sheet for profile → form fields | BLOCKED (depends on field list) |
| Form template license for regeneration | UNKNOWN |

### Related forms (do not substitute silently)

| Artifact | Status |
|---|---|
| EWS Income & Asset Certificate application form | Available (S4); **different service** |
| Agriculture Income Certificate form | Separate service in CSP catalog |

---

## 6. Open questions

1. Exact mandatory/optional fields on the current APSEVA Income Certificate service form (including village/mandal, income year, income breakup, parent vs self).  
2. Whether a printable application PDF is still accepted at MeeSeva/GSWS centers as a primary path.  
3. Whether our generated PDF may reproduce official form layout or only a citizen worksheet + portal fill checklist.  
4. Undertaking / declaration text that must appear verbatim.  
5. Photo requirements (if any) for regular Income Certificate.  
6. Validity period of issued certificate and renewal patterns.  
7. Current G.O. / circular governing issuance (follow S5 PDF and CCLA/Revenue circulars).  
8. Aadhaar: optional vs practically required in portal UX (EWS form marks Aadhaar optional; regular service unknown).

---

## 7. Feasibility assessment

| Dimension | Assessment |
|---|---|
| Product fit | HIGH — clear citizen pain; documents + income data map well to vault/profile model |
| Technical fit for vault/profile/HITL | HIGH |
| Deterministic form mapping | BLOCKED — missing field schema |
| Official package acceptance claim | BLOCKED — online-first channel |
| Assistive preparation without claiming official submission | FEASIBLE — recommended MVP framing if blockers remain |
| Compliance sensitivity | HIGH — identity + income documents |

**Recommendation:** Keep Income Certificate as preferred pilot, but unblock M3 only after field capture **or** explicitly approve an “assistive worksheet + portal checklist” package format that does not claim to be the official form.

---

## 8. Detecting requirement changes (RECOMMENDATION)

1. Quarterly review of APSEVA SOP/user manuals and MeeSeva Revenue forms directory.  
2. Manual walkthrough of published citizen portal screens; screenshot/hash field schema into `ServiceDefinition` changelog.  
3. Track district/CCLA G.O. notices for income certificate rules.  
4. Retire prior `ServiceDefinition` versions; never silently mutate published versions used by in-flight applications.

---

## 9. Implementation blockers (must clear before M3)

| ID | Blocker | Owner |
|---|---|---|
| B1 | Capture authoritative field-level schema for current Income Certificate online form | Product + research |
| B2 | Decide package format: official-form facsimile vs assistive worksheet + portal checklist | Product owner |
| B3 | Confirm form usage/reproduction permissions | Legal / product |
| B4 | Validate whether package supports any official offline channel, or online-assist only | Product |
| B5 | Write versioned `ServiceDefinition` from verified evidence only | Engineering (after B1–B4) |

Until B1–B4 are resolved, mark workflow **BLOCKED**. Do not invent fields.

---

## 10. Fallback — Residence Certificate (not dual-MVP)

Documented for contingency if Income Certificate remains blocked.

| Attribute | Value | Source examples |
|---|---|---|
| Service | Residence Certificate (General / Passport variants) | District sites e.g. https://prakasam.ap.gov.in/service/residence-certificate/ |
| Supporting docs | Application form; Ration/EPIC/Aadhaar; House tax / telephone / electricity bill; Photo mandatory for Passport type | Same |
| Portal | MeeSeva / district guidance | District pages + ap.meeseva.gov.in |
| Form PDF | Telugu residence form exists under MeeSeva Revenue forms | https://ap.meeseva.gov.in/DeptPortal/Application%20Forms%20New/Revenue-pdf/REVENUE%20-%20RESIDENCE-Telugu.pdf |

Fallback also requires field-level verification and package-format decision before M3. **Do not implement both services in MVP.**

---

## 11. Synthetic development policy

Until compliance approval: use only synthetic identities and synthetic income/ID document images. No real Aadhaar, PAN, passport, or citizen income documents in external AI pipelines.
