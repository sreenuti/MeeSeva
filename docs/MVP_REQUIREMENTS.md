# MVP Requirements

**Status:** M2 approved for synthetic local development; M3 not authorized  
**Last updated:** 2026-10-18  
**Depends on:** `PRODUCT_VISION.md`, `PILOT_SERVICE.md`

---

## 1. Primary user journey

1. Citizen creates an account and completes MFA enrollment.
2. Citizen consents to stated processing purposes.
3. Citizen uploads personal documents (PDF/images).
4. System stores documents privately, validates uploads, and queues processing.
5. System classifies documents and extracts structured fields with confidence.
6. Citizen reviews, corrects, and verifies extracted information.
7. System builds/updates a reusable citizen profile with provenance.
8. Citizen selects the pilot government service.
9. System loads the versioned service definition and required documents.
10. System maps verified profile fields into the application draft.
11. System flags missing and conflicting information.
12. Citizen reviews, corrects, and explicitly approves the application.
13. System generates a PDF application package + supporting documents + instructions.
14. Citizen downloads the package and submits through the official channel (outside product).
15. Citizen may view document expiry status and ask grounded guidance questions.

---

## 2. Functional requirements

### A. Identity and access

| ID | Requirement |
|---|---|
| IAM-1 | Citizen registration and login via managed identity provider |
| IAM-2 | MFA required for authenticated sessions |
| IAM-3 | Secure session management and logout |
| IAM-4 | Password recovery (provider-supported) |
| IAM-5 | Strict user-level data isolation |
| IAM-6 | Account deletion with cascading data deletion workflow |
| IAM-7 | Consent and privacy preference capture/update |

### B. Secure document vault

| ID | Requirement |
|---|---|
| DOC-1 | Upload PDF and common image formats |
| DOC-2 | Enforce file size, type, and content validation |
| DOC-3 | Private encrypted object storage; no public buckets |
| DOC-4 | Short-lived signed access URLs for preview/download |
| DOC-5 | Classification label + editable metadata |
| DOC-6 | Versioning when a document is replaced |
| DOC-7 | Soft delete + retention-aware hard delete |
| DOC-8 | Audit events for upload, access, delete |
| DOC-9 | Design for malware scanning (implement in vault milestone) |

### C. Document intelligence

| ID | Requirement |
|---|---|
| AI-1 | Pluggable classification and OCR/extraction pipeline |
| AI-2 | Structured fields with confidence scores |
| AI-3 | Source document and page/location references where available |
| AI-4 | Extraction never auto-marks fields as verified |
| AI-5 | User correction and explicit verification actions |
| AI-6 | Graceful handling of unsupported/poor-quality documents |

### D. Citizen profile

| ID | Requirement |
|---|---|
| PRF-1 | Minimal structured profile for pilot service needs |
| PRF-2 | Per-field verified/unverified state |
| PRF-3 | Multiple sources and conflict representation |
| PRF-4 | Field-level provenance and audit history |
| PRF-5 | Data minimization—no speculative attributes |

### E. Service catalog

| ID | Requirement |
|---|---|
| SVC-1 | Versioned service definitions maintainable without code changes for form updates |
| SVC-2 | MVP publishes exactly one validated service |
| SVC-3 | Definition includes jurisdiction, department, official source refs, required fields, docs, validation rules, form template ref, effective dates, publication status |

### F. Application preparation engine

| ID | Requirement |
|---|---|
| APP-1 | Deterministic required-field validation and mapping |
| APP-2 | Missing and conflict detection |
| APP-3 | Supporting-document matching |
| APP-4 | Draft generation without inventing required values |
| APP-5 | Explicit citizen approval gate before finalization |
| APP-6 | Workflow state transitions are deterministic and audited |

### G. Human-in-the-loop review

