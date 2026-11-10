# 01: Schema/Modelo Reclamado (PF ou PJ)

**Blocked by:** None

**Status:** done

- [x] Schema `Reclamado`: `tipo` (`Literal["pf","pj"]`); `cpf` se PF; `cnpj` se PJ (`regex ^[A-Z0-9]{2}\.[A-Z0-9]{3}\.[A-Z0-9]{3}/[A-Z0-9]{4}-\d{2}$`)
- [x] ADR-0001: `Cliente` = PF; `Reclamado` pode ser PF ou PJ
- [x] Teste `pytest`: `ReclamadoPF` (CPF) passa; `ReclamadoPJ` (CNPJ) passa; `ReclamadoPF` com CNPJ falha
