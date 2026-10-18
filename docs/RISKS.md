# Risks & Mitigations

**Status:** M0 baseline  
**Last updated:** 2026-10-18

| ID | Category | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|---|
| R1 | Product | Weak differentiation vs DigiLocker if MVP ships as “vault + reminders” only | M | H | Keep MVP centered on application preparation + provenance; validate positioning with users |
| R2 | Product | Online-first AP Income Certificate reduces value of download/print package | H | H | Decide assistive worksheet vs official form (`DECISIONS` D4); set expectations in UX copy |
| R3 | Product | Pilot service field schema unavailable → delayed M3 | H | H | Parallel research; fallback Residence Certificate path; block inventing fields |
| R4 | Technical | OCR/extraction accuracy low on phone photos | H | M | Confidence scores; HITL; capture guidelines; evaluate on synthetic/hard cases |
| R5 | Technical | Modular monolith module boundaries erode | M | M | Explicit module ownership; typed contracts; reviews |
| R6 | AI | Hallucinated government requirements in assistant | M | H | Approved KB only; citations; refuse when unknown; eval suite in M5/M6 |
| R7 | AI | Prompt injection via uploaded documents | M | H | Untrusted-doc handling; no tool autonomy; constrain assistant context |
| R8 | AI | Silent trust of extracted values | M | H | Never auto-verify; approval gates; provenance UI |
| R9 | Security | Unauthorized document access (IDOR) | M | H | Ownership tests from M1; M6 authZ regression suite |
| R10 | Security | Malware in uploads | M | H | Validation + scanning; isolated workers |
| R11 | Security | Sensitive data leakage to logs/providers | M | H | Log redaction; provider allowlist; synthetic-only until approval |
| R12 | Regulatory | DPDP non-compliance in notices/consents/retention | M | H | Legal review before pilot; consent records; deletion proofs |
| R13 | Regulatory | Aadhaar handling violations | M | H | Policy blocker before real docs; masking; avoid UIDAI auth in MVP |
| R14 | Regulatory | Form copyright / misuse of official templates | M | M | Confirm rights; prefer assistive package if unclear |
| R15 | Business | Freemium limits/pricing unvalidated | H | M | Instrument usage; delay billing; customer interviews |
| R16 | Business | Trademark/branding conflict with government “MeeSeva” name | M | M | Choose distinct commercial brand before public pilot (`DECISIONS` D10) |
| R17 | Business | Trust barrier uploading income/ID docs to a private startup | H | H | Security UX, transparency, MFA, India residency recommendation |
| R18 | Delivery | Scope creep into multi-service / integrations | H | H | Hard MVP exclusions; milestone exit gates |

---

## Top residual blockers entering M1

1. Income Certificate implementation details incomplete (`PILOT_SERVICE` B1–B4) — **does not block M1–M2**.  
2. IdP vendor selection (`DECISIONS` D1).  
3. Legal path for real identity documents and Aadhaar (`SECURITY_PRIVACY` SP1–SP2) — blocks real-data pilot, not synthetic M1.  
4. Commercial product name distinct from government MeeSeva branding.
