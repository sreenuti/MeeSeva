"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { appConfig, cognitoConfigured } from "@/lib/config";

export default function RegisterPage() {
  const { registerCognito, confirmCognito, mode } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [code, setCode] = useState("");
  const [step, setStep] = useState<"signup" | "confirm">("signup");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  if (mode !== "cognito" || !cognitoConfigured()) {
    return (
      <main className="mx-auto max-w-md px-4 py-16">
        <h1 className="font-display text-3xl font-semibold">Registration</h1>
        <p className="mt-3 text-ink/70">
          Cognito registration is available when{" "}
          <code className="text-sm">NEXT_PUBLIC_AUTH_MODE=cognito</code> and pool settings are
          configured. Current mode: {appConfig.authMode}.
        </p>
        <Link href="/login" className="mt-6 inline-block text-accent underline">
          Back to sign in
        </Link>
      </main>
    );
  }

  async function onSignup(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const next = await registerCognito(email, password);
      if (next === "CONFIRM_SIGN_UP") setStep("confirm");
      else router.push("/login");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setBusy(false);
    }
  }

  async function onConfirm(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await confirmCognito(email, code);
      router.push("/login");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Confirmation failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4 py-10">
      <h1 className="font-display text-4xl font-semibold text-ink">Create account</h1>
      <p className="mt-2 text-ink/70">
        MFA will be enforced by the Cognito user pool configuration after sign-in.
      </p>

      {step === "signup" ? (
        <form onSubmit={onSignup} className="mt-8 space-y-4 rounded-xl border border-ink/10 bg-white/80 p-5">
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
          <label className="block text-sm">
            <span className="mb-1 block font-medium">Password</span>
            <input
              type="password"
              className="w-full rounded-md border border-ink/20 px-3 py-2"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={12}
            />
          </label>
          {error && <p className="text-sm text-red-700">{error}</p>}
          <button
            type="submit"
            disabled={busy}
            className="w-full rounded-md bg-accent px-4 py-2.5 font-medium text-white"
          >
            {busy ? "Creating…" : "Create account"}
          </button>
        </form>
      ) : (
        <form onSubmit={onConfirm} className="mt-8 space-y-4 rounded-xl border border-ink/10 bg-white/80 p-5">
          <p className="text-sm text-ink/70">Enter the verification code sent to {email}.</p>
          <label className="block text-sm">
            <span className="mb-1 block font-medium">Confirmation code</span>
            <input
              className="w-full rounded-md border border-ink/20 px-3 py-2"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              required
            />
          </label>
          {error && <p className="text-sm text-red-700">{error}</p>}
          <button
            type="submit"
            disabled={busy}
            className="w-full rounded-md bg-accent px-4 py-2.5 font-medium text-white"
          >
            {busy ? "Confirming…" : "Confirm account"}
          </button>
        </form>
      )}

      <Link href="/login" className="mt-4 text-sm text-accent underline">
        Already registered? Sign in
      </Link>
    </main>
  );
}
