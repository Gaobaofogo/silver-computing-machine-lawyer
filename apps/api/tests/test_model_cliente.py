import pytest
from datetime import datetime
from uuid import UUID

from apps.api.src.models.cliente import Cliente, EstadoCivil, StatusCliente, UF


def cliente_valido():
    """Endereço embutido como dict (mesmo formato armazenado na coluna JSON)."""
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
        estado_civil=EstadoCivil.CASADO,
    )


class TestModeloCliente:
    def test_instancia_com_uuid_pk(self):
        c = Cliente(**cliente_valido())
        assert isinstance(c.cliente_id, UUID)

    def test_defaults_status_e_auditoria(self):
        c = Cliente(**cliente_valido())
        assert c.status == StatusCliente.ATIVO
        assert isinstance(c.created_at, datetime)
        assert isinstance(c.updated_at, datetime)
        assert c.observacao is None
        assert c.telefone is None
        assert c.email is None

    def test_model_ddl_preserva_nullable_false(self):
        """table=True silencia missing para None; presença real = DDL NOT NULL (ticket 04/schema)."""
        from sqlalchemy import inspect
        table = Cliente.__table__
        cols = {col.name: col for col in table.columns}
        assert cols["nome_completo"].nullable is False
        assert cols["cpf"].nullable is False
        assert cols["estado_civil"].nullable is False
        assert cols["endereco"].nullable is False

    def test_endereco_embedded_como_dict(self):
        """SQLModel table=True guarda o JSON puro; a camada schema materializa Endereco."""
        c = Cliente(**cliente_valido())
        assert isinstance(c.endereco, dict)
        assert c.endereco["logradouro"] == "Rua das Flores"
        assert c.endereco["uf"] == "CE"

    def test_estado_civil_aceita_membro_enum(self):
        c = Cliente(**{**cliente_valido(), "estado_civil": EstadoCivil.SOLTEIRO})
        assert c.estado_civil == EstadoCivil.SOLTEIRO

    def test_campos_opcionais_aceitos(self):
        c = Cliente(**{
            **cliente_valido(),
            "telefone": "(85) 98765-4321",
            "email": "joao@exemplo.com",
            "observacao": "Cliente em conciliação",
        })
        assert c.telefone == "(85) 98765-4321"
        assert c.email == "joao@exemplo.com"
        assert c.observacao == "Cliente em conciliação"
