"""Histórico: este arquivo era um stub (sintaxe inválida) de RED para ClienteSchema.
O campo `observacao` foi implementado no schema; aqui registramos o contrato verdadeiro."""
import pytest
from pydantic import ValidationError

from apps.api.src.schemas.cliente import ClienteSchema


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


class TestObservacaoCliente:
    def test_observacao_valida(self):
        s = ClienteSchema(**{**payload_valido(), "observacao": "Registro sensível"})
        assert s.observacao == "Registro sensível"

    def test_observacao_curta_rejeitada(self):
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "observacao": "x"})

    def test_observacao_vazia_rejeitada(self):
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "observacao": ""})
