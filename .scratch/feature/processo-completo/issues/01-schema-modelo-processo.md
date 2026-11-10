# 01: Enums + Schema/Modelo Processo (ADR-0001, GLOSSARY 4.1.1)

**What to build:** schema/modelo completo do `Processo` (raiz do agregado).

**Status:** done

- [ ] Enums `Area` (TRABALHISTA|CIVEL|PREVIDENCIARIO|TRIBUTARIO|PENAL) e `Rito` (ORDINARIO|SUMARIO|ESPECIAL) em `models/processo.py` (str-enum).
- [ ] Enum `StatusProcesso` (CADASTRADO|EM_ANDAMENTO|CONCLUIDO|ARQUIVADO).
- [ ] Schema `ProcessoSchema`: idCliente (UUID), idReclamado (UUID), numeroProcesso 2..30, dataAutuacao (Date opcional), valorCausa money 0..99999999.99, idArea/idRito enum, status enum, observacao min 2 max 2000 optional; extra=forbid.
- [ ] Model `Processo`: PK UUID `processo_id`, FKs UUID idCliente/idReclamado, audit `created_at`/`updated_at`, `status` default CADASTRADO; DDL colunas tipoas enums.
- [ ] Teste: schema valida todos os ramos; DDL NOT NULL.
