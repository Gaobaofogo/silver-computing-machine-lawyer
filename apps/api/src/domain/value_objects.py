"""Value Objects de domínio (GLOSSARY §2.1, ADR-0005).

Encapsulam invariantes que não devem ser expressas por tipos comuns do Python.
Validação ocorre no boundary (schema) e no VO; persistência continua recebendo
o valor primitivo (string UUID; Decimal money)."""
from decimal import Decimal
import re

NUMERO_PROCESSO_PATTERN = re.compile(r"^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$")

VALOR_CAUSA_MAX = Decimal("99999999.99")
VALOR_CAUSA_MIN = Decimal("0.00")
VALOR_CAUSA_DECIMALS = 2


class NumeroProcesso:
    """Número de processo no formato CNJ (NNNNNNN-DD.AAAA.J.TR.OOOO)."""

    PATTERN = NUMERO_PROCESSO_PATTERN

    def __init__(self, valor: str):
        candidato = (valor or "").strip()
        if not candidato:
            raise ValueError("numero_processo não pode ser vazio")
        if not self.PATTERN.fullmatch(candidato):
            raise ValueError(
                f"numero_processo inválido: {candidato!r} "
                "(esperado padrão CNJ '0001234-56.2026.8.06.0001')"
            )
        self.valor = candidato

    def __str__(self) -> str:  # p/ logging
        return self.valor

    def __repr__(self) -> str:
        return f"NumeroProcesso({self.valor!r})"

    def __eq__(self, other) -> bool:
        return isinstance(other, NumeroProcesso) and self.valor == other.valor

    def __hash__(self) -> int:
        return hash(("NumeroProcesso", self.valor))


class ValorCausa:
    """Valor da causa em Reais: >= 0, <= 99.999.999,99, duas casas decimais."""

    def __init__(self, valor):
        try:
            v = Decimal(str(valor))
        except Exception:
            raise ValueError(f"valor_causa inválido (não decimal): {valor!r}")
        if v < VALOR_CAUSA_MIN:
            raise ValueError(f"valor_causa negativo: {v}")
        if v > VALOR_CAUSA_MAX:
            raise ValueError(f"valor_causa acima do limite ({VALOR_CAUSA_MAX}): {v}")
        if v.as_tuple().exponent < -VALOR_CAUSA_DECIMALS:
            raise ValueError(
                f"valor_causa com mais de {VALOR_CAUSA_DECIMALS} casas decimais: {v}"
            )
        self.valor = v.quantize(Decimal("0.01"))

    def __str__(self) -> str:
        return str(self.valor)

    def __repr__(self) -> str:
        return f"ValorCausa({self.valor})"

    def __eq__(self, other) -> bool:
        return isinstance(other, ValorCausa) and self.valor == other.valor

    def __hash__(self) -> int:
        return hash(("ValorCausa", self.valor))
