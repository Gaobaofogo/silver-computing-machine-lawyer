"""Testes ticket 08 — validacao de Reclamado + mascara helper."""
import pytest
from apps.api.src.schemas.reclamado import ReclamadoSchema
from apps.api.src.services.reclamado import validar_reclamado
from apps.api.src.utils.lgpd_mask import mascara_cnpj, mascara_reclamado


def _endereco_pf():
    return {
        "logradouro": "Rua das Flores",
        "numero": "123",
        "bairro": "Centro",
        "cidade": "Fortaleza",
        "uf": "CE",
        "cep": "60010-000",
    }


def payload_pf():
    return dict(tipo="pf", cpf="411.133.456-70", endereco=_endereco_pf())


def payload_pj():
    return dict(
        tipo="pj",
        cnpj="12.345.678/0001-90",
        razao="Empresa X Ltda",
        endereco={**_endereco_pf(), "logradouro": "Av. Bezerra de Menezes", "numero": "1234", "bairro": "Aldeota"},
    )


class TestValidarReclamado:
    def test_pf_valido(self):
        assert validar_reclamado(ReclamadoSchema(**payload_pf())) == ReclamadoSchema(**payload_pf())

    def test_pj_valido(self):
        assert validar_reclamado(ReclamadoSchema(**payload_pj())) == ReclamadoSchema(**payload_pj())

    def test_cross_field_fail(self):
        with pytest.raises(Exception):
            ReclamadoSchema(**{**payload_pf(), "cnpj": "12.345.678/0001-90"})
        with pytest.raises(Exception):
            ReclamadoSchema(**{**payload_pj(), "cpf": "411.133.456-70"})

    def test_missing_razao_fail(self):
        p = payload_pj()
        p.pop("razao")
        with pytest.raises(Exception):
            ReclamadoSchema(**p)


class TestMascaraHelper:
    def test_cnpj_mask(self):
        assert mascara_cnpj("12.345.678/0001-90") == "***.***.***/***-90"

    def test_mascara_reclamado_cnpj(self):
        out = mascara_reclamado({"cnpj": "12.345.678/0001-90"})
        assert out["cnpj"] == "***.***.***/***-90"
        assert "cpf" not in out

    def test_mascara_reclamado_cpf(self):
        out = mascara_reclamado({"cpf": "411.133.456-70"})
        assert out["cpf"].startswith("***")
        assert out["cpf"].endswith("-70")
        assert "cnpj" not in out
