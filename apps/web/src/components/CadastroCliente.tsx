import React from 'react';

export const CadastroCliente: React.FC = () => {
  return (
    <form aria-label="Cadastro de Cliente">
      <label htmlFor="nome">Nome</label>
      <input id="nome" name="nome" aria-required="true" />
      <label htmlFor="cpf">CPF</label>
      <input id="cpf" name="cpf" aria-required="true" aria-label="CPF do Cliente" maxLength={14} placeholder="000.000.000-00" />
      <label htmlFor="estado_civil">Estado Civil</label>
      <select id="estado_civil" name="estado_civil" aria-required="true" aria-label="Estado Civil do Cliente">
        <option value="">Selecione</option>
        <option value="Solteiro">Solteiro</option>
        <option value="Casado">Casado</option>
        <option value="Divorciado">Divorciado</option>
      </select>
    </form>
  );
};
