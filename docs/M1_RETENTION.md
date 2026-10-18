# M1 Retention & Deletion Limitations

## Implemented in M1

- Soft delete sets `documents.deleted_at` and `status=deleted`.
- Soft-deleted documents are excluded from list/get/download for the owner.
- Object storage blobs are **not** immediately purged on soft delete (grace period design).
- Audit events retain action metadata (no document contents).

## Not fully implemented yet (limitations)

| Topic | Limitation |
|---|---|
| Hard purge job | No scheduled worker yet to delete storage objects after `soft_delete_grace_days` |
| Account deletion cascade | User record deletion API not exposed in M1 UI/API |
| Backup retention | DB/volume backups may retain deleted document metadata/blobs until backup expiry |
| Point-in-time restore | Restores can resurrect soft-deleted rows/objects |
| Legal hold | No legal-hold flag |

## Backup note

Until backup policies are defined:

1. Treat backup media as in-scope for sensitive document data.
2. Deletion from the live system does **not** guarantee immediate removal from backups.
3. M6 must verify end-to-end deletion including storage objects and document retention evidence.
