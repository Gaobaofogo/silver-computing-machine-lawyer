# AGENTS.md — Direito Projeto

> Este arquivo orienta humanos e agentes de IA que trabalham no repositório
> `direito-projeto`. Ele define o domínio, o stack, as skills disponíveis, o
> fluxo de trabalho (gitflow), o rastreador de issues e as convenções de
> desenvolvimento assistido por IA.

---

## Stack

| Camada | Tecnologia | Versão | Uso |
|--------|------------|--------|-----|
| Backend | FastAPI | 3.12+ | API REST |
| Backend | Python | 3.15+ | Lógica de domínio |
| Backend | SQLModel / SQLAlchemy 2.0 | — | Modelagem e persistência |
| Backend | PostgreSQL | — | Banco de dados relacional |
| Frontend | React | 18/19 | Interface de usuário |
| Frontend | TypeScript | 5.5+ | Tipagem estática |
| Infra | Docker + Docker Compose | — | Containerização local |
| Testes | pytest | — | Testes backend |
| Testes | React Testing Library | — | Testes frontend |
| Issue Tracker | GitHub Issues | — | Via `gh` CLI |

O domínio do projeto segue o vocabulário definido em `judis-advocacia/GLOSSARY.md`:

- **Cliente**: parte autora do processo (pessoa física ou jurídica).
- **Reclamado**: parte ré do processo (pessoa física ou jurídica).
- **Processo**: registro judicial com número, data de autuação, valor da causa, área, rito.
- **Área**: especialidade do direito do processo (ex.: Trabalhista, Cível, Previdenciário).
- **Rito**: procedimento processual aplicável (ex.: Ordinário, Sumário, Especial).
- **EstadoCivil**: estado civil do cliente (ex.: Solteiro, Casado, Divorciado).
- **Dados Sensíveis**: informações protegidas pela LGPD (CPF, RG, CTPS, PIS/PASEP).
- **LGPD**: Lei Geral de Proteção de Dados (Lei nº 13.709/2018).

---

## Agent Skills

As seguintes skills estão instaladas e vinculadas nos diretórios locais (`~/.claude/skills` e `~/.agents/skills`). Os agentes do DSH devem consultá-las quando aplicável.

### Matt Pocock / Skills (engenharia e produtividade)

Essas são as skills base, extraídas do repositório `mattpocock/skills`. Elas definem o fluxo de trabalho geral do agente:

- `ask-matt` — roteador que mapeia cada skill e como elas se relacionam.
- `setup-matt-pocock-skills` — configuração inicial do repositório (issue tracker, labels de triage, documentos de domínio).
- `grill-me` / `grill-with-docs` — entrevista implacável para afinar planos e decisões de domínio (gera `GLOSSARY.md` e ADRs).
- `grilling` — fundamento da entrevista por design tree.
- `domain-modeling` — construção ativa do modelo de domínio (glossário + ADR).
- `code-review` — revisão por padrões (standards) e especificação.
- `codebase-design` — vocabulário compartilhado para módulos profundos.
- `diagnosing-bugs` — loop de diagnóstico para bugs e regressões.
- `implement` / `implement-spec` — implementação baseada em spec ou tickets (usa `tdd` nos seams pré-acordados).
- `to-spec` — sintetiza a conversa atual em um spec publicado no issue tracker.
- `to-tickets` — quebra specs em tickets verticais com blocos.
- `wayfinder` — planejamento de grandes esforços como mapa de decisão tickets.
- `triage` — classificação de issues usando os labels canônicos.
- `tdd` — desenvolvimento guiado por testes.
- `prototype` — protótipo descartável para responder a perguntas de design.
- `research` — investigação contra fontes primárias, salva como Markdown.
- `retro` — retrospectiva de sessão.
- `wayfinder` — mapa de decisão para esforços grandes.
- `writing-for-agents` — criação e edição de habilidades, AGENTS.md, CLAUDE.md.

### Frontend (React)

- `react-patterns` — padrões React 18/19 (hooks, Server/Client Components, Suspense, state trees, acessibilidade).
- `react-hook-form` — otimização de desempenho para React Hook Form (35 regras, 7 categorias).
- `react-router-framework-mode` — React Router framework mode (loaders, actions, rotas, navegação).
- `vercel-react-best-practices` — 70 regras de desempenho da Vercel (fetching, bundle, SSR, re-render).
- `baseline-ui` — padrões de UI base (design tokens, composição acessível).

### Backend / Infra

