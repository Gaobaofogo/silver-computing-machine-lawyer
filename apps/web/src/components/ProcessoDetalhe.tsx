import React from 'react';

export type AreaProcesso = 'Trabalhista' | 'Civel' | 'Previdenciario' | 'Tributario' | 'Penal';
export type RitoProcesso = 'Ordinario' | 'Sumario' | 'Especial';
export type StatusProcesso = 'Cadastrado' | 'Em Andamento' | 'Concluido' | 'Arquivado';

export interface ProcessoDetalheProps {
  id?: string;
  numeroProcesso?: string;
  idArea?: AreaProcesso;
  idRito?: RitoProcesso;
  status?: StatusProcesso;
  valorCausa?: number;
}

const money = (v?: number) =>
  v === undefined ? '—' : v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

export const ProcessoDetalhe: React.FC<ProcessoDetalheProps> = ({
  id,
  numeroProcesso,
  idArea,
  idRito,
  status = 'Cadastrado',
  valorCausa,
}) => (
  <div aria-label="Detalhe do Processo">
    <h1>Processo</h1>
    <dl>
      <dt>IdProcesso</dt>
      <dd aria-label="IdProcesso">{id ?? '—'}</dd>
      <dt>numero_processo</dt>
      <dd aria-label="numero_processo">{numeroProcesso ?? '—'}</dd>
      <dt>id_area</dt>
      <dd aria-label="id_area">{idArea ?? '—'}</dd>
      <dt>id_rito</dt>
      <dd aria-label="id_rito">{idRito ?? '—'}</dd>
      <dt>status</dt>
      <dd aria-label="status">{status}</dd>
      <dt>valor_causa</dt>
      <dd aria-label="valor_causa">{money(valorCausa)}</dd>
    </dl>
  </div>
);
