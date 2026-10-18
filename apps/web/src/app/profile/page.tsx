"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Shell } from "@/components/Shell";
import { useAuth } from "@/lib/auth";
import {
  CitizenProfile,
  ProfileField,
  getConflicts,
  getProfile,
  resolveConflict,
} from "@/lib/api";

type Candidate = {
  value: string;
  source_document_id?: string | null;
  source_extracted_field_id?: string | null;
  label?: string;
};

export default function ProfilePage() {
  const { ready, token } = useAuth();
  const router = useRouter();
  const [profile, setProfile] = useState<CitizenProfile | null>(null);
  const [conflicts, setConflicts] = useState<ProfileField[]>([]);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    if (!token) return;
    setProfile(await getProfile(token));
    setConflicts(await getConflicts(token));
  }, [token]);

  useEffect(() => {
    if (!ready) return;
    if (!token) {
      router.replace("/login");
      return;
    }
    void refresh().catch((err) => setError(err instanceof Error ? err.message : "Load failed"));
  }, [ready, token, router, refresh]);

  async function onResolve(field: ProfileField, value: string, sourceId?: string | null) {
    if (!token) return;
    await resolveConflict(token, {
      field_key: field.field_key,
      value,
      source_extracted_field_id: sourceId || undefined,
    });
    await refresh();
  }

  if (!ready || !token || !profile) {
    return (
      <main className="mx-auto flex min-h-screen items-center justify-center px-4">
        <p className="text-sm text-ink/70">Loading profile…</p>
      </main>
    );
  }

  const verified = profile.fields.filter((f) => f.verification_state === "verified");
  const unverified = profile.fields.filter((f) =>
    ["unverified", "needs_review"].includes(f.verification_state),
  );

  return (
    <Shell title="Your information">
      <p className="mb-6 text-sm text-ink/70">
        This profile is built only from details you confirm. Extracted values are never treated as
        confirmed on their own.
      </p>
      {error && <p className="mb-4 text-sm text-red-700">{error}</p>}

      {conflicts.length > 0 && (
        <section className="mb-8 rounded-xl border border-amber-300 bg-amber-50 p-4">
          <h2 className="font-display text-lg font-semibold text-amber-950">Needs your decision</h2>
          <p className="mt-1 text-sm text-amber-900">
            Two documents contain different values. Which one should we use?
          </p>
          <ul className="mt-4 space-y-4">
            {conflicts.map((field) => {
              let candidates: Candidate[] = [];
              try {
                candidates = field.conflict_candidates_json
                  ? (JSON.parse(field.conflict_candidates_json) as Candidate[])
                  : [];
              } catch {
                candidates = [];
              }
              return (
                <li key={field.id} className="rounded-md border border-amber-200 bg-white/80 p-3">
                  <p className="text-xs uppercase tracking-wide text-ink/50">
                    {field.field_key.replaceAll("_", " ")}
                  </p>
                  <div className="mt-2 flex flex-col gap-2">
                    {candidates.map((c, idx) => (
                      <button
                        key={`${field.id}-${idx}`}
                        type="button"
                        onClick={() =>
                          void onResolve(field, c.value, c.source_extracted_field_id)
                        }
                        className="rounded-md border border-ink/15 px-3 py-2 text-left text-sm hover:border-accent"
                      >
                        Use “{c.value}”
                        {c.label ? ` (${c.label.replaceAll("_", " ")})` : ""}
                      </button>
                    ))}
                  </div>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      <section className="mb-8">
        <h2 className="font-display text-xl font-semibold">Confirmed</h2>
        {verified.length === 0 ? (
          <p className="mt-2 text-sm text-ink/65">No confirmed details yet.</p>
        ) : (
          <ul className="mt-3 space-y-3">
            {verified.map((field) => (
              <li key={field.id} className="rounded-xl border border-ink/10 bg-white/90 p-4">
                <p className="text-xs uppercase tracking-wide text-ink/50">
                  {field.field_key.replaceAll("_", " ")}
                </p>
                <p className="mt-1 font-medium">{field.value}</p>
                {field.original_extracted_value && field.user_corrected && (
                  <p className="mt-1 text-xs text-ink/50">
                    Originally found as “{field.original_extracted_value}”
                  </p>
                )}
                {field.source_document_id && (
                  <p className="mt-1 text-xs text-ink/45">Source document on file</p>
                )}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2 className="font-display text-xl font-semibold">Not yet confirmed</h2>
        {unverified.length === 0 ? (
          <p className="mt-2 text-sm text-ink/65">Nothing waiting for confirmation.</p>
        ) : (
          <ul className="mt-3 space-y-3">
            {unverified.map((field) => (
              <li key={field.id} className="rounded-xl border border-dashed border-ink/15 bg-white/60 p-4">
                <p className="text-xs uppercase tracking-wide text-ink/50">
                  {field.field_key.replaceAll("_", " ")}
                </p>
                <p className="mt-1 font-medium">{field.value || "—"}</p>
                <p className="mt-1 text-xs text-ink/50">{field.verification_state}</p>
              </li>
            ))}
          </ul>
        )}
      </section>
    </Shell>
  );
}
