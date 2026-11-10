# 02: Auth backend JWT HS256 + bcrypt (POST /auth/login)

**What to build:** backend de autenticação funcional com login, senha hashing, JWT, expiração 8h.

**Status:** ready-for-agent

Fonte: ADR-0006 (Sec. 1-4,7-8); Spec front-end LoginForm já expõe stub.

- [ ] `POST /auth/login` body `{login: str, password: str}` -> valida bcrypt(`users.password_hash`) -> gera JWT HS256 `{sub: <user_id>, nome, role, exp: now+8h}`.
- [ ] JWT cookie `HttpOnly; SameSite=Strict; Secure`; máx-age 28800.
- [ ] Cookie attribute `Secure` desabilitado apenas quando `COOKIE_SECURE=false` env (dev).
- [ ] Nenhum endpoint existente alterado (ticket 02 somente auth + middleware hook).
- [ ] Endpoint `GET /me` com role + nome (validado pelo JWT).
- [ ] Sem refresh token; usuário logout re-expiiria em 8h.
- [ ] Testes `test_auth.py` cobrindo login ok/erro/password inválida; cobertura backend ≥ 80% para `apps.api.src.auth`.
- [ ] Sem logs de senha. LGPD: auditoria de login (admin).
