import React from 'react';
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { vi, beforeEach, afterEach } from 'vitest';
import { ProcessoDetalhe } from './ProcessoDetalhe';
import { useAuth } from '../hooks/useAuth';

vi.mock('../hooks/useAuth', () => ({ useAuth: vi.fn() }));
import { useAuth as _useAuth } from '../hooks/useAuth';
const mockUseAuth = vi.mocked(_useAuth);

const okJson = (o: unknown, status = 200) =>
  new Response(JSON.stringify(o), { status, headers: { 'Content-Type': 'application/json' } });

const MOCK_MOVS = [
  { movimento_id: 'm1', processo_id: 'p1', data_movimento: '2026-10-01', tipo: 'Petição',
    descricao: 'Moção inicial', status_anterior: 'Cadastrado', status_novo: 'Em Andamento',
    created_at: '2026-10-01T10:00:00-03:00' },
  { movimento_id: 'm2', processo_id: 'p1', data_movimento: '2026-11-05', tipo: 'Audiência',
    descricao: 'Instrução', status_anterior: 'Em Andamento', status_novo: 'Concluido',
    created_at: '2026-11-05T14:00:00-03:00' },
];

const renderWithRole = (role: string, ui: React.ReactElement) => {
  mockUseAuth.mockReturnValue({
    user: { user_id: 'u', nome: 'Test', role }, isAuthenticated: true, loading: false,
    login: async () => true, logout: async () => {},
  } as any);
  return render(<MemoryRouter initialEntries={['/processos/p1']}>{ui}</MemoryRouter>);
};

describe('ProcessoDetalhe — timeline + RBAC', () => {
  beforeEach(() => {
    global.fetch = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.startsWith('/movimentos') && url.includes('processo_id=')) {
        return Promise.resolve(okJson({ status: 'listado', movimentos: MOCK_MOVS }));
      }
      if (url.startsWith('/movimentos') && init?.method === 'POST') {
        return Promise.resolve(okJson({ status: 'criado', movimento: { movimento_id: 'm3', processo_id: 'p1',
          data_movimento: '2026-11-10', tipo: 'Petição', descricao: 'Envio de docs', status_anterior: 'Concluido',
          status_novo: 'Concluido', created_at: '2026-11-10T11:00:00-03:00' } }, 201));
      }
      if (url.startsWith('/processos/') && init?.method === 'DELETE') {
        return Promise.resolve(okJson({ status: 'deletado', processo: { id: 'p1' } }));
      }
      return Promise.resolve(okJson({ status: 'error' }, 404));
    }) as any;
  });
  afterEach(() => vi.clearAllMocks());

  test('renders detalhes + timeline ordenada (m1 antes de m2)', async () => {
    renderWithRole('advogado',
      <ProcessoDetalhe id="p1" numeroProcesso="0001234-56.2026.8.06.0001"
                       idArea="Trabalhista" idRito="Ordinario"
                       status="Em Andamento" valorCausa={15000.5} />);
    expect(screen.getByRole('heading', { name: /processo/i })).toBeInTheDocument();
    const timeline = await screen.findByRole('list', { name: /linha do tempo/i });
    const items = within(timeline).getAllByRole('listitem');
    expect(items[0]).toHaveTextContent('Petição');
    expect(items[1]).toHaveTextContent('Audiência');
  });

  test('badge status reflete status atual (Em Andamento)', () => {
    renderWithRole('advogado',
      <ProcessoDetalhe id="p1" status="Em Andamento" numeroProcesso="0001234-56.2026.8.06.0001"
                       idArea="Trabalhista" idRito="Ordinario" valorCausa={1000} />);
    expect(screen.getByLabelText('status')).toHaveTextContent(/em andamento/i);
    expect(screen.getAllByTestId('status-badge').length).toBeGreaterThanOrEqual(1);
  });

  test('registrar movimento: POST ao clicar no submit', async () => {
    renderWithRole('advogado',
      <ProcessoDetalhe id="p1" status="Em Andamento" numeroProcesso="0001234-56.2026.8.06.0001"
                       idArea="Trabalhista" idRito="Ordinario" valorCausa={1000} />);
    fireEvent.click(screen.getByRole('button', { name: /registrar movimento/i }));
    const form = await screen.findByLabelText(/registrar movimento/i);
    fireEvent.change(within(form).getByLabelText(/tipo/i), { target: { value: 'Petição' } });
    fireEvent.change(within(form).getByLabelText(/descrição|descricao/i), { target: { value: 'Envio de docs' } });
    fireEvent.click(within(form).getByRole('button', { name: /registrar|salvar/i }));
    await waitFor(() => expect((global.fetch as any).mock.calls.some((c: any[]) =>
      String(c[0]) === '/movimentos' && c[1]?.method === 'POST')).toBe(true));
  });

  test('assistente não vê botão excluir nem arquivar administrativamente', async () => {
    renderWithRole('assistente',
      <ProcessoDetalhe id="p1" status="Em Andamento" numeroProcesso="0001234-56.2026.8.06.0001"
                       idArea="Trabalhista" idRito="Ordinario" valorCausa={1000} />);
    await screen.findByRole('list', { name: /linha do tempo/i });
    expect(screen.queryByRole('button', { name: /excluir/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /arquivar/i })).not.toBeInTheDocument();
  });

  test('admin vê botões excluir + gestão de usuários', async () => {
    renderWithRole('admin',
      <ProcessoDetalhe id="p1" status="Em Andamento" numeroProcesso="0001234-56.2026.8.06.0001"
                       idArea="Trabalhista" idRito="Ordinario" valorCausa={1000} />);
    await screen.findByRole('list', { name: /linha do tempo/i });
    expect(screen.getByRole('button', { name: /excluir/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /gerenciar usuários|gerenciar usuarios/i })).toBeInTheDocument();
  });

  test('advogado não vê gerenciar usuários', async () => {
    renderWithRole('advogado',
      <ProcessoDetalhe id="p1" status="Em Andamento" numeroProcesso="0001234-56.2026.8.06.0001"
                       idArea="Trabalhista" idRito="Ordinario" valorCausa={1000} />);
    await screen.findByRole('list', { name: /linha do tempo/i });
    expect(screen.queryByRole('link', { name: /gerenciar usuários|gerenciar usuarios/i })).not.toBeInTheDocument();
  });
});
