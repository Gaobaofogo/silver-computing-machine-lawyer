import pytest

from apps.api.src.schemas.reclamado import ReclamadoSchema
from apps.api.src.models.reclamado import Reclamado

def test_modelo_reclamado_sqlmodel():
    r = Reclamado(tipo="pf", cpf="411.133.456-70", razao="João Silva")
    assert r.tipo == "pf"
    assert r.cpf == "411.133.456-70"

def test_reclamado_pf_com_cpf():
    r = ReclamadoSchema(tipo="pf", cpf="411.133.456-70", estado_civil="Casado")
    assert r.tipo == "pf"
    assert r.cpf == "411.133.456-70"

def test_reclamado_pj_com_cnpj():
    r = ReclamadoSchema(tipo="pj", cnpj="12.345.678/0001-90", razao="Empresa X")
    assert r.tipo == "pj"
    assert r.cnpj == "12.345.678/0001-90"

def test_reclamado_pf_com_cnpj_falha():
    with pytest.raises(ValueError):
        ReclamadoSchema(tipo="pf", cnpj="12.345.678/0001-90")  # CNPJ removido no PF
