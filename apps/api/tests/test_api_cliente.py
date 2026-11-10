from fastapi.testclient import TestClient
from apps.api.src.main import app
from apps.api.tests._auth_stub import enable_admin_override, disable_admin_override
import pytest
from apps.api.src.auth.dependencies import current_user



@pytest.fixture(autouse=True)
def _admin_auth():
    enable_admin_override()
    yield
    disable_admin_override()

def cliente_json_valido():
    return {
        "nome_completo": "Maria Souza",
        "cpf": "411.133.456-70",
        "endereco": {
            "logradouro": "Rua das Flores",
            "numero": "45",
            "bairro": "Aldeota",
            "cidade": "Fortaleza",
            "uf": "CE",
            "cep": "60010-000",
        },
        "estado_civil": "Solteiro",
    }


class TestAPICliente:
    def test_post_clientes_cria_pf_com_filtros(self):
        """Seam: endpoint POST /clientes aceita PF completo com endereco/enum/audit."""
        client = TestClient(app)
        resp = client.post("/clientes", json=cliente_json_valido())
        assert resp.status_code == 201
        body = resp.json()
        assert body["status"] == "criado"
        assert body["cliente"]["cpf"] == "411.133.456-70"

    def test_post_rejeita_estado_civil_invalido(self):
        """Seam: POST rejeita EstadoCivil fora do dominio."""
        client = TestClient(app)
        resp = client.post("/clientes", json={
            **cliente_json_valido(),
            "estado_civil": "Solteira",
        })
        assert resp.status_code == 422

    def test_post_rejeita_endereco_invalido(self):
        """Seam: POST rejeita endereco invalido (UFs invalidos)."""
        client = TestClient(app)
        data = cliente_json_valido()
        data["endereco"]["uf"] = "EN"
        resp = client.post("/clientes", json=data)
        assert resp.status_code == 422

    def test_post_rejeita_nome_completo_invalido(self):
        """Seam: POST rejeita nome_completo < 2."""
        client = TestClient(app)
        data = cliente_json_valido()
        data["nome_completo"] = "a"
        resp = client.post("/clientes", json=data)
        assert resp.status_code == 422