| ID | Requirement |
|---|---|
| HITL-1 | UI distinguishes extracted / user-entered / missing / conflicting / verified values |
| HITL-2 | Supporting-document references visible per requirement |
| HITL-3 | Sensitive declarations require explicit confirmation |
| HITL-4 | No final package without required approvals |

### H. Package generation

| ID | Requirement |
|---|---|
| PKG-1 | Downloadable PDF application form output |
| PKG-2 | Include matched supporting documents |
| PKG-3 | Package manifest + remaining manual-step instructions |
| PKG-4 | Do not claim official acceptance unless verified |
| PKG-5 | No direct government submission |

### I. Expiry and notifications

| ID | Requirement |
|---|---|
| EXP-1 | Optional expiry metadata on documents |
| EXP-2 | Upcoming-expiry dashboard |
| EXP-3 | Configurable reminder thresholds (in-app first) |
| EXP-4 | External email/SMS delivery may be deferred |

### J. Basic AI assistant

| ID | Requirement |
|---|---|
| AST-1 | Explain supported service requirements from approved knowledge base |
| AST-2 | Explain missing information for current application |
| AST-3 | Guide user through preparation steps |
| AST-4 | Cite sources / express uncertainty; no fabricated requirements |
| AST-5 | No autonomous submission; no unapproved model exposure of sensitive docs |

### K. Freemium readiness

| ID | Requirement |
|---|---|
| ENT-1 | Configurable plans and entitlements (storage, application usage, reminders, advanced assistance) |
| ENT-2 | Enforce entitlement checks in application layer |
| ENT-3 | No payment gateway/billing in MVP |

---

## 3. Nonfunctional requirements

| Area | Target |
|---|---|
| Security | Encryption in transit and at rest; least privilege; audit logging; secrets not in code |
| Privacy | Consent, purpose limitation, minimization, deletion support; DPDP-aware design |
| Reliability | Idempotent job processing for extraction; safe retries |
| Performance | Mobile-first responsive UI; vault preview usable on smartphone networks |
| Accessibility | WCAG-oriented review before pilot (M6) |
| Maintainability | Modular monolith, typed APIs, versioned service definitions |
| Observability | Structured logs without sensitive payloads; audit trail for security events |
| Correctness | Deterministic mapping/validation; AI outputs validated before use |

---

## 4. MVP success / acceptance criteria

Provisional until baseline testing:

| Criterion | Target |
|---|---|
| Explicit approval before finalization | 100% |
| Fabricated required-field values | 0 |
| Provenance on auto-populated fields | 100% |
| Required-field validation correctness | 100% of defined rules |
| Ownership isolation | 100% unauthorized access denied in tests |
| Final required-field accuracy after user review | ≥ 95% (provisional) |
| Preparation time vs manual | Measurable reduction (baseline TBD) |

### Required test scenarios

- Missing documents
- Conflicting information
- Poor OCR quality
- Unsupported document types
- Expired documents
- Invalid field formats
- Unauthorized access
- Interrupted processing
- Form/service version changes
- User corrections
- Package generation failures

---

## 5. MVP exclusions

- Government API submission or status tracking against APSEVA/MeeSeva
- Payment/subscription billing
- Real Aadhaar/PAN/passport processing via external AI before approvals
- Multi-service catalog beyond one validated pilot
- Multilingual UI
- Family/partner accounts
- Microservices, Kubernetes, vector DB, multi-agent orchestration

---

## 6. Pilot dependency gate

M2 may proceed on synthetic data. M3 application-engine work requires `PILOT_SERVICE.md` and `M3_READINESS_REPORT.md` to show the chosen service **UNBLOCKED**, plus an explicit product-owner approval to implement.

As of 2026-10-18 the provisional workflow is Andhra Pradesh Residence Certificate (General), limited to an assistive worksheet. Income Certificate is a future candidate. Residence Certificate (Passport) is excluded. The readiness verdict is **NOT READY**. Do not implement the service catalog, application engine, or PDF generator.
