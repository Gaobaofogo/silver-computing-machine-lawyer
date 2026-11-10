"""Tickets 02: Schema + Modelo de MovimentoProcessual (ADR-0001, GLOSSARY 4.1.1)."""
import pytest
from datetime import date, datetime
from uuid import UUID

from apps.api.src.schemas.processo import MovimentoProcessualSchema
from apps.api.src.models.processo import (
    MovimentoProcessual as MovimentoModel,
    StatusProcesso,
)

def payload_full():
    from uuid import uuid4
    return dict(
        processo_id=str(uuid4()),
        data_movimento="2026-11-09",
        tipo="Petição",
        descricao="Movimento de sustentação oral",
    )


class TestMovimentoSchema:
    def test_minimo_valido(self):
        m = MovimentoProcessualSchema(**payload_full())
        assert m.tipo == "Petição"
        assert m.descricao == "Movimento de sustentação oral"

    def test_tipo_range_min(self):
        p = payload_full()
        p["tipo"] = "x"
        with pytest.raises(Exception):
            MovimentoProcessualSchema(**p)

    def test_tipo_range_max(self):
        p = payload_full()
        p["tipo"] = "x" * 51
        with pytest.raises(Exception):
            MovimentoProcessualSchema(**p)

    def test_datamovimento_requerido(self):
        with pytest.raises(Exception):
            MovimentoProcessualSchema(**{**payload_full(), "data_movimento": ""})

    def test_descricao_max(self):
        p = payload_full()
        p["descricao"] = "y" * 2001
        with pytest.raises(Exception):
            MovimentoProcessualSchema(**p)

    def test_extra_forbid(self):
        with pytest.raises(Exception):
            MovimentoProcessualSchema(**{**payload_full(), "odd": "xx"})


class TestMovimentoModel:
    def test_audit_defaults(self):
        m = MovimentoModel(**payload_full())
        assert isinstance(m.movimento_id, UUID)
        assert isinstance(m.created_at, type(date.today()))

    def test_ddl_not_null(self):
        table = MovimentoModel.__table__
        cols = {c.name: c for c in table.columns}
        assert cols["processo_id"].nullable is False
        assert cols["data_movimento"].nullable is False
        assert cols["tipo"].nullable is False
