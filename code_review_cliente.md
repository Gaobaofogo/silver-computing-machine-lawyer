# Code-Review: Cliente (model/schema/teste) vs GLOSSARY.md

Fixed point: `main` (branch atual); diff: `feature/cliente-cadastro` vs `main`.

---

## Standards

**Fontes de padrão consultadas:** `AGENTS.md` (§Testes — TDD, proibição assert True vazio, 80% cobertura), `docs/backend-patterns.md` (§2.1 linguagem, §4 validação separada, §6.4 fixtures), `docs/frontend-patterns.md` (§1.1 linguagem, §2 domínio, §6.5 tokens).

- **Standard OK — separação validação (Pydantic/Schema vs Service)**: `schemas/cliente.py` (Pydantic entry) vs `services/processo.py` (business rules). Não há `if` no router (router fino, conforme §4).
- **Standard OK — regex CPF**: `CPF_REGEX` definido e usado (`re.match`). `CNPJ_REGEX` também definido (para Reclamado, não Cliente — correto).
- **Standard OK — LGPD máscara**: `mascara_cpf()` no `main.py`; `Observacoes` não exposto no retorno (ainda não há campo `observacoes` no modelo — ver Spec).
- **Standard OK — linguagem**: código técnico (`ClienteSchema`, `validar_cliente_pf`) em inglês; domínio (`EstadoCivil`, `CPF`) em português (§2.1 / §1.1).
- **Standard OK — testes**: `test_cliente.py` com red-green (não `assert True` vazio, conforme atualização `AGENTS.md` §225); `test_integracao_cliente.py` (E2E).
- **Smell — Primitive Obsession (julgamento)**: `cpf` é `str`; poderia ser `Cpf` (tipo de valor). Não obrigatório agora, mas o código já tem regex, então o domínio está contido. Não viola padrão documentado.
- **Smell — Feature Envy (julgamento)**: `models/cliente.py` tem apenas campos simples; `schemas/cliente.py` faz validação. Não há método que envide dados de `Cliente` — aceitável para este tamanho.

---

## Spec (vs GLOSSARY.md)

**Especificação consultada:** `GLOSSARY.md` (linha 5 — Cliente PF; linha 19 — CPF/CNPJ sensível; linha 21 — Observação como campo LGPD), `ADR-0001` (implícito no código e docs).

- **✓ Cliente = PF**: `GLOSSARY.md` atualizado; código `ClienteSchema` não aceita `cnpj` (`extra="forbid"`); `state/cliente.py` não tem `cnpj`. Confere.
- **✓ CPF obrigatório + regex**: `GLOSSARY.md` menciona `CPF`; esquema valida com `^\d{3}\.\d{3}\.\d{3}-\d{2}$`; testes confirmam (red-green).
- **✓ EstadoCivil obrigatório**: `GLOSSARY.md` linha 15; `validate_estado_civil()` presente.
- **✗ Observacoes (`Observa`) faltante**: `GLOSSARY.md` linha 21 define `Observação` como campo livre associado a Cliente. `models/cliente.py` e `schemas/cliente.py` **não possuem** `observacoes`. `CadastroCliente.tsx` também não inclui. É uma lacuna real de spec (LGPD sensível).
- **✗ Cliente = PF notado no GLOSSARY (já corrigido)**: A atualização do `GLOSSARY.md` já refletiu `ADR-0001`; código alinha.
- **✓ LGPD — dados sensíveis**: `CPF` mascarado no retorno (`mascara_cpf`); nenhum token salvado no frontend (`localStorage` proibido documentado); `Observacoes` ainda faltante mas quando for adicionado deve ser mascarado/logado com cautela.

---

## Summary

- **Standards**: Passam. Nenhum hard violation; julgamento leve (`Primitive Obsession` aceitável).
- **Spec**: **Falha 1 (crítica)** — `Observacoes` (`Observa`) faltante no schema/modelo/teste, contrariando `GLOSSARY.md` §Observação e o domínio LGPD. **Falha 2 (menor)** — `Cliente` no GLOSSARY antes dizia PF/PJ (já corrigido na atualização `AGENTS.md`).

**Ação recomendada:** adicionar `observacoes: str | None = None` ao `models/cliente.py` e `schemas/cliente.py`; incluir no componente `CadastroCliente` com aviso LGPD; adicionar teste `test_cliente_rejeita_observacoes_sensiveis_em_log`.
