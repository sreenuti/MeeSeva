# Security & Privacy

**Status:** M0 baseline — design requirements, not a compliance certification  
**Last updated:** 2026-10-18

This document distinguishes **verified legal research items** from **design assumptions**. Do not claim regulatory compliance without qualified legal review.

---

## 1. Data classification

| Class | Examples | Handling |
|---|---|---|
| Public | Marketing site copy, published service catalog titles | Standard web controls |
| Account | Email, phone, IdP subject | Access-controlled; minimize |
| Identity documents | Aadhaar, voter ID, ration card images | Highly sensitive; private storage; extraction controls |
| Financial / income | ITR, payslips, declared income | Highly sensitive |
| Derived profile | Name, DOB, address, income fields | Sensitive; provenance retained |
| Audit | Security events | Protected; avoid embedding secrets/PII values |

---

## 2. Threat model (initial)

| Threat | Example | Mitigations |
|---|---|---|
| Account takeover | Stolen password | Managed IdP + MFA; session controls |
| Broken object access | IDOR on document/package IDs | Ownership checks on every read/write |
| Malicious upload | Malware, polyglot files | Type/size validation; malware scanning; isolate processing |
| Storage exposure | Public bucket / leaked keys | Private buckets; short-lived signed URLs; no long-lived client creds |
| Prompt injection via documents | Hidden text influencing LLM | Treat document text as untrusted; constrain tools; grounded KB only for assistant; structured extraction schemas |
| Sensitive data in logs | OCR text logged | Redaction policies; structured logging allowlists |
| AI data leakage | Real PII to unapproved model | Provider allowlist; DPA; synthetic-only until approval |
| Insider misuse | Support browsing vault | No broad admin document browser in MVP; audited break-glass later |
| Supply chain | Dependency compromise | Lockfiles; minimal deps; updates |
| Insufficient deletion | “Delete” leaves objects | Cascading delete verification in M6 |

---

## 3. Security controls (MVP architecture)

1. **Authentication:** Managed IdP; MFA required.  
2. **Authorization:** Least privilege; user-scoped queries; deny by default.  
3. **Transport:** TLS everywhere.  
4. **At rest:** DB and object storage encryption.  
5. **Secrets:** Env/secret manager; never commit secrets.  
6. **Vault:** Private storage; content validation; malware scan design; signed short-lived access.  
7. **AI:** Pluggable providers; schema validation; no silent verify; minimize payload.  
8. **Audit:** Append-oriented security/business events without document bodies.  
9. **Backups:** Encrypted backups before pilot; tested restore.  
10. **Incident response:** Document owner contacts + containment runbook before pilot (M6).  

---

## 4. Consent, purpose limitation, minimization

| Principle | MVP application |
|---|---|
| Consent | Capture purpose-bound consents (storage, extraction, application prep, notifications) |
| Purpose limitation | Do not reuse vault docs for unrelated training/marketing |
| Minimization | Profile fields limited to pilot service needs |
| User control | Correction, verification, deletion, package download under user intent |
| Transparency | Clear UI that AI values are unverified until accepted |

---

## 5. Retention and deletion

| Data | Retention direction |
|---|---|
| Active vault docs | Until user delete or account deletion |
| Soft-deleted objects | Short grace period then hard purge |
| Application packages | Until user delete / policy window |
| Consent + critical audit | Retain longer as legally advised |
| Extractions | Tied to document versions |

**M6 gate:** Prove account deletion removes DB rows and storage objects (except legally required records).

---

## 6. Regulatory research items (India)

> Not legal advice. Flag for counsel.

### Digital Personal Data Protection Act, 2023 (DPDP)

| Topic | Relevance | Status |
|---|---|---|
| Personal data processing basis / consent | Core to vault + AI extraction | RESEARCH — implement consent UX; counsel to confirm notice/consent text |
| Significant Data Fiduciary obligations | May apply depending on volume/sensitivity | UNVERIFIED whether platform will be designated |
| Cross-border transfer | Provider/region choice | OPEN with hosting/provider decisions |
| Data Principal rights | Access, correction, erasure | Design for correction/deletion; counsel for full rights set |
| Children’s data | Avoid targeting minors | UNVERIFIED age policy — RECOMMEND 18+ for MVP |

### Aadhaar-related restrictions

| Topic | Relevance | Status |
|---|---|---|
| Storage / display / sharing of Aadhaar numbers | High | BLOCKER for production: legal review before collecting/storing/extracting Aadhaar |
| Use of Aadhaar for authentication | Not in MVP | Do not integrate UIDAI auth without authorization pathway |
| Masking / redaction | Likely required if stored | RECOMMEND mask in UI; avoid full number in logs |

### Other

| Topic | Status |
|---|---|
| IT Act / SPDI legacy interplay with DPDP | RESEARCH with counsel |
| Government form copyright / reproduction | BLOCKER for facsimile PDFs (`DECISIONS` D11) |
| Intermediary / platform liability for incorrect applications | RECOMMEND strong disclaimers + human approval; counsel review |

**Do not claim DPDP/Aadhaar compliance in marketing or docs without review.**

---

## 7. AI-specific controls

- Human-in-the-loop for verification and application approval.  
- Ground assistant answers in approved service knowledge; cite; express uncertainty.  
- Document content is untrusted input (prompt-injection surface).  
- Prefer extraction models/APIs with enterprise DPA and no training on customer data.  
- **Development rule:** synthetic documents only to external AI until approvals complete.

---

## 8. Production readiness blockers (security/privacy)

| ID | Blocker |
|---|---|
| SP1 | Legal review of DPDP notices/consents and retention |
| SP2 | Aadhaar (and other ID) handling policy approved |
| SP3 | AI provider DPAs + data residency alignment |
| SP4 | Hosting region decision + encryption/backup verification |
| SP5 | Malware scanning operational in upload pipeline |
| SP6 | Deletion verification test evidence |
| SP7 | Incident response contacts/runbook |
| SP8 | Form reproduction rights if claiming official layout |

---

## 9. Development safeguards (immediate)

- No real citizen documents in repos, tickets, or prompts.  
- No production secrets in git.  
- No government API credentials in M0–M5 unless explicitly approved later.  
- Prefer fixture synthetic PDFs/images checked into a `testdata/` path without real PII.
