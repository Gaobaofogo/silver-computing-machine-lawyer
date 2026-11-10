import pytest

from apps.api.src.schemas.reclamado import ReclamadoSchema
from apps.api.src.models.reclamado import Reclamado


def payload_pf():
    return dict(
        tipo="pf",
        cpf="411.133.456-70",
        estado_civil="Casado",
        endereco={
            "logradouro": "Rua das Flores",
            "numero": "123",
            "bairro": "Centro",
            "cidade": "Fortaleza",
            "uf": "CE",
            "cep": "60010-000",
        },
    )


def payload_pj():
    return dict(
        tipo="pj",
        cnpj="12.345.678/0001-90",
        razao="Empresa X",
        endereco={
            "logradouro": "Rua das Flores",
            "numero": "123",
            "bairro": "Centro",
            "cidade": "Fortaleza",
            "uf": "CE",
            "cep": "60010-000",
        },
    )


def test_modelo_reclamado_sqlmodel():
    r = Reclamado(**payload_pf())
    assert r.tipo == "pf"
    assert r.cpf == "411.133.456-70"


def test_reclamado_pf_com_cpf():
    r = ReclamadoSchema(**payload_pf())
    assert r.tipo == "pf"
    assert r.cpf == "411.133.456-70"


def test_reclamado_pj_com_cnpj():
    r = ReclamadoSchema(**payload_pj())
    assert r.tipo == "pj"
    assert r.cnpj == "12.345.678/0001-90"


def test_reclamado_pf_com_cnpj_falha():
    p = payload_pf()
    p.pop("cpf")
    p["cnpj"] = "12.345.678/0001-90"
    with pytest.raises(Exception):
        ReclamadoSchema(**p)
