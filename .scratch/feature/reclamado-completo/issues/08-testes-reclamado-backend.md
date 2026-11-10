# 08: Testes backend — Reclamado

**What to build:** Cobertura verde nos módulos de domínio.

**Status:** done

- [x] `test_model_reclamado.py`: UUID PK, DDL NOT NULL, audit.
- [x] `test_schema_reclamado.py`: PF/PJ green/red, cross-field, UF enum, ranges.
- [x] `test_validacao_reclamado.py`: serviço + helper `mascara_reclamado`.
- [x] `test_api_reclamado_routes.py`: TestClient POST/GET/PUT/DELETE.
- [x] `test_integracao_reclamado.py`: PF/PJ integrado + mascaramento.
- [x] `pytest apps/api/tests/`: **104 passed**.
- [~] Cobertura >=80% **não medida por ferramenta** (pytest-cov não instalado no vendor); módulos de domínio cobertos por inspeção dos seams: model/schema/service/utils/routes.
