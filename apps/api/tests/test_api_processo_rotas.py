"""Ticket 03 rewritten — Rotas /processos e /movimentos (agora persistentes)."""
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from apps.api.src.main import app
from apps.api.src.infra import database
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine

_PAYLOAD = {
    "id_cliente": str(uuid4()),
    "id_reclamado": str(uuid4()),
    "numero_processo": "0001234-56.2026.8.06.0001",
    "data_autua": "2026-11-09",
    "valor_causa": 15000.50,
    "id_area": "Trabalhista",
    "id_rito": "Ordinario",
    "status": "Cadastrado",
    "observacao": "Prioridade máxima",
}

def _movimento(proc_id):
    return {"processo_id": proc_id, "data_movimento": "2026-11-10", "tipo": "Petição"}


@pytest.fixture()
def client():
    test_engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    original_engine = database.engine
    database.engine = test_engine
    database.init_db()

    def override_db():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[database.get_db] = override_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        database.engine = original_engine


class TestRotasProcessos:
    def test_post_cria_201(self, client):
        r = client.post("/processos", json=_PAYLOAD)
        assert r.status_code == 201
        assert r.json()["status"] == "criado"
        assert r.json()["processo"]["numero_processo"] == "0001234-56.2026.8.06.0001"

    def test_post_rejeita_id_area_invalida(self, client):
        r = client.post("/processos", json={**_PAYLOAD, "id_area": "NaoArea"})
        assert r.status_code == 422

    def test_get_processo(self, client):
        proc_id = client.post("/processos", json=_PAYLOAD).json()["processo"]["id"]
        r = client.get(f"/processos/{proc_id}")
        assert r.status_code == 200
        assert r.json()["status"] == "consultado"

    def test_put_processo(self, client):
        proc_id = client.post("/processos", json=_PAYLOAD).json()["processo"]["id"]
        payload = dict(_PAYLOAD)
        payload["observacao"] = "Atualizado"
        r = client.put(f"/processos/{proc_id}", json=payload)
        assert r.status_code == 200
        assert r.json()["status"] == "atualizado"

    def test_delete_processo(self, client):
        proc_id = client.post("/processos", json=_PAYLOAD).json()["processo"]["id"]
        r = client.delete(f"/processos/{proc_id}")
        assert r.status_code == 200
        assert r.json()["status"] == "deletado"


class TestRotasMovimentos:
    def test_post_movimento_201(self, client):
        proc_id = client.post("/processos", json=_PAYLOAD).json()["processo"]["id"]
        r = client.post("/movimentos", json=_movimento(proc_id))
        assert r.status_code == 201
        assert r.json()["movimento"]["tipo"] == "Petição"

    def test_get_movimentos_por_processo(self, client):
        proc_id = client.post("/processos", json=_PAYLOAD).json()["processo"]["id"]
        client.post("/movimentos", json=_movimento(proc_id))
        r = client.get("/movimentos", params={"processo_id": proc_id})
        assert r.status_code == 200
        assert isinstance(r.json()["movimentos"], list)
