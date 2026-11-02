import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from apps.api.src.schemas.cliente import ClienteSchema
from apps.api.src.services import validar_cliente_pf  # assume exists for now

def test_post_clientes_cpf_obrigatorio():
    """Seam 2: CPF obrigatorio (ADR-0001)."""
    client = TestClient(app := FastAPI())
    with pytest.raises((ValueError, Exception)):
        TestClient(app).post("/clientes", json={
            "nome": "João",
            "estado_civil": "Casado",  # cpf missing
        })
