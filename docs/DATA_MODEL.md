# Data Model

**Status:** M0 + M1/M2 implementation  
**Last updated:** 2026-10-18  
**Store:** PostgreSQL (metadata) + private object storage (blobs)

Ownership rule: every citizen-owned row is scoped by `user_id` (or equivalent) and enforced in the application layer and, where practical, with DB constraints/RLS later.

---

## Entity catalog

### User

| | |
|---|---|
| **Purpose** | Local application user linked to managed IdP subject |
| **Key fields** | `id`, `idp_subject`, `email`, `phone` (optional), `locale`, `status`, `created_at`, `deleted_at` |
| **Relationships** | 1→N Documents, Profiles, Applications, Consents, Entitlements, Notifications, AuditEvents |
| **Ownership** | Self |
| **Security** | No passwords stored locally if IdP-managed; minimize PII copies |
| **Retention** | Delete or anonymize on account deletion per policy |

### Document

| | |
|---|---|
| **Purpose** | Logical document in the vault |
| **Key fields** | `id`, `user_id`, `doc_type`, `display_name`, `status`, `expires_on` (nullable), `current_version_id`, `created_at` |
| **Relationships** | N→1 User; 1→N DocumentVersion; referenced by ExtractedField, ApplicationDocument |
| **Ownership** | User |
| **Security** | Access only by owner; audit access |
| **Retention** | User delete; policy-driven purge of soft-deleted objects |

### DocumentVersion

| | |
|---|---|
| **Purpose** | Immutable stored file revision |
| **Key fields** | `id`, `document_id`, `storage_key`, `content_hash`, `mime_type`, `byte_size`, `page_count` (nullable), `scan_status`, `created_at` |
| **Relationships** | N→1 Document; 1→N ExtractedField |
| **Ownership** | Via Document.user_id |
| **Security** | Storage key never exposed; signed URLs only |
| **Retention** | Kept for audit/history until document purge |

### DocumentProcessingJob (M2)

| | |
|---|---|
| **Purpose** | Per-version intelligence job lifecycle |
| **Key fields** | `id`, `document_id`, `document_version_id` (unique), `user_id`, `status` (`queued`/`processing`/`awaiting_user_review`/`completed`/`failed`/`unsupported`), `error_code`, `error_message` |
| **Ownership** | User |
| **Security** | Enqueued only after malware clean + ownership checks |

### DocumentExtraction (M2)

| | |
|---|---|
| **Purpose** | Classification summary for a processing job |
| **Key fields** | `predicted_category`, `category_certainty`, `user_category`, `extraction_method`, `page_count` |

### ExtractedField

| | |
|---|---|
| **Purpose** | Proposed value before/after user review |
| **Key fields** | `id`, `document_id`, `document_version_id`, `field_key`, `raw_value`, `normalized_value`, `confidence` (`unknown`/`low`/`medium`/`high`), `validation_result`, `verification_status` (`extracted_unverified`/`needs_review`/`user_verified`/`user_corrected`/`rejected`), `source_page`, `source_text_snippet`, `extraction_method` |
| **Relationships** | N→1 DocumentExtraction; may seed ProfileField |
| **Ownership** | Via document owner |
| **Security** | Treat as sensitive; do not log values |
| **Retention** | Tied to extraction/document lifecycle |

### CitizenProfile

| | |
|---|---|
| **Purpose** | Aggregate reusable profile for a citizen user |
| **Key fields** | `id`, `user_id`, `version`, `updated_at` |
| **Relationships** | 1→1 User (MVP); 1→N ProfileField |
| **Ownership** | User |
| **Security** | Owner-only |
| **Retention** | Deleted with account |

### ProfileField

| | |
|---|---|
| **Purpose** | Single profile attribute with verification and provenance |
| **Key fields** | `id`, `profile_id`, `field_key`, `value`, `verification_state` (`unverified`/`verified`/`conflict`/`needs_review`), `source_document_id`, `source_document_version_id`, `source_extracted_field_id`, `original_extracted_value`, `user_corrected`, `conflict_candidates_json`, `updated_at` |
| **Relationships** | N→1 CitizenProfile; references Documents/ExtractedFields |
| **Ownership** | Via profile |
| **Security** | Field-level audit on verify/correct |
| **Retention** | Deleted with profile; confirmed values retained if source document is soft-deleted (IDs may dangle) |

### ServiceDefinition

| | |
|---|---|
| **Purpose** | Versioned catalog entry for an administrative service |
| **Key fields** | `id`, `service_key`, `state`, `jurisdiction`, `department`, `title`, `description`, `version`, `official_source_urls[]`, `status` (`draft`/`published`/`retired`), `effective_from`, `review_by`, `form_template_id` |
| **Relationships** | 1→N ServiceRequirement; N→1 FormTemplate |
| **Ownership** | Platform-owned (not user data) |
| **Security** | Only published versions selectable by citizens |
| **Retention** | Retain retired versions for historical applications |

### ServiceRequirement

| | |
|---|---|
| **Purpose** | Required field or supporting document for a service version |
| **Key fields** | `id`, `service_definition_id`, `req_type` (`field`/`document`), `key`, `label`, `required`, `validation_rules_json`, `profile_field_mapping`, `doc_type_match_rules` |
| **Relationships** | N→1 ServiceDefinition |
| **Ownership** | Platform |
| **Security** | Integrity of rules is critical; change via controlled publish |
| **Retention** | With service version |

