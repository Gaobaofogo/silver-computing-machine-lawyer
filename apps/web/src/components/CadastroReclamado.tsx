import React, { useState } from 'react';

const ESTADO_CIVIS = ['Solteiro', 'Casado', 'Divorciado', 'Viúvo', 'Separado Judicialmente'];

const UF_VALIDAS = [
  'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG',
  'PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO',
];

export const CadastroReclamado: React.FC = () => {
  const [data, setData] = useState<Record<string, string>>({ tipo: '' });
  const set = (field: string, v: string) =>
    setData((s) => ({ ...s, [field]: v }));
  const tipo = data.tipo ?? '';

  const submit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    if (tipo !== 'pf' && tipo !== 'pj') return;
    const requiredFields = ['logradouro', 'numero', 'bairro', 'cidade', 'uf', 'cep'];
    if (tipo === 'pf') requiredFields.push('cpf');
    if (tipo === 'pj') requiredFields.push('cnpj', 'razao');
    for (const field of requiredFields) {
      const el = form.elements.namedItem(field) as HTMLInputElement | HTMLSelectElement | null;
      if (!el || !el.value.trim()) return;
    }
    const endereco = {
      logradouro: data.logradouro ?? '',
      numero: data.numero ?? '',
      bairro: data.bairro ?? '',
      cidade: data.cidade ?? '',
      uf: data.uf ?? '',
      cep: data.cep ?? '',
    };
    const body: Record<string, unknown> = { tipo, endereco };
    if (tipo === 'pf') {
      body.cpf = data.cpf ?? '';
      if (data.estado_civil) body.estado_civil = data.estado_civil;
    } else {
      body.cnpj = data.cnpj ?? '';
      body.razao = data.razao ?? '';
    }
    if (data.telefone) body.telefone = data.telefone;
    if (data.email) body.email = data.email;
    void fetch('/api/reclamados', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }).catch(() => undefined);
  };

  return (
    <form aria-label="Cadastro de Reclamado" onSubmit={submit}>
      <div className="space-y-4">
        <label htmlFor="tipo">
          Tipo <span className="text-red-500 ml-1">*</span>
        </label>
        <select id="tipo" name="tipo" required aria-label="Tipo de Reclamado" value={tipo} onChange={(e) => set('tipo', e.target.value)} className="w-full px-3 py-2 border rounded">
          <option value="">Selecione</option>
          <option value="pf">PF</option>
          <option value="pj">PJ</option>
        </select>

        {tipo === 'pf' && (
          <>
            <label htmlFor="cpf">CPF <span className="text-red-500 ml-1">*</span></label>
            <input id="cpf" name="cpf" type="tel" required maxLength={14} aria-label="CPF do Reclamado" placeholder="000.000.000-00" value={data.cpf ?? ''} onChange={(e) => set('cpf', e.target.value)} className="w-full px-3 py-2 border rounded" />

            <label htmlFor="estado_civil">Estado Civil</label>
            <select id="estado_civil" name="estado_civil" aria-label="Estado Civil do Reclamado" value={data.estado_civil ?? ''} onChange={(e) => set('estado_civil', e.target.value)} className="w-full px-3 py-2 border rounded">
              <option value="">Selecione</option>
              {ESTADO_CIVIS.map((v) => (
                <option key={v} value={v}>{v}</option>
              ))}
            </select>
          </>
        )}

        {tipo === 'pj' && (
          <>
            <label htmlFor="cnpj">CNPJ <span className="text-red-500 ml-1">*</span></label>
            <input id="cnpj" name="cnpj" type="tel" required maxLength={18} aria-label="CNPJ do Reclamado" placeholder="00.000.000/0000-00" value={data.cnpj ?? ''} onChange={(e) => set('cnpj', e.target.value)} className="w-full px-3 py-2 border rounded" />

            <label htmlFor="razao">Razão Social <span className="text-red-500 ml-1">*</span></label>
            <input id="razao" name="razao" required maxLength={100} aria-label="Razão social do Reclamado" value={data.razao ?? ''} onChange={(e) => set('razao', e.target.value)} className="w-full px-3 py-2 border rounded" />
          </>
        )}

        <label htmlFor="telefone" className="block">Telefone</label>
        <input id="telefone" name="telefone" type="tel" value={data.telefone ?? ''} onChange={(e) => set('telefone', e.target.value)} className="w-full px-3 py-2 border rounded" />

        <label htmlFor="email" className="block">Email</label>
        <input id="email" name="email" type="email" value={data.email ?? ''} onChange={(e) => set('email', e.target.value)} className="w-full px-3 py-2 border rounded" />

        <fieldset>
          <legend>Endereço</legend>
          <label htmlFor="logradouro">Logradouro</label>
          <input id="logradouro" name="logradouro" required minLength={3} maxLength={200} value={data.logradouro ?? ''} onChange={(e) => set('logradouro', e.target.value)} className="w-full px-3 py-2 border rounded" />

          <label htmlFor="numero">Número</label>
          <input id="numero" name="numero" required minLength={1} maxLength={10} value={data.numero ?? ''} onChange={(e) => set('numero', e.target.value)} className="w-full px-3 py-2 border rounded" />

          <label htmlFor="bairro">Bairro</label>
          <input id="bairro" name="bairro" required minLength={2} maxLength={100} value={data.bairro ?? ''} onChange={(e) => set('bairro', e.target.value)} className="w-full px-3 py-2 border rounded" />

          <label htmlFor="cidade">Cidade</label>
          <input id="cidade" name="cidade" required minLength={2} maxLength={100} value={data.cidade ?? ''} onChange={(e) => set('cidade', e.target.value)} className="w-full px-3 py-2 border rounded" />

          <label htmlFor="uf">UF <span className="text-red-500 ml-1">*</span></label>
          <select id="uf" name="uf" required value={data.uf ?? ''} onChange={(e) => set('uf', e.target.value)} className="w-full px-3 py-2 border rounded">
            <option value="">Selecione</option>
            {UF_VALIDAS.map((u) => (
              <option key={u} value={u}>{u}</option>
            ))}
          </select>

          <label htmlFor="cep">CEP</label>
          <input id="cep" name="cep" type="text" minLength={8} maxLength={9} value={data.cep ?? ''} onChange={(e) => set('cep', e.target.value)} className="w-full px-3 py-2 border rounded" />
        </fieldset>

        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Cadastrar Reclamado</button>

        <p className="text-xs text-gray-500 mt-2">* Campos obrigatórios <span className="underline">azul</span>; PF exige CPF, PJ exige CNPJ e Razão Social. CPF/CNPJ registrados sob LGPD.</p>
      </div>
    </form>
  );
};
