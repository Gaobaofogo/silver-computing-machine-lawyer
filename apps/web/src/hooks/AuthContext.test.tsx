import { renderHook, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { vi, beforeEach } from 'vitest';
import { AuthProvider, useAuth, AuthContext } from './AuthContext';
import React from 'react';

const okJson = (o: unknown) => new Response(JSON.stringify(o), { status: 200, headers: { 'Content-Type': 'application/json' } });

describe('AuthContext — MVP 05', () => {
  beforeEach(() => {
    global.fetch = vi.fn(() => Promise.resolve(okJson({ sub: 'u1', nome: 'Dra Ana', role: 'advogado' }))) as any;
  });

  test('useAuth expõe o role como string (ADR-0006 — sem token em JS)', async () => {
    const wrapper = ({ children }: { children: React.ReactNode }) => (
      <MemoryRouter initialEntries={['/']}>
        <AuthProvider>{children}</AuthProvider>
      </MemoryRouter>
    );
    const { result } = renderHook(() => useAuth(), { wrapper });
    await waitFor(() => expect(result.current.isAuthenticated).toBe(true));
    expect(typeof result.current.user?.role).toBe('string');
    expect(result.current.user?.role).toBe('advogado');
    expect(result.current.user).not.toHaveProperty('token');
  });
});
