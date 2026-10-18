# M3 Readiness Report

**Evidence date:** 2026-10-18  
**Verdict: M3 is NOT READY.**  
**Implementation:** not authorized. Stop after this report.

This report covers G.O.Ms.No.592, the 2015 conflict, the provisional pilot, the draft schema, the readiness gate, and the decisions still required. Field-level detail is in `M3_SERVICE_SCHEMA_RESEARCH.md`.

---

## 1. Government Order 592

**Not verified. R-GO remains BLOCKED.**

No Andhra Pradesh government-hosted copy of G.O.Ms.No.592 was obtained. `https://goir.ap.gov.in/` timed out on 2026-10-18. Searches of `ap.gov.in` and `goir.ap.gov.in` did not return the order. The Internet Archive CDX query used in this pass did not return a captured copy.

The date, department, and operative provisions are therefore not established from an official text. Secondary articles name Revenue (Ser.II), 16 September 2026, and Special Chief Secretary G. Sai Prasad. Those details are not adopted as verified facts.

### Evidence still missing

1. Official PDF or gazette text.  
2. Number, date, and department as printed on that copy.  
3. Operative paragraphs on G.O.Rt.No.581.  
4. Whether issuance is general or limited to named purposes.  
5. Issuing officer as named in the order.  
6. Any annexure or prescribed format.  
7. Any later clarification order. Press reports around 18–19 September 2026 describe a narrowing. Its number and text were not found on a government host.

---

## 2. Is the 2015 conflict resolved?

**No.**

G.O.Rt.No.581 dated 20 June 2015 is still the order understood to have stopped residence-certificate issuance. This pass also did not retrieve a government-hosted copy of that 2015 order. An indexed non-government PDF exists at `http://www.schoolinfo.yolasite.com/resources/2015REV_RT581.PDF` and is not treated as authentication.

Current district sites still advertise the service. Secondary accounts of G.O.Ms.No.592 disagree:

- Some say the 2015 order was repealed and issuance restored generally, including for education, employment, and electoral-roll work.  
- Others say issuance is only for PVTG Aadhaar enrolment or update, central-institution admissions, and central or armed-forces recruitment.  
- Andhra Jyothy (19 September 2026) reports that the 16 September order was then amended so that Aadhaar or a ration card remains ordinary address proof.

Those accounts cannot be turned into a repeal, a modification, or a supersession finding.

The advertised General service was **not** shown to match the 2026 order. District pages do not cite it. The Kakinada page snippet displayed an update date of 5 September 2026, before the reported order. The GSWS CSP manual fetched the same day omits Residence Certificate from its 35 Revenue services.

---

## 3. Recommended pilot service

**Keep Andhra Pradesh Residence Certificate (General) as the provisional first workflow, and do not build it yet.**

| Choice | Position |
|---|---|
| Residence Certificate (General) | Provisional pilot, assistive worksheet only |
| Residence Certificate (Passport) | Excluded |
| Income Certificate | Future candidate. Metadata and a document checklist exist. The regular field schema is still missing |
| Publish the service as active | No |
| Tell citizens the certificate is currently available for general purposes | No |

The recommendation to keep the provisional choice means the research target stays stable. It does not mean the legal gate is clear. If the product owner wants a service whose current authorization is already verified, this pilot does not meet that test, and implementation should wait.

---

## 4. Proposed service schema

Draft only: `ap.revenue.residence_certificate.general` version `0.1-draft`, status `draft`.

It separates:

- Verified district-page rules and document groups.  
- Reviewed English translations of the Telugu form, read visually from the 1 July 2015 archive capture of the MeeSeva PDF.  
- One product-defined field, `district_name`, because the form has no district line and the citizen needs it to find the right office.  
- Unverified portal items: fee, processing time, online field schema, and acceptance of a private worksheet.  
- Deferred Aadhaar, and the excluded Passport photograph.  
- Legal restrictions: no Aadhaar storage or extraction, no government marks, no affiliation, no claim of official submission.

