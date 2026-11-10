"""Ticket 09 integration — boundary 422 con VOs en ProcessoSchema (ADR-0005)."""
import pytest
from uuid import uuid4
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine

from apps.api.src.main import app
from apps.api.src.auth.dependencies import current_user

from apps.api.src.infra import database

_PAYLOAD = {
    "id_cliente": str(uuid4()),
    "id_reclamado": str(uuid4()),
    "numero_processo": "0001234-56.2026.8.06.0001",
    "data_autua": "2026-11-09",
    "valor_causa": 15000.50,
    "id_area": "Trabalhista",
    "id_rito": "Ordinario",
    "status": "Cadastrado",
}


@pytest.fixture()
def client():
    test_engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    original = database.engine
    database.engine = test_engine
    database.init_db()

    def override_db():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[database.get_db] = override_db
    app.dependency_overrides[current_user] = lambda: {"user_id": "00000000-0000-0000-0000-000000000000", "login": "admin@test", "nome": "Administrador", "role": "admin"}
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        database.engine = original


def test_processo_rejeita_numero_fora_do_cnj(client):
    bad = dict(_PAYLOAD, numero_processo="123/4567")
    r = client.post("/processos", json=bad)
    assert r.status_code == 422


def test_processo_rejeita_mais_de_2_decimais(client):
    bad = dict(_PAYLOAD)
    bad["valor_causa"] = "10.999"
    r = client.post("/processos", json=bad)
    assert r.status_code == 422
