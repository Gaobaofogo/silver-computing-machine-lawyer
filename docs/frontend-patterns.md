# Padrões Técnicos — Frontend (UI/UX + Fluxos)

Referencia: `GLOSSARY.md` (Cliente = pessoa fisica, Reclamado = PF/PJ, Processo com IdProcesso/DataAutua/ValorCausa/IdArea/IdRito), `AGENTS.md` (ADR-0001: Cliente sempre PF, CPF/EstadoCivil obrigatorios, CNPJ removido), `frontend-skills/baseline-ui`, `frontend-skills/react-patterns`.

---

## 1. Escopo e Objetivo

Documento de referencia para agentes que constroem a interface do sistema `JudisJMD` / `direito-projeto`. Nao e design system completo — e um guia de padroes aplicaveis ao dominio juridico.

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

---

## 6. Padroes de Formulario (LGPD + Dados Sensiveis)

- **Campos obrigatorios**: `required` + `aria-required="true"`.
- **Mascaras**: CPF, CNPJ, telefone — nunca mostrar dados brutos sem mascara.
- **Confirmacoes**: ao salvar `Cliente`, confirmar que `EstadoCivil` e `CPF` foram preenchidos (ADR-0001).
- **Mensagens de erro**: usar termos do glossario (ex.: "CPF do Cliente e obrigatorio" nao "Campo CPF invalid.").

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

---

*Escrito com assistencia de `/grill-with-docs`, `/writing-for-agents`, alinhado a `GLOSSARY.md` e `ADR-0001`. Atualizar quando `GLOSSARY.md` ou ADRs mudarem.*
