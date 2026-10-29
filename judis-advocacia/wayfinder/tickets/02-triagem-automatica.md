# 02: Triagem Automática e Classificação

**What to build:** Serviço de triagem que lê o lead, calcula urgência (>=3 é quente) e match de especialidade, e define se é um caso.

**Blocked by:** 01 - Formulário Público e Schema de Lead

**Status:** ready-for-agent

- [ ] Regra de corte: urgência >= 3
- [ ] Regra de match: especialidade do lead contém pelo menos uma palavra da especialidade do escritório
- [ ] Geração do caso se as duas condições forem satisfeitas
- [ ] Persistência do caso na base de dados (se aplicável)
