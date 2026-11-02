"""Testes consolidados — Processo (01-05) — validados contra código disponível."""
import pytest
from apps.api.src.models.processo import Processo
from apps.api.src.schemas.processo import ProcessoSchema
from apps.api.src.services.processo import validar_processo
from apps.api.src.services.processo_access import can_access

def test_modelo_sqlmodel_cria_processo():
    p = Processo(id_processo="PROC-001", data_autua="2026-01-01", valor_causa=10000.0,
                 id_area="TRAB", id_rito="ORD", id_reclamado="REC-01")
    assert p.id_processo == "PROC-001"
    assert p.valor_causa == 10000.0

def test_schema_pydantic_rejeita_extra_e_aceita_valido():
    s = ProcessoSchema(id_processo="PROC-002", data_autua="2026-02-01",
                       valor_causa=5000.0, id_area="CIV", id_rito="SUM",
                       id_reclamado="REC-02")
    assert s.id_processo == "PROC-002"
    with pytest.raises(Exception):
        # extra="forbid" rejeita campo desconhecido
        ProcessoSchema(id_processo="X", data_autua="d", valor_causa=1,
                       id_area="A", id_rito="R", id_reclamado="R", campo_invalido="bad")

def test_service_validar_processo():
    s = ProcessoSchema(id_processo="PROC-003", data_autua="2026-03-01",
                       valor_causa=0.0, id_area="PREV", id_rito="ESP",
                       id_reclamado="REC-03")
    assert validar_processo(s) == s

def test_access_role_advogado_e_admin():
    assert can_access("advogado") is True
    assert can_access("admin") is True
    assert can_access("atendente") is False

def test_integracao_e2e_processo_com_reclamado():
    # Integração vertical: schema + serviço + access
    s = ProcessoSchema(id_processo="PROC-004", data_autua="2026-04-01",
                       valor_causa=25000.0, id_area="TRAB", id_rito="ORD",
                       id_reclamado="REC-04", observacoes="Movimento inicial")
    p = validar_processo(s)
    assert can_access("advogado")
    assert s.observacoes == "Movimento inicial"
