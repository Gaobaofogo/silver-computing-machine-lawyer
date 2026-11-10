/**
 * LoginForm — ADR-0006 (cookie HttpOnly; sem token em JS).
 *
 * Comportamento:
 *   - Envia POST /auth/login (cookie Set-Cookie SameSite=Strict) via useAuth.
 *   - Em caso de sucesso, `useAuth.login()` navega para `/processos`.
 *   - Em caso de 401, exibe `Credenciais inválidas` (rotulado `role="alert"`).
 */
import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

export const LoginForm: React.FC = () => {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { login: doLogin } = useAuth();

  const submit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const ok = await doLogin(login.trim(), password);
      if (!ok) setError('Credenciais inválidas');
    } catch {
      setError('Erro ao entrar — tente novamente');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto bg-white rounded-2xl shadow" aria-label="LoginForm">
      <h2 className="text-2xl font-bold text-blue-900 mb-4">Entrar no Judis</h2>
      {error && <div role="alert" className="text-rose-700 text-sm p-2 bg-rose-50 border border-rose-300 rounded">{error}</div>}
      <form onSubmit={submit} className="flex flex-col gap-3">
        <label className="text-sm font-semibold" htmlFor="login-input">Identificador</label>
        <input
          id="login-input"
          type="text"
          aria-label="Identificador"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
          required
          className="border rounded px-3 py-2"
        />
        <label className="text-sm font-semibold" htmlFor="senha-input">Senha</label>
        <input
          id="senha-input"
          type="password"
          aria-label="Senha"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="border rounded px-3 py-2"
        />
        <button type="submit" disabled={loading}
                className="rounded bg-blue-700 text-white py-2 disabled:opacity-60">
          {loading ? 'Entrando…' : 'Entrar'}
        </button>
      </form>
    </div>
  );
};
