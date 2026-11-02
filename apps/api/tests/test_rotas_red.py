"""Testes red — rotas API reais."""
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.api.src.schemas.cliente import ClienteSchema
from apps.api.src.schemas.reclamado import ReclamadoSchema
from apps.api.src.schemas.processo import ProcessoSchema
from apps.api.src.main import app

def test_post_cliente():
    client = TestClient(app)
    resp = client.post("/clientes", json={"nome":"João","cpf":"411.133.456-70","estado_civil":"Casado"})
    assert resp.status_code in (200, 201)
    assert "cpf" in resp.json()["cliente"]

def test_get_cliente_por_id():
    client = TestClient(app)
    resp = client.get("/clientes/1")
    assert resp.status_code == 200
    assert resp.json()["status"] == "consultado"
    # LGPD: cpf mascarado
    assert "***" in resp.json()["cliente"]["cpf"]

def test_put_cliente():
    client = TestClient(app)
    resp = client.put("/clientes", json={
        "nome":"João Silva", "cpf":"411.133.456-70", "estado_civil":"Divorciado"
    })
    assert resp.status_code in (200, 201)
    assert resp.json()["status"] == "atualizado"

def test_delete_cliente():
    client = TestClient(app)
    resp = client.delete("/clientes/1")
    assert resp.status_code == 200
    assert resp.json()["status"] == "deletado"
