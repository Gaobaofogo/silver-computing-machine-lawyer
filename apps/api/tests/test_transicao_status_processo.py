"""Ticket 08 — Máquina de estados StatusProcesso (GLOSSARY 4.1.3).

TDD: red -> green. Cobertura: service-level transitions + integração via API."""
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine

from apps.api.src.main import app
from apps.api.src.infra import database
from apps.api.src.services.processo import transicionar_status, transicoes_permitidas
from apps.api.src.models.processo import StatusProcesso

_PAYLOAD = {
    "id_cliente": str(uuid4()),
    "id_reclamado": str(uuid4()),
    "numero_processo": "0001234-56.2026.8.06.0001",
    "valor_causa": 15000.50,
    "id_area": "Trabalhista",
    "id_rito": "Ordinario",
    "status": "Cadastrado",
}


def _proc(client, payload=None):
    payload = payload or _PAYLOAD
    r = client.post("/processos", json=payload)
    assert r.status_code == 201
    return r.json()["processo"]["id"]


class TestTransicoesPermitidas:
    def test_cadastrado_vai_para_em_andamento(self):
        assert transicoes_permitidas(StatusProcesso.CADASTRADO) == [StatusProcesso.EM_ANDAMENTO]

    def test_em_andamento_vai_para_em_andamento_ou_concluido(self):
        out = transicoes_permitidas(StatusProcesso.EM_ANDAMENTO)
        assert StatusProcesso.EM_ANDAMENTO in out
        assert StatusProcesso.CONCLUIDO in out

    def test_concluido_vai_para_arquivado(self):
        assert transicoes_permitidas(StatusProcesso.CONCLUIDO) == [StatusProcesso.ARQUIVADO]

    def test_arquivado_terminal(self):
        assert transicoes_permitidas(StatusProcesso.ARQUIVADO) == []

    def test_transicao_invalida_levanta(self):
        with pytest.raises(ValueError):
            transicionar_status(StatusProcesso.CADASTRADO, StatusProcesso.CONCLUIDO)

    def test_transicao_valida_passa(self):
        assert transicionar_status(StatusProcesso.CADASTRADO, StatusProcesso.EM_ANDAMENTO) == StatusProcesso.EM_ANDAMENTO

    def test_arquivamento_em_cadastrado_levanta(self):
        with pytest.raises(ValueError):
            transicionar_status(StatusProcesso.CADASTRADO, StatusProcesso.ARQUIVADO)


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
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        database.engine = original


class TestMovimentoTransicionaProcesso:
    def test_primeira_peticao_transiciona_cad_para_em(self, client):
        proc_id = _proc(client)
        mov = {
            "processo_id": proc_id,
            "data_movimento": "2026-11-10",
            "tipo": "Petição inicial",
            "status_novo": "Em Andamento",
        }
        r = client.post("/movimentos", json=mov)
        assert r.status_code == 201
        proc = client.get(f"/processos/{proc_id}").json()["processo"]
        assert proc["status"] == "Em Andamento"

    def test_sentenca_transiciona_em_andamento_para_concluido(self, client):
        proc_id = _proc(client, dict(_PAYLOAD, status="Em Andamento"))
        mov = {
            "processo_id": proc_id,
            "data_movimento": "2026-12-01",
            "tipo": "Sentença",
            "status_novo": "Concluido",
        }
        r = client.post("/movimentos", json=mov)
        assert r.status_code == 201
        proc = client.get(f"/processos/{proc_id}").json()["processo"]
        assert proc["status"] == "Concluido"

    def test_arquivamento_transiciona_concluido_para_arquivado(self, client):
        proc_id = _proc(client, dict(_PAYLOAD, status="Concluido"))
        mov = {
            "processo_id": proc_id,
            "data_movimento": "2027-01-15",
            "tipo": "Arquivamento administrativo",
            "status_novo": "Arquivado",
        }
        r = client.post("/movimentos", json=mov)
        assert r.status_code == 201
        proc = client.get(f"/processos/{proc_id}").json()["processo"]
        assert proc["status"] == "Arquivado"

    def test_movimento_sem_status_novo_nao_transiciona(self, client):
        proc_id = _proc(client)
        mov = {
            "processo_id": proc_id,
            "data_movimento": "2026-11-10",
            "tipo": "Outra petição",
        }
        r = client.post("/movimentos", json=mov)
        assert r.status_code == 201
        proc = client.get(f"/processos/{proc_id}").json()["processo"]
        assert proc["status"] == "Cadastrado"

    def test_movimentacao_continua_em_andamento_e_valida(self, client):
        proc_id = _proc(client, dict(_PAYLOAD, status="Em Andamento"))
        mov = {
            "processo_id": proc_id,
            "data_movimento": "2026-11-12",
            "tipo": "Resposta",
            "status_novo": "Em Andamento",
        }
        r = client.post("/movimentos", json=mov)
        assert r.status_code == 201
        proc = client.get(f"/processos/{proc_id}").json()["processo"]
        assert proc["status"] == "Em Andamento"

    def test_transicao_invalida_pela_api_retorna_409(self, client):
        proc_id = _proc(client)
        mov = {
            "processo_id": proc_id,
            "data_movimento": "2026-11-10",
            "tipo": "Petição inválida",
            "status_novo": "Concluido",  # CADASTRADO -> CONCLUIDO: forbidden
        }
        r = client.post("/movimentos", json=mov)
        assert r.status_code == 409
