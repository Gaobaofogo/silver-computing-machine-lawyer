# MVP Goal — JudisAdvocacia

**Data decisão:** 2026-11-10 (sessão de `grill-with-docs`)
**Status:** decisão consolidada — 3 roles, RBAC granular, auth (ADR-0006) y matriz RBAC (ADR-0007)

## O que este documento diz
O **objetivo do MVP** — a primeira entrega funcional que prova o valor central do produto em produção local. O foco é provar que o ciclo de negócio central (advogado atua/cadastra o processo com LGPD) funciona **na mesma sessão, sem reload**, num projeto cujo domínio foi lacrado na sessão passada (`processo-completo` tickets 06–09 + `cliente-cadastro/01–05`).

* `judis-advocacia/spec.md` continua sendo a referência arquitetural obrigatória.
* Todo o resto — funcionalidade central, interface, granular RBAC, auditoria LGPD — cai sob escopo deste MVP. O que não entra **vai para non-goals**.

## Ciclo-valor do MVP
`Login -> Cadastrar Cliente -> Cadastrar Processo (Área/Rito/ValorCausa) -> Registrar MovimentoInicial -> ProcessoDetalhe mostra StatusProcesso EM_ANDAMENTO`.
Funciona para as três personas (`Advogado`, `Assistente`, `Administrador`).
Se a demo é finalizável, o MVP acabou.

O MVP **não inclui**: relatórios/exportação, dashboard estatístico, e-mail/WhatsApp, integração com tribunais (PJe), múltiplos tenants/escritórios, auditoria de logs granular fora do necessário para o admin, dígitos verificadores CNJ (`mod-97`), deploy em nuvem, CI/CD automatizado.

## Critério de aceite (hand-off)
1. `docker compose up --build` em caminho limpo sobe 3 containers (postgres 5432, api 8000, web 8080); primeira migração inclui o seed `manage.py create-admin` via `ADMIN_LOGIN`/`ADMIN_PASSWORD`.
2. Login por JWT: cookie `HttpOnly; SameSite=Strict` com HS256 + bcrypt; exp 8 h.
3. Fluxo central navegável numa mesma sessão: login → criar cliente → criar processo (Área/Rito/ValorCausa) → criar `MovimentoProcessual` com `status_novo="Em Andamento"` → `ProcessoDetalhe` revela `EM_ANDAMENTO`. Funciona para todas as três personas.
4. Testes: backend **≥ 80%** de cobertura; frontend RTL **17/17 green**; matriz RBAC **revalidada**.
5. Documentação: Glossário alinhado; ADRs 0005/0006/0007 criadas e consistentes.

## Personas e capacidades RBAC

- **Advogado** (`advogado`): cria/atualiza/consulta processo completo com CPF claro. Cria/atualiza cliente. Cria/atualiza `ValorCausa`. Se arquiva processo. **Não** configura usuários nem audita logs.
- **Assistente** (`assistente`): consultas mascaradas (CPF pseudonimizado `***.***.***-XX`); cria/atualiza cliente/processo/movimentos (sem `ValorCausa`); não audita, não gerencia usuários.
- **Administrador** (`administrador`): auditoria de logs; CRUD de usuários (criar/desativar/reset senha); acessa todos os dados em texto claro.

Matriz completa (ver **ADR-0007**):

| Capacidade | Advogado | Assistente | Admin |
|---|:---:|:---:|:---:|
| Cliente — ler | ✔ | ✔ (CPF mascarado) | ✔ |
| Cliente — criar/editar | ✔ | ✔ | ✔ |
| Cliente — excluir | ✔ | ✘ | ✔ |
| Processo — ler | ✔ | ✔ | ✔ |
| Processo — criar/editar (sem `ValorCausa`) | ✔ | ✔ | ✔ |
| Processo — alterar `ValorCausa` | ✔ | ✘ | ✔ |
| Processo — arquivar | ✔ | ✘ | ✔ |
| Processo — excluir | ✔ | ✘ | ✔ |
| MovimentoProcessual — criar/ler | ✔ | ✔ (sem valor) | ✔ |
| Auditoria / logs | ✘ | ✘ | ✔ |
| Gestão de usuários | ✘ | ✘ | ✔ |
| Resetar senha | ✘ | ✘ | ✔ |

## Autenticação e LGPD
Refs **ADR-0006**: JWT HS256 + bcrypt; payload `{ sub, nome, role, exp }`; exp 8 h; cookie `HttpOnly; SameSite=Strict; Secure`; senha política mínimo 10, com ao menos: 1 número, 1 símbolo, 1 letra maiúscula. Script `manage.py create-admin` lido na primeira `docker compose up`; falha se `ADMIN_*` ausentes. Sem refresh token.
LGPD: middleware loga leitura/escrita em CPF/CNPJ com hora, IP, userId, role. `assistente` só vê CPF mascarado.

## Sequência de tarefas (ready-for-agent prioritizadas nesta ordem)

Tickets 01–05 prontos para `ready-for-agent`. Eles vigiam, na ordem, a partir de dependencias resolvidas.

1. **01** — `scripts/manage.py create-admin` (env `ADMIN_LOGIN`, `ADMIN_PASSWORD`; falha se ausentes). Consegue remover o seed do `localhost` na demonstração.
2. **02** — Backend autenticação (bcrypt; `POST /auth/login`; exp 8 h). Reusa engine `.scratch/feature/processo-completo` já testado.
3. **03** — RBAC granular `require_role(...)` + middleware LGPD (log de CPF/CNPJ).
4. **04** — Cliente + Reclamado com CRUD completo (absorve `cliente-cadastro/01 –04`) sob a mesma disciplina TDD.
5. **05** — Frontend `LoginForm` com role guard; `ProcessoDetalhe` refatorado; **timeline visual** dos movimentos com botão de transição de status para todas as personas.

## Deferred / não incluso (tickets futuros)
- Dígitos verificadores CNJ (`mod-97`).
- Múltiplos tenants/escritórios; dashboard estatístico.
- Auditoria de logs granular fora dos dois níveis exigidos pelo admin.
- E-mail transacional; ação de redefinição de senha por link.
- Integração com tribunais (PJe); envio automático de petição.
- CI/CD em nuvem; redis; observability cloud; HA.

## Definition of Done (hand-off para fase 2)
Uma linha é **done** quando: função central roda contra banco real; testes verdes (backend ≥ 80%, frontend RTL 17/17); docs atualizadas incluindo Glossário (LGPD, ADR-0001, 0005, 0006, 0007). O backlog `cliente-cadastro/01..05` é absorvido por esta roadmap; `processo-cadastro/06..09` já foram finalizados em 2026-11-09.
