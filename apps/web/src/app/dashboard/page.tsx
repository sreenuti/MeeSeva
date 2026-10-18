"use client";

import Link from "next/link";
import { FormEvent, useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Shell } from "@/components/Shell";
import { useAuth } from "@/lib/auth";
import {
  DocumentItem,
  deleteDocument,
  downloadDocument,
  listDocuments,
  uploadDocument,
} from "@/lib/api";

function formatBytes(n: number | null) {
  if (n == null) return "—";
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / (1024 * 1024)).toFixed(1)} MB`;
}

export default function DashboardPage() {
  const { ready, token } = useAuth();
  const router = useRouter();
  const [items, setItems] = useState<DocumentItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [displayName, setDisplayName] = useState("");
  const [docType, setDocType] = useState("unclassified");
  const [file, setFile] = useState<File | null>(null);

  const refresh = useCallback(async () => {
    if (!token) return;
    const docs = await listDocuments(token);
    setItems(docs);
  }, [token]);

  useEffect(() => {
    if (!ready) return;
    if (!token) {
      router.replace("/login");
      return;
    }
    void refresh().catch((err) => setError(err instanceof Error ? err.message : "Load failed"));
  }, [ready, token, router, refresh]);

  async function onUpload(e: FormEvent) {
    e.preventDefault();
    if (!token || !file) return;
    setBusy(true);
    setUploadError(null);
    try {
      await uploadDocument(token, file, { displayName: displayName || file.name, docType });
      setFile(null);
      setDisplayName("");
      await refresh();
    } catch (err) {
      setUploadError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setBusy(false);
    }
  }

  async function onDelete(id: string, name: string) {
    if (!token) return;
    if (!window.confirm(`Delete “${name}”? This removes it from your vault.`)) return;
    await deleteDocument(token, id);
    await refresh();
  }

  async function onDownload(doc: DocumentItem) {
    if (!token) return;
    try {
      await downloadDocument(token, doc.id, doc.display_name);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Download failed");
    }
  }

  if (!ready || !token) {
    return (
      <main className="mx-auto flex min-h-screen items-center justify-center px-4">
        <p className="text-sm text-ink/70">Loading vault…</p>
      </main>
    );
  }

  return (
    <Shell title="Document vault">
      <section className="mb-8">
        <h2 className="font-display text-xl font-semibold">Upload</h2>
        <p className="mt-1 text-sm text-ink/70">
          PDF, JPEG, PNG, or WebP up to 10 MB. Use synthetic documents only. Files are scanned before
          download is allowed.
        </p>
        <form
          onSubmit={onUpload}
          className="mt-4 space-y-3 rounded-xl border border-ink/10 bg-white/80 p-4"
        >
          <label className="block text-sm">
            <span className="mb-1 block font-medium">File</span>
            <input
              type="file"
              accept=".pdf,image/jpeg,image/png,image/webp"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              required
              className="block w-full text-sm"
            />
          </label>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="block text-sm">
              <span className="mb-1 block font-medium">Display name</span>
              <input
                className="w-full rounded-md border border-ink/20 px-3 py-2"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="Optional"
              />
            </label>
            <label className="block text-sm">
              <span className="mb-1 block font-medium">Type label</span>
              <select
                className="w-full rounded-md border border-ink/20 px-3 py-2"
                value={docType}
                onChange={(e) => setDocType(e.target.value)}
              >
                <option value="unclassified">Unclassified</option>
                <option value="ration_card">Ration card (synthetic)</option>
                <option value="epic">Voter ID (synthetic)</option>
                <option value="income_proof">Income proof (synthetic)</option>
                <option value="photo">Photo</option>
              </select>
            </label>
          </div>
          {uploadError && <p className="text-sm text-red-700">{uploadError}</p>}
          <button
            type="submit"
            disabled={busy || !file}
            className="rounded-md bg-accent px-4 py-2.5 text-sm font-medium text-white disabled:opacity-60"
          >
            {busy ? "Uploading…" : "Upload document"}
          </button>
        </form>
      </section>

      <section>
        <div className="mb-3 flex items-center justify-between gap-3">
          <h2 className="font-display text-xl font-semibold">Your documents</h2>
          <button
            type="button"
            onClick={() => void refresh()}
            className="text-sm text-accent underline-offset-2 hover:underline"
          >
            Refresh
          </button>
        </div>
        {error && <p className="mb-3 text-sm text-red-700">{error}</p>}
        {items.length === 0 ? (
          <div className="rounded-xl border border-dashed border-ink/20 bg-white/50 px-4 py-10 text-center">
            <p className="font-medium">No documents yet</p>
            <p className="mt-1 text-sm text-ink/65">
              Upload a synthetic PDF or image to start building your vault.
            </p>
          </div>
        ) : (
          <ul className="space-y-3">
            {items.map((doc) => (
              <li
                key={doc.id}
                className="rounded-xl border border-ink/10 bg-white/90 p-4 shadow-sm"
              >
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <p className="font-medium">{doc.display_name}</p>
                    <p className="mt-1 text-xs text-ink/60">
                      {doc.doc_type} · {doc.mime_type || "unknown"} · {formatBytes(doc.byte_size)} ·
                      scan: {doc.scan_status}
                    </p>
                    <p className="mt-1 text-xs text-ink/50">
                      Added {new Date(doc.created_at).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <Link
                      href={`/documents/${doc.id}`}
                      className="rounded-md bg-accent px-3 py-1.5 text-sm text-white"
                    >
                      Check details
                    </Link>
                    <button
                      type="button"
                      disabled={!doc.downloadable}
                      onClick={() => void onDownload(doc)}
                      className="rounded-md border border-ink/20 px-3 py-1.5 text-sm disabled:opacity-40"
                    >
                      Download
                    </button>
                    <button
                      type="button"
                      onClick={() => void onDelete(doc.id, doc.display_name)}
                      className="rounded-md border border-red-200 px-3 py-1.5 text-sm text-red-700"
                    >
                      Delete
                    </button>
                  </div>
                </div>
                {!doc.downloadable && (
                  <p className="mt-2 text-xs text-amber-800">
                    Not downloadable until malware scan status is clean (fail-closed quarantine).
                  </p>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>
    </Shell>
  );
}
