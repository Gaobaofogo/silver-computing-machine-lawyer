# SUPERSEDED — ver .scratch/feature/processo-completo/issues/ (contrato novo, ADR-0001/GLOSSARY 4.1.1)

# 01: Schema/Modelo Processo

**Blocked by:** None

**Status:** ready-for-agent

- [ ] SQLModel `Processo`: `id` (PK), `id_processo` (str, index), `data_autua` (date), `valor_causa` (float/currency), `id_area` (str, FK ref), `id_rito` (str, FK ref), `id_reclamado` (str, FK ref), `observa` (str, LGPD sensivel)
- [ ] Pydantic `ProcessoSchema`: valida todos os campos; `id_processo` obrigatorio; `valor_causa` >= 0
