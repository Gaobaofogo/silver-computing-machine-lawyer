# 03: RBAC granular `require_role(...)` + middleware LGPD de auditoria

**What to build:** middleware `require_role`, decoradores na rota decorada(role herdados), auditoria logar CPF/CNPJ.

**Status:** ready-for-agent

Fonte: ADR-0007; ADR-0001 ("Decisão registrada"); mvp-goal ("Matriz RBAC").

- [ ] `apps/api/src/auth/__init__.py`: `require_role(arg: str | list[str])` dependency FastAPI.
- [ ] `HTTP 403` com mensagem genérica quando falta permissão; sem payload de erro filtrado por role no corpo.
- [ ] Middleware `LGPDAudit` loga leitura/escrita CPF/CNPJ com `{ts, ip, user_id, role, op, resource}` em `logs_acesso`.
- [ ] Endpoints existentes refatorados para usar `require_role`:
  - `/clientes*`: advogado+admin (escrita); assistente ler (CPF mascarado)
  - `/reclamados*`: advogado+admin (escrita); assistente ler
  - `/processos*`: advogado+admin (criação); assistente create sem `value`; tudo exigirauth
  - `/movimentos*`: advogado+assistente+administrador create; transição arquivamento exige advogado+administrador
  - `DELETE /processos/{id}`: somente `administrador`
- [ ] Testes cobrindo `403` para assistente em valor_causa e arquivamento; `200` para dizer.
- [ ] Sem logs de CPF completo; pseudonimização no log (mesos mask format).
- [ ] Cobertura mantida ≥ 80%.
