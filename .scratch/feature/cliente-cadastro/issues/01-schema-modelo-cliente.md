# 01: Schema/Modelo Cliente PF

**What to build:** Modelo `Cliente` (PF obrigatorio) no backend: `cpf` obrigatório, `estado_civil` obrigatório, `cnpj` removido (ADR-0001). Nenhum campo `tipo` (Cliente = sempre PF).

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Schema SQLModel `Cliente` (`table=True`) com `cpf` (str, index=True), `estado_civil` (str), `nome` (str), sem `cnpj`
- [ ] Schema Pydantic `ClienteSchema` com validacao `min_length=11` no `cpf` e `estado_civil` nao vazio
- [ ] Teste `pytest`: `test_cliente_criado_com_cpf_e_estado_civil` passa (red-green)
- [ ] `GLOSSARY.md` referencia: `Cliente` = pessoa fisica, `CPF` obrigatorio, `EstadoCivil` obrigatorio
