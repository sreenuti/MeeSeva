"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";

export default function HomePage() {
  const { ready, token } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!ready) return;
    router.replace(token ? "/dashboard" : "/login");
  }, [ready, token, router]);

  return (
    <main className="mx-auto flex min-h-screen max-w-lg items-center justify-center px-4">
      <p className="text-sm text-ink/70">Loading…</p>
    </main>
  );
}
