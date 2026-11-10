import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CadastroCliente } from '../src/components/CadastroCliente';

const UF_VALIDAS = [
  'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG',
  'PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO',
];

describe('CadastroCliente — PF (ADR-0001)', () => {
  it('renderiza campos obrigatórios completos', () => {
    render(<CadastroCliente />);
    expect(screen.getByLabelText(/nome/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/cpf/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/telefone/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/logradouro/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/número|numero/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/bairro/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/cidade/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^uf/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/cep/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/estado civil/i)).toBeInTheDocument();
  });

  it('UF select contém as 27 UFs brasileiras', () => {
    render(<CadastroCliente />);
    const select = screen.getByLabelText(/^uf/i) as HTMLSelectElement;
    expect(select.tagName).toBe('SELECT');
    for (const uf of UF_VALIDAS) {
      expect(select.innerHTML).toContain(uf);
    }
  });

  it('EstadoCivil aceito com as 5 opções', () => {
    render(<CadastroCliente />);
    const select = screen.getByLabelText(/estado civil/i) as HTMLSelectElement;
    for (const v of ['Solteiro','Casado','Divorciado','Viúvo','Separado Judicialmente']) {
      expect(select.innerHTML).toContain(v);
    }
  });

  it('submit chama fetch /api/clientes com payload completo', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 201,
      json: async () => ({ status: 'criado' }),
    });
    vi.stubGlobal('fetch', fetchMock);

    render(<CadastroCliente />);
    fireEvent.change(screen.getByLabelText(/nome/i), { target: { value: 'Maria Souza' } });
    fireEvent.change(screen.getByLabelText(/cpf/i), { target: { value: '411.133.456-70' } });
    fireEvent.change(screen.getByLabelText(/telefone/i), { target: { value: '(85) 98765-4321' } });
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'maria@exemplo.com' } });
    fireEvent.change(screen.getByLabelText(/logradouro/i), { target: { value: 'Rua das Flores' } });
    fireEvent.change(screen.getByLabelText(/número|numero/i), { target: { value: '123' } });
    fireEvent.change(screen.getByLabelText(/bairro/i), { target: { value: 'Centro' } });
    fireEvent.change(screen.getByLabelText(/cidade/i), { target: { value: 'Fortaleza' } });
    fireEvent.change(screen.getByLabelText(/^uf/i), { target: { value: 'CE' } });
    fireEvent.change(screen.getByLabelText(/cep/i), { target: { value: '60010-000' } });
    fireEvent.change(screen.getByLabelText(/estado civil/i), { target: { value: 'Casado' } });

    fireEvent.submit(screen.getByRole('form'));

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    const [url, init] = fetchMock.mock.calls[0] as [string, RequestInit];
    expect(url).toMatch(/\/clientes$/);
    const body = JSON.parse(String(init?.body));
    expect(body.nome_completo).toBe('Maria Souza');
    expect(body.cpf).toBe('411.133.456-70');
    expect(body.telefone).toBe('(85) 98765-4321');
    expect(body.email).toBe('maria@exemplo.com');
    expect(body.endereco).toEqual({
      logradouro: 'Rua das Flores',
      numero: '123',
      bairro: 'Centro',
      cidade: 'Fortaleza',
      uf: 'CE',
      cep: '60010-000',
    });
    expect(body.estado_civil).toBe('Casado');
  });

  it('submit rejeita nome_completo vazio sem chamar fetch', async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    render(<CadastroCliente />);
    fireEvent.submit(screen.getByRole('form'));
    await waitFor(() => expect(fetchMock).not.toHaveBeenCalled());
  });

  it('renderiza legenda LGPD para CPF', () => {
    render(<CadastroCliente />);
    expect(screen.getByText(/CPF registrado sob LGPD/i)).toBeInTheDocument();
  });
});
