import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apps.api.src.main import app

def test_post_clientes_cria_pf_com_cpf_e_estado_civil():
    """Seam 1+2: endpoint POST /clientes aceita PF com CPF/EstadoCivil."""
    client = TestClient(app)
    resp = client.post("/clientes", json={
        "nome": "João Silva",
        "cpf": "411.133.456-70",
        "estado_civil": "Casado",
    })
    # Red: endpoint não existe ainda → 404
    assert resp.status_code == 201 or resp.status_code == 200
    assert "cpf" in resp.json()
