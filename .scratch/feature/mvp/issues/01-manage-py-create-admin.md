# 01: Script `manage.py create-admin` (bootstrap admin)

**What to build:** script "manage.py create-admin" lido na primeira `docker compose up` cria o primeiro usuario admin.

**Status:** ready-for-agent

Fonte: ADR-0006 (Sec. 6), ADR-0006 (Sec. 1,4,5), mvp-goal.

- [ ] `./scripts/manage.py create-admin` (shebang `#!/usr/bin/env python3`, python3.11+).
- [ ] Lê env `ADMIN_LOGIN`, `ADMIN_PASSWORD`. Se ausentes, exit 1 com mensagem "ADMIN_LOGIN/ADMIN_PASSWORD ausentes".
- [ ] Gera bcrypt(cost=12) para a senha. Cria/atualiza user role=`admin`.
- [ ] Nome completo padrão `"Administrador"` ("Administrador").
- [ ] idempotente: se admin já existir, não duplica; avisa no stdout.
- [ ] Senha política mínima: ≥10 chars, ≥1 número, ≥1 símbolo, ≥1 maiúscula. Exit 2 com mensagem clara se quebrada.
- [ ] Sem senha no código / commits / testes.
- [ ] Sanity test faceando `manage.py create-admin` com mocks de env (pytest).
