"""Testes ticket 06 — LGPD mascara CNPJ."""

from apps.api.src.utils.lgpd_mask import mascara_cnpj


class TestMascaraCNPJ:
    def test_mascara_completa_rejeita_36(self):
        assert mascara_cnpj("12.345.678/0001-90") == "***.***.***/***-90"

    def test_formato_plano(self):
        assert mascara_cnpj("12345678000190") == "***.***.***/***-90"

    def test_string_invalida(self):
        assert mascara_cnpj("") == "***.***.***/***-**"
        assert mascara_cnpj("abc") == "***.***.***/***-**"
