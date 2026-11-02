import { render, screen, fireEvent } from '@testing-library/react';
import { CadastroCliente } from '../components/CadastroCliente';

describe('CadastroCliente LGPD — ciclo 2', () => {
  test('mascara CPF no input e nao salva em localStorage', () => {
    render(<CadastroCliente />);
    const cpfInput = screen.getByLabelText(/CPF/i) as HTMLInputElement;

    fireEvent.change(cpfInput, { target: { value: '411.133.456-70' } });

    // LGPD: nunca salvar em localStorage
    expect(localStorage.getItem('token_cliente')).toBeNull();
    expect(sessionStorage.getItem('token_cliente')).toBeNull();
  });
});