M2 profile mapping that is allowed in the draft is narrow: verified `full_name` may propose `applicant_name`; verified `date_of_birth` may propose `date_of_birth`. Address lines are not split. Nothing else is auto-filled.

The proposed package, when a later milestone is approved, is:

1. Citizen information worksheet.  
2. Supporting-document checklist, with the district list and the form enclosure list kept apart.  
3. Missing-information checklist.  
4. Official submission instructions with the district links in `PILOT_SERVICE.md`.  
5. A disclaimer that this is not an official government application or an issued certificate.

---

## 5. Readiness gate

| Criterion | Result | Why |
|---|---|---|
| Service currently authorized and available | **BLOCKED** | R-GO unresolved. District pages advertise the service. The CSP manual omits it. Authorization is not established |
| Eligible applicant scenario confirmed | **BLOCKED** | Secondary sources conflict on whether any resident may apply or only specified purposes qualify |
| Field schema verified, or explicitly limited to a product-defined assistive worksheet | **PARTIAL** | The worksheet limit is explicit, and the Telugu labels were visually reviewed. The readable copy is a 2015 archive. The live file was not hash-matched. The form is absent from the current forms index. Required versus optional is unmarked on the form |
| Supporting-document checklist sourced | **PARTIAL** | District pages agree with each other and were fetched from government hosts. They do not agree with the blank form’s enclosure line |
| Submission instructions validated | **PARTIAL** | Government pages name MeeSeva or a Grama Sachivalayam and give status URLs. They do not validate a private worksheet as an accepted application, and the channel is not the same on every district page |
| Legal restrictions documented | **PARTIAL** | Aadhaar exclusion, no direct submission, and no government affiliation are recorded. The legal effect of the 2015 and 2026 orders is not |
| Product-owner approval | **BLOCKED** | The provisional service and the worksheet format are recorded. Approval to implement M3 has not been given |

No criterion is a full PASS. Material blockers remain.

---

## 6. Documents changed

| Document | Change |
|---|---|
| `docs/DECISIONS.md` | Recorded M2 approval, D4, D5, Passport exclusion, Income as a future candidate, Aadhaar exclusion, R-GO blocked, M3 not authorized |
| `docs/PILOT_SERVICE.md` | Reset the pilot to Residence Certificate (General) and retained Income Certificate evidence as a future candidate |
| `docs/MVP_REQUIREMENTS.md` | Pointed the M3 gate at this verdict |
| `docs/MILESTONES.md` | Marked M2 approved for synthetic local development and M3 not authorized |
| `docs/M3_SERVICE_SCHEMA_RESEARCH.md` | Created. Order search, field inventory, draft specification |
| `docs/M3_READINESS_REPORT.md` | Created. This report |

No M1 or M2 application code was modified. The service catalog, application engine, and PDF generator were not implemented.

---

## 7. Verdict

**M3 is not ready.**

Do not declare the service active. Do not implement the catalog, engine, or package generator.

---

## 8. Decisions required from the product owner

1. Accept R-GO as BLOCKED, and accept that the worksheet must not state that a General Residence Certificate is currently authorized.  
2. Either keep Residence Certificate (General) as the provisional research target under that limit, or pause the pilot until an official copy of G.O.Ms.No.592 and any September 2026 clarification is obtained.  
3. Approve or reject draft `0.1-draft`, including reviewed translations and the single product-defined district field. Approving the draft is not approval to code it.  
4. Confirm that Aadhaar stays off the worksheet even though the official form prints an Aadhaar line.  
5. Confirm that the document checklist must show the district-page list and the form enclosure list as a conflict, not as one merged list.  
6. Confirm Passport remains excluded and Income Certificate remains a future candidate.  
7. Give or withhold authorization to start M3 implementation.

**Recommendation: withhold implementation authorization.**

Work stops here pending those decisions.
