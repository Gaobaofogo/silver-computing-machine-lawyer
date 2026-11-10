import React, { useEffect, useState } from 'react';
import { Navigate, Route, Routes, useParams } from 'react-router-dom';
import { AuthProvider, useAuth } from './hooks/useAuth';
import { RequireRole } from './components/RequireRole';
import { LoginForm } from './components/LoginForm';
import { ProcessoDetalhe, AreaProcesso, RitoProcesso, StatusProcesso } from './components/ProcessoDetalhe';

interface ProcessoDTO {
  id: string;
  numero_processo: string;
  id_area: string;
  id_rito: string;
  status: string;
  valor_causa: string;
}

const ProcessoDetalhePage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [processo, setProcesso] = useState<ProcessoDTO | null>(null);
  const [erro, setErro] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    fetch(`/processos/${encodeURIComponent(id)}`, { credentials: 'include' })
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error('erro'))))
      .then((body) => setProcesso(body?.processo ?? null))
      .catch(() => setErro('Processo não encontrado.'));
  }, [id]);

  if (erro) return <p className="p-6">{erro}</p>;
  if (!processo) return <p className="p-6">Carregando processo…</p>;
  return (
    <ProcessoDetalhe id={processo.id}
                     numeroProcesso={processo.numero_processo}
                     idArea={processo.id_area as AreaProcesso}
                     idRito={processo.id_rito as RitoProcesso}
                     status={processo.status as StatusProcesso}
                     valorCausa={parseFloat(processo.valor_causa)} />
  );
};

const NavBar: React.FC = () => {
  const { user, logout } = useAuth();
  if (!user) return null;
  return (
    <nav className="px-6 py-3 bg-slate-900 text-slate-100 flex items-center justify-between"
         aria-label="Barra superior">
      <span className="font-semibold">Judis</span>
      <div className="flex items-center gap-3 text-sm">
        <span>{user.nome}</span>
        <span className="px-2 py-0.5 rounded bg-slate-700 text-xs uppercase tracking-wider">{user.role}</span>
        <button onClick={() => void logout()} aria-label="Encerrar sessão"
                className="underline underline-offset-2">Sair</button>
      </div>
    </nav>
  );
};

const ProcessoListPlaceholder: React.FC = () => (
  <section className="p-6 space-y-3">
    <h1 className="text-2xl font-bold text-blue-900">Processos</h1>
    <p className="text-slate-600 text-sm">A listagem de processos está disponível para todos os papéis (RBAC: read).</p>
  </section>
);

const AdminPlaceholder: React.FC = () => (
  <section className="p-6 space-y-3">
    <h1 className="text-2xl font-bold text-blue-900">Auditoria LGPD</h1>
    <ul className="list-disc list-inside text-sm text-slate-700">
      <li>/clientes — leitura/escrita auditadas</li>
      <li>/reclamados — leitura/escrita auditadas</li>
      <li>/processos — leitura/escrita auditadas</li>
      <li>/movimentos — leitura/escrita auditadas</li>
    </ul>
  </section>
);

function App() {
  return (
    <AuthProvider>
      <NavBar />
      <main className="min-h-screen bg-slate-50">
        <Routes>
          <Route path="/login" element={<LoginForm />} />
          <Route path="/processos" element={<RequireRole roles={['advogado', 'assistente', 'admin']}><ProcessoListPlaceholder /></RequireRole>} />
          <Route path="/processos/:id" element={<RequireRole roles={['advogado', 'assistente', 'admin']}><ProcessoDetalhePage /></RequireRole>} />
          <Route path="/admin/auditoria" element={<RequireRole roles={['admin']}><AdminPlaceholder /></RequireRole>} />
          <Route path="/" element={<Navigate to="/processos" replace />} />
          <Route path="*" element={<Navigate to="/processos" replace />} />
        </Routes>
      </main>
    </AuthProvider>
  );
}
export default App;
