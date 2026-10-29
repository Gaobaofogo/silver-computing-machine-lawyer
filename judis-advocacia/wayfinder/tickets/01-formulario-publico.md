# 01: Formulário Público e Schema de Lead

**What to build:** Um formulário HTML curto de 8 perguntas que captura urgência, especialidade e maturidade de um lead, com API REST para receber e triar os dados. O schema define quais campos estão disponíveis.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Entrada pública do formulário com as 8 perguntas
- [ ] Schema TypeScript/JSON dos dados do lead
- [ ] API POST /api/leads com validação dos campos (urgência: 1-5, escala ordinal; especialidade: string livre; maturidade: boolean)
