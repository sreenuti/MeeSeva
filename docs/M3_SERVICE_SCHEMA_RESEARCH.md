# M3 Service Schema Research

**Status:** Research only. Specification version `0.1-draft` is **not published** and **not authorized for implementation**.  
**Evidence date:** 2026-10-18  
**Service key:** `ap.revenue.residence_certificate.general`  
**Jurisdiction:** Andhra Pradesh, Revenue  
**Companion:** `M3_READINESS_REPORT.md`, `PILOT_SERVICE.md`, `DECISIONS.md`

No M1 or M2 application code was changed for this research.

---

## 1. How to read evidence labels

| Label | Meaning |
|---|---|
| Verified rule | Read from an Andhra Pradesh government host on the evidence date |
| Reviewed translation | English rendering after visual reading of the Telugu form. Not an official government English edition |
| Product-defined | Added for the assistive worksheet. Not printed on the government form |
| Unverified portal requirement | Mentioned on a government page, but not confirmed in a portal field schema or order |
| Deferred | Present on a source, and intentionally out of the product |
| Legal restriction | Must not be implemented or asserted |

Machine extraction of the Telugu PDF did not produce readable Unicode. Labels below were read from a rendered page. They are reviewed translations, not a second official text.

---

## 2. G.O.Ms.No.592 — verification result

**Result: R-GO is BLOCKED.**

An official Andhra Pradesh government-hosted copy was not obtained on 2026-10-18. Secondary news and blog articles are not treated as legal verification. They also disagree with each other, so they cannot be reconciled into an operative rule.

### 2.1 Retrieval attempts

| Attempt | URL or query | Evidence date | Result |
|---|---|---|---|
| Government orders portal | https://goir.ap.gov.in/ | 2026-10-18 | Connection timed out from this environment (`ERR_CONNECTION_TIMED_OUT` / curl timeout). No order text retrieved |
| Indexed government-domain search | `G.O.Ms.No.592` with 16 September 2026, limited to `ap.gov.in` and `goir.ap.gov.in` | 2026-10-18 | No government-hosted copy of this order |
| Wayback CDX for `goir.ap.gov.in` paths containing `592` | web.archive.org CDX | 2026-10-18 | No captured object returned |
| MeeSeva / district / APSEVA pages reviewed in this pass | Listed in §4 | 2026-10-18 | None quotes G.O.Ms.No.592 |

### 2.2 What remains missing

Legal verification needs all of the following. None of them is in hand:

1. A PDF or gazette text hosted on `goir.ap.gov.in`, `ap.gov.in`, the Chief Commissioner of Land Administration, or the Andhra Pradesh Gazette.  
2. The printed order number, date, and department on that copy.  
3. The operative paragraphs: whether G.O.Rt.No.581 dated 20 June 2015 is repealed, modified, or superseded, and from which date.  
4. Whether certificates may be issued generally or only for named purposes.  
5. The designated issuing officer, as named in the order.  
6. Any enclosed application or certificate format.  
7. Any later September 2026 clarification or amendment, including its number and date. Newspaper accounts describe a narrowing around 18 September 2026. No order number for that clarification was verified.

### 2.3 Secondary accounts (not verification)

Recorded only to show the conflict. Do not implement from this table.

| Source | Date on the article | What it claims | Why it is not enough |
|---|---|---|---|
| The New Indian Express, “Andhra Tahsildars empowered to issue residence certificates” | Updated 17 Sep 2026 | G.O.Ms.No.592 repealed G.O.Rt.No.581 immediately and restored Tahsildar issuance. Reasons described include employment, education, electoral-roll revision, and PVTG Aadhaar. Local enquiry if documents are absent | News report. No order text |
| https://www.teachersbook.in/2026/09/ap-residence-certificate-re-introduced.html | September 2026 | Full repeal and general restoration by Revenue (Ser.II); Tahsildars; QR-enabled format | Blog. No government PDF |
| https://www.gswshelper.com/2026/09/ap-govt-go-ms-592-residence-certificate-new-rules-2026.html | 18 Sep 2026 | Purpose-limited restoration: PVTG Aadhaar, central-institution admissions, central and armed-forces recruitment. Describes a partial modification rather than a clean repeal | Blog. Conflicts with the New Indian Express account |
| Andhra Jyothy, Aadhaar and ration cards as address proof | Published 19 Sep 2026, dateline 18 Sep | Says the 16 September order was then fundamentally amended: Aadhaar or ration card remains address proof for ordinary needs; certificates described for tribal Aadhaar updates, central admissions, jobs, and the army | News report of a clarification. The clarification’s own order number was not retrieved |

