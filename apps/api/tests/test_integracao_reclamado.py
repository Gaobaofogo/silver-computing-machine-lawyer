# 04 — Integracao TDD Reclamado (PF/PJ)
from apps.api.src.schemas.reclamado import ReclamadoSchema
from apps.api.src.services.reclamado import validar_reclamado

def test_integracao_reclamado_pf_e_pj():
    pf = ReclamadoSchema(tipo="pf", cpf="411.133.456-70")
    assert validar_reclamado(pf) == pf
    pj = ReclamadoSchema(tipo="pj", cnpj="12.345.678/0001-90")
    assert validar_reclamado(pj) == pj
