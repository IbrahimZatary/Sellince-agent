import { createContext, useCallback, useEffect, useState } from "react";
import { login, logout, me, signup, updateMe } from "@/api/auth.api";
import { tokenStore } from "@/api/tokenStore";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [status, setStatus] = useState("loading"); // 'loading' | 'authenticated' | 'unauthenticated'

  // On boot: if a token exists, validate it against the backend (/auth/me).
  const boot = useCallback(async () => {
    if (!tokenStore.get()) {
      setStatus("unauthenticated");
      return;
    }
    try {
      const currentUser = await me();
      setUser(currentUser);
      setStatus("authenticated");
    } catch {
      tokenStore.clear();
      setUser(null);
      setStatus("unauthenticated");
    }
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect -- boot must validate the stored token against /auth/me on mount
    boot();
  }, [boot]);

  const signIn = useCallback(async (credentials) => {
    const data = await login(credentials);
    tokenStore.set(data.access_token);
    const currentUser = await me();
    setUser(currentUser);
    setStatus("authenticated");
    return currentUser;
  }, []);

  const signUp = useCallback(async (form) => {
    const data = await signup(form);
    tokenStore.set(data.access_token);
    const currentUser = await me();
    setUser(currentUser);
    setStatus("authenticated");
    return currentUser;
  }, []);

  const signOut = useCallback(async () => {
    try {
      await logout();
    } catch {
      // ignore: always clear the local session
    }
    tokenStore.clear();
    setUser(null);
    setStatus("unauthenticated");
  }, []);

  const updateProfile = useCallback(async (payload) => {
    const updated = await updateMe(payload);
    setUser(updated);
    return updated;
  }, []);

  return (
    <AuthContext.Provider value={{ user, status, signIn, signUp, signOut, updateProfile }}>
      {children}
    </AuthContext.Provider>
  );
}
