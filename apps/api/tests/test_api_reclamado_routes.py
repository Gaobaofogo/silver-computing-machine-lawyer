"""Ticket 04 — Rotas /reclamados (ADR-0001 + LGPD) persistentes."""
import pytest
from fastapi.testclient import TestClient
from apps.api.src.main import app
from apps.api.tests._auth_stub import enable_admin_override, disable_admin_override

CLIENTE_FULL_PF = {
    "tipo": "pf",
    "cpf": "411.133.456-70",
    "estado_civil": "Casado",
    "endereco": {
        "logradouro": "Rua das Flores",
        "numero": "123",
        "bairro": "Centro",
        "cidade": "Fortaleza",
        "uf": "CE",
        "cep": "60010-000",
    },
}

CLIENTE_FULL_PJ = {
    "tipo": "pj",
    "cnpj": "12.345.678/0001-90",
    "razao": "Empresa X Ltda",
    "endereco": {
        "logradouro": "Av. Bezerra de Menezes",
        "numero": "1234",
        "bairro": "Aldeota",
        "cidade": "Fortaleza",
        "uf": "CE",
        "cep": "60115-001",
    },
}


@pytest.fixture(autouse=True)
def _admin_auth():
    enable_admin_override()
    yield
    disable_admin_override()


class TestRotasReclamado:
    def test_post_cria_pf(self):
        client = TestClient(app)
        resp = client.post("/reclamados", json=CLIENTE_FULL_PF)
        assert resp.status_code == 201
        body = resp.json()
        assert body["status"] == "criado"
        assert body["reclamado"]["cpf"] == "411.133.456-70"
        assert body["reclamado"]["tipo"] == "pf"

    def test_post_cria_pj(self):
        client = TestClient(app)
        resp = client.post("/reclamados", json=CLIENTE_FULL_PJ)
        assert resp.status_code == 201
        body = resp.json()
        assert body["status"] == "criado"
        assert body["reclamado"]["cnpj"] == "12.345.678/0001-90"
        assert body["reclamado"]["razao"] == "Empresa X Ltda"

    def test_roundtrip_pf(self):
        client = TestClient(app)
        created = client.post("/reclamados", json=CLIENTE_FULL_PF).json()["reclamado"]
        rid = created["id"]
        got = client.get(f"/reclamados/{rid}")
        assert got.status_code == 200
        assert got.json()["reclamado"]["cpf"] == "411.133.456-70"

        upd = client.put(f"/reclamados/{rid}", json=dict(CLIENTE_FULL_PF, estado_civil="Solteiro"))
        assert upd.status_code == 200
        assert upd.json()["status"] == "atualizado"
        assert upd.json()["reclamado"]["tipo"] == "pf"

        d = client.delete(f"/reclamados/{rid}")
        assert d.status_code == 200
        assert d.json()["status"] == "deletado"
        assert client.get(f"/reclamados/{rid}").status_code == 404

    def test_get_reclamado_404(self):
        client = TestClient(app)
        resp = client.get("/reclamados/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404

    def test_delete_reclamado(self):
        client = TestClient(app)
        created = client.post("/reclamados", json=CLIENTE_FULL_PJ).json()["reclamado"]
        rid = created["id"]
        resp = client.delete(f"/reclamados/{rid}")
        assert resp.status_code == 200
        assert resp.json()["status"] == "deletado"

    def test_assistente_mascara_cpf(self):
        from apps.api.src.auth.dependencies import current_user
        from apps.api.src.main import app as a
        a.dependency_overrides[current_user] = lambda: {"user_id": "x", "login": "y", "nome": "S", "role": "assistente"}
        try:
            client = TestClient(app)
            resp = client.post("/reclamados", json=CLIENTE_FULL_PF)
            assert resp.status_code == 201
            assert "***" in resp.json()["reclamado"]["cpf"]
        finally:
            a.dependency_overrides.pop(current_user, None)
