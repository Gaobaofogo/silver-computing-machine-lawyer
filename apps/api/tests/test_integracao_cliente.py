from apps.api.src.main import app
from fastapi.testclient import TestClient


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

        # LGPD: CPF mascarado no retorno
        assert "***" in data["cliente"]["cpf"]
        assert data["cliente"]["nome_completo"] == "João Silva"
        assert data["cliente"]["telefone"] == "(85) 98765-4321"
        assert data["cliente"]["email"] == "joao@exemplo.com"

    def test_e2e_cliente_retorna_status_ativo_e_estado_civil_casado(self):
        client = TestClient(app)
        resp = client.post("/clientes", json={
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
        assert resp.status_code == 201
        data = resp.json()
        assert data["cliente"]["status"] == "Ativo"
        assert data["cliente"]["estado_civil"] == "Solteiro"

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
