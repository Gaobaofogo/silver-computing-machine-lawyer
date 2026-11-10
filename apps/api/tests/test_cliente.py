import pytest
import uuid

from apps.api.src.schemas.cliente import ClienteSchema, EnderecoSchema
from apps.api.src.models.cliente import Cliente, EstadoCivil, StatusCliente, UF, Endereco


def payload_valido():
    return dict(
        nome_completo="João Silva",
        cpf="411.133.456-70",
        endereco={
            "logradouro": "Rua das Flores",
            "numero": "123",
            "bairro": "Centro",
            "cidade": "Fortaleza",
            "uf": "CE",
            "cep": "60010-000",
        },
        estado_civil="Casado",
    )


class TestClienteSchema:
    def test_cliente_pf_schema_completo(self):
        """ADR-0001: Cliente = PF; CPF + EstadoCivil + Endereco obrigatorios."""
        s = ClienteSchema(**payload_valido())
        assert s.nome_completo == "João Silva"
        assert s.cpf == "411.133.456-70"
        assert s.estado_civil.value == "Casado"
        assert s.endereco.uf.value == "CE"
        assert s.status.value == "Ativo"

    def test_cliente_rejeita_cnpj_removido_adr_0001(self):
        """CNPJ removido (ADR-0001): extra=forbid derruba tentativa."""
        with pytest.raises(ValueError):
            ClienteSchema(**{**payload_valido(), "cnpj": "12.345.678/0001-90"})


class TestModelCliente:
    def test_cliente_model_instancia(self):
        c = Cliente(**payload_valido())
        assert isinstance(c.cliente_id, uuid.UUID)
        assert c.estado_civil == EstadoCivil.CASADO
        assert c.status == StatusCliente.ATIVO
        assert c.endereco["logradouro"] == "Rua das Flores"

class TestEnderecoSchema:
    def test_endereco_schema_cep_minimo(self):
        with pytest.raises(ValueError):
            EnderecoSchema(
                logradouro="Rua X", numero="1", bairro="aa", cidade="aa",
                uf="CE", cep="aaa",
            )
