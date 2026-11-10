# 10: Candidatos para o próximo ciclo de implementação

**Status:** decidido — A
**Data:** 2026-11-09 — fila de amanhã (2026-11-10)

## O que já está feito
- Processo 01–09 ✅ persistência real, máquina de estados, value objects (ADR-0005)
- Reclamado 05–09 ✅ (cpf/cnpj + schema + integração)
- Cliente enum suite (cliente-cpf-endereco-enum) 01–08 ✅
- Observação adicionada ao Cliente (commit 55fe7e5 observacoes-green)

## Candidatos

### A) Replicar padrão em Cliente (≈2 sessões)
- `cliente-cadastro/01..05` (schema persistência, rotas CRUD real, auth/LGPD)
- Igual ao que fizemos para Processo hoje, só que para Cliente.
- Impacto: back-end Cliente 100% persistente em produção.

### B) UI Process — conectar front às transições
- `apps/web/src/components/ProcessoDetalhe.tsx` já existe e renderiza status.
- Falta: timeline visual de movimentos, seleção de status de movimento,
  cronograma, talvez página `/processos` com listagem.
- Impacto: demo boss, E2E navegável.

### C) CNJ mod-97 dígitos verificadores
- Hoje NumeroProcesso só valida formato; check digits não implementado.
- ADR-0005 registra como ticket futuro.
- Esforço: pequeno, alto rigor.

### D) Code review + Hardening pós-recalibragem
- `git diff a555ef4~1 3f1820b` — 94 files, 9053 insertions.
- Acessar split 2-tier: padrão + spec com `code-review` skill.
- Impacto: confidence no que acabamos de entregar.

### E) Auditoria do `updated_at` / `created_at` em SQLite
- Hoje os timestamps são naive local timezone semantics (`datetime.now(timezone.utc)` é ok) — validar no padrão 12-factor.

## Decisão (2026-11-09, escolhido pelo usuário)
PRIORIDADE: **A) Cliente persistência idêntica a Processo**

Sequência amanhã (2026-11-10):
1. Ler `cliente-cadastro/01-modelo-schema-cliente.md`
2. Executar do 01 ao 05 (schema, rotas, UI, auth) com TDD.
3. Reutilizar padrão do 06-09 do `processo-completo` (engine, get_db, CRUD persistente,
   Integration tests, auth/LGPD).
4. Commitar como `feat(cliente): persistência real (CLI-01..05)`
