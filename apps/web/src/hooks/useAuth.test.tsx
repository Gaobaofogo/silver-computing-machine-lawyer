import { renderHook, act, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useAuth, AuthProvider } from './useAuth';
import { vi, beforeEach, afterEach } from 'vitest';

const okJson = (obj: unknown, status = 200) =>
  new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json' } });

describe('useAuth (RBAC)', () => {
  beforeEach(() => {
    global.fetch = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes('/auth/login')) {
        return Promise.resolve(okJson({ status: 'ok', nome: 'Dra Ana', role: 'advogado' }));
      }
      if (url.includes('/me')) {
        return Promise.resolve(okJson({ sub: '00000000-0000-0000-0000-000000000001', nome: 'Dra Ana', role: 'advogado' }));
      }
      return Promise.resolve(okJson({ status: 'error' }, 404));
    }) as any;
  });
  afterEach(() => { vi.restoreAllMocks(); });

  test('login POSTs para /auth/login e popula user via /me', async () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
    <MemoryRouter initialEntries={['/login']}>
      <AuthProvider>{children}</AuthProvider>
    </MemoryRouter>
  );
    const { result } = renderHook(() => useAuth(), { wrapper });
    // login resolve + refresh popular /me no contexto
    await act(async () => { await result.current.login('ana@judis.adv.br', 'Senha-Forte-2026!'); });
    expect(result.current.isAuthenticated).toBe(true);
    expect(result.current.user?.role).toBe('advogado');
    expect(result.current.user?.nome).toBe('Dra Ana');
    expect(result.current.user?.user_id).toBe('00000000-0000-0000-0000-000000000001');
    // POST foi chamado com credenciais
    expect((global.fetch as any).mock.calls.some((c: any[]) => String(c[0]).includes('/auth/login'))).toBe(true);
  });

  test('isAuthenticated=false quando /me retorna 401', async () => {
    global.fetch = vi.fn(() => Promise.resolve(new Response('{}', { status: 401 }))) as any;
    const wrapper = ({ children }: { children: React.ReactNode }) => (
    <MemoryRouter initialEntries={['/login']}>
      <AuthProvider>{children}</AuthProvider>
    </MemoryRouter>
  );
    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(result.current.isAuthenticated).toBe(false);
  });

  test('logout apaga contexto', async () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
    <MemoryRouter initialEntries={['/login']}>
      <AuthProvider>{children}</AuthProvider>
    </MemoryRouter>
  );
    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.loading).toBe(false));
    await act(async () => { await result.current.logout(); });
    expect(result.current.isAuthenticated).toBe(false);
  });
});
