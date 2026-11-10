"""Testes green — rotas API reais (ADR-0001: Cliente = PF com endereço + enum)."""
import pytest
from fastapi.testclient import TestClient
from apps.api.src.main import app

CLIENTE_FULL = {
    "nome_completo": "João Silva",
    "cpf": "411.133.456-70",
    "endereco": {
        "logradouro": "Rua das Flores",
        "numero": "123",
        "bairro": "Centro",
        "cidade": "Fortaleza",
        "uf": "CE",
        "cep": "60010-000",
    },
    "estado_civil": "Casado",
}


class TestRotasCliente:
    def test_post_cliente_cria_pf(self):
        client = TestClient(app)
        resp = client.post("/clientes", json=CLIENTE_FULL)
        assert resp.status_code == 201
        body = resp.json()
        assert body["status"] == "criado"
        data = body["cliente"]
        # LGPD: cpf mascarado
        assert "***" in data["cpf"]
        assert data["nome_completo"] == "João Silva"
        assert data["estado_civil"] == "Casado"
        # observacoes padrão = None
        assert data["observacao"] is None

    def test_get_cliente_consulta(self):
        client = TestClient(app)
        resp = client.get("/clientes/1")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "consultado"
        assert "***" in body["cliente"]["cpf"]

    def test_put_cliente_atualiza(self):
        client = TestClient(app)
        resp = client.put("/clientes/1", json={
            **CLIENTE_FULL,
            "estado_civil": "Solteiro",
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "atualizado"

    def test_delete_cliente_por_cpf(self):
        client = TestClient(app)
        resp = client.delete("/clientes/411.133.456-70")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "deletado"
        assert body["cpf"].startswith("***")
