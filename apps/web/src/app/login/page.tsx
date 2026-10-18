"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";

export default function LoginPage() {
  const { mode, loginDev, loginCognito } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("citizen.a@example.com");
  const [password, setPassword] = useState("");
  const [subject, setSubject] = useState("user-a-subject");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      if (mode === "dev") {
        await loginDev(subject, email);
      } else {
        await loginCognito(email, password);
      }
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4 py-10">
      <p className="text-xs uppercase tracking-[0.18em] text-accent">Citizen Services</p>
      <h1 className="mt-2 font-display text-4xl font-semibold text-ink">Sign in</h1>
      <p className="mt-2 text-ink/70">
        Secure access to your private document vault. Synthetic identities only during development.
      </p>

      <form onSubmit={onSubmit} className="mt-8 space-y-4 rounded-xl border border-ink/10 bg-white/80 p-5 shadow-sm">
        {mode === "dev" && (
          <label className="block text-sm">
            <span className="mb-1 block font-medium">Dev subject</span>
            <input
              className="w-full rounded-md border border-ink/20 px-3 py-2"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              required
            />
          </label>
        )}
        <label className="block text-sm">
          <span className="mb-1 block font-medium">Email</span>
          <input
            type="email"
            className="w-full rounded-md border border-ink/20 px-3 py-2"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        {mode === "cognito" && (
          <label className="block text-sm">
            <span className="mb-1 block font-medium">Password</span>
            <input
              type="password"
              className="w-full rounded-md border border-ink/20 px-3 py-2"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>
        )}
        {error && <p className="text-sm text-red-700">{error}</p>}
        <button
          type="submit"
          disabled={busy}
          className="w-full rounded-md bg-accent px-4 py-2.5 font-medium text-white disabled:opacity-60"
        >
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>

      {mode === "cognito" && (
        <p className="mt-4 text-sm text-ink/70">
          New citizen?{" "}
          <Link href="/register" className="font-medium text-accent underline-offset-2 hover:underline">
            Create an account
          </Link>
        </p>
      )}
      {mode === "dev" && (
        <p className="mt-4 text-sm text-ink/60">
          Tip: use different subjects (user-a-subject / user-b-subject) to verify ownership isolation.
        </p>
      )}
    </main>
  );
}