Until the missing items in §2.2 are filed, this project does not decide whether G.O.Rt.No.581 was repealed, modified, or superseded, and does not decide whether Residence Certificates are available generally or only for specified purposes.

### 2.4 The 2015 conflict

The earlier conflict stands.

- District government pages still advertise Residence Certificate — General and Passport.  
- G.O.Rt.No.581, Revenue (Ser.II), dated 20 June 2015, is the order previously understood to have stopped Revenue authorities from issuing residence certificates and to have directed use of ration cards or Aadhaar for state-government business.  
- This pass did not retrieve an `ap.gov.in` or `goir.ap.gov.in` copy of G.O.Rt.No.581 either. An indexed non-government PDF is at `http://www.schoolinfo.yolasite.com/resources/2015REV_RT581.PDF`. That host is not authentication.  
- G.O.Ms.No.592 is reported by secondary sources to have changed that 2015 position, and a further narrowing is also reported. Neither instrument was authenticated.

**The 2015 conflict is not resolved.**

### 2.5 Match to the current General service

**Not established.**

The district pages reviewed on 2026-10-18 still describe an ordinary General service and a separate Passport service. They do not cite G.O.Ms.No.592, and the Kakinada snippet’s displayed update date (5 September 2026) is before 16 September 2026. The current GSWS citizen-service manual’s list of 35 Revenue services does not include Residence Certificate. Those facts do not prove the General service matches, or fails to match, an order this review could not read.

---

## 3. Telugu form — what was actually read

| Item | Value |
|---|---|
| Live URL | https://ap.meeseva.gov.in/DeptPortal/Application%20Forms%20New/Revenue-pdf/REVENUE%20-%20RESIDENCE-Telugu.pdf |
| Readable copy used | https://web.archive.org/web/20150701174554/http://ap.meeseva.gov.in/DeptPortal/Application%20Forms%20New/Revenue-pdf/REVENUE%20-%20RESIDENCE-Telugu.pdf |
| Archive capture date | 2015-07-01 |
| Pages | 1 |
| Review method | Rendered to an image and read visually on 2026-10-18. Embedded text extraction is not readable Telugu |
| Live check the same day | A content fetch of the live URL returned a one-page PDF with the same 12 numbered rows. Direct download timed out, so the live file was **not** hash-compared with the 2015 capture |
| Forms index | http://ap.meeseva.gov.in/DeptPortal/Meeseva-Applications.html fetched 2026-10-18 does **not** list this form under Revenue |

Title read from the form: **నివాస ధృవీకరణ పత్రము కొరకు ధరఖాస్తు**  
Reviewed translation: **Application for a residence certificate**

The page header contains the MeeSeva emblem. This product must not reproduce that emblem, or any government seal, signature, or certificate layout.

The form does not print asterisks. This inventory therefore does not mark numbered lines as mandatory. “Unmarked” means the form does not say.

The form has no photograph box and no separate Passport section. It is the General blank that was reviewed. Passport remains excluded.

---

## 4. Bilingual field inventory

Sources:

- **F-2015** — Telugu form, archive capture 2015-07-01 of the MeeSeva URL, visual review 2026-10-18.  
- **D-2026** — district service pages fetched 2026-10-18:  
  - https://visakhapatnam.ap.gov.in/service/residence-certificate/  
  - https://kakinada.ap.gov.in/service/residence-certificate/  
  - https://ananthapuramu.ap.gov.in/service/residence-certificate/  
  - https://westgodavari.ap.gov.in/service/residence-certificate/  
  - https://ntr.ap.gov.in/service/residence-certificate-19/  
