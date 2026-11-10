# 02: API / Service Cliente

**What to build:** Endpoint `/clientes` (create + read por CPF); seam `Depends(auth_verify)`; seam de negocio `Depends(validar_cliente_pf)` (CPF obrigatorio, EstadoCivil, nenhuma regra CNPJ); mascara `cpf` no retorno; não expor CPF nem `observacoes` no log; teste `pytest` red-green.

**Blocked by:** 01

**Status:** ready-for-agent

- [ ] Endpoint `POST /clientes` e `GET /clientes/{cpf}` com schemas validados via Depends
- [ ] Regra negocio: CPF obrigatorio, EstadoCivil obrigatorio, nenhum CNPJ (ADR-0001)
- [ ] Retorno mascara CPF (`***.***.***-**`) para lista, valor com nome cliente
- [ ] Teste `test_cliente_criado_com_cpf_e_estado_civil`: valida que `GET /clientes/411.133.456-7` retorna `estado_civil` OK
