# 04: Auth / Role + LGPD no Frontend

**What to build:** Seam `useContext` (`AuthContext`) para `role` apenas (`advogado`/`atendente`/`admin`); `LoginForm` e `Logout` com `httpOnly` cookie; nunca montar `Authorization: Bearer` no JS (cookie enviado pelo navegador via `credentials: 'include'`); `ProcessoCard` mostra/oculta botoes conforme `role`.

**Blocked by:** 03

**Status:** ready-for-agent

- [ ] `AuthContext` guarda apenas `role` (string), nunca token
- [ ] `LoginForm` envia credenciais ao backend; recebe `access_token` apenas como cookie `HttpOnly`
- [ ] `Logout` limpa cookie; nao usa `localStorage.removeItem('token')`
- [ ] `ProcessoCard`: botao `Editar` visivel só se `role === 'advogado'`; `Cadastrar` visivel se `role === 'advogado' || 'atendente'`
