"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { Amplify } from "aws-amplify";
import {
  confirmSignUp,
  fetchAuthSession,
  signIn,
  signOut,
  signUp,
} from "aws-amplify/auth";
import { appConfig, cognitoConfigured } from "./config";
import { mintDevToken, recordVaultConsent } from "./api";

type AuthState = {
  ready: boolean;
  token: string | null;
  email: string | null;
  mode: "cognito" | "dev";
  loginDev: (subject: string, email: string) => Promise<void>;
  loginCognito: (email: string, password: string) => Promise<void>;
  registerCognito: (email: string, password: string) => Promise<"CONFIRM_SIGN_UP" | "DONE">;
  confirmCognito: (email: string, code: string) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthState | null>(null);

let amplifyConfigured = false;

function ensureAmplify() {
  if (amplifyConfigured || !cognitoConfigured()) return;
  Amplify.configure({
    Auth: {
      Cognito: {
        userPoolId: appConfig.cognito.userPoolId,
        userPoolClientId: appConfig.cognito.appClientId,
      },
    },
  });
  amplifyConfigured = true;
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [email, setEmail] = useState<string | null>(null);
  const mode: "cognito" | "dev" =
    appConfig.authMode === "cognito" && cognitoConfigured() ? "cognito" : "dev";

  useEffect(() => {
    async function hydrate() {
      if (mode === "dev") {
        const saved = sessionStorage.getItem("dev_access_token");
        const savedEmail = sessionStorage.getItem("dev_email");
        if (saved) {
          setToken(saved);
          setEmail(savedEmail);
        }
        setReady(true);
        return;
      }
      ensureAmplify();
      try {
        const session = await fetchAuthSession();
        const access = session.tokens?.accessToken?.toString() ?? null;
        setToken(access);
        setEmail(session.tokens?.idToken?.payload?.email?.toString() ?? null);
      } catch {
        setToken(null);
      } finally {
        setReady(true);
      }
    }
    void hydrate();
  }, [mode]);

  const loginDev = useCallback(async (subject: string, emailValue: string) => {
    const data = await mintDevToken(subject, emailValue);
    sessionStorage.setItem("dev_access_token", data.access_token);
    sessionStorage.setItem("dev_email", emailValue);
    setToken(data.access_token);
    setEmail(emailValue);
    try {
      await recordVaultConsent(data.access_token);
    } catch {
      // consent may already exist
    }
  }, []);

  const loginCognito = useCallback(async (emailValue: string, password: string) => {
    ensureAmplify();
    await signIn({ username: emailValue, password });
    const session = await fetchAuthSession();
    const access = session.tokens?.accessToken?.toString();
    if (!access) throw new Error("No access token after sign-in");
    setToken(access);
    setEmail(emailValue);
    try {
      await recordVaultConsent(access);
    } catch {
      // ignore duplicate consent
    }
  }, []);

  const registerCognito = useCallback(async (emailValue: string, password: string) => {
    ensureAmplify();
    const result = await signUp({
      username: emailValue,
      password,
      options: { userAttributes: { email: emailValue } },
    });
    return result.nextStep.signUpStep === "CONFIRM_SIGN_UP" ? "CONFIRM_SIGN_UP" : "DONE";
  }, []);

  const confirmCognito = useCallback(async (emailValue: string, code: string) => {
    ensureAmplify();
    await confirmSignUp({ username: emailValue, confirmationCode: code });
  }, []);

  const logout = useCallback(async () => {
    if (mode === "dev") {
      sessionStorage.removeItem("dev_access_token");
      sessionStorage.removeItem("dev_email");
      setToken(null);
      setEmail(null);
      return;
    }
    ensureAmplify();
    await signOut();
    setToken(null);
    setEmail(null);
  }, [mode]);

  const value = useMemo(
    () => ({
      ready,
      token,
      email,
      mode,
      loginDev,
      loginCognito,
      registerCognito,
      confirmCognito,
      logout,
    }),
    [ready, token, email, mode, loginDev, loginCognito, registerCognito, confirmCognito, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
