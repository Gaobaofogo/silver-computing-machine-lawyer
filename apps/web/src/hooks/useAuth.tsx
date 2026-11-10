/**
 * useAuth — hook de autenticação do frontend (ADR-0006).
 *
 * Persiste sessão em cookie HttpOnly (no backend). Frontend só consome /me
 * para popular o contexto; token nunca viaja em localStorage. LGPD:
 *   - Não persiste CPF/email em localStorage.
 *   - Logout não toca storage; cookie é expirado pelo backend
 *     (Set-Cookie Max-Age=0 quando POST /auth/logout existir;
 *      no MVP usamos limpeza de contexto no cliente + cookie Max-Age=0).
 */
import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export interface AuthUser { user_id: string; nome: string; role: string }

interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (login: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue>({
  user: null,
  isAuthenticated: false,
  loading: true,
  login: async () => false,
  logout: async () => {},
});

const fetchWithCreds = (url: string, init: RequestInit = {}) =>
  fetch(url, { credentials: 'include', ...init });

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const refresh = useCallback(async () => {
    try {
      const r = await fetchWithCreds('/me');
      if (!r.ok) { setUser(null); setLoading(false); return; }
      const body = await r.json();
      setUser({ user_id: body.sub ?? body.user_id, nome: body.nome, role: body.role });
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);

  const login = useCallback(async (loginStr: string, password: string) => {
    try {
      const r = await fetchWithCreds('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login: loginStr, password }),
      });
      if (!r.ok) return false;
      // Cookie HttpOnly set pelo backend; refazemos /me para resolver sub/nome/role.
      await refresh();
      navigate('/processos', { replace: true });
      return true;
    } catch {
      return false;
    }
  }, [navigate, refresh]);

  const logout = useCallback(async () => {
    // limpar cookie enviando header Expires para o backend
    try {
      await fetchWithCreds('/auth/logout', { method: 'POST' });
    } catch {
      // backend pode ainda não expor /auth/logout — manter cliente idempotente
    }
    setUser(null);
    navigate('/login', { replace: true });
  }, [navigate]);

  const isAuthenticated = !!user;
  return (
    <AuthContext.Provider value={{ user, isAuthenticated, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextValue => useContext(AuthContext);
