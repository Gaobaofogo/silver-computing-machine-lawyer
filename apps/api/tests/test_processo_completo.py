"""Testes consolidados — Processo (01-05) — contrato ADR-0001/GLOSSARY 4.1.1."""
import pytest
from decimal import Decimal
from datetime import date
from uuid import UUID, uuid4
from apps.api.src.models.processo import Area, Rito, StatusProcesso
from apps.api.src.models.processo import Processo
from apps.api.src.schemas.processo import ProcessoSchema
from apps.api.src.services.processo import validar_processo
from apps.api.src.services.processo_access import can_access, can_alter_valor_causa

def _payload_valido():
    return {
        "id_cliente": str(uuid4()),
        "id_reclamado": str(uuid4()),
        "numero_processo": "0001234-56.2026.8.06.0001",
        "data_autua": "2026-11-09",
        "valor_causa": Decimal("25000.00"),
        "id_area": "Trabalhista",
        "id_rito": "Ordinario",
        "status": "Cadastrado",
        "observacao": "Movimento inicial",
    }

def test_modelo_sqlmodel_cria_processo():
    p = Processo(
        id_cliente=UUID(_payload_valido()["id_cliente"]),
        id_reclamado=UUID(_payload_valido()["id_reclamado"]),
        numero_processo="0001234-56.2026.8.06.0001",
        data_autua=date(2026, 11, 9),
        valor_causa=Decimal("10000.00"),
        id_area=Area.TRABALHISTA,
        id_rito=Rito.ORDINARIO,
        status=StatusProcesso.CADASTRADO,
    )
    assert isinstance(p.processo_id, UUID)
    assert p.valor_causa == Decimal("10000.00")
    assert p.status == StatusProcesso.CADASTRADO

def test_schema_pydantic_rejeita_extra_e_aceita_valido():
    s = ProcessoSchema(**_payload_valido())
    assert s.numero_processo == "0001234-56.2026.8.06.0001"
    with pytest.raises(Exception):
        ProcessoSchema(**{**_payload_valido(), "campo_invalido": "bad"})

def test_service_validar_processo():
    s = ProcessoSchema(**{**_payload_valido(), "observacao": None})
    out = validar_processo(s)
    assert out.numero_processo == s.numero_processo
    assert out.status.value == "Cadastrado"

def test_access_role_advogado_e_admin():
    assert can_access("advogado") is True
    assert can_access("admin") is True
    assert can_access("atendente") is False

def test_integracao_e2e_processo_com_reclamado():
    s = ProcessoSchema(**_payload_valido())
    assert validar_processo(s).observacao == "Movimento inicial"
    assert can_access("advogado")

def test_assistente_nao_altera_valor_causa():
    # Primeiro teste red -> verde: ensures ADR-0001 persona rule
    assert can_alter_valor_causa("advogado") is True
    assert can_alter_valor_causa("admin") is True
    assert can_alter_valor_causa("assistente") is False