### FormTemplate

| | |
|---|---|
| **Purpose** | Deterministic rendering template for application PDF |
| **Key fields** | `id`, `name`, `version`, `storage_key` or `template_spec_json`, `field_map_json`, `license_notes`, `source_url` |
| **Relationships** | Referenced by ServiceDefinition / ApplicationPackage |
| **Ownership** | Platform |
| **Security** | Template integrity; do not claim official status without rights |
| **Retention** | Keep versions used by finalized applications |

### Application

| | |
|---|---|
| **Purpose** | Citizen application preparation instance |
| **Key fields** | `id`, `user_id`, `service_definition_id`, `status` (`draft`/`needs_info`/`in_review`/`approved`/`packaged`/`abandoned`), `approved_at`, `created_at` |
| **Relationships** | N→1 User, ServiceDefinition; 1→N ApplicationField, ApplicationDocument; 0..1 ApplicationPackage |
| **Ownership** | User |
| **Security** | Owner-only; approval events audited |
| **Retention** | User delete; retain package artifacts per retention policy |

### ApplicationField

| | |
|---|---|
| **Purpose** | Mapped value for a form field in an application |
| **Key fields** | `id`, `application_id`, `field_key`, `value`, `value_source` (`profile`/`user`/`missing`), `profile_field_id` (nullable), `conflict_flag`, `verified_for_submission` |
| **Relationships** | N→1 Application |
| **Ownership** | Via application |
| **Security** | Provenance required for auto-populated values |
| **Retention** | With application |

### ApplicationDocument

| | |
|---|---|
| **Purpose** | Supporting document matched to a requirement |
| **Key fields** | `id`, `application_id`, `requirement_key`, `document_id`, `match_status` (`matched`/`missing`/`user_override`) |
| **Relationships** | N→1 Application, Document |
| **Ownership** | Via application |
| **Security** | Must not attach another user’s documents |
| **Retention** | With application |

### ApplicationPackage

| | |
|---|---|
| **Purpose** | Generated downloadable package |
| **Key fields** | `id`, `application_id`, `storage_key`, `manifest_json`, `generated_at`, `checksum` |
| **Relationships** | 1→1 Application (MVP) |
| **Ownership** | Via application |
| **Security** | Signed download URLs; audit downloads |
| **Retention** | Configurable; delete with application/account |

### ConsentRecord

| | |
|---|---|
| **Purpose** | Evidence of purpose-bound consent |
| **Key fields** | `id`, `user_id`, `purpose`, `policy_version`, `granted`, `granted_at`, `revoked_at`, `channel` |
| **Relationships** | N→1 User |
| **Ownership** | User |
| **Security** | Immutable grant history preferred (append revoke) |
| **Retention** | Retain as required for legal defense/compliance |

### AuditEvent

| | |
|---|---|
| **Purpose** | Security and significant business audit trail |
| **Key fields** | `id`, `actor_user_id` (nullable), `action`, `entity_type`, `entity_id`, `metadata_json` (non-sensitive), `ip_hash`, `created_at` |
| **Relationships** | Loose references to entities |
| **Ownership** | Platform / per-user visibility limited |
| **Security** | Append-only; no sensitive document contents |
| **Retention** | Longer than operational data per policy |

### Notification

| | |
|---|---|
| **Purpose** | In-app (and later external) reminders/alerts |
| **Key fields** | `id`, `user_id`, `type`, `payload_json`, `scheduled_for`, `sent_at`, `status` |
| **Relationships** | N→1 User; may reference Document |
| **Ownership** | User |
| **Security** | Minimal PII in payload |
| **Retention** | Short operational window |

### SubscriptionPlan

| | |
|---|---|
| **Purpose** | Configurable freemium plan definition |
| **Key fields** | `id`, `code`, `name`, `limits_json`, `features_json`, `active` |
| **Relationships** | 1→N UserEntitlement |
| **Ownership** | Platform |
| **Security** | Admin-controlled |
| **Retention** | Keep historical plans referenced by entitlements |

### UserEntitlement

| | |
|---|---|
| **Purpose** | User’s current plan and usage counters |
| **Key fields** | `id`, `user_id`, `plan_id`, `period_start`, `period_end`, `usage_json`, `status` |
| **Relationships** | N→1 User, SubscriptionPlan |
| **Ownership** | User |
| **Security** | Server-side enforcement only |
| **Retention** | Billing-adjacent history if payments added later |

---

## Provenance model (summary)

```
DocumentVersion → ExtractedField (proposed)
                → user accepts/corrects
                → ProfileField (verified/unverified/conflict + source refs)
                → ApplicationField (mapped + value_source + profile_field_id)
```

Auto-populated application fields must retain links sufficient to show which document/version produced the value.

---

## Consent and audit (summary)

- Consent is purpose-specific (e.g., vault storage, AI extraction, application preparation).
- Audit covers authz failures, uploads, downloads, verifies, approvals, deletes, package generation.
- Logs and audit metadata must not contain full document text or raw identity numbers unless strictly necessary and protected.
