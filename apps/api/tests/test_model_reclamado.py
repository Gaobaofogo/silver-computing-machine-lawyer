"""Tickets 05: Modelo Reclamado completo."""
import pytest
from datetime import datetime
from uuid import UUID

from apps.api.src.models.reclamado import Reclamado


def payload_pf():
    return dict(
        tipo="pf",
        cpf="411.133.456-70",
        endereco={
            "logradouro": "Rua das Flores",
            "numero": "123",
            "bairro": "Centro",
            "cidade": "Fortaleza",
            "uf": "CE",
            "cep": "60010-000",
        },
    )


def payload_pj():
    return dict(
        tipo="pj",
        cnpj="12.345.678/0001-90",
        razao="Empresa X Ltda",
        endereco={
            "logradouro": "Av. Bezerra de Menezes",
            "numero": "1234",
            "bairro": "Aldeota",
            "cidade": "Fortaleza",
            "uf": "CE",
            "cep": "60115-001",
        },
    )


class TestModeloReclamado:
    def test_uuid_pk(self):
        r = Reclamado(**payload_pf())
        assert isinstance(r.reclamado_id, UUID)

    def test_defaults_audit(self):
        r = Reclamado(**payload_pf())
        assert isinstance(r.created_at, datetime)
        assert isinstance(r.updated_at, datetime)

    def test_ddl_not_null_obrigatoria(self):
        table = Reclamado.__table__
        cols = {c.name: c for c in table.columns}
        assert cols["tipo"].nullable is False
        assert cols["endereco"].nullable is False

    def test_uuid_pk_pj_audit(self):
        r = Reclamado(**payload_pj())
        assert isinstance(r.reclamado_id, UUID)
        assert r.razao == "Empresa X Ltda"

    def test_endereco_embedded_dict(self):
        r = Reclamado(**payload_pf())
        assert isinstance(r.endereco, dict)
        assert r.endereco["uf"] == "CE"
