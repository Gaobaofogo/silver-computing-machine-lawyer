# ADR-0005: Value Objects NumeroProcesso e ValorCausa

- **Status:** Aceito
- **Data:** 2026-11-09
- **Contexto ticket:** .scratch/feature/processo-completo/issues/09-value-objects.md

## Contexto

GLOSSARY §2.1 lista `NumeroProcesso` e `ValorCausa` como Value Objects mas a
implementação antiga só validava comprimento (`min_length=2`, `max_length=30`).
ValorCausa já tinha bounds no schema, porém sem enforcement de 2 casas decimais.

## Decisão

### NumeroProcesso
- Formato obrigatório (formatação CNJ): `NNNNNNN-DD.AAAA.J.TR.OOOO`
  - 7 dígitos, `-`, 2 dígitos, `.`, 4 dígitos (ano), `.`, 1 dígito (J), `.`,
    2 dígitos (TR), `.`, 4 dígitos (OOOO).
  - Exemplo aceito: `0001234-56.2026.8.06.0001`.
- Regex: `^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$`
- **Aritmética de dígitos verificadores (mod-97) não implementada nesta etapa** —
  será tratada em ticket futuro se o produto exigir validação de cadastro CNJ.

### ValorCausa
- Decimal ≥ 0, ≤ 99.999.999,99 (dois decimais fixos).
- Mais de duas casas decimais: rejeitado.
- Mantém alinhamento com o limite já usado em `ProcessoSchema.valor_causa`.

## Consequências

- Schema Processo passa a rejeitar números de processo fora do padrão CNJ com
  HTTP 422, antes de o registro chegar à camada de persistência.
- Testes existentes que usavam números fora do padrão foram migrados para
  exemplos CNJ plausíveis.
- Número monetário inválido persistido é impossível via Pydantic.
