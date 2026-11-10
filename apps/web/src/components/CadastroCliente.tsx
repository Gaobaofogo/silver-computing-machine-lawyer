import React, { useState } from 'react';

const ESTADO_CIVIS = ['Solteiro', 'Casado', 'Divorciado', 'Viúvo', 'Separado Judicialmente'];

const UF_VALIDAS = [
  'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG',
  'PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO',
];

export const CadastroCliente: React.FC = () => {
  const [data, setData] = useState<Record<string, string>>({});
  const set = (field: string, v: string) =>
    setData((s) => ({ ...s, [field]: v }));

  const submit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const requiredFields = ['nome_completo', 'cpf', 'logradouro', 'numero', 'bairro', 'cidade', 'uf', 'cep', 'estado_civil'];
    for (const field of requiredFields) {
      const el = form.elements.namedItem(field) as HTMLInputElement | HTMLSelectElement | null;
      if (!el || !el.value.trim()) return;
    }
    const body: Record<string, unknown> = {
      nome_completo: data.nome_completo ?? '',
      cpf: data.cpf ?? '',
      endereco: {
        logradouro: data.logradouro ?? '',
        numero: data.numero ?? '',
        bairro: data.bairro ?? '',
        cidade: data.cidade ?? '',
        uf: data.uf ?? '',
        cep: data.cep ?? '',
      },
      estado_civil: data.estado_civil ?? '',
    };
    if (data.telefone) body.telefone = data.telefone;
    if (data.email) body.email = data.email;
    void fetch('/api/clientes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }).catch(() => undefined);
  };

  return (
    <form aria-label="Cadastro de Cliente" onSubmit={submit}>
      <div className="space-y-4">
        <label htmlFor="nome_completo">
          Nome Completo <span className="text-red-500 ml-1">*</span>
        </label>
        <input id="nome_completo" name="nome_completo" required value={data.nome_completo ?? ''} onChange={(e) => set('nome_completo', e.target.value)} className="w-full px-3 py-2 border rounded" />

        <label htmlFor="cpf">CPF <span className="text-red-500 ml-1">*</span></label>
        <input id="cpf" name="cpf" type="tel" required maxLength={14} aria-label="CPF do Cliente" placeholder="000.000.000-00" value={data.cpf ?? ''} onChange={(e) => set('cpf', e.target.value)} className="w-full px-3 py-2 border rounded" />

        <label htmlFor="telefone" className="block">Telefone</label>
        <input id="telefone" name="telefone" type="tel" value={data.telefone ?? ''} onChange={(e) => set('telefone', e.target.value)} className="w-full px-3 py-2 border rounded" />

        <label htmlFor="email" className="block">Email</label>
        <input id="email" name="email" type="email" value={data.email ?? ''} onChange={(e) => set('email', e.target.value)} className="w-full px-3 py-2 border rounded" />

        <fieldset>
          <legend>Endereco</legend>
          <label htmlFor="logradouro">Logradouro</label>
          <input id="logradouro" name="logradouro" required minLength={3} maxLength={200} value={data.logradouro ?? ''} onChange={(e) => set('logradouro', e.target.value)} className="w-full px-3 py-2 border rounded" />

          <label htmlFor="numero">Numero</label>
          <input id="numero" name="numero" required minLength={1} maxLength={10} value={data.numero ?? ''} onChange={(e) => set('numero', e.target.value)} className="w-full px-3 py-2 border rounded" />

          <label htmlFor="bairro">Bairro</label>
          <input id="bairro" name="bairro" required minLength={2} maxLength={100} value={data.bairro ?? ''} onChange={(e) => set('bairro', e.target.value)} className="w-full px-3 py-2 border rounded" />

          <label htmlFor="cidade">Cidade</label>
          <input id="cidade" name="cidade" required minLength={2} maxLength={100} value={data.cidade ?? ''} onChange={(e) => set('cidade', e.target.value)} className="w-full px-3 py-2 border rounded" />

          <label htmlFor="uf">UF <span className="text-red-500 ml-1">*</span></label>
          <select id="uf" name="uf" value={data.uf ?? ''} onChange={(e) => set('uf', e.target.value)} className="w-full px-3 py-2 border rounded">
            {UF_VALIDAS.map((u) => (
              <option key={u} value={u}>{u}</option>
            ))}
          </select>

          <label htmlFor="cep">CEP</label>
          <input id="cep" name="cep" type="text" minLength={8} maxLength={9} value={data.cep ?? ''} onChange={(e) => set('cep', e.target.value)} className="w-full px-3 py-2 border rounded" />
        </fieldset>

        <label htmlFor="estado_civil">Estado Civil <span className="text-red-500 ml-1">*</span></label>
        <select id="estado_civil" name="estado_civil" required value={data.estado_civil ?? ''} onChange={(e) => set('estado_civil', e.target.value)} className="w-full px-3 py-2 border rounded">
          {ESTADO_CIVIS.map((v) => (
            <option key={v} value={v}>{v}</option>
          ))}
        </select>

        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Cadastrar Cliente</button>

        <p className="text-xs text-gray-500 mt-2">* Campos obrigatórios <span className="underline">azul</span>; CPF registrado sob LGPD. Email/Telefone opcionais.</p>
      </div>
    </form>
  );
};
