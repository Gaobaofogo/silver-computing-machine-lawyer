"""Testes green rotas /clientes & /reclamados — novo contrato persistente (ticket 04)."""
import pytest
from fastapi.testclient import TestClient
from apps.api.src.main import app
from apps.api.src.auth.dependencies import current_user
from apps.api.tests._auth_stub import enable_admin_override, disable_admin_override

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
CLIENTE_ADD = dict(CLIENTE_FULL, telefone="(85) 98765-4321", email="joao@exemplo.com", estado_civil="Solteiro")
CLIENTE_POST = dict(CLIENTE_FULL, estado_civil="Solteiro", observacao="dado2")


@pytest.fixture(autouse=True)
def _admin_auth():
    enable_admin_override()
    yield
    disable_admin_override()


class TestRotasCliente:
    def test_post_cliente_cria_pf(self):
        client = TestClient(app)
        resp = client.post("/clientes", json=CLIENTE_FULL)
        assert resp.status_code == 201
        data = resp.json()["cliente"]
        assert data["cpf"] == "411.133.456-70"          # admin vê CPF próprio
        assert data["estado_civil"] == "Casado"
        assert data["observacao"] is None
        cid = data["id"]

        # consultar retorna o mesmo negócio
        g = client.get(f"/clientes/{cid}")
        assert g.status_code == 200
        assert g.json()["cliente"]["cpf"] == "411.133.456-70"
        assert g.json()["cliente"]["estado_civil"] == "Casado"

        # put atualiza estado civil + observacoes
        u = client.put(f"/clientes/{cid}", json=dict(CLIENTE_ADD, estado_civil="Solteiro", observacao="dado2"))
        assert u.status_code == 200
        up = u.json()["cliente"]
        assert up["estado_civil"] == "Solteiro"
        assert up["observacao"] == "dado2"

        # delete por id
        d = client.delete(f"/clientes/{cid}")
        assert d.status_code == 200
        assert d.json()["status"] == "deletado"

    def test_assistente_mascara_cpf_no_retorno(self):
        from apps.api.src.auth.dependencies import current_user
        from apps.api.src.main import app as a
        a.dependency_overrides[current_user] = lambda: {"user_id": "x-ass", "login": "a@t", "nome": "S", "role": "assistente"}
        try:
            client = TestClient(app)
            resp = client.post("/clientes", json=CLIENTE_FULL)
            assert resp.status_code == 201
            assert "***" in resp.json()["cliente"]["cpf"]
        finally:
            a.dependency_overrides.pop(current_user, None)

        client = TestClient(app)
        orig_dep = None

    def test_delete_cliente_por_id(self):
        client = TestClient(app)
        c = client.post("/clientes", json=CLIENTE_FULL).json()["cliente"]
        cid = c["id"]
        r = client.delete(f"/clientes/{cid}")
        assert r.status_code == 200
        assert r.json()["status"] == "deletado"


# Reclamado (PF/PJ) — assumes admin+ assistente mascara
class TestRotasReclamado:
    def test_post_cria_pf(self):
        client = TestClient(app)
        payload = {"tipo": "pf", "cpf": "411.133.456-70", "razao": None,
                   "endereco": dict(CLIENTE_FULL["endereco"], cep="60010-000")}
        resp = client.post("/reclamados", json=payload)
        assert resp.status_code == 201
        r = resp.json()["reclamado"]
        assert r["tipo"] == "pf"
        assert r["cpf"] == "411.133.456-70"

    def test_post_cria_pj(self):
        client = TestClient(app)
        payload = {"tipo": "pj", "cnpj": "12.345.678/0001-90", "razao": "Empresa X Ltda",
                   "endereco": dict(CLIENTE_FULL["endereco"], cep="60115-001")}
        resp = client.post("/reclamados", json=payload)
        assert resp.status_code == 201
        assert resp.json()["reclamado"]["cnpj"] == "12.345.678/0001-90"

    def test_assistente_mascara_reclamado(self):
        from apps.api.src.auth.dependencies import current_user
        from apps.api.src.main import app as a
        a.dependency_overrides[current_user] = lambda: {"user_id": "y", "login": "z", "nome": "S", "role": "assistente"}
        try:
            client = TestClient(app)
            resp = client.post("/reclamados", json={
                "tipo": "pj", "cnpj": "12.345.678/0001-90", "razao": "Empresa X Ltda",
                "endereco": dict(CLIENTE_FULL["endereco"], cep="60115-001"),
            })
            assert resp.status_code == 201
            rr = resp.json()["reclamado"]
            assert "***" in rr["cnpj"]
        finally:
            a.dependency_overrides.pop(current_user, None)
