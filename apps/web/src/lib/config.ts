export type AuthMode = "cognito" | "dev";

export const appConfig = {
  apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
  authMode: (process.env.NEXT_PUBLIC_AUTH_MODE || "dev") as AuthMode,
  cognito: {
    region: process.env.NEXT_PUBLIC_COGNITO_REGION || "",
    userPoolId: process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID || "",
    appClientId: process.env.NEXT_PUBLIC_COGNITO_APP_CLIENT_ID || "",
  },
};

export function cognitoConfigured(): boolean {
  return Boolean(
    appConfig.cognito.region &&
      appConfig.cognito.userPoolId &&
      appConfig.cognito.appClientId,
  );
}