- **CSP** — https://apseva.ap.gov.in/assets/User-Manuals/CSP-User-Manual.pdf fetched 2026-10-18. Residence Certificate is absent from the 35-service Revenue table. The manual’s own publication date is not printed on the extracted cover.  
- **M2** — profile keys already produced by the synthetic extractor: `full_name`, `date_of_birth`, `synthetic_identifier`, `address_line`, `city`, `village`, `district`, `state`, `postal_code`, `income_amount`, `income_period`, `income_source`, `currency`.

### 4.1 Fields printed on the form

| Key | Telugu label | Reviewed English | Data type | Status on the form | M2 profile mapping | Source | Verification |
|---|---|---|---|---|---|---|---|
| `applicant_name` | దరఖాస్తుదారుని పేరు | Applicant’s name | string | Unmarked | `full_name` | F-2015 | Reviewed translation |
| `father_or_husband_name` | తండ్రి / భర్త పేరు | Father’s or husband’s name | string | Unmarked | None | F-2015 | Reviewed translation |
| `house_number` | ఇంటి నెంబర్ | House number | string | Unmarked | None. `address_line` is one line and must not be split automatically | F-2015 | Reviewed translation |
| `street_or_ward_number` | వీధి / వార్డు నెంబర్ | Street or ward number | string | Unmarked | None | F-2015 | Reviewed translation |
| `village_or_town` | గ్రామము / పట్టణము | Village or town | string | Unmarked | `village` only when the value is a village. A town must not be forced into `village` or `city` | F-2015 | Reviewed translation |
| `mandal` | మండలము | Mandal | string | Unmarked | None | F-2015 | Reviewed translation |
| `date_of_birth` | పుట్టిన తేది | Date of birth | date | Unmarked | `date_of_birth` | F-2015 | Reviewed translation |
| `place_of_birth` | పుట్టిన ప్రదేశం | Place of birth | string | Unmarked | None | F-2015 | Reviewed translation |
| `years_at_present_residence` | ప్రస్తుత నివాస స్థలములో ఎన్ని సంవత్సరములనుండి నివసించుచున్నారు | How many years have you been residing at the present place of residence? | number of years | Unmarked | None | F-2015 | Reviewed translation |
| `ration_card_number` | రేషన్ కార్డు నెంబర్ | Ration card number | string | Unmarked | None | F-2015 | Reviewed translation |
| `aadhaar_number` | ఆధార్ నెంబర్ | Aadhaar number | identity number | Printed on the form. **Deferred.** Do not store or extract | None. Excluded | F-2015; D9 | Legal restriction |
| `epic_number` | ఓటు గుర్తింపు కార్డు నెంబర్ | Voter identity card (EPIC) number | string | Unmarked | None | F-2015 | Reviewed translation |
| `certificate_purpose` | నాకు …… నిమిత్తం | Blank in the declaration: the purpose for which the certificate is required | string | Unmarked fill-in. Not a numbered row | None | F-2015 | Reviewed translation |
| `cell_number` | సెల్ నెంబర్ | Cell number | string | Unmarked | None. Not a profile field | F-2015 | Reviewed translation |
| `applicant_signature` | అభ్యర్థి సంతకం | Applicant’s signature | signature | Present. Not collected as a stored profile value | None | F-2015 | Reviewed translation |
| `guardian_signature` | అభ్యర్థి తల్లి / తండ్రి / సంరక్షకుని సంతకం (మైనర్ అయినచో) | Signature of the applicant’s mother, father, or guardian (if the applicant is a minor) | signature | Conditional on the applicant being a minor, as printed | None | F-2015 | Reviewed translation |

Declaration paragraph printed under the table. Telugu as read from the render:

