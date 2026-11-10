"""Ticket 06 — Infra de persistência: engine, DDL, round-trip real.

TDD (red -> green). Cada teste usa engine própria (tmp_path SQLite).
"""
from decimal import Decimal
from datetime import date, datetime
import pytest
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Session, select, create_engine
from sqlalchemy import inspect

from apps.api.src.models.cliente import Cliente
from apps.api.src.models.processo import Area, MovimentoProcessual, Processo, Rito, StatusProcesso
from apps.api.src.infra.database import init_db, drop_db
import apps.api.src.infra.database as database


def _engine(tmp_path, name="test.db"):
    return create_engine(f"sqlite:///{tmp_path}/{name}")


def test_init_db_create_tables(monkeypatch, tmp_path):
    engine = _engine(tmp_path, "init_test.db")
    monkeypatch.setattr(database, "engine", engine)
    init_db()
    tables = set(inspect(engine).get_table_names())
    assert "processos" in tables
    assert "movimentos_processuais" in tables


def test_round_trip_processo(monkeypatch, tmp_path):
    engine = _engine(tmp_path, "round_trip_p.db")
    monkeypatch.setattr(database, "engine", engine)
    init_db()
    with Session(engine) as s:
        payload = Processo(
            id_cliente=uuid4(),
            id_reclamado=uuid4(),
            numero_processo="0001234-56.2026.8.06.0001",
            data_autua=date(2026, 11, 9),
            valor_causa=Decimal("12345.67"),
            id_area=Area.TRABALHISTA,
            id_rito=Rito.ORDINARIO,
        )
        s.add(payload)
        s.commit()
    with Session(engine) as s:
        row = s.exec(
            select(Processo).where(Processo.numero_processo == "0001234-56.2026.8.06.0001")
        ).first()
        assert row is not None
        assert isinstance(row.processo_id, UUID)
        assert row.status == StatusProcesso.CADASTRADO
        assert row.valor_causa == Decimal("12345.67")
        assert isinstance(row.created_at, datetime)


def test_movimento_processual_round_trip(monkeypatch, tmp_path):
    engine = _engine(tmp_path, "round_trip_m.db")
    monkeypatch.setattr(database, "engine", engine)
    init_db()
    pid = None
    with Session(engine) as s:
        p = Processo(
            id_cliente=uuid4(),
            id_reclamado=uuid4(),
            numero_processo="0009999-88.2026.8.06.0001",
            valor_causa=Decimal("100.00"),
            id_area=Area.CIVEL,
            id_rito=Rito.SUMARIO,
        )
        s.add(p)
        s.commit()
        s.refresh(p)
        pid = p.processo_id
        m = MovimentoProcessual(
            processo_id=pid,
            data_movimento=date(2026, 11, 10),
            tipo="Petição",
            descricao="Primeira petição",
            status_novo=StatusProcesso.EM_ANDAMENTO,
        )
        s.add(m)
        s.commit()
    with Session(engine) as s:
        rows = s.exec(select(MovimentoProcessual).where(MovimentoProcessual.processo_id == pid)).all()
        assert len(rows) == 1
        assert rows[0].tipo == "Petição"
        assert rows[0].status_novo == StatusProcesso.EM_ANDAMENTO
