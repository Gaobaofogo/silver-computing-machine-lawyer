"""Ticket 07 — Rotas /reclamados (ADR-0001 + LGPD)."""
from fastapi.testclient import TestClient

from apps.api.src.main import app

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


class TestRotasReclamado:
    def test_post_cria_pf(self):
        client = TestClient(app)
        resp = client.post("/reclamados", json=CLIENTE_FULL_PF)
        assert resp.status_code == 201
        body = resp.json()
        assert body["status"] == "criado"
        assert "***" in body["reclamado"]["cpf"]
        assert body["reclamado"]["tipo"] == "pf"

    def test_post_cria_pj(self):
        client = TestClient(app)
        resp = client.post("/reclamados", json=CLIENTE_FULL_PJ)
        assert resp.status_code == 201
        body = resp.json()
        assert body["status"] == "criado"
        assert "***" in body["reclamado"]["cnpj"]
        assert body["reclamado"]["razao"] == "Empresa X Ltda"

    def test_get_reclamado(self):
        client = TestClient(app)
        resp = client.get("/reclamados/xyz")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "consultado"
        assert "***" in body["reclamado"]["cnpj"]

    def test_put_reclamado(self):
        client = TestClient(app)
        data = dict(CLIENTE_FULL_PF)
        data["estado_civil"] = "Solteiro"
        resp = client.put("/reclamados/xyz", json=data)
        assert resp.status_code == 200
        assert resp.json()["status"] == "atualizado"
        assert "***" in resp.json()["reclamado"]["cpf"]

    def test_delete_reclamado(self):
        client = TestClient(app)
        resp = client.delete("/reclamados/xyz")
        assert resp.status_code == 200
        assert resp.json()["status"] == "deletado"

    def test_post_cnpj_invalido(self):
        client = TestClient(app)
        bad = dict(CLIENTE_FULL_PJ)
        bad["cnpj"] = "999"
        resp = client.post("/reclamados", json=bad)
        assert resp.status_code == 422

    def test_post_pf_sem_cpf(self):
        client = TestClient(app)
        bad = dict(CLIENTE_FULL_PF)
        bad.pop("cpf")
        resp = client.post("/reclamados", json=bad)
        assert resp.status_code == 422

    def test_post_pj_sem_razao(self):
        client = TestClient(app)
        bad = dict(CLIENTE_FULL_PJ)
        bad.pop("razao")
        resp = client.post("/reclamados", json=bad)
        assert resp.status_code == 422
