"""Ticket 09 — ValueObjects (GLOSSARY §2.1, ADR-0005).

TDD (red -> green): boundary + VO validation."""
import pytest
from decimal import Decimal

from apps.api.src.domain.value_objects import NumeroProcesso, ValorCausa


class TestNumeroProcesso:
    def test_aceita_numero_cnj_valido(self):
        assert str(NumeroProcesso("0001234-56.2026.8.06.0001")) == "0001234-56.2026.8.06.0001"

    def test_normaliza_espacos(self):
        assert str(NumeroProcesso("  0001234-56.2026.8.06.0001  ")) == "0001234-56.2026.8.06.0001"

    def test_rejeita_sem_mascaras(self):
        with pytest.raises(ValueError):
            NumeroProcesso("00012345620268060001")

    def test_rejeita_formato_errado(self):
        with pytest.raises(ValueError):
            NumeroProcesso("123.45.6789")

    def test_rejeita_letras(self):
        with pytest.raises(ValueError):
            NumeroProcesso("ABC1234-56.2026.8.06.0001")

    def test_rejeita_vazio(self):
        with pytest.raises(ValueError):
            NumeroProcesso("")

    def test_igualdade_e_hash(self):
        a, b = NumeroProcesso("0001234-56.2026.8.06.0001"), NumeroProcesso("0001234-56.2026.8.06.0001")
        assert a == b
        assert hash(a) == hash(b)


class TestValorCausa:
    def test_aceita_zero(self):
        assert ValorCausa(Decimal("0.00")).valor == Decimal("0.00")

    def test_aceita_maximo(self):
        assert ValorCausa(Decimal("99999999.99")).valor == Decimal("99999999.99")

    def test_aceita_minimo_fracionario(self):
        assert ValorCausa(Decimal("0.01")).valor == Decimal("0.01")

    def test_rejeita_negativo(self):
        with pytest.raises(ValueError):
            ValorCausa(Decimal("-1.00"))

    def test_rejeita_acima_do_limite(self):
        with pytest.raises(ValueError):
            ValorCausa(Decimal("100000000.00"))

    def test_rejeita_mais_de_2_decimais(self):
        with pytest.raises(ValueError):
            ValorCausa(Decimal("10.999"))

    def test_quantiza_para_2_casas(self):
        assert ValorCausa(Decimal("10.99")).valor == Decimal("10.99")

    def test_aceita_string(self):
        assert ValorCausa("1234.56").valor == Decimal("1234.56")

    def test_igualdade_e_hash(self):
        a, b = ValorCausa(Decimal("100.00")), ValorCausa(Decimal("100.00"))
        assert a == b
        assert hash(a) == hash(b)
