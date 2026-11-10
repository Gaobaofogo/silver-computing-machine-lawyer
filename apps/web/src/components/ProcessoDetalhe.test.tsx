import { render, screen } from '@testing-library/react';
import { ProcessoDetalhe } from './ProcessoDetalhe';

describe('ProcessoDetail (TDD)', () => {
  test('exibe campos do agregado do Processo', () => {
    render(
      <ProcessoDetalhe
        id="Proc-001"
        numeroProcesso="0001234-56.2026.8.06.0001"
        idArea="Trabalhista"
        idRito="Ordinario"
        status="Em Andamento"
        valorCausa={15000.5}
      />,
    );
    expect(screen.getByRole('heading', { name: /processo/i })).toBeInTheDocument();
    expect(screen.getByLabelText('IdProcesso')).toHaveTextContent('Proc-001');
    expect(screen.getByLabelText('numero_processo')).toHaveTextContent('0001234-56.2026.8.06.0001');
    expect(screen.getByLabelText('id_area')).toHaveTextContent('Trabalhista');
    expect(screen.getByLabelText('id_rito')).toHaveTextContent('Ordinario');
    expect(screen.getByLabelText('status')).toHaveTextContent('Em Andamento');
    expect(screen.getByLabelText('valor_causa')).toHaveTextContent('R$');
  });

  test('aplica fallback e status default Cadastrado', () => {
    render(<ProcessoDetalhe />);
    expect(screen.getByLabelText('IdProcesso')).toHaveTextContent('—');
    expect(screen.getByLabelText('status')).toHaveTextContent('Cadastrado');
  });
});