> నాకు ……………… నిమిత్తం నివాస ధృవీకరణ పత్రము కావలసియున్నది. కావున ఇచ్చించగోరుచున్నాను. పైన తెలిపిన విషయములన్నియు యథార్థములనియు ధృవీకరించుచున్నాను. అసత్యములని ధృవీకరించబడిన ఎడల ప్రభుత్వము వారు తీసుకొను అన్ని చర్యలకు బద్ధుడనై వుందునని ఇందుమూలముగా తెలియపరచుచున్నాను.

Reviewed translation:

> I require a residence certificate for the purpose of [blank]. I therefore request that it be issued. I certify that all the particulars stated above are true. If they are found to be false, I shall be bound by whatever action the Government takes.

The dotted blank is `certificate_purpose`. The English sentence is a reviewed translation. It is not an official government English text, and the product must not imitate the form’s declaration layout.

The residence-duration verb in row 9 was read as నివసించుచున్నారు (residing). Embedded PDF text cannot confirm that one akshara. The reviewed meaning is years lived at the present residence.

### 4.2 Enclosures printed on the form

| Key | Telugu | Reviewed English | Status | Source |
|---|---|---|---|---|
| `enclosure_application_form` | అప్లికేషన్ ఫారం | Application form | Printed as enclosure 1. The form does not say “mandatory” with an asterisk | F-2015 |
| `enclosure_identity_set_on_form` | రేషన్ కార్డు నెంబర్ / బ్యాంకు పాస్ బుక్ / డ్రైవింగ్ లైసెన్సు / ఆధార్ కార్డు | Ration card number / bank pass book / driving licence / Aadhaar card | Printed as one slash-separated enclosure line | F-2015 |
| `enclosure_address_set_on_form` | ఇంటి పన్ను రసీదు / కరెంట్ బిల్ / టెలిఫోన్ బిల్ | House-tax receipt / electricity bill / telephone bill | Printed as one slash-separated enclosure line | F-2015 |

### 4.3 Current district-page requirements (separate source)

These are verified as the words on the district pages. They are not a captured online form schema.

| Key | English text on the pages | Status | M2 mapping | Source | Verification |
|---|---|---|---|---|---|
| `doc_application_form` | Application Form | Listed under “Required Documents” | Document type, not a profile field | D-2026 | Verified rule |
| `doc_identity_district` | Ration Card / EPIC Card / Aadhaar Card | Listed as one required group. Aadhaar handling remains excluded in this product | Ration and EPIC have no profile keys. Aadhaar excluded | D-2026 | Verified rule for the page text. Portal required-ness of each alternative is unverified |
| `doc_premises_district` | House Tax / Telephone Bill / Electricity Bill | Listed as one required group | None | D-2026 | Verified rule for the page text |
| `doc_photo_passport_only` | Photo (mandatory if Residence Passport) | Out of scope. Passport variant is excluded | None | D-2026 | Verified rule; excluded from this service |
| `service_description` | Proof of permanent residence in a village, town, or ward, issued on the basis of stay at a place or permanent employment | Descriptive text, not a field | None | D-2026 | Verified rule |
| `service_variants` | General and Passport | Passport excluded | None | D-2026 | Verified rule |
| `service_category_wording` | “Category B”, with a sentence that it can be converted to Category A | Boilerplate on these pages. Not used as an SLA | None | D-2026 | Unverified portal requirement if treated as a processing rule |

### 4.4 Not on the form, and not invented as government fields

| Key | Treatment | Reason |
|---|---|---|
| `district_name` | Product-defined worksheet field | The blank form has village/town and mandal, not district. The citizen needs a district to open the correct government page. Label it as product-defined |
| `state` | Fixed jurisdiction “Andhra Pradesh” on the worksheet header | Not an applicant answer on this form. M2 `state` may be shown as context and must not be written onto a fake form |
| Gender, PIN code, religion, email, photograph, income | Not in this specification | Not on the reviewed General form |
| Fee, SLA, issuing officer | Not specified as facts | Not on the form. Not in the CSP Residence row, because that row does not exist. District pages do not state a fee or a number of days. Secondary articles name the Tahsildar; that is not verified from the order |

---

## 5. Draft service specification

**Not active. Do not load this into a catalog.**

