import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { vi, beforeEach } from 'vitest';
import { LoginForm } from './LoginForm';
import { AuthProvider } from '../hooks/useAuth';

const okJson = (o: unknown, status = 200) =>
  new Response(JSON.stringify(o), { status, headers: { 'Content-Type': 'application/json' } });

describe('LoginForm', () => {
  let postBody: { login: string; password: string } | null;

  beforeEach(() => {
    postBody = null;
    global.fetch = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.includes('/auth/login') && init?.method === 'POST') {
        postBody = JSON.parse(init.body as string);
        return Promise.resolve(okJson({ status: 'ok', nome: 'Dra Ana', role: 'advogado' }));
      }
      if (url.includes('/me')) {
        return Promise.resolve(okJson({ sub: 'u1', nome: 'Dra Ana', role: 'advogado' }));
      }
      return Promise.resolve(okJson({}, 404));
    }) as any;
  });

  test('submit do form chama POST /auth/login com as credenciais digitadas', async () => {
    render(
      <MemoryRouter initialEntries={['/login']}>
        <AuthProvider><LoginForm /></AuthProvider>
      </MemoryRouter>
    );
    fireEvent.change(screen.getByLabelText('Identificador'), { target: { value: 'ana@judis.adv.br' } });
    fireEvent.change(screen.getByLabelText('Senha'), { target: { value: 'Senha-Forte-2026!' } });
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));

    await waitFor(() => expect(postBody).not.toBeNull());
    expect(postBody?.login).toBe('ana@judis.adv.br');
    expect(postBody?.password).toBe('Senha-Forte-2026!');
  });

  test('credenciais inválidas exibem mensagem de erro', async () => {
    global.fetch = vi.fn(() => Promise.resolve(new Response('{}', { status: 401 }))) as any;
    render(
      <MemoryRouter initialEntries={['/login']}>
        <AuthProvider><LoginForm /></AuthProvider>
      </MemoryRouter>
    );
    fireEvent.change(screen.getByLabelText('Identificador'), { target: { value: 'x@y' } });
    fireEvent.change(screen.getByLabelText('Senha'), { target: { value: 'x' } });
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));
    await waitFor(() => expect(screen.getByRole('alert')).toBeInTheDocument());
    expect(screen.getByRole('alert')).toHaveTextContent(/credenciais|inválidas|invalidas/i);
  });
});
