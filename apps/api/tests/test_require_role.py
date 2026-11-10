"""Ticket 03 — require_role dependency + LGPD audit middleware."""
import os
import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from apps.api.src.main import app
from apps.api.src.infra import database
from apps.api.src.models.auth import Role, User
from apps.api.src.models.audit import LogsAcesso
from apps.api.src.services.auth import create_user

PW = "Admin#2026a"
LOGIN = "admin@test"


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
    with Session(test_engine) as s:
        create_user(s, LOGIN, "Administrador", Role.ADMIN, PW)
        create_user(s, "adv@test", "Advogado", Role.ADVOGADO, PW)
        create_user(s, "ass@test", "Assistente", Role.ASSISTENTE, PW)

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        database.engine = original


def _login_as(client, login):
    r = client.post("/auth/login", json={"login": login, "password": PW})
    assert r.status_code == 200
    return r.cookies.get("access_token")


def _jogo_cpfc(client):
    return {
        "id_cliente": "11111111-1111-1111-1111-111111111111",
        "id_reclamado": "22222222-2222-2222-2222-222222222222",
        "numero_processo": "0001234-56.2026.8.06.0001",
        "data_autua": "2026-11-09",
        "valor_causa": 15000.50,
        "id_area": "Trabalhista",
        "id_rito": "Ordinario",
        "status": "Cadastrado",
        "observacao": "Obs válida",
    }


class TestRequireRole:
    def test_advogado_cria_processo(self, client):
        cookie = _login_as(client, "adv@test")
        r = client.post("/processos", json=_jogo_cpfc(client), cookies={"access_token": cookie})
        assert r.status_code == 201

    def test_admin_cria_processo(self, client):
        cookie = _login_as(client, LOGIN)
        r = client.post("/processos", json=_jogo_cpfc(client), cookies={"access_token": cookie})
        assert r.status_code == 201

    def test_assistente_pode_criar_processo_sem_valor_novo(self, client):
        cookie = _login_as(client, "ass@test")
        resp = client.post("/processos", json=_jogo_cpfc(client), cookies={"access_token": cookie})
        assert resp.status_code == 201  # sem valor_novo explicitamente pedido

    def test_assistente_nao_pode_atualizar_valor_causa(self, client):
        cookie = _login_as(client, "adv@test")
        sess = client.post("/processos", json=_jogo_cpfc(client), cookies={"access_token": cookie})
        proc_id = sess.json()["processo"]["id"]

        cookie_ass = _login_as(client, "ass@test")
        payload = _jogo_cpfc(client)
        payload["valor_causa"] = 99999.99
        r = client.put(f"/processos/{proc_id}", json=payload, cookies={"access_token": cookie_ass})
        assert r.status_code == 403

    def test_assistente_nao_pode_deletar_processo(self, client):
        cookie = _login_as(client, "adv@test")
        proc_id = client.post("/processos", json=_jogo_cpfc(client), cookies={"access_token": cookie}).json()["processo"]["id"]
        cookie_ass = _login_as(client, "ass@test")
        r = client.delete(f"/processos/{proc_id}", cookies={"access_token": cookie_ass})
        assert r.status_code == 403

    def test_admin_deleta_processo(self, client):
        cookie = _login_as(client, "adv@test")
        proc_id = client.post("/processos", json=_jogo_cpfc(client), cookies={"access_token": cookie}).json()["processo"]["id"]
        cookie_admin = _login_as(client, LOGIN)
        r = client.delete(f"/processos/{proc_id}", cookies={"access_token": cookie_admin})
        assert r.status_code == 200

    def test_require_role_invalid_role(self, client):
        cookie = _login_as(client, "ass@test")
        proc_id = client.post("/processos", json=_jogo_cpfc(client), cookies={"access_token": _login_as(client, "adv@test")}).json()["processo"]["id"]
        r = client.delete(f"/processos/{proc_id}", cookies={"access_token": cookie})
        assert r.status_code == 403


class TestLGPDAuditMiddleware:
    def test_audit_log_escrito_em_acessados_sensiveis(self, client):
        cookie = _login_as(client, "adv@test")
        # consulta um cliente (rota que usa CPF em texto ou mascarado)
        client.get("/clientes/1", cookies={"access_token": cookie})
        with Session(database.engine) as s:
            rows = s.exec(select(LogsAcesso)).all()
            assert len(rows) >= 1
            assert all(r.path and r.role and r.op for r in rows)
