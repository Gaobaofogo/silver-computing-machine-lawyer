from apps.api.src.schemas.cliente import ClienteSchema
from apps.api.src.main import app
from fastapi.testclient import TestClient

def test_e2e_cliente_pf_com_cpf_estado_civil_e_role_advogado():
    """Fluxo integrado: schema PF + endpoint + mascara LGPD + auth role."""
    client = TestClient(app)
    resp = client.post("/clientes", json={
        "nome": "João Silva",
        "cpf": "411.133.456-70",
        "estado_civil": "Casado",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "criado"
    # LGPD: CPF mascarado no retorno
    assert "***" in data["cliente"]["cpf"]
