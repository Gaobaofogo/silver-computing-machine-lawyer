import pytest
from apps.api.src.models.cliente import EstadoCivil, StatusCliente, UF


class TestEstadoCivilEnum:
    def test_valores_validos(self):
        expected = {
            "SOLTEIRO": "Solteiro",
            "CASADO": "Casado",
            "DIVORCIADO": "Divorciado",
            "VIUVO": "Viúvo",
            "SEPARADO_JUDICIALMENTE": "Separado Judicialmente",
        }
        for name, value in expected.items():
            member = getattr(EstadoCivil, name)
            assert member.name == name
            assert member.value == value

    def test_nao_aceita_texto_livre(self):
        assert not hasattr(EstadoCivil, "SOLTEIRA")
        with pytest.raises(ValueError):
            EstadoCivil("Solu")


class TestStatusClienteEnum:
    def test_valores_validos(self):
        expected = {
            "ATIVO": "Ativo",
            "INATIVO": "Inativo",
            "BLOQUEADO": "Bloqueado",
        }
        for name, value in expected.items():
            member = getattr(StatusCliente, name)
            assert member.name == name
            assert member.value == value

    def test_nao_aceita_texto_livre(self):
        with pytest.raises(ValueError):
            StatusCliente("BLOQUEADOS")


class TestUFEnum:
    def test_valores_validos(self):
        ufs = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA",
               "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN",
               "RO", "RR", "RS", "SC", "SP", "SE", "TO"]
        for uf in ufs:
            member = getattr(UF, uf)
            assert member.name == uf
            assert member.value == uf

    def test_27_unidades_federativas(self):
        assert len(list(UF)) == 27

    def test_nao_aceita_texto_livre(self):
        with pytest.raises(ValueError):
            UF("EN")
