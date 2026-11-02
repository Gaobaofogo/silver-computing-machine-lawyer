import { render, screen } from '@testing-library/react';
import { CadastroCliente } from '../components/CadastroCliente';

describe('CadastroCliente — ADR-0001 + LGPD', () => {
  test('renderiza formulario com CPF e EstadoCivil', () => {
    render(<CadastroCliente />);
    expect(screen.getByLabelText(/CPF/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Estado Civil/i)).toBeInTheDocument();
  });
});
