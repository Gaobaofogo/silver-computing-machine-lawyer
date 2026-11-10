import pytest
from pydantic import ValidationError

from apps.api.src.schemas.cliente import ClienteSchema
from apps.api.src.models.cliente import EstadoCivil, StatusCliente, Endereco, UF


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


def payload_sem_endereco():
    p = payload_valido()
    p["endereco"] = {
        "logradouro": "Rua das Flores",
        "numero": "123",
        "bairro": "Centro",
        "cidade": "Fortaleza",
        "uf": "CE",
        "cep": "60010-000",
    }
    return p


class TestClienteSchemaCompleto:
    def test_aceita_pf_com_endereco_e_estado_civil(self):
        s = ClienteSchema(**payload_valido())
        assert s.nome_completo == "João Silva"
        assert s.cpf == "411.133.456-70"
        assert s.estado_civil.value == "Casado"
        assert s.endereco.uf.value == "CE"
        assert s.status.value == "Ativo"

    def test_telefone_e_email_opcionais(self):
        s = ClienteSchema(**{**payload_valido(), "telefone": "(85) 98765-4321", "email": "joao@exemplo.com"})
        assert s.telefone == "(85) 98765-4321"
        assert s.email == "joao@exemplo.com"

    def test_cpf_regex(self):
        for bad in ["41113345670", "411.133.456-701", "411.133.456-7"]:
            with pytest.raises(ValidationError):
                ClienteSchema(**{**payload_valido(), "cpf": bad})

    def test_cpf_formato_valido_aceito(self):
        """O regex não valida checksum, apenas o formato (GLOSSARY/§2.1 — Cpf como VO; checksum fica no seam de integração)."""
        s = ClienteSchema(**{**payload_valido(), "cpf": "111.222.333-44"})
        assert s.cpf == "111.222.333-44"

    def test_estado_civil_enum(self):
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "estado_civil": "Solteira"})

    def test_status_enum(self):
        s = ClienteSchema(**{**payload_valido(), "status": "Inativo"})
        assert s.status.value == "Inativo"
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "status": "Inativooo"})

    def test_extra_forbid_cnpj_rejeitado(self):
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "cnpj": "12.345.678/0001-90"})

    def test_nome_completo_range(self):
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "nome_completo": "a"})
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "nome_completo": "x" * 101})

    def test_telefone_range(self):
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "telefone": "123"})
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "telefone": "x" * 21})

    def test_email_range(self):
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "email": "ab"})
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "email": "x" * 121})

    def test_observacao_range(self):
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "observacao": "x"})
        with pytest.raises(ValidationError):
            ClienteSchema(**{**payload_valido(), "observacao": "x" * 2001})

    def test_endereco_logradouro_range(self):
        base = payload_sem_endereco()
        base["endereco"]["logradouro"] = "ab"
        with pytest.raises(ValidationError):
            ClienteSchema(**base)

    def test_endereco_complemento_opcional(self):
        base = payload_sem_endereco()
        base["endereco"] = {**base["endereco"], "complemento": "Apto 401"}
        s = ClienteSchema(**base)
        assert s.endereco.complemento == "Apto 401"

    def test_endereco_uf_obrigatoria(self):
        base = payload_sem_endereco()
        base["endereco"]["uf"] = "EN"
        with pytest.raises(ValidationError):
            ClienteSchema(**base)
