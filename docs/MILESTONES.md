# Milestones M0–M6

**Status:** M0 baseline  
**Last updated:** 2026-10-18  
**Rule:** Do not start Mi+1 until exit gate of Mi is met and product owner approves.

---

## M0 — Product Alignment and Architecture

| | |
|---|---|
| **Objective** | Establish implementation-ready product, architecture, security, and pilot research foundation |
| **Scope** | Unified docs; pilot validation research; data model; roadmap; open decisions |
| **Dependencies** | None |
| **Deliverables** | `docs/PRODUCT_VISION.md`, `MVP_REQUIREMENTS.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`, `PILOT_SERVICE.md`, `MILESTONES.md`, `DECISIONS.md`, `SECURITY_PRIVACY.md`, `RISKS.md` |
| **Acceptance criteria** | Confirmed decisions recorded; pilot status explicit (incl. blockers); architecture and schema sufficient for M1; no app feature implementation required |
| **Focused tests** | Doc consistency review; pilot source URLs resolvable |
| **Exit gate** | Product-owner acknowledgment of M0 report and blockers |
| **Exclusions** | Application code, infra deploy, payments, government APIs |

---

## M1 — Secure Identity and Document Vault

| | |
|---|---|
| **Objective** | Citizens can register/login with MFA and securely upload/retrieve their own documents |
| **Scope** | Managed IdP integration; sessions; vault upload/validation; private storage; signed access; ownership checks; basic audit; consent capture skeleton |
| **Dependencies** | M0 exit; IdP vendor choice (open decision) |
| **Deliverables** | Auth-enabled web+API; document CRUD/preview; audit events; Docker local stack; threat-control checklist for vault |
| **Acceptance criteria** | MFA enforced; user A cannot access user B documents; no public bucket access; uploads reject disallowed types/oversized files; consent recorded at signup |
| **Focused tests** | AuthZ isolation; upload validation; signed URL expiry; audit emission |
| **Exit gate** | Security review of vault access path; synthetic-only data confirmed |
| **Exclusions** | OCR/extraction, profile, applications, payments, notifications delivery |

---

## M2 — Document Intelligence and Citizen Profile

| | |
|---|---|
| **Objective** | Extract structured fields from documents and build a verified profile with provenance |
| **Dependencies** | M1 complete |
| **Scope** | Local OCR/text extraction; classification; extraction jobs; confidence; manual correction; profile fields; conflicts |
| **Deliverables** | Intelligence APIs; profile APIs; review/profile UI; migration `20261018_0002`; `docs/M2_INTELLIGENCE.md` |
| **Acceptance criteria** | No auto-verify; every accepted field has source refs; conflicts surfaced; security gate enforced; ownership isolation |
| **Focused tests** | Clean process; quarantine deny; provenance; corrections; conflicts; isolation; duplicate jobs; M1 vault intact |
| **Exit gate** | Product-owner review of M2 report |
| **Exclusions** | Service catalog, application prep, package PDF, assistant, real PII to external AI, M3+ |
| **Implementation status** | **Implemented (pending review)** — 2026-10-18 |

---

## M3 — Service Catalog and Application Engine

| | |
|---|---|
| **Objective** | One validated service definition drives deterministic application drafts |
| **Dependencies** | M2; **PILOT_SERVICE blockers B1–B4 cleared** (or approved fallback + its validation) |
| **Scope** | Versioned ServiceDefinition; requirements; mapping; missing/conflict detection; supporting-doc match; draft application |
| **Deliverables** | Published pilot service version; engine APIs; draft UI |
| **Acceptance criteria** | Zero invented required values; mapping deterministic; missing/conflicts correct per definition; only published version selectable |
| **Focused tests** | Missing docs; conflicts; invalid formats; service version change mid-draft |
| **Exit gate** | Product sign-off that service definition matches verified official evidence |
| **Exclusions** | Final package PDF, HITL approval UX polish (basic draft OK), billing |

---

## M4 — Human Review and Application Package

| | |
|---|---|
| **Objective** | Citizen can review/correct/approve and download a complete package |
| **Dependencies** | M3 |
| **Scope** | HITL review UI; explicit approvals; PDF generation; supporting pack; manifest; instructions; download audit |
| **Deliverables** | Approval workflow; package artifacts; disclaimer that official acceptance is not claimed unless verified |
| **Acceptance criteria** | 100% approval gate; provenance visible; package checksum; regenerate on approved edits only under rules |
| **Focused tests** | Approval bypass attempts; package generation failure; unauthorized download |
| **Exit gate** | End-to-end synthetic journey demo for pilot service |
| **Exclusions** | Government submission, status tracking, payments |

---

## M5 — Expiry Tracking and AI Guidance

| | |
|---|---|
| **Objective** | Expiry dashboard/reminders and grounded assistant; freemium entitlement foundation |
| **Dependencies** | M1–M4 core paths stable |
| **Scope** | Expiry metadata UX; reminder thresholds; in-app notifications; KB-grounded assistant; plan/entitlement enforcement hooks |
| **Deliverables** | Dashboard; notification records; assistant with citations/uncertainty; Free/Premium limit config (no gateway) |
| **Acceptance criteria** | No fabricated service rules; entitlement limits enforced; docs without expiry handled cleanly |
| **Focused tests** | Hallucination refusal cases; entitlement exceed; reminder scheduling |
| **Exit gate** | Assistant evaluation against approved KB; entitlement config reviewed |
| **Exclusions** | Payment processor; SMS/email provider mandatory; multi-agent systems |

---

## M6 — Security Validation and Pilot Readiness

| | |
|---|---|
| **Objective** | Controlled pilot readiness under security, privacy, accuracy, and accessibility bars |
| **Dependencies** | M1–M5; legal review items from `SECURITY_PRIVACY.md` |
| **Scope** | Threat-model review; authZ tests; extraction/application accuracy eval; deletion verification; accessibility review; pilot ops checklist |
| **Deliverables** | Pilot readiness report; residual risk list; go/no-go recommendation |
| **Acceptance criteria** | Ownership isolation green; deletion verified; no unresolved critical security findings; pilot service unblocked; synthetic→limited pilot plan approved |
| **Focused tests** | Full scenario suite from `MVP_REQUIREMENTS.md` §4 |
| **Exit gate** | Product + security + compliance go/no-go |
| **Exclusions** | Public launch; real government integration; production billing |

---

## Cross-milestone dependency graph

```
M0 → M1 → M2 → M3 → M4 → M5 → M6
                 │
                 └── requires pilot UNBLOCKED (or approved fallback)
```

M1–M2 may proceed while Income Certificate research completes. **M3 must not invent form fields.**
