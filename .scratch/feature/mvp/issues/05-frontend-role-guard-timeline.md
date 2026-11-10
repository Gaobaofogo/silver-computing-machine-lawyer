# 05: Frontend RBAC guard + timeline de movimentos + refatoração ProcessoDetalhe

**What to build:** LoginForm aplicando role-aware tokens, ProcessoDetalhe timeline cronológica, refatoração do state machine DOM.

**Status:** ready-for-agent

Fonte: mvp-goal ("Critério aceite" 3,5); ADR-0007.

- [ ] `LoginForm` já existente: integrar `useAuth` hook (`POST /auth/login` -> cookie) com redirect em sucesso (`http://localhost:8080/processos`).
- [ ] Route guard no frontend (`RequireRole` com `<Navigate to="/login"/>` caso não autenticado; espelha require_role do backend).
- [ ] `ProcessoDetalhe.tsx`: timeline cronológica de movimentos (`GET /movimentos?processo_id=`), botão "Registrar movimento" com opção `status_novo`.
- [ ] RBAC checks no UI: assistente não vê botão de "Excluir processo" nem "Arquivamento administrativo"; admin vê menu de auditoria; advogado vê tudo menos gerenciar usuários.
- [ ] Timeline renderiza status badge (`CADASTRADO ⇒ EM_ANDAMENTO ⇒ CONCLUIDO ⇒ ARQUIVADO`).
- [ ] CSS: Tailwind tokens já existentes (`tailwind.config.js` mantido); sticky sidebar; padrões em `docs/frontend-patterns.md`.
- [ ] Testes RTL cobrindo todos os novos eventos; suite green 17 -> 24+; sem novos `<div>` sem `data-testid`.
- [ ] Sem reload na transição de estado (`onClick` via fetch).
