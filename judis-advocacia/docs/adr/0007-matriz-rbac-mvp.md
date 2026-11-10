# ADR-0007 — Matriz RBAC granular do MVP
Status: decidido na sessão 2026-11-10

## Contexto
ADR-0006 firma a autenticação (JWT HS256 + bcrypt). A persona exige acesso granular por role — o MVP quer mostrar que três personas (`Advogado`, `Assistente`, `Administrador`) têm o mesmo fluxo central de negócio com privilégios distintos, LGPD confiada e auditoria. Este ADR fixa a matriz de capacidades e o modo de implementação (FastAPI dependencies no decorator de rota; middleware LGPD para auditoria de CPF/CNPJ).

## Decisões

### Papéis e capacidades

| Capacidade | Advogado | Assistente | Administrador |
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
| Gestão de usuários (criar/desativar) | ✘ | ✘ | ✔ |
| Resetar senha de outro usuário | ✘ | ✘ | ✔ |
| Configuração de roles | ✘ | ✘ | ✔ |

`assistente` nunca vê CPF em texto puro. `advogado` e `administrador` veem CPF. `Administrador` audita logs de acesso a CPF/CNPJ; `Assistente` não tem acesso a logs.

### Implementação
1. FastAPI dependencies `require_role(role: str | list[str])` injetáveis em todos os decorators de rota que exijam permissão específica. Erro `403` se o role não corresponde (`HTTPException`).
2. Middleware dedicado a **LGPD auditoria**: registra leitura/escrita a CPF/CNPJ com hora, IP, userId, role.
3. `ValorCausa` é campo de criação/edição restrito a `advogado` e `administrador`; validado via schema e blocked in `PUT/PATCH /processos/{id}`.
4. ArquivarProcesso (movimento com `status_novo="Arquivado"`) exige `advogado` ou `administrador`; `assistente` recebe `403`.
5. `delete` de Processo exige `administrador` (somente) — gestão crítica.

## Trade-offs
- Esquema RBAC estático no código vs. tabular(False): chove complexidade no MVP; escolhe-se enums `Role` em Python + decorators simples.
- `require_role` open-coded por rota ao invés de matriz de permissões: transparência no decorator; baixo custo de manutenção no MVP.
- Nenhum grant granular por recurso (ex.: "advogado X só acessa processo Y"). Obs exige tenency model — fora do MVP.

## Consequências
- Todas as rotas `/clientes`, `/reclamados`, `/processos`, `/movimentos` precisam de decorator `require_role`.
- Middleware de auditoria deve ser implementado **antes** que a primeira demo `E2E` rode.
- Frontend incumbe role guard em `LoginForm` e ribbon colapsado em `ProcessoDetalhe.tsx` (`assistente` não vê botão de excluir, `advogado` não vê audit.).
- Implementação do endpoint \`GET /admin/logs_acesso\` será feita no ticket 04 do MVP com permissão restrita a `administrador`.
