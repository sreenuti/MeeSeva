# Architecture

**Status:** M0 baseline  
**Last updated:** 2026-10-18  
**Style:** Modular monolith

---

## 1. System context

```
┌─────────────┐     HTTPS      ┌──────────────────────────────┐
│ Citizen     │ ◄─────────────► │ Web App (Next.js)            │
│ (browser)   │                 └──────────────┬───────────────┘
└─────────────┘                                │ typed API
                                               ▼
┌─────────────┐                 ┌──────────────────────────────┐
│ Managed IdP │ ◄─────────────► │ API (FastAPI modular monolith)│
│ + MFA       │                 └──────┬───────────┬───────────┘
└─────────────┘                        │           │
                                       ▼           ▼
                              ┌────────────┐ ┌────────────┐
                              │ PostgreSQL │ │ Private    │
                              │            │ │ Object     │
                              │            │ │ Storage    │
                              └────────────┘ └────────────┘
                                       │
                          ┌────────────┴────────────┐
                          ▼                         ▼
                 ┌────────────────┐      ┌────────────────────┐
                 │ Job worker     │      │ Approved AI        │
                 │ (OCR/extract/  │─────►│ providers (OCR/LLM)│
                 │  package jobs) │      │ under DPA controls │
                 └────────────────┘      └────────────────────┘
```

**External actors (MVP):** Citizen, Managed IdP, AI providers (approved), (optional later) email/SMS gateway.  
**Not in MVP:** Government submission APIs, DigiLocker partner APIs, payment processors.

---

## 2. Modular monolith modules

| Module | Responsibility |
|---|---|
| `identity` | Auth session bridging, user records, MFA status mirrors, account deletion orchestration |
| `consent` | Purpose-bound consent records and preference updates |
| `vault` | Upload validation, storage keys, metadata, signed access, versioning, delete |
| `intelligence` | Classification/OCR/extraction jobs, confidence, provenance refs |
| `profile` | CitizenProfile / ProfileField, verification, conflicts |
| `catalog` | Versioned ServiceDefinition, requirements, form templates |
| `applications` | Draft mapping, missing/conflict logic, HITL approval, packages |
| `notifications` | Expiry reminders and in-app notification records |
| `entitlements` | Plans, limits, enforcement hooks |
| `audit` | Immutable security/business audit events |
| `assistant` | Grounded Q&A over approved knowledge base |

Modules communicate in-process via clear interfaces/data contracts. No network microservices for MVP.

---

## 3. Technology stack (baseline)

| Layer | Choice | Notes |
|---|---|---|
| Frontend | Next.js + TypeScript + Tailwind | Mobile-first responsive web |
| Backend | Python FastAPI + Pydantic | Typed APIs and validation |
| DB | PostgreSQL | System of record |
| Object storage | Private encrypted bucket | No public document ACLs |
| Auth | Managed IdP with MFA | Prefer Auth0 / Clerk / Cognito / equivalent after compliance review |
| Jobs | Lightweight queue + worker | Redis only when justified |
| OCR/LLM | Pluggable providers | Structured output validation; approved processors only |
| PDF | Deterministic form render + packaging | No AI-invented form content |
| Local ops | Docker Compose | Env-based config |
| Deploy | Containerized | Region TBD after compliance review |

### Justified deviations

None yet. Any stack change must be recorded in `DECISIONS.md`.

### Explicitly deferred

Microservices, Kubernetes, event mesh, vector databases, multi-agent orchestration.

---

## 4. Key data flows

### 4.1 Document upload → profile update

1. Browser uploads file to API (authenticated).
2. `vault` validates MIME/size/content heuristics; stores object privately; writes `Document` + `DocumentVersion`.
3. Worker runs classification + OCR + extraction → `ExtractedField` records (unverified).
4. Citizen reviews in UI; verified values upsert `ProfileField` with provenance.
5. Conflicts remain visible until resolved by user.

### 4.2 Application preparation

1. Citizen selects published `ServiceDefinition` version.
2. Engine loads requirements; maps verified profile fields deterministically.
3. Missing/conflicts computed; supporting docs matched.
4. Draft `Application` created; citizen edits/approves.
5. Package job renders PDF + attaches docs → signed download.

### 4.3 AI assistant

1. User question + application context (non-sensitive where possible).
2. Retriever limited to approved service knowledge snippets.
3. LLM answers with citations/uncertainty; refused if out of knowledge.

---

## 5. Security boundaries

| Boundary | Control |
|---|---|
| Public internet → Web/API | TLS; security headers; rate limits |
| Unauthenticated → authenticated | Managed IdP + MFA |
| Tenant isolation | `user_id` ownership checks on every document/application query |
| Object storage | Private; short-lived signed URLs; no public listing |
| AI providers | Allowlisted; contractual controls; synthetic-only until approval; minimize payloads |
| Secrets | Env/secret manager; never logged |
| Admin | No broad admin document browser in MVP |

See `SECURITY_PRIVACY.md` for threat model and controls.

---

## 6. AI integration boundaries

| Allowed | Disallowed (MVP) |
|---|---|
| Classification, OCR, field extraction | Autonomous form invention |
| Explanations from approved KB | Silent acceptance of extracted facts |
| Structured outputs validated by schema | Sending real Aadhaar/PAN/passport to unapproved providers |
| Confidence + provenance | Multi-agent orchestration |

**Rule:** Deterministic code owns validation, authorization, mapping, and workflow transitions. AI assists; humans approve.

---

## 7. Deployment assumptions

- Docker-based local development for web, API, worker, Postgres, (optional) queue.
- Single deployable API process + worker process initially.
- Hosting region and data residency decided after legal/compliance review (RECOMMENDATION: India region for production PII).
- Backups for Postgres and object storage required before pilot.
- No production infrastructure created in M0.

---

## 8. API contract principles

- Versioned REST (or RPC-over-HTTP) with Pydantic models.
- Explicit error codes for ownership, entitlement, and validation failures.
- Idempotency keys for upload completion and package generation.
- Pagination for document/application lists.
- Never return long-lived raw storage credentials to clients.
