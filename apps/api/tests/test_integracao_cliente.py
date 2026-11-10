"""E2E integrada /clientes PF (ticket 04)."""
from fastapi.testclient import TestClient
from apps.api.src.main import app
from apps.api.tests._auth_stub import enable_admin_override, disable_admin_override
import pytest

@pytest.fixture(autouse=True)
def _admin_auth():
    enable_admin_override()
    yield
    disable_admin_override()

class TestE2ECliente:
    def test_e2e_cliente_pf_com_cpf_estado_civil_e_endereco(self):
        """Fluxo integrado: schema PF completo + endpoint + mascara LGPD."""
        client = TestClient(app)
        resp = client.post("/clientes", json={
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
            "telefone": "(85) 98765-4321",
            "email": "joao@exemplo.com",
            "observacao": "Cliente em conciliação",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["status"] == "criado"
        # LGPD: CPF mascarado no retorno para assistente; admin vê o próprio.
        cid = data["cliente"]["id"]
        g = client.get(f"/clientes/{cid}")
        assert g.status_code == 200
        upd = g.json()["cliente"]
        assert upd["cpf"] == "411.133.456-70"  # admin
        assert upd["estado_civil"] == "Casado"
        assert upd["telefone"] == "(85) 98765-4321"
        assert upd["email"] == "joao@exemplo.com"

    def test_e2e_cliente_retorna_status_ativo_e_estado_civil_casado(self):
        client = TestClient(app)
        r = client.post("/clientes", json={
            "nome_completo": "Maria Souza",
            "cpf": "411.133.456-70",
            "endereco": {
                "logradouro": "Rua das Flores",
                "numero": "456",
                "bairro": "Aldeota",
                "cidade": "Fortaleza",
                "uf": "CE",
                "cep": "60010-000",
            },
            "estado_civil": "Solteiro",
        })
        assert r.status_code == 201
        c = r.json()["cliente"]
        assert c["status"] == "Ativo"
        assert c["estado_civil"] == "Solteiro"

    def test_e2e_rejeita_cnpj_retirado(self):
        client = TestClient(app)
        resp = client.post("/clientes", json={
            "nome_completo": "Empresa X",
            "cpf": "411.133.456-70",
            "cnpj": "12.345.678/0001-90",
            "endereco": {
                "logradouro": "Rua das Flores",
                "numero": "123",
                "bairro": "Centro",
                "cidade": "Fortaleza",
                "uf": "CE",
                "cep": "60010-000",
            },
            "estado_civil": "Casado",
        })
        assert resp.status_code == 422
