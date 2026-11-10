"""Ticket 07 — Rotas /processos e /movimentos com persistência real.
TDD (red -> green). Testes usam TestClient + override de get_db()."""
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from apps.api.src.main import app
from apps.api.src.auth.dependencies import current_user
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
    "observacao": "Movimento inicial",
}

def _movimento(proc_id, data="2026-11-10"):
    return {
        "processo_id": proc_id,
        "data_movimento": data,
        "tipo": "Petição",
        "descricao": "Primeira petição",
    }


@pytest.fixture()
def client():
    test_engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    database.engine = test_engine
    database.init_db()

    def override_db():
        with Session(test_engine) as session:
            yield session

    original_engine = database.engine
    app.dependency_overrides[database.get_db] = override_db
    app.dependency_overrides[current_user] = lambda: {"user_id": "00000000-0000-0000-0000-000000000000", "login": "admin@test", "nome": "Administrador", "role": "admin"}
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        database.engine = original_engine


class TestRotasProcessos:
    def _proc_id(self, client):
        return client.post("/processos", json=_PAYLOAD).json()["processo"]["id"]

    def test_post_then_get_roundtrip(self, client):
        r = client.post("/processos", json=_PAYLOAD)
        assert r.status_code == 201
        proc_id = r.json()["processo"]["id"]
        r2 = client.get(f"/processos/{proc_id}")
        assert r2.status_code == 200
        read_back = r2.json()["processo"]
        assert read_back["numero_processo"] == "0001234-56.2026.8.06.0001"
        assert read_back["valor_causa"] == "15000.50"
        assert read_back["id_area"] == "Trabalhista"
        assert read_back["id_rito"] == "Ordinario"
        assert read_back["observacao"] == "Movimento inicial"

    def test_put_updates_and_returns(self, client):
        proc_id = self._proc_id(client)
        new = dict(_PAYLOAD)
        new["valor_causa"] = 25000.50
        new["observacao"] = "Atualizado por sala"
        upd = client.put(f"/processos/{proc_id}", json=new)
        assert upd.status_code == 200
        body = upd.json()
        assert body["processo"]["valor_causa"] == "25000.50"
        assert body["processo"]["observacao"] == "Atualizado por sala"

    def test_delete_removes_and_404_on_miss(self, client):
        proc_id = self._proc_id(client)
        del_resp = client.delete(f"/processos/{proc_id}")
        assert del_resp.status_code == 200
        gone = client.get(f"/processos/{proc_id}")
        assert gone.status_code == 404

    def test_get_missing_returns_404(self, client):
        r = client.get("/processos/9d8e-7f6g-5h4i-3j2k")
        assert r.status_code == 404


class TestRotasMovimentos:
    def test_post_movimento_for_existing_processo(self, client):
        proc_id = client.post("/processos", json=_PAYLOAD).json()["processo"]["id"]
        out = client.post("/movimentos", json=_movimento(proc_id)).json()
        assert out["status"] == "criado"
        assert out["movimento"]["tipo"] == "Petição"

    def test_get_movimentos_filtered_by_processo(self, client):
        proc_id = client.post("/processos", json=_PAYLOAD).json()["processo"]["id"]
        client.post("/movimentos", json=_movimento(proc_id))
        rows = client.get("/movimentos", params={"processo_id": proc_id}).json()["movimentos"]
        assert len(rows) >= 1
        assert rows[0]["tipo"] == "Petição"
