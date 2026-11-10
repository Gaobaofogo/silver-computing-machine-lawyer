# 02: Schema/Modelo MovimentoProcessual (GLOSSARY 4.1.1)

**What to build:** `MovimentoProcessual` — entidade interna ao agregado `Processo` (subordinado, não raiz independente).

**Status:** done

- [ ] Schema `MovimentoProcessualSchema`: movimentoId UUID, processoId UUID, dataMovimento Date, tipo String 2..50, descricao 2..2000 optional, statusAnterior/statusNovo StatusProcesso opcionais; extra=forbid.
- [ ] Model `MovimentoProcessual`: PK UUID, FK UUID processoId, audit created_at/updated_at; DDL NOT NULL.
- [ ] Teste: schema + DDL.