```text
service_key: ap.revenue.residence_certificate.general
version: 0.1-draft
status: draft
effective_from: null
publication: withheld until product-owner approval after R-GO is resolved or explicitly waived
jurisdiction: Andhra Pradesh
department: Revenue
title: Residence Certificate (General) — assistive worksheet
output: assistive worksheet, not an official form and not a certificate
government_submission: none
aadhaar_storage: prohibited
aadhaar_extraction: prohibited
```

### 5.1 Rule classes inside the draft

| Class | Contents |
|---|---|
| Verified rules | District pages advertise General and Passport; document groups in §4.3; MeeSeva or Grama Sachivalayam named as the place to apply; status URLs in `PILOT_SERVICE.md`; forms index does not list this blank form; CSP manual’s 35 Revenue services omit it |
| Reviewed translations | §4.1 and §4.2 |
| Product-defined worksheet fields | `district_name`; a citizen confirmation that they have read the disclaimer; a prompt that missing unmarked lines should be completed on the official channel. No other extra identity fields |
| Unverified portal requirements | Online field schema, fee, SLA, whether a private worksheet is accepted, whether Category B wording changes the path, whether the service is open to every resident |
| Deferred fields | `aadhaar_number`; Passport photograph; any certificate template |
| Legal restrictions | No Aadhaar storage or extraction. No government logo, seal, or signature. No statement that the worksheet is a government application. No statement that G.O.Ms.No.592 authorizes general issuance. No API submission |

### 5.2 Worksheet behaviour, if later approved

- Map `full_name` to `applicant_name` and `date_of_birth` to `date_of_birth` only when the profile value is user-verified.  
- Do not map `address_line` into `house_number` or `street_or_ward_number`.  
- Do not invent `years_at_present_residence`, `certificate_purpose`, names of relatives, or identity numbers.  
- Leave `aadhaar_number` out of the worksheet entirely.  
- Show document requirements as two checklists: district-page group, and form enclosure group.  
- A missing unmarked field is reported as missing. It is not filled.  
- Guardian signature is shown only as a conditional instruction when the citizen says the applicant is a minor. The product does not collect a signature image in this draft.

### 5.3 Proposed package contents

Specified for a later milestone. Not generated now.

1. **Citizen information worksheet** — the §4.1 fields except Aadhaar, plus product-defined `district_name`.  
2. **Supporting-document checklist** — §4.2 and §4.3 kept distinct.  
3. **Missing-information checklist** — any included field or document group with no verified value.  
4. **Official submission instructions** — links in `PILOT_SERVICE.md` §2.2, plus a line to confirm at that office whether a General Residence Certificate is being issued.  
5. **Disclaimer** — this package is not an official government application, not an issued certificate, and not affiliated with the Government of Andhra Pradesh or MeeSeva.

---

## 6. Eligibility, channel, fee, time

| Topic | Finding | Label |
|---|---|---|
| Eligibility | District pages describe permanent residence in a village, town, or ward, based on stay or permanent employment. No tighter statutory test was verified. Purpose limits reported in secondary accounts of G.O.Ms.No.592 are not adopted | Verified description on district pages; legal eligibility **blocked** with R-GO |
| Minor applicants | Form asks for a parent or guardian signature if the applicant is a minor | Reviewed translation |
| Channel | MeeSeva centre on four district pages; Grama Sachivalayam on the Kakinada page. No authenticated portal field list | Verified as page text; portal schema unverified |
| Fee | Not stated on the sources in §4 | Unverified |
| Processing time | Not stated. Category B wording is not an SLA | Unverified |

---

## 7. Change control

Version `0.1-draft` stays draft. A later version may be published only after:

1. An official copy of G.O.Ms.No.592, and of any later clarification, is filed and the eligibility section is rewritten from that text; or the product owner explicitly accepts a worksheet that refuses to state legal availability.  
2. The product owner approves the field inventory, including omission of Aadhaar.  
3. The document-list conflict is either resolved from a current official form or left visible in the checklist.  
4. Implementation is separately authorized. This document does not authorize it.
