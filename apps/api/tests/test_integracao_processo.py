# 04 — Integracao TDD Processo (PF) + MovimentoProcessual (ADR-0001, GLOSSARY 4.1.1)
from uuid import uuid4
import pytest
from apps.api.src.schemas.processo import ProcessoSchema
from apps.api.src.services.processo import validar_processo, validar_movimento
from apps.api.src.schemas.processo import MovimentoProcessualSchema
from decimal import Decimal

def payload_valido():
    return dict(
        id_cliente=str(uuid4()),
        id_reclamado=str(uuid4()),
        numero_processo="0001234-56.2026.8.06.0001",
        data_autua="2026-11-09",
        valor_causa=Decimal("15000.50"),
        id_area="Civel",
        id_rito="Ordinario",
        status="Cadastrado",
    )

def test_validacao_processo_roundtrip():
    p = validar_processo(ProcessoSchema(**payload_valido()))
    assert p.id_area.value == "Civel"
    assert p.status.value == "Cadastrado"

def test_validacao_movimento_roundtrip():
    m = MovimentoProcessualSchema(
        processo_id=uuid4(),
        data_movimento="2026-11-09",
        tipo="Petição",
    )
    out = validar_movimento(m)
    assert out.tipo == "Petição"

def test_processo_invalido():
    with pytest.raises(Exception):
        validar_processo(ProcessoSchema(**{**payload_valido(), "id_area": "X"}))

def test_movimento_invalido():
    m = MovimentoProcessualSchema(
        processo_id=uuid4(),
        data_movimento="2026-11-09",
        tipo="Petição",
    )
    m = m.model_dump()
    m["tipo"] = ""
    with pytest.raises(Exception):
        validar_movimento(MovimentoProcessualSchema(**m))
