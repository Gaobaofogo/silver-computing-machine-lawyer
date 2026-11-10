# 05: Schema / Modelo Reclamado completo

**What to build:** Atualizar `ReclamadoSchema` e o modelo SQLModel para fechar lacunas entre GLOSSARY (ADR-0001) e código.

**Status:** done

- [x] Schema `ReclamadoSchema`: cross-field conditional — PF não entrega cnpj; PJ não entrega cpf.
- [x] `razao` obrigatório para PJ; opcional para PF.
- [x] `extra=forbid`.
- [x] Model `Reclamado` (table=True) com `reclamado_id: UUID`.
- [x] Audit: `created_at`/`updated_at`.
- [x] Testes: schema valida PF/PJ; rejeita transgressões.
