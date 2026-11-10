"""Tickets 05 + 08: Schema Reclamado completo."""
import pytest
from pydantic import ValidationError

from apps.api.src.schemas.reclamado import ReclamadoSchema
from apps.api.src.schemas.endereco import EnderecoSchema
from apps.api.src.models.cliente import EstadoCivil, UF


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
        estado_civil=EstadoCivil.CASADO,
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


class TestSchemaReclamadoCompleto:
    def test_pf_minimo_valido(self):
        s = ReclamadoSchema(**payload_pf())
        assert s.tipo == "pf"
        assert s.cpf == "411.133.456-70"
        assert s.estado_civil.value == "Casado"
        assert s.endereco.uf.value == "CE"

    def test_pj_minimo_valido(self):
        s = ReclamadoSchema(**payload_pj())
        assert s.tipo == "pj"
        assert s.cnpj == "12.345.678/0001-90"
        assert s.razao == "Empresa X Ltda"

    def test_pf_rejeita_cnpj(self):
        with pytest.raises(ValidationError):
            ReclamadoSchema(**{**payload_pf(), "cnpj": "12.345.678/0001-90"})

    def test_pj_rejeita_cpf(self):
        with pytest.raises(ValidationError):
            ReclamadoSchema(**{**payload_pj(), "cpf": "411.133.456-70"})

    def test_pj_exige_razao(self):
        p = payload_pj()
        p.pop("razao")
        with pytest.raises(ValidationError):
            ReclamadoSchema(**p)

    def test_endereco_uf_invalida(self):
        p = payload_pf()
        p["endereco"]["uf"] = "EN"
        with pytest.raises(ValidationError):
            ReclamadoSchema(**p)

    def test_endereco_logradouro_minimo(self):
        p = payload_pf()
        p["endereco"]["logradouro"] = "ab"
        with pytest.raises(ValidationError):
            ReclamadoSchema(**p)

    def test_endereco_logradouro_max(self):
        p = payload_pf()
        p["endereco"]["logradouro"] = "x" * 201
        with pytest.raises(ValidationError):
            ReclamadoSchema(**p)

    def test_extra_forbid(self):
        with pytest.raises(ValidationError):
            ReclamadoSchema(**{**payload_pf(), "odd": "xx"})

    def test_cpf_formato(self):
        for bad in ["41113345670", "411.133.456-701"]:
            with pytest.raises(ValidationError):
                ReclamadoSchema(**{**payload_pf(), "cpf": bad})

    def test_cnpj_formato(self):
        for bad in ["12345678000190", "12.345.678/0001-901"]:
            with pytest.raises(ValidationError):
                ReclamadoSchema(**{**payload_pj(), "cnpj": bad})

    def test_estado_civil_enum_invalido(self):
        with pytest.raises(ValidationError):
            ReclamadoSchema(**{**payload_pf(), "estado_civil": "Solteira"})

    def test_complemento_opcional(self):
        s = ReclamadoSchema(**{**payload_pf(), "endereco": {**payload_pf()["endereco"], "complemento": "não"}})
        assert s.endereco.complemento == "não"

    def test_telefone_email_opcionais(self):
        s = ReclamadoSchema(**{**payload_pf(), "telefone": "(85) 98765-4321", "email": "a@b.com"})
        assert s.telefone == "(85) 98765-4321"


class TestEnderecoSchema:
    def test_cep_minimo(self):
        with pytest.raises(ValidationError):
            EnderecoSchema(logradouro="Rua X", numero="1", bairro="aa", cidade="aa", uf="CE", cep="aaa")
