import { render, screen, fireEvent } from '@testing-library/react';
import { CadastroReclamado } from '../components/CadastroReclamado';

describe('CadastroReclamado — ADR-0001', () => {
  test('renderiza tipo PF ou PJ com campos condicionais', () => {
    render(<CadastroReclamado />);
    expect(screen.getByLabelText(/Tipo/i)).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText(/Tipo/i), { target: { value: 'pf' } });
    expect(screen.getByLabelText(/CPF/i)).toBeInTheDocument();
  });
});
