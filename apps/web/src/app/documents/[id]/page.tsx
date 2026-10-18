"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { Shell } from "@/components/Shell";
import { useAuth } from "@/lib/auth";
import {
  ExtractionResult,
  ProcessJob,
  getExtraction,
  getProcessingStatus,
  reviewExtractedField,
  startProcessing,
  updateClassification,
} from "@/lib/api";

const CATEGORY_LABELS: Record<string, string> = {
  identity_proof: "Identity proof",
  address_proof: "Address proof",
  income_proof: "Income proof",
  unknown: "Unknown / unsupported",
};

export default function DocumentIntelligencePage() {
  const { id } = useParams<{ id: string }>();
  const { ready, token } = useAuth();
  const router = useRouter();
  const [job, setJob] = useState<ProcessJob | null>(null);
  const [extraction, setExtraction] = useState<ExtractionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [edits, setEdits] = useState<Record<string, string>>({});

  const refresh = useCallback(async () => {
    if (!token || !id) return;
    try {
      const status = await getProcessingStatus(token, id);
      setJob(status);
      if (["awaiting_user_review", "completed"].includes(status.status)) {
        setExtraction(await getExtraction(token, id));
      }
    } catch {
      setJob(null);
      setExtraction(null);
    }
  }, [token, id]);

  useEffect(() => {
    if (!ready) return;
    if (!token) {
      router.replace("/login");
      return;
    }
    void refresh();
  }, [ready, token, router, refresh]);

  async function onProcess() {
    if (!token || !id) return;
    setBusy(true);
    setError(null);
    try {
      const status = await startProcessing(token, id);
      setJob(status);
      if (["awaiting_user_review", "completed"].includes(status.status)) {
        setExtraction(await getExtraction(token, id));
      } else if (status.status === "queued" || status.status === "processing") {
        // Poll briefly for background completion in non-test environments
        for (let i = 0; i < 20; i++) {
          await new Promise((r) => setTimeout(r, 500));
          const next = await getProcessingStatus(token, id);
          setJob(next);
          if (!["queued", "processing"].includes(next.status)) {
            if (["awaiting_user_review", "completed"].includes(next.status)) {
              setExtraction(await getExtraction(token, id));
            }
            break;
          }
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Processing failed");
    } finally {
      setBusy(false);
    }
  }

  async function onCategoryChange(category: string) {
    if (!token || !id) return;
    setExtraction(await updateClassification(token, id, category));
  }

  async function onReview(fieldId: string, action: "confirm" | "correct" | "reject") {
    if (!token) return;
    setBusy(true);
    setError(null);
    try {
      await reviewExtractedField(token, fieldId, {
        action,
        value: action === "correct" ? edits[fieldId] : undefined,
      });
      setExtraction(await getExtraction(token, id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not save");
    } finally {
      setBusy(false);
    }
  }

  if (!ready || !token) {
    return (
      <main className="mx-auto flex min-h-screen items-center justify-center px-4">
        <p className="text-sm text-ink/70">Loading…</p>
      </main>
    );
  }

  return (
    <Shell title="Check document details">
      <p className="mb-4 text-sm text-ink/70">
        <Link href="/dashboard" className="text-accent underline">
          Back to vault
        </Link>
      </p>

      <section className="mb-6 rounded-xl border border-ink/10 bg-white/80 p-4">
        <h2 className="font-display text-lg font-semibold">Read information from this document</h2>
        <p className="mt-1 text-sm text-ink/70">
          We only process documents that have passed security checks. Please review everything we find —
          nothing is treated as confirmed until you approve it.
        </p>
        <button
          type="button"
          disabled={busy}
          onClick={() => void onProcess()}
          className="mt-4 rounded-md bg-accent px-4 py-2.5 text-sm font-medium text-white disabled:opacity-60"
        >
          {busy ? "Working…" : job ? "Process again" : "Find information"}
        </button>
        {job && (
          <p className="mt-3 text-sm text-ink/70">
            Status: <span className="font-medium text-ink">{job.status.replaceAll("_", " ")}</span>
            {job.error_message ? ` — ${job.error_message}` : ""}
          </p>
        )}
        {error && <p className="mt-2 text-sm text-red-700">{error}</p>}
      </section>

      {extraction && (
        <>
          <section className="mb-6 rounded-xl border border-ink/10 bg-white/80 p-4">
            <h2 className="font-display text-lg font-semibold">Document type</h2>
            <p className="mt-1 text-sm text-ink/70">
              Suggested: {CATEGORY_LABELS[extraction.predicted_category] || extraction.predicted_category}{" "}
              (certainty: {extraction.category_certainty})
            </p>
            <label className="mt-3 block text-sm">
              <span className="mb-1 block font-medium">Correct type if needed</span>
              <select
                className="w-full rounded-md border border-ink/20 px-3 py-2 sm:max-w-xs"
                value={extraction.effective_category}
                onChange={(e) => void onCategoryChange(e.target.value)}
              >
                {Object.entries(CATEGORY_LABELS).map(([value, label]) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>
            </label>
          </section>

          <section className="rounded-xl border border-ink/10 bg-white/80 p-4">
            <h2 className="font-display text-lg font-semibold">We found the following information</h2>
            <p className="mt-1 text-sm text-ink/70">Please check whether these details are correct.</p>
            {extraction.fields.length === 0 ? (
              <p className="mt-4 text-sm text-ink/70">
                We couldn&apos;t read structured information. You can enter details later in your profile.
              </p>
            ) : (
              <ul className="mt-4 space-y-4">
                {extraction.fields.map((field) => (
                  <li key={field.id} className="border-t border-ink/10 pt-4">
                    <p className="text-xs uppercase tracking-wide text-ink/50">
                      {field.field_key.replaceAll("_", " ")}
                    </p>
                    <p className="mt-1 font-medium">
                      {field.normalized_value || field.raw_value || "—"}
                    </p>
                    <p className="mt-1 text-xs text-ink/55">
                      Status: {field.verification_status.replaceAll("_", " ")} · confidence:{" "}
                      {field.confidence}
                      {field.source_page ? ` · page ${field.source_page}` : ""}
                    </p>
                    {field.source_text_snippet && (
                      <p className="mt-1 text-xs text-ink/50">Source: “{field.source_text_snippet}”</p>
                    )}
                    {!["user_verified", "user_corrected", "rejected"].includes(field.verification_status) && (
                      <div className="mt-3 flex flex-col gap-2 sm:flex-row sm:flex-wrap sm:items-center">
                        <input
                          className="w-full rounded-md border border-ink/20 px-3 py-2 text-sm sm:max-w-xs"
                          placeholder="Corrected value"
                          value={edits[field.id] ?? field.normalized_value ?? field.raw_value ?? ""}
                          onChange={(e) => setEdits((prev) => ({ ...prev, [field.id]: e.target.value }))}
                        />
                        <button
                          type="button"
                          disabled={busy}
                          onClick={() => void onReview(field.id, "confirm")}
                          className="rounded-md bg-ink px-3 py-1.5 text-sm text-sand"
                        >
                          Looks correct
                        </button>
                        <button
                          type="button"
                          disabled={busy}
                          onClick={() => void onReview(field.id, "correct")}
                          className="rounded-md border border-ink/20 px-3 py-1.5 text-sm"
                        >
                          Save correction
                        </button>
                        <button
                          type="button"
                          disabled={busy}
                          onClick={() => void onReview(field.id, "reject")}
                          className="rounded-md border border-red-200 px-3 py-1.5 text-sm text-red-700"
                        >
                          Reject
                        </button>
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </section>
        </>
      )}
    </Shell>
  );
}
