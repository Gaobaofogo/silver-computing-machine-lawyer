# 08: Máquina de estados StatusProcesso ligada a MovimentoProcessual

**What to build:** Transições CADASTRADO→EM_ANDAMENTO→CONCLUIDO→ARQUIVADO válidas/invalidas via serviço de aplicação.

**Status:** done

Fonte: GLOSSARY 4.1.3 e 7.1 ("primeira petição → StatusProcesso muda de CADASTRADO para EM_ANDAMENTO").

- [ ] FOQ-01: `RegistrarMovimentoProcessual(processo_id, tipo, descricao?, status_novo=EM_ANDAMENTO)` cria movimento E transiciona Processo de CADASTRADO → EM_ANDAMENTO.
- [ ] FOQ-02: `registrar_espaco_final` (CONCLUIDO) transita EM_ANDAMENTO → CONCLUIDO via movimento.
- [ ] FOQ-03: `registrar_arquivamento` (ARQUIVADO) transita CONCLUIDO → ARQUIVADO.
- [ ] FOQ-04: transição inválida (ex.: CADASTRADO → CONCLUIDO, EM_ANDAMENTO → CADASTRADO) rejeitada com `ValueError`.
- [ ] FOQ-05: movimento com `status_novo=None` só registra movimento, não transita status.
- [ ] Testes em `test_transicao_status_processo.py` (service-level) — TDD red → green.
