import { render, screen } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import { vi, beforeEach, afterEach } from 'vitest';
import { RequireRole } from './RequireRole';
import { useAuth } from '../hooks/useAuth';

vi.mock('../hooks/useAuth', () => ({
  useAuth: vi.fn(),
  AuthProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
}));
import React from 'react';

describe('RequireRole', () => {
  const mockLoggedIn = (role: string) => vi.mocked(useAuth).mockReturnValue({
    user: { user_id: 'x', nome: 'User', role },
    isAuthenticated: true,
    loading: false,
    login: async () => true,
    logout: async () => {},
  } as any);

  beforeEach(() => { vi.mocked(useAuth).mockReset(); });
  afterEach(() => vi.clearAllMocks());

  test('redireciona usuario nao autenticado para /login', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: null, isAuthenticated: false, loading: false,
      login: async () => false, logout: async () => {},
    } as any);
    render(
      <MemoryRouter initialEntries={['/processos']}>
        <Routes>
          <Route path="/login" element={<button data-testid="login-page">Entrar</button>} />
          <Route path="/processos" element={<RequireRole><div data-testid="ok">OK</div></RequireRole>} />
        </Routes>
      </MemoryRouter>
    );
    expect(screen.queryByTestId('ok')).not.toBeInTheDocument();
    expect(screen.getByTestId('login-page')).toBeInTheDocument();
  });

  test('admin enxerga /admin/auditoria; assistente e redirecionado', () => {
    mockLoggedIn('admin');
    const { rerender } = render(
      <MemoryRouter initialEntries={['/admin/auditoria']}>
        <Routes>
          <Route path="/login" element={<div data-testid="login-page" />} />
          <Route path="/admin/auditoria" element={<RequireRole roles={['admin']}><div data-testid="audit">audit</div></RequireRole>} />
        </Routes>
      </MemoryRouter>
    );
    expect(screen.getByTestId('audit')).toBeInTheDocument();

    mockLoggedIn('assistente');
    rerender(
      <MemoryRouter initialEntries={['/admin/auditoria']}>
        <Routes>
          <Route path="/login" element={<div data-testid="login-block-page" />} />
          <Route path="/admin/auditoria" element={<RequireRole roles={['admin']}><div data-testid="audit-2">x</div></RequireRole>} />
        </Routes>
      </MemoryRouter>
    );
    expect(screen.getByTestId('login-block-page')).toBeInTheDocument();
  });

  test('roles vazio permite qualquer usuario autenticado', () => {
    mockLoggedIn('assistente');
    render(
      <MemoryRouter initialEntries={['/clientes']}>
        <Routes>
          <Route path="/clientes" element={<RequireRole><div data-testid="cli">clientes</div></RequireRole>} />
        </Routes>
      </MemoryRouter>
    );
    expect(screen.getByTestId('cli')).toBeInTheDocument();
  });
});
