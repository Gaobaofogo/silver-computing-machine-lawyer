/**
 * ProcessoDetalhe — detalhe + linha do tempo de movimentos (ADR-0001, ADR-0007).
 *
 * Dados:
 *   GET /processos/{id} (informacao agregado nas props) +
 *   GET /movimentos?processo_id={id} (timeline cronologica).
 *   POST /movimentos on the submit form (sem reload).
 *
 * RBAC na UI:
 *   - advogado/assistente/admin enxergam "Registrar movimento".
 *   - Excluir processo: admin apenas.
 *   - Arquivar administrativamente: advogado e admin.
 *   - Gerenciar usuarios: admin apenas.
 */
import React, { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

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

interface Movimento {
  movimento_id: string;
  processo_id: string;
  data_movimento: string;
  tipo: string;
  descricao?: string | null;
  status_anterior?: string | null;
  status_novo?: string | null;
  created_at?: string | null;
}

const money = (v?: number) =>
  v === undefined ? '—' : v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

const STATUS_BADGE: Record<string, string> = {
  'Cadastrado': 'bg-zinc-100 text-zinc-800 border-zinc-300',
  'Em Andamento': 'bg-amber-100 text-amber-900 border-amber-400',
  'Concluido': 'bg-emerald-100 text-emerald-900 border-emerald-400',
  'Arquivado': 'bg-rose-100 text-rose-900 border-rose-400',
};

const StatusBadge: React.FC<{ value?: string | null }> = ({ value }) => {
  if (!value) return null;
  const cls = STATUS_BADGE[value] ?? 'bg-slate-100 text-slate-800 border-slate-300';
  return (
    <span data-testid="status-badge"
          className={`inline-flex items-center px-2 py-0.5 rounded-full border text-xs font-semibold ${cls}`}>
      {value}
    </span>
  );
};

export const ProcessoDetalhe: React.FC<ProcessoDetalheProps> = ({
  id,
  numeroProcesso,
  idArea,
  idRito,
  status = 'Cadastrado',
  valorCausa,
}) => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [movimentos, setMovements] = useState<Movimento[] | null>(null);
  const [registrarAberto, setRegistrarAberto] = useState(false);
  const [tipoMovimento, setTipoMovimento] = useState('');
  const [descricaoMovimento, setDescricaoMovimento] = useState('');

  // Fetch movimentos
  useEffect(() => {
    if (!id) { setMovements([]); return; }
    fetch(`/movimentos?processo_id=${encodeURIComponent(id)}`, { credentials: 'include' })
      .then((r) => (r.ok ? r.json() : { movimentos: [] }))
      .then((body) => setMovements(Array.isArray(body?.movimentos) ? body.movimentos : []))
      .catch(() => setMovements([]));
  }, [id]);

  const movimentosOrdenados = useMemo(
    () => (movimentos ?? []).slice().sort((a, b) => a.data_movimento.localeCompare(b.data_movimento)),
    [movimentos]
  );

  const podeRegistrar = ['advogado', 'assistente', 'admin'].includes(user?.role ?? '');
  const podeArquivar = ['advogado', 'admin'].includes(user?.role ?? '');
  const podeExcluir = user?.role === 'admin';
  const podeGerenciarUsuarios = user?.role === 'admin';

  const handleRegistrar = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!id) return;
    const resp = await fetch('/movimentos', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        processo_id: id,
        tipo: tipoMovimento,
        descricao: descricaoMovimento || undefined,
      }),
    });
    if (resp.ok) {
      const body = await resp.json();
      setMovements((prev) => [...(prev ?? []), body.movimento ?? body]);
      setRegistrarAberto(false);
      setTipoMovimento('');
      setDescricaoMovimento('');
    }
  };

  const handleExcluir = async () => {
    if (!id) return;
    const r = await fetch(`/processos/${encodeURIComponent(id)}`, { method: 'DELETE', credentials: 'include' });
    if (r.ok) navigate('/processos', { replace: true });
  };

  return (
    <div className="p-6 space-y-6" aria-label="Detalhe do Processo">
      <header className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-blue-900">Processo</h1>
          <p className="text-xs text-slate-500">detalhe do agregado</p>
        </div>
        <StatusBadge value={status} />
      </header>

      <dl className="grid grid-cols-2 gap-3 text-sm md:grid-cols-3">
        <div><dt className="text-slate-500">IdProcesso</dt><dd aria-label="IdProcesso">{id ?? '—'}</dd></div>
        <div className="col-span-2 md:col-span-3"><dt className="text-slate-500">numero_processo</dt><dd aria-label="numero_processo">{numeroProcesso ?? '—'}</dd></div>
        <div><dt className="text-slate-500">id_area</dt><dd aria-label="id_area">{idArea ?? '—'}</dd></div>
        <div><dt className="text-slate-500">id_rito</dt><dd aria-label="id_rito">{idRito ?? '—'}</dd></div>
        <div><dt className="text-slate-500">status</dt><dd aria-label="status">{status}</dd></div>
        <div><dt className="text-slate-500">valor_causa</dt><dd aria-label="valor_causa">{money(valorCausa)}</dd></div>
      </dl>

      <section aria-label="Ações" className="flex flex-wrap gap-2">
        {podeRegistrar && (
          <button type="button" onClick={() => setRegistrarAberto((s) => !s)}
                  className="rounded bg-blue-700 text-white px-3 py-2">
            Registrar movimento
          </button>
        )}
        {podeArquivar && (
          <button type="button" className="rounded border border-slate-300 px-3 py-2">
            Arquivar administrativamente
          </button>
        )}
        {podeExcluir && (
          <button type="button" onClick={handleExcluir}
                  className="rounded bg-rose-700 text-white px-3 py-2">
            Excluir processo
          </button>
        )}
        {podeGerenciarUsuarios && (
          <a href="/admin/usuarios" aria-label="Gerenciar usuários"
             className="rounded border border-emerald-600 text-emerald-700 px-3 py-2">
            Gerenciar usuários
          </a>
        )}
      </section>

      {registrarAberto && (
        <form
          aria-label="Registrar movimento"
          onSubmit={handleRegistrar}
          className="border border-slate-200 rounded-2xl p-4 space-y-3 max-w-xl"
        >
          <h2 className="font-semibold">Registrar movimento</h2>
          <div>
            <label htmlFor="tipo-mov" className="block text-sm font-semibold">Tipo</label>
            <input id="tipo-mov" aria-label="Tipo" required value={tipoMovimento}
                   onChange={(e) => setTipoMovimento(e.target.value)}
                   className="border rounded px-3 py-2 w-full" />
          </div>
          <div>
            <label htmlFor="descricao-mov" className="block text-sm font-semibold">Descrição</label>
            <textarea id="descricao-mov" aria-label="Descrição"
                      value={descricaoMovimento}
                      onChange={(e) => setDescricaoMovimento(e.target.value)}
                      className="border rounded px-3 py-2 w-full" />
          </div>
          <button type="submit" className="rounded bg-blue-700 text-white px-3 py-2">Salvar movimento</button>
        </form>
      )}

      <section>
        <h2 className="text-lg font-semibold mb-2">Linha do tempo</h2>
        <ol aria-label="Linha do tempo de movimentos" role="list"
            className="space-y-3 border-l-2 border-slate-300 pl-4">
          {movimentosOrdenados.map((m) => (
            <li key={m.movimento_id} data-testid="mov-item"
                className="relative pl-2">
              <span aria-hidden className="absolute -left-[1.1rem] top-1 h-3 w-3 rounded-full bg-slate-500" />
              <div className="text-xs text-slate-500">{m.data_movimento}</div>
              <div className="font-semibold">{m.tipo}</div>
              {m.descricao && <p className="text-sm text-slate-700">{m.descricao}</p>}
              {m.status_novo && <div><StatusBadge value={m.status_novo} /></div>}
            </li>
          ))}
          {movimentosOrdenados.length === 0 && (
            <li className="text-sm text-slate-500">Sem movimentos registrados ainda.</li>
          )}
        </ol>
      </section>
    </div>
  );
};
