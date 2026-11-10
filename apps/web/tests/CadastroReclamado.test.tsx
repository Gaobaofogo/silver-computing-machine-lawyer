import { describe, expect, it, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CadastroReclamado } from '../src/components/CadastroReclamado';

describe('CadastroReclamado — ADR-0001 (PF/PJ)', () => {
  it('renderiza tipo PF ou PJ e alterna campos condicionais', () => {
    render(<CadastroReclamado />);
    expect(screen.getByLabelText(/tipo/i)).toBeInTheDocument();
    expect(screen.getByRole('option', { name: 'PF' })).toBeInTheDocument();
    expect(screen.getByRole('option', { name: 'PJ' })).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText(/tipo/i), { target: { value: 'pf' } });
    expect(screen.getByLabelText(/CPF/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/cnpj/i)).not.toBeInTheDocument();
    fireEvent.change(screen.getByLabelText(/tipo/i), { target: { value: 'pj' } });
    expect(screen.getByLabelText(/cnpj/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/razão social|razao social/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/CPF/i)).not.toBeInTheDocument();
  });

  it('PJ sem razão social não chama fetch', async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    render(<CadastroReclamado />);
    fireEvent.change(screen.getByLabelText(/tipo/i), { target: { value: 'pj' } });
    fireEvent.change(screen.getByLabelText(/cnpj/i), { target: { value: '12.345.678/0001-90' } });
    fireEvent.change(screen.getByLabelText(/logradouro/i), { target: { value: 'Rua das Flores' } });
    fireEvent.submit(screen.getByRole('form'));
    await waitFor(() => expect(fetchMock).not.toHaveBeenCalled());
  });

  it('PF chama fetch /api/reclamados com payload completo', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 201,
      json: async () => ({ status: 'criado' }),
    });
    vi.stubGlobal('fetch', fetchMock);

    render(<CadastroReclamado />);
    fireEvent.change(screen.getByLabelText(/tipo/i), { target: { value: 'pf' } });
    fireEvent.change(screen.getByLabelText(/CPF/i), { target: { value: '411.133.456-70' } });
    fireEvent.change(screen.getByLabelText(/telefone/i), { target: { value: '(85) 98765-4321' } });
    fireEvent.change(screen.getByLabelText(/logradouro/i), { target: { value: 'Rua das Flores' } });
    fireEvent.change(screen.getByLabelText(/número|numero/i), { target: { value: '123' } });
    fireEvent.change(screen.getByLabelText(/bairro/i), { target: { value: 'Centro' } });
    fireEvent.change(screen.getByLabelText(/cidade/i), { target: { value: 'Fortaleza' } });
    fireEvent.change(screen.getByLabelText(/^uf/i), { target: { value: 'CE' } });
    fireEvent.change(screen.getByLabelText(/cep/i), { target: { value: '60010-000' } });

    fireEvent.submit(screen.getByRole('form'));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toMatch(/\/reclamados$/);
    const body = JSON.parse(String(init?.body));
    expect(body.tipo).toBe('pf');
    expect(body.cpf).toBe('411.133.456-70');
    expect(body.endereco).toEqual({
      logradouro: 'Rua das Flores',
      numero: '123',
      bairro: 'Centro',
      cidade: 'Fortaleza',
      uf: 'CE',
      cep: '60010-000',
    });
  });

  it('PJ chama fetch /api/reclamados com payload completo', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 201,
      json: async () => ({ status: 'criado' }),
    });
    vi.stubGlobal('fetch', fetchMock);

    render(<CadastroReclamado />);
    fireEvent.change(screen.getByLabelText(/tipo/i), { target: { value: 'pj' } });
    fireEvent.change(screen.getByLabelText(/cnpj/i), { target: { value: '12.345.678/0001-90' } });
    fireEvent.change(screen.getByLabelText(/razão social|razao social/i), { target: { value: 'Empresa X Ltda' } });
    fireEvent.change(screen.getByLabelText(/logradouro/i), { target: { value: 'Av. Bezerra de Menezes' } });
    fireEvent.change(screen.getByLabelText(/número|numero/i), { target: { value: '1234' } });
    fireEvent.change(screen.getByLabelText(/bairro/i), { target: { value: 'Aldeota' } });
    fireEvent.change(screen.getByLabelText(/cidade/i), { target: { value: 'Fortaleza' } });
    fireEvent.change(screen.getByLabelText(/^uf/i), { target: { value: 'CE' } });
    fireEvent.change(screen.getByLabelText(/cep/i), { target: { value: '60115-001' } });

    fireEvent.submit(screen.getByRole('form'));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toMatch(/\/reclamados$/);
    const body = JSON.parse(String(init?.body));
    expect(body.tipo).toBe('pj');
    expect(body.cnpj).toBe('12.345.678/0001-90');
    expect(body.razao).toBe('Empresa X Ltda');
  });
});
