import { test, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../src/App';
import { useAuth } from '../src/hooks/useAuth';

vi.mock('../src/hooks/useAuth', () => ({
  AuthProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>,
  useAuth: vi.fn(),
}));
import React from 'react';

test('renderiza shell Minimal com a marca Judis quando autenticado', () => {
  vi.mocked(useAuth).mockReturnValue({
    user: { user_id: 'u', nome: 'Dra Ana', role: 'admin' },
    isAuthenticated: true, loading: false,
    login: async () => true, logout: async () => {},
  } as any);
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
  expect(screen.getAllByText(/Judis/i).length).toBeGreaterThan(0);
});
