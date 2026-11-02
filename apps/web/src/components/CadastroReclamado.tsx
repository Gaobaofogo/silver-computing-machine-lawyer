import React from 'react';

export const CadastroReclamado: React.FC = () => {
  return (
    <form aria-label="Cadastro de Reclamado">
      <label htmlFor="tipo">Tipo</label>
      <select id="tipo" name="tipo" aria-label="Tipo de Reclamado">
        <option value="pf">PF</option>
        <option value="pj">PJ</option>
      </select>
      <label htmlFor="cpf">CPF</label>
      <input id="cpf" name="cpf" aria-label="CPF do Reclamado" maxLength={14} />
      <label htmlFor="cnpj">CNPJ</label>
      <input id="cnpj" name="cnpj" aria-label="CNPJ do Reclamado" maxLength={18} />
      <label htmlFor="estado_civil">Estado Civil</label>
      <select id="estado_civil" name="estado_civil" aria-label="Estado Civil do Reclamado">
        <option value="">Selecione</option>
        <option value="Solteiro">Solteiro</option>
        <option value="Casado">Casado</option>
      </select>
    </form>
  );
};
