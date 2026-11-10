# 06: LGPD — mascara CNPJ no serviço/rotas Reclamado

**What to build:** mascaramento LGPD para CNPJ nas respostas (`mascara_cnpj`).

**Status:** done

- [x] Função `mascara_cnpj(cpf)` em `apps/api/src/utils/lgpd_mask.py`.
- [x] Rotas `/reclamados` retornam CNPJ mascarado no payload `reclamado.cnpj`.
- [x] Testes: `test_lgpd_mask.py`, `test_validacao_reclamado.py` (helper), `test_integracao_reclamado.py` (PF/PJ mascarado).
- [x] `utils/lgpd_mask.py` também comporta `mascara_cpf` e `mascara_reclamado`.
