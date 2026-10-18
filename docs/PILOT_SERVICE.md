# Pilot Service Validation

**Status:** Residence Certificate (General) — provisional assistive workflow; **M3 NOT READY**  
**Last researched:** 2026-10-18  
**Provisional first workflow:** Andhra Pradesh Residence Certificate (General)  
**Service key (draft only):** `ap.revenue.residence_certificate.general`  
**Publication status:** `draft` — not active, not selectable  
**Excluded:** Residence Certificate (Passport)  
**Future candidate:** Income Certificate  
**Legal availability:** **R-GO BLOCKED** — see `M3_SERVICE_SCHEMA_RESEARCH.md` and `M3_READINESS_REPORT.md`

Do not implement the service catalog, application engine, or PDF generator from this document.

Do not use the EWS Income & Asset Certificate form as a substitute for the regular Income Certificate.

---

## 1. What is decided, and what is not

| Item | Status |
|---|---|
| Provisional pilot choice | Residence Certificate (General), as an assistive worksheet |
| Package format (D4) | Worksheet + supporting-document checklist + missing-information checklist + official submission instructions + disclaimer |
| Government API or direct submission | Excluded |
| Aadhaar storage or extraction | Excluded until legal approval |
| Passport residence variant | Excluded |
| Income Certificate | Future candidate; field schema still missing |
| G.O.Ms.No.592 operative effect | **BLOCKED** |
| Whether the General service is currently authorized | **Not established** |
| M3 implementation | **Not authorized** |

---

## 2. Residence Certificate (General) — evidence summary

Detail, the bilingual field inventory, and the draft specification are in `M3_SERVICE_SCHEMA_RESEARCH.md`. This section is the pilot conclusion.

| Question | Result |
|---|---|
| Do current district `.ap.gov.in` pages advertise the service? | **Yes.** General and Passport, accessed 2026-10-18 |
| Is there one official English field list? | **No** |
| Was the Telugu blank form read? | **Yes, visually**, from the Internet Archive capture (2015-07-01) of the MeeSeva PDF URL. Embedded text is not readable Unicode. A live byte-for-byte match on 2026-10-18 was not completed |
| Is that form linked from the current MeeSeva forms index? | **No**, on the index fetched 2026-10-18. The historical PDF URL still returned a document to a content fetch the same day |
| Does the GSWS CSP manual list it among 35 Revenue services? | **No**, in the manual fetched 2026-10-18 |
| Fee and processing time | **Not found** in the district pages or that manual |
| Does the blank form match the 2026 district document list? | **No.** Conflict recorded below |
| Does the advertised General service match G.O.Ms.No.592? | **Cannot be determined.** The order text was not obtained, and secondary accounts conflict |

### 2.1 Document-list conflict (do not merge silently)

**District service pages (English, 2026-10-18), labeled “Required Documents”:**

1. Application Form  
2. Ration Card / EPIC Card / Aadhaar Card  
3. House Tax / Telephone Bill / Electricity Bill  
4. Photo — mandatory only for Residence Passport, which this product excludes  

**Telugu blank form enclosure line (archive capture 2015-07-01):**

1. Application form  
2. Ration card number / bank pass book / driving licence / Aadhaar card  
3. House tax receipt / electricity bill / telephone bill  

The form has no photograph box. EPIC is a numbered data field on the form and a listed document on the district pages. Bank pass book and driving licence appear on the form’s enclosure line and not on the district pages reviewed.

### 2.2 Channels named on government pages

| District page | Channel named on the page | Status URL on the page | Accessed |
|---|---|---|---|
| Visakhapatnam, Ananthapuramu, West Godavari, NTR | MeeSeva centre | `http://ap.meeseva.gov.in/DeptPortal/UserInterface/LoginForm.aspx` | 2026-10-18 |
| Kakinada | Grama Sachivalayam | `https://gramawardsachivalayam.ap.gov.in/gsws/Landing/citizen-corner.html` | 2026-10-18 |

An indexed snippet of the Kakinada page displayed “Last Updated: Sep 05, 2026”, which is before 16 September 2026. The body fetched on 18 October 2026 still describes General and Passport. These pages are not evidence that the service was revised to match a 16 September 2026 order.

Offline acceptance of a private worksheet was not verified. The product must not claim that a downloaded worksheet is the application the office will accept.

---

## 3. Assistive package (specified, not built)

When implementation is later approved, the package is:

1. Citizen information worksheet, using only the reviewed form fields plus the product-defined district field in the draft spec.  
2. Supporting-document checklist that shows the district-page list and the form enclosure list as separate sources.  
3. Missing-information checklist derived from unmarked form lines the citizen has not filled.  
4. Official submission instructions with the district-page links above, telling the citizen to confirm current availability at that office.  
5. A disclaimer that the package is not an official government application, not an issued certificate, and not affiliated with the Government of Andhra Pradesh or MeeSeva.

No government logo, seal, signature, or certificate template.

Aadhaar is not printed, stored, or extracted. The worksheet tells the citizen that the official form has an Aadhaar line and that this product does not collect it.

---

## 4. Future candidate — regular Income Certificate

Retained, not selected. Do not use the EWS form as a substitute.

| Item | Status | Evidence |
|---|---|---|
| Service exists | VERIFIED | APSEVA SOP; GSWS CSP manual |
| Department / authority | VERIFIED | Revenue; Tahsildar / Deputy Tahsildar |
| SLA / fee | VERIFIED in the SOP | 7 days; ₹12 |
| Supporting documents | VERIFIED as a checklist | Application form; IT returns / pay slips / other income proof; Ration Card / EPIC / Aadhaar |
| Regular blank form on the MeeSeva forms index | **MISSING** | Index fetched 2026-10-18 lists EWS and Agricultural Income, not regular Income |
| Field schema | **BLOCKED** | |

Sources, accessed 2026-10-18:

- https://apseva.ap.gov.in/assets/User-Manuals/EoDB%20SOP%20final.pdf  
- https://apseva.ap.gov.in/assets/User-Manuals/CSP-User-Manual.pdf  
- https://vswsonline.ap.gov.in/#/home  
- http://ap.meeseva.gov.in/DeptPortal/Meeseva-Applications.html  

Prior blockers B1–B4 remain if Income is reopened. They do not authorize inventing Income fields.

---

## 5. Can M3 proceed?

| Workstream | Allowed now? |
|---|---|
| Research updates to these documents | Done for this pass |
| Publish `ap.revenue.residence_certificate.general` as an active service | **No** |
| Application engine or PDF generator | **No** |
| Claim that Residence Certificates are generally available under G.O.Ms.No.592 | **No** |

**Verdict: M3 is not ready.** See `M3_READINESS_REPORT.md`.