- `fastapi` — skill oficial do FastAPI (dependências, OpenTelemetry, Pydantic, roteamento, SSE).
- `fastapi-python` — FastAPI + padrões Python (async/await, Pydantic v2, RORO, guard clauses).
- `python-type-safety` — tipo de Python (mypy/pyright, protocols, narrowing, APIs tipo-safe).
- `python-patterns` — padrões idiomáticos Python (PEP 8, legibilidade, composição).
- `python-testing-patterns` — testes com pytest (AAA, fixtures, mocking, TDD, propriedade, CI/CD).
- `docker-project-foundations` — Dockerização de projeto (Dockerfile, compose.yaml, .dockerignore).
- `docker-best-practices` — boas práticas de Docker.

---

## Issue Tracker

Issues e specs deste repositório vivem como **GitHub Issues** no repositório `Gaobaofogo/silver-computing-machine-lawyer`. Use a CLI `gh` para todas as operações.

- Criar issue: `gh issue create --title "..." --body "..."`
- Ver issue: `gh issue view <n>`
- Listar issues abertas: `gh issue list --state open`
- Aplicar/remover labels: `gh issue edit <n> --add-label "..."` / `--remove-label "..."`

O tracker usa os **labels de triagem** definidos abaixo.

### Triage labels (padrão)

Os cinco rótulos canônicos:

1. `needs-triage`
2. `needs-info`
3. `ready-for-agent`
4. `ready-for-human`
5. `wontfix`

Ao criar tickets via `to-tickets`, aplique `ready-for-agent` quando o ticket estiver pronto para implementação automática.

---

## Workflow (Gitflow)

Este repositório segue o padrão **gitflow**:

| Branch | Propósito |
|--------|-----------|
| `main` | Código em produção, estável |
| `develop` | Integração contínua; ponto de partida de features |
| `feature/*` | Desenvolvimento de funcionalidades (a partir de `develop`) |
| `release/*` | Preparação de lançamento (a partir de `develop`) |
| `hotfix/*` | Correção urgente em produção (a partir de `main`) |

Fluxo típico:

1. Crie `feature/nome-da-feature` a partir de `develop`.
2. Implemente a feature.
3. Abra Pull Request para `develop`.
4. Após revisão e aprovação, faça merge para `develop`.
5. Quando estiver pronto para lançar, crie `release/versao` a partir de `develop`.
6. Após testes de lançamento, faça merge para `main` e `develop`.
7. Tague o lançamento em `main`.

---

## Documentos de Domínio

- `judis-advocacia/GLOSSARY.md` — vocabulário do domínio.
- `judis-advocacia/docs/adr/` — ADRs.
- `judis-advocacia/estrutura-pastas.md` — estrutura de pastas (`apps/` + `wayfinder/`).

Não existe `GLOSSARY-MAP.md`; este é um repositório **single-context**. Se futuramente o projeto crescer para múltiplos contextos (ex.: contexto jurídico, contexto administrativo), crie `GLOSSARY-MAP.md` apontando para cada `GLOSSARY.md` específico.

---

## Testes

Testes são escritos antes ou junto com a implementação (`tdd`). Categorias:

| Tipo | Ferramenta | Escopo |
|------|------------|--------|
| Unitário | pytest | Funções e módulos Python isolados |
| Integração | pytest | APIs FastAPI, banco de dados |
| Frontend | React Testing Library | Componentes React, formulários, roteamento |
| E2E (opcional) | — | Fluxo completo processo → consulta → acesso por role → log |

Cobertura mínima esperada: 80% nos módulos de domínio backend.

### Diretriz de Testes (Testing-First / TDD)

**Todas as features devem ser validadas por testes antes do código ser aceito.**

- **Antes de implementar**: a feature deve ter testes criados que definam o comportamento esperado (red-green-refactor).
- **O código gerado só é considerado completo** quando os testes passam e validam o requisito.
- **Se o código for refatorado** (refatoração de estrutura, otimização, limpeza de código): os testes devem ser atualizados imediatamente para garantir que continuam refletindo o pleno funcionamento do sistema. Nenhuma refatoração pode ser considerada concluída sem a verificação dos testes correspondentes.
- **Em caso de falha de testes após refatoração**: reverta a alteração até que os testes estejam alinhados e passando novamente.

---

## Deploy

O desenvolvimento local usa **Docker Compose** para orquestrar FastAPI + PostgreSQL + (futuro) frontend React. Consulte `docker-project-foundations` para criar a estrutura inicial e `docker-best-practices` para boas práticas de imagens.

---

## Como usar este arquivo

- Humanos: leiam as seções relevantes antes de iniciar trabalho novo.
- Agentes DSH: consultem as skills listadas acima antes de gerar código ou specs; atualizem `GLOSSARY.md` e ADRs conforme decisões de domínio se consolidam.

---

*Este documento foi gerado a partir da entrevista `/grill-with-docs` e deve ser mantido sincronizado com o código e com as decisões de arquitetura do projeto.*