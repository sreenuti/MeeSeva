import { appConfig } from "./config";

export type DocumentItem = {
  id: string;
  display_name: string;
  doc_type: string;
  status: string;
  expires_on: string | null;
  mime_type: string | null;
  byte_size: number | null;
  scan_status: string | null;
  created_at: string;
  downloadable: boolean;
};

async function apiFetch(path: string, token: string, init: RequestInit = {}) {
  const headers = new Headers(init.headers || {});
  headers.set("Authorization", `Bearer ${token}`);
  const res = await fetch(`${appConfig.apiBaseUrl}${path}`, { ...init, headers });
  return res;
}

export async function getMe(token: string) {
  const res = await apiFetch("/api/v1/me", token);
  if (!res.ok) throw new Error("Unable to load profile");
  return res.json();
}

export async function recordVaultConsent(token: string) {
  const res = await apiFetch("/api/v1/consents", token, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ purposes: ["vault_storage"], granted: true }),
  });
  if (!res.ok) throw new Error("Unable to record consent");
  return res.json();
}

export async function listDocuments(token: string): Promise<DocumentItem[]> {
  const res = await apiFetch("/api/v1/documents", token);
  if (!res.ok) throw new Error("Unable to list documents");
  const data = await res.json();
  return data.items;
}

export async function uploadDocument(
  token: string,
  file: File,
  meta: { displayName?: string; docType?: string },
) {
  const form = new FormData();
  form.append("file", file);
  form.append("display_name", meta.displayName || file.name);
  form.append("doc_type", meta.docType || "unclassified");
  const res = await apiFetch("/api/v1/documents", token, { method: "POST", body: form });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Upload failed");
  }
  return res.json() as Promise<DocumentItem>;
}

export async function deleteDocument(token: string, id: string) {
  const res = await apiFetch(`/api/v1/documents/${id}`, token, { method: "DELETE" });
  if (!res.ok) throw new Error("Delete failed");
}

export async function downloadDocument(token: string, id: string, filename: string) {
  const res = await apiFetch(`/api/v1/documents/${id}/download`, token);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Download failed");
  }
  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    const data = await res.json();
    window.open(data.url, "_blank", "noopener,noreferrer");
    return;
  }
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export async function mintDevToken(subject: string, email: string) {
  const res = await fetch(`${appConfig.apiBaseUrl}/api/v1/dev/token`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ subject, email }),
  });
  if (!res.ok) throw new Error("Dev login unavailable");
  return res.json() as Promise<{ access_token: string }>;
}

export type ProcessJob = {
  id: string;
  document_id: string;
  status: string;
  error_code: string | null;
  error_message: string | null;
};

export type ExtractedField = {
  id: string;
  field_key: string;
  raw_value: string | null;
  normalized_value: string | null;
  confidence: string;
  validation_result: string;
  verification_status: string;
  source_page: number | null;
  source_text_snippet: string | null;
  user_corrected_value: string | null;
};

export type ExtractionResult = {
  id: string;
  document_id: string;
  predicted_category: string;
  category_certainty: string;
  user_category: string | null;
  effective_category: string;
  job_status: string;
  fields: ExtractedField[];
};

export type ProfileField = {
  id: string;
  field_key: string;
  value: string | null;
  verification_state: string;
  source_document_id: string | null;
  original_extracted_value: string | null;
  user_corrected: boolean;
  conflict_candidates_json: string | null;
};

export type CitizenProfile = {
  id: string;
  version: number;
  fields: ProfileField[];
};

function detailMessage(err: unknown, fallback: string) {
  if (err && typeof err === "object" && "detail" in err) {
    const detail = (err as { detail: unknown }).detail;
    if (typeof detail === "string") return detail;
  }
  return fallback;
}

export async function startProcessing(token: string, documentId: string) {
  const res = await apiFetch(`/api/v1/documents/${documentId}/process`, token, { method: "POST" });
  if (!res.ok) throw new Error(detailMessage(await res.json().catch(() => ({})), "Could not start processing"));
  return res.json() as Promise<ProcessJob>;
}

export async function getProcessingStatus(token: string, documentId: string) {
  const res = await apiFetch(`/api/v1/documents/${documentId}/process`, token);
  if (!res.ok) throw new Error(detailMessage(await res.json().catch(() => ({})), "No processing status"));
  return res.json() as Promise<ProcessJob>;
}

export async function getExtraction(token: string, documentId: string) {
  const res = await apiFetch(`/api/v1/documents/${documentId}/extraction`, token);
  if (!res.ok) throw new Error(detailMessage(await res.json().catch(() => ({})), "Results not available"));
  return res.json() as Promise<ExtractionResult>;
}

export async function updateClassification(token: string, documentId: string, category: string) {
  const res = await apiFetch(`/api/v1/documents/${documentId}/classification`, token, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ category }),
  });
  if (!res.ok) throw new Error("Could not update document type");
  return res.json() as Promise<ExtractionResult>;
}

export async function reviewExtractedField(
  token: string,
  fieldId: string,
  body: { action: "confirm" | "correct" | "reject"; value?: string },
) {
  const res = await apiFetch(`/api/v1/extracted-fields/${fieldId}/review`, token, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(detailMessage(await res.json().catch(() => ({})), "Could not save review"));
  return res.json() as Promise<ExtractedField>;
}

export async function getProfile(token: string) {
  const res = await apiFetch("/api/v1/profile", token);
  if (!res.ok) throw new Error("Unable to load profile");
  return res.json() as Promise<CitizenProfile>;
}

export async function getConflicts(token: string) {
  const res = await apiFetch("/api/v1/profile/conflicts", token);
  if (!res.ok) throw new Error("Unable to load conflicts");
  return res.json() as Promise<ProfileField[]>;
}

export async function resolveConflict(
  token: string,
  body: { field_key: string; value: string; source_extracted_field_id?: string },
) {
  const res = await apiFetch("/api/v1/profile/conflicts/resolve", token, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error("Could not resolve conflict");
  return res.json() as Promise<ProfileField>;
}
