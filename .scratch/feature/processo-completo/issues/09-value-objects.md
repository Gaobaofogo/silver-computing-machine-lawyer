# 09: ValueObjects NumeroProcesso e ValorCausa (GLOSSARY §2.1)

**What to build:** Value Objects baseados em glossary §2.1.

**Status:** done

- [ ] `NumeroProcesso` — Tipo literal/regex validado no schema. ADR ou número de processo CNJ a confirmar.
- [ ] `ValorCausa` — tipo monetário (money) Decimal, range 0..99999999.99, max 2 decimais.
- [ ] Observação preserved: ValueObject substitutable without DDL changes.
- [ ] Testes RED → GREEN em `test_value_objects.py`.
- [ ] ADR/decisão número de processo se formato puder ser inferido do ADR-0001 ou glossário.
