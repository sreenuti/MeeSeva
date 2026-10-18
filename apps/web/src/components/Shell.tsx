"use client";

import Link from "next/link";
import { useAuth } from "@/lib/auth";

export function Shell({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  const { email, logout, mode } = useAuth();

  return (
    <div className="mx-auto min-h-screen max-w-3xl px-4 pb-16 pt-6">
      <header className="mb-8 flex flex-wrap items-end justify-between gap-4 border-b border-ink/10 pb-4">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-accent">Citizen Services</p>
          <h1 className="font-display text-3xl font-semibold text-ink">{title}</h1>
        </div>
        <div className="flex items-center gap-3 text-sm">
          <Link href="/dashboard" className="underline-offset-4 hover:underline">
            Vault
          </Link>
          <Link href="/profile" className="underline-offset-4 hover:underline">
            Profile
          </Link>
          <span className="text-ink/40">|</span>
          <span className="max-w-[12rem] truncate text-ink/70" title={email || ""}>
            {email || "Signed in"}
          </span>
          <button
            type="button"
            onClick={() => void logout()}
            className="rounded-md bg-ink px-3 py-1.5 text-sand"
          >
            Log out
          </button>
        </div>
      </header>
      {mode === "dev" && (
        <p className="mb-4 rounded-md border border-amber-300 bg-amber-50 px-3 py-2 text-sm text-amber-900">
          Development auth mode. Cognito MFA is required for staging/production.
        </p>
      )}
      {children}
    </div>
  );
}
