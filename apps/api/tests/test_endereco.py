import pytest
from apps.api.src.models.cliente import Endereco, UF


def endereco_valido():
    return dict(
        logradouro="Rua das Flores",
        numero="123",
        complemento=None,
        bairro="Centro",
        cidade="Fortaleza",
        uf=UF.CE,
        cep="60010-000",
    )


class TestEndereco:
    def test_endereco_valido_inicia(self):
        e = Endereco(**endereco_valido())
        assert e.logradouro == "Rua das Flores"
        assert e.numero == "123"
        assert e.complemento is None
        assert e.bairro == "Centro"
        assert e.cidade == "Fortaleza"
        assert e.uf == UF.CE
        assert e.cep == "60010-000"

    def test_cep_formato_8_ou_9_digitos(self):
        e = Endereco(**{**endereco_valido(), "cep": "60010000"})
        assert e.cep in ("60010000", "60010-000")

    def test_logradouro_minimo_3(self):
        with pytest.raises(ValueError):
            Endereco(**{**endereco_valido(), "logradouro": "ab"})

    def test_logradouro_maximo_200(self):
        with pytest.raises(ValueError):
            Endereco(**{**endereco_valido(), "logradouro": "x" * 201})

    def test_numero_minimo_1_maximo_10(self):
        with pytest.raises(ValueError):
            Endereco(**{**endereco_valido(), "numero": ""})
        with pytest.raises(ValueError):
            Endereco(**{**endereco_valido(), "numero": "x" * 11})

    def test_bairro_minimo_2_maximo_100(self):
        with pytest.raises(ValueError):
            Endereco(**{**endereco_valido(), "bairro": "a"})
        with pytest.raises(ValueError):
            Endereco(**{**endereco_valido(), "bairro": "x" * 101})

    def test_cidade_minimo_2_maximo_100(self):
        with pytest.raises(ValueError):
            Endereco(**{**endereco_valido(), "cidade": "a"})
        with pytest.raises(ValueError):
            Endereco(**{**endereco_valido(), "cidade": "x" * 101})

    def test_complemento_opcional(self):
        e = Endereco(**{**endereco_valido(), "complemento": "Apto 401"})
        assert e.complemento == "Apto 401"

    def test_uf_obrigatoria(self):
        with pytest.raises(ValueError):
            Endereco(**{**endereco_valido(), "uf": "EN"})
