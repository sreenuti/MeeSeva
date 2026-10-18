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
