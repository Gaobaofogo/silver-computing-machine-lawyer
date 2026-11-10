# 04 — Integração Reclamado (PF/PJ)
import pytest
from apps.api.src.schemas.reclamado import ReclamadoSchema
from apps.api.src.services.reclamado import validar_reclamado
from apps.api.src.utils.lgpd_mask import mascara_reclamado


def payload_pf():
    return {
        "tipo": "pf",
        "cpf": "411.133.456-70",
        "endereco": {
            "logradouro": "Rua das Flores",
            "numero": "123",
            "bairro": "Centro",
            "cidade": "Fortaleza",
            "uf": "CE",
            "cep": "60010-000",
        },
    }


def payload_pj():
    return {
        "tipo": "pj",
        "cnpj": "12.345.678/0001-90",
        "razao": "Empresa X Ltda",
        "endereco": {
            "logradouro": "Av. Bezerra de Menezes",
            "numero": "1234",
            "bairro": "Aldeota",
            "cidade": "Fortaleza",
            "uf": "CE",
            "cep": "60115-001",
        },
    }


def test_integracao_reclamado_pf_e_pj():
    pf = ReclamadoSchema(**payload_pf())
    assert validar_reclamado(pf) == pf
    pj = ReclamadoSchema(**payload_pj())
    assert validar_reclamado(pj) == pj


class TestIntegracaoReclamadoMascara:
    def test_pf_mascara_cpf_no_retorno(self):
        out = mascara_reclamado({
            "tipo": "pf",
            "cpf": "411.133.456-70",
            "cnpj": None,
        })
        assert out["cpf"].startswith("***")

    def test_pj_mascara_cnpj_no_retorno(self):
        out = mascara_reclamado({
            "tipo": "pj",
            "cpf": None,
            "cnpj": "12.345.678/0001-90",
        })
        assert "***" in out["cnpj"]
