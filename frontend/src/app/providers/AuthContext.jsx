import { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { login, logout, me, signup } from '../../services/api/auth.api';
import { tokenStore } from '../../services/api/tokenStore';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [status, setStatus] = useState('loading'); // 'loading' | 'authenticated' | 'unauthenticated'

  // On boot: if a token exists, validate it against the backend (/auth/me).
  const boot = useCallback(async () => {
    if (!tokenStore.get()) {
      setStatus('unauthenticated');
      return;
    }
    try {
      const currentUser = await me();
      setUser(currentUser);
      setStatus('authenticated');
    } catch {
      tokenStore.clear();
      setUser(null);
      setStatus('unauthenticated');
    }
  }, []);

  useEffect(() => {
    boot();
  }, [boot]);

  const signIn = useCallback(async (credentials) => {
    const data = await login(credentials);
    tokenStore.set(data.access_token);
    const currentUser = await me();
    setUser(currentUser);
    setStatus('authenticated');
    return currentUser;
  }, []);

  const signUp = useCallback(async (form) => {
    const data = await signup(form);
    tokenStore.set(data.access_token);
    const currentUser = await me();
    setUser(currentUser);
    setStatus('authenticated');
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
    setStatus('unauthenticated');
  }, []);

  return (
    <AuthContext.Provider value={{ user, status, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);