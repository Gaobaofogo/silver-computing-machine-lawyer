# Padrões Técnicos — Frontend (UI/UX + Fluxos)

Referencia: `GLOSSARY.md` (Cliente = pessoa fisica, Reclamado = PF/PJ, Processo com IdProcesso/DataAutua/ValorCausa/IdArea/IdRito), `AGENTS.md` (ADR-0001: Cliente sempre PF, CPF/EstadoCivil obrigatorios, CNPJ removido), `frontend-skills/baseline-ui`, `frontend-skills/react-patterns`.

---

## 1. Escopo e Objetivo

Documento de referencia para agentes que constroem a interface do sistema `JudisJMD` / `direito-projeto`. Nao e design system completo — e um guia de padroes aplicaveis ao dominio juridico.

---

## 1.1 Convenção de Idioma: Código vs Domínio

Referencia: `docs/backend-patterns.md` (§2.1), `AGENTS.md`.

O código técnico (funções, componentes, módulos) é escrito em **inglês**; nomes de domínio permanecem em **português** (`GLOSSARY.md`).

| Tipo | Regra | Exemplo |
|------|-------|---------|
| Componentes / funções / props | Inglês | `ClientForm`, `ClaimForm`, `ProcessCard`, `LoginForm`, `useProcessData()` |
| Rotulos de UI / textos ao usuário | Português (domínio) | `"CPF do Cliente"`, `"Estado Civil"`, `"Valor da Causa"`, `"Observações"` |
| Nome de arquivo (componente) | Inglês técnico | `ClientForm.tsx`, `ProcessDetail.tsx` |
| Nome de arquivo (documento) | Português / inglês conforme contexto | `frontend-patterns.md` (doc técnico) |
| Variáveis de estado / props do domínio | Português (termos do glossário) | `cliente`, `reclamado`, `processo`, `id_area`, `estado_civil` |
| Comentários no componente | Português para regras de domínio; inglês para lógica técnica | `// Cliente sempre PF per ADR-0001` vs `// Memoize render only when props change` |

---

## 2. Vocabulário do Dominio (referencia obrigatoria)

Usar os termos do `GLOSSARY.md` em todos os componentes, rotulos e mensagens:

| Termo | Definicao no doc | Regra de UI |
|-------|------------------|-------------|
| **Cliente** | Pessoa fisica, autor do processo. Sempre `Cpf` + `EstadoCivil`. | Campo `CPF` obrigatorio, campo `EstadoCivil` obrigatorio. Nenhum campo `CNPJ`. |
| **Reclamado** | Parte re. Pode ser PF (`Cpf`) ou PJ (`CNPJ`). | Campo `Tipo` (PF/PJ) selecionavel; condicionalmente mostra CPF ou CNPJ. |
| **Processo** | Registro judicial (IdProcesso, DataAutua, ValorCausa, IdArea, IdRito, IdReclamado, Observa). | Tela de detalhe mostra todos os campos; `Observa` pode conter dados sensiveis (LGPD). |
| **Area Juridica** | Especialidade (Trabalhista, Civil, Previdenciario, etc.). | Dropdown com nomes do glossario. |
| **Rito** | Ordinario, Sumario, Especial. | Dropdown. |
| **Dados Sensiveis** | CPF, RG, CTPS, PIS/PASEP (LGPD). | Sempre mascarados na exibe; input com `type="password"` ou mascara visual; alertas de privacidade. |

---

## 2.5 Accessibility Standard (axe / WCAG)

Referencia: `baseline-ui`, `react-patterns` (accessibility-first), `tdd`.

- **Teste automatizado**: usar `axe-core` com `React Testing Library` (`@testing-library/react`); incluir `expect(screen.getByRole('button', {name: /Cadastrar Cliente/i})).toBeInTheDocument()`.
- **Padrao de query**: preferir `getByRole`, `getByLabelText` sobre `getByText` para acessibilidade.
- **Contraste**: minimo `4.5:1` para texto normal, `3:1` para texto grande; verificar com `axe` no CI.
- **Teclado**: todos os componentes interativos (`CadastroCliente`, `LoginForm`) devem ser navegaveis por `Tab` e acionaveis por `Enter` / `Space`; foco visivel (`outline: 2px solid #005fcc`).
- **Labels**: todo input precisa `label` associado (`htmlFor`) ou `aria-label`; `CPF` e `Estado Civil` nao podem ser apenas placeholders.
- **Live regions**: mensagens de erro/sucesso devem usar `aria-live="polite"` para leitores de tela.

Referencias de comando:

```bash
# Exemplo de teste com axe
npm test -- --testNamePattern="accessibility"
# Ou diretamente
npx axe-core --tags wcag2a,section508
```

---

## 3.2 Responsive / Breakpoints (Mobile-First)

Referencia: `react-patterns`, `baseline-ui` (design tokens responsivo), `frontend-skills/react-best-practices`.

Regra: mobile-first — escrever CSS base para telas pequenas, depois aumentar com media queries (`min-width`).

| Breakpoint | Nome | Regra de layout |
|------------|------|-----------------|
| `< 640px` | `sm` (mobile) | Layout single-column (`CadastroCliente`: campos empilhados; `ProcessoCard`: titulo, valor, data — tudo vertical). Menu de navegacao vira `hamburger` ou `dropdown`. |
| `640px - 1024px` | `md` (tablet) | `ProcessoCard` usa grid 2 colunas; `CadastroCliente` usa 2 colunas (nome | CPF/EstadoCivil). |
| `> 1024px` | `lg` (desktop) | `ProcessoCard` usa grid 3 colunas (numero | valor | data); `CadastroReclamado` usa layout lado a lado (tipo PF/PJ | campos condicionais). |

Padroes por componente:

- `ProcessoCard`: `< 768px` stack vertical (`flex-direction: column`); `> 768px` `flex-direction: row` com espaco entre.
- `CadastroCliente`: `< 640px` single-column; `> 640px` 2-colunas (`nome` ocupa 60%, `CPF` e `EstadoCivil` 40%).
- `LoginForm`: sempre centralizado, largura max `400px`, single-column.
- `ProcessoDetalhe`: `< 768px` tabs viram `accordion`; `> 768px` tabs horizontais.

Referencia de implementacao (React / CSS):

```css
/* Referencia de breakpoint (nao implementacao completa) */
.card-container {
  display: grid;
  grid-template-columns: 1fr; /* mobile first */
}
@media (min-width: 768px) {
  .card-container { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 1024px) {
  .card-container { grid-template-columns: repeat(3, 1fr); }
}
```

Nota: `frontend-skills/react-patterns` trata Server/Client Components; nao trata responsividade diretamente — esta secao supre essa lacuna.

---

## 3. Design Tokens e Padroes Visuais

Baseado em `baseline-ui`; nao inventar paleta nova sem decisao de ADR.

- **Cores**: neutro juridico (cinza-escuro, branco, azul-escuro para acao primaria). Evitar cores vibrantes (associadas a geral, nao a advocacia).
- **Fontes**: sans-serif legivel (Inter / system-ui); tamanho base 16px; escala tipografica consistente.
- **Espacamento**: 8px grid (padding/margin). Componentes com bordas sutis, sombra leve ou nenhuma (formalidade).
- **Acessibilidade**: contraste minimo 4.5:1; teclado navegavel; rotulos `aria-label` para todos os campos sensiveis.

---

## 4. Componentes de UI (mapeados ao dominio)

### 4.1 Formulario de Cliente (PF obrigatorio)

```tsx
// Componente: CadastroCliente
// Regra: Cliente = sempre PF per ADR-0001
// Campos: Nome, CPF (mascarado), EstadoCivil (select), Observacoes (textarea, LGPD)
// Nenhum campo CNPJ
```

- **CPF**: input com mascara `000.000.000-00`; validacao de digito verificador; label com informacao LGPD.
- **EstadoCivil**: select (Solteiro, Casado, Divorciado, Viuvio, etc.) — termos do glossario.
- **Observacoes**: textarea; se conter dados sensiveis, mostrar badge "Dados sensiveis — LGPD".

### 4.2 Formulario de Reclamado (PF ou PJ)

```tsx
// Componente: CadastroReclamado
// Regra: Reclamado pode ser PF (Cpf) ou PJ (CNPJ)
// Campos: Tipo (radio/select), Nome, CPF ou CNPJ condicional, Observacoes
```

- **Tipo**: `PF` ou `PJ`; muda o campo de identificacao.
- **Validador**: CPF valida com digito; CNPJ valida com digito.

### 4.3 Tela de Processo (detalhe)

```tsx
// Componente: ProcessoDetalhe
// Campos: IdProcesso (readonly), DataAutua, ValorCausa (currency), Area (select), Rito (select), Reclamado (link/readonly), Observacoes
```

- `ValorCausa`: input com mascara monetaria (ex.: `R$ 10.000,00`).
- `Observacoes`: se contiver dados sensiveis, mostrar alerta de privacidade.

---

### 4.4 State Management Decision Tree (useState / useContext / Store)

Referencia: `react-patterns` (State Location Decision Tree).

| Contexto | Recomendacao | Razao |
|----------|--------------|-------|
| **Formulário local** (CadastroCliente, CadastroReclamado) | `useState` / `useForm` (React Hook Form) | Dados locais; nao compartilhados com outros componentes. |
| **Autenticacao / Role** (quem pode ver/editar) | `useContext` (`AuthContext`) | Compartilhado entre rotas (`/clientes`, `/processos`); baixa frequencia de mudanca. |
| **Processo detalhado + edição simultanea** (multi-user concurrent) | `useState` local no componente + sincronizacao via `SWR` / `TanStack Query` se servidor externo; nao usar `useContext` para dados de alta frequencia (evita re-render cascata). | `Processo` pode ser editado por advogados; se alta frequencia, contexto causaria re-renderes desnecessarios na arvore. |
| **Estado global da aplicacao** (lista de processos, filtros) | Se apenas uma origem de verdade (ex.: `ProcessoList` carregado uma vez): `useState` no componente pai + props. Se multusarios concorrentes: considerar `Zustand` / `Jotai` (apenas se `useContext` provar inadequado). | Evitar store externo sem necessidade (complexidade). |

Regra pratica para `Processo` + `Cliente`:

- `CadastroCliente` → `useForm` (local).
- `ProcessoDetalhe` → `useState` para edicao local + `useEffect` para carregar do servidor; se outro usuario editar, usar `SWR` para revalidar, nao contexto.
- `Auth` / `Role` → `useContext` (compartilhado, baixa frequencia).

Nota: se o projeto crescer para `multi-context` (`GLOSSARY-MAP.md`), reavaliar store quando houver necessidade de sincronizacao entre `cliente`, `reclamado` e `processo` em tempo real.

---

## 5. Fluxos de Navegacao e Tela por Funcao

### 5.1 Estrutura de telas por papel (role-based layout)

| Funcao | Tela inicial | Navegacao principal | Componentes chave |
|--------|--------------|---------------------|-------------------|
| **Advogado / Usuario** | Dashboard com lista de `Processos` | Lista → Detalhe → Edicao (Cliente/Reclamado) | `ProcessoCard`, `ProcessoDetalhe`, `CadastroCliente` |
| **Atendente / Cadastro** | Lista de `Clientes` | Lista → Cadastro Cliente → Cadastro Reclamado → Associacao a Processo | `CadastroCliente`, `CadastroReclamado`, `AssociarReclamado` |
| **Admin / Gestor** | Relatorio / Estatisticas por `Area` e `Rito` | Dashboard → Filtros → Exportacao | `AreaFilter`, `RitoFilter`, `Relatorio` |

### 5.2 Fluxo de Login, Logout e Esqueci a Senha

```tsx
// Flow: Login → Dashboard (redirecionado por role) → Logout (limpa session, volta para Login)
// Recuperacao: Login → "Esqueci a senha" → Email → Link de reset (expira em 1h, LGPD: nao expor CPF no email)
```

- **Login**: campos `email` + `senha`; botao "Entrar"; link "Esqueci a senha".
- **Esqueci a senha**: apenas email; mensagem de confirmacao generica (nao confirmar existencia de conta).
- **Logout**: botao visivel; acao limpa storage / cookie de sessao.
- **Sessao / Token — Proibicao LGPD**: nao salvar `JWT`, `access_token` nem dados sensiveis (`CPF`, `RG`) em `localStorage`, `sessionStorage` ou `IndexedDB`. Usar `httpOnly` cookie (`cookie: access_token=...; HttpOnly; Secure; SameSite=Strict`) gerenciado pelo servidor; `fetch` envia automaticamente via `credentials: 'include'`. Se `useContext` (`AuthContext`) precisa do papel (`role`), armazenar apenas `role` (string), nunca o token completo.
- **Bearer header**: se a API exige `Authorization: Bearer`, o frontend nao deve construir o header com token armazenado no JS — o cookie `httpOnly` e enviado pelo navegador; apenas o backend valida o JWT.

---

### 5.3 Fluxo de Acesso por Role

Referencia: `AGENTS.md` (gitflow), `GLOSSARY.md` (Cliente, Reclamado, Processo).

- **Advogado**: acesso total a `Processo` (ler, editar, criar), `Cliente` (ler/editar), `Reclamado` (ler/editar).
- **Atendente / Cadastro**: apenas cadastro (criar/ler `Cliente`, `Reclamado`); nao edita `Processo` sem autorizacao.
- **Admin / Gestor**: acesso a relatorios (`Area`, `Rito`, `ValorCausa`).

---

### 5.4 Loading / Error / Empty States

Referencia: `react-patterns`, `baseline-ui` (feedback patterns).

- **Skeleton / Loading**: ao carregar `ProcessoDetalhe` ou lista de processos, usar `Skeleton` (forma simplificada de `ProcessoCard`) enquanto `useQuery` / `SWR` carrega. Nao mostrar tela vazia.
- **ErrorBoundary**: envolver `ProcessoDetalhe` com `ErrorBoundary`; se falhar, mostrar mensagem generica ("Erro ao carregar processo") sem expor detalhes internos.
- **NotFound / Vazio**: se `Processo` com `IdProcesso` nao existe (404) ou lista retorna vazio, mostrar `NotFound` com acao de retorno (`"Voltar para lista de processos"`).
- **LGPD em erro**: se erro envolve dados sensiveis, mascarar `CPF` mesmo na mensagem de erro (`"CPF do Cliente nao encontrado"` — sem expor o valor).

---

## 6. Padroes de Formulario (LGPD + Dados Sensiveis)

- **Campos obrigatorios**: `required` + `aria-required="true"`.
- **Regex de validacao no input** (`CPF`): pattern `^(\d{3}\.\d{3}\.\d{3}-\d{2})$`; `CNPJ` (quando PJ): `^[A-Z0-9]{2}\.[A-Z0-9]{3}\.[A-Z0-9]{3}/[A-Z0-9]{4}-\d{2}$`; nunca permitir valores fora do pattern.
- **Mascaras**: CPF, CNPJ, telefone — nunca mostrar dados brutos sem mascara.
- **Confirmacoes**: ao salvar `Cliente`, confirmar que `EstadoCivil` e `CPF` foram preenchidos (ADR-0001).
- **Mensagens de erro**: usar termos do glossario (ex.: "CPF do Cliente e obrigatorio" nao "Campo CPF invalid.").

---

## 6.5 Design Tokens (Referencia a arquivo concreto)

Referencia: `frontend-skills/baseline-ui`, `baseline-ui` (design tokens, composição acessível).

- **Arquivo de referência**: `styles/design-tokens.css` ou `theme/config.ts` (escolha uma; não inventar paleta sem ADR). Se ainda não existe, criar `styles/design-tokens.css` com variáveis CSS (`--color-primary`, `--spacing-unit`, `--font-base`).
- **Regras**: nao criar novos tokens de cor sem decisao de arquitetura (ADR). Usar apenas tokens definidos neste arquivo.
- **Aplicação**: todos os componentes (`CadastroCliente`, `ProcessoCard`, `LoginForm`) devem usar `var(--color-primary)` em vez de valores hex diretos (`#005fcc` etc.).
- **Nota de decisão**: se o projeto futuramente precisar de tema escuro/claro, criar `theme/config.ts` e apontar para ADR futuro; nao adicionar antes.

---

## 7. Referencias de Pattern (skills)

- Comentarios de componente devem apontar para `react-patterns` (hooks discipline, Server/Client boundaries).
- Testes de componente: `React Testing Library`; cobrir fluxo de cadastro de Cliente com CPF valido + CPF invalido.
- Design tokens: consultar `baseline-ui`; nao criar nova paleta sem ADR.

---

## 8. Out of Scope

- Design system completo (tokens globais, tema escuro/claro nao definido, nao usar sem ADR).
- Implementacao real de componentes (este doc e referencia, nao codigo).
- Mobile-native (isto e web React 18/19, nao React Native).
- **Nao e spec formal para `/implement-spec`**: este documento e referencia de padroes. Para implementacao baseada em spec, usar `/to-spec` + `/to-tickets` derivando deste e do `GLOSSARY.md` (mesma regra do `docs/backend-patterns.md`).

---

*Escrito com assistencia de `/grill-with-docs`, `/writing-for-agents`, alinhado a `GLOSSARY.md` e `ADR-0001`. Atualizar quando `GLOSSARY.md` ou ADRs mudarem.*
