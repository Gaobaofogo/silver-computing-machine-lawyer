import pytest
from decimal import Decimal
from apps.api.src.models.processo import Area, Rito, StatusProcesso
from apps.api.src.schemas.processo import ProcessoSchema
from apps.api.src.models.processo import Processo
from datetime import date, datetime
from uuid import UUID


class TestAreaEnum:
    def test_valores_validos(self):
        expected = {
            "TRABALHISTA": "Trabalhista",
            "CIVEL": "Civel",
            "PREVIDENCIARIO": "Previdenciario",
            "TRIBUTARIO": "Tributario",
            "PENAL": "Penal",
        }
        for name, value in expected.items():
            member = getattr(Area, name)
            assert member.name == name
            assert member.value == value

    def test_nao_aceita_texto_livre(self):
        with pytest.raises(ValueError):
            Area("TRABALHETANO")


class TestRitoEnum:
    def test_valores_validos(self):
        expected = {
            "ORDINARIO": "Ordinario",
            "SUMARIO": "Sumario",
            "ESPECIAL": "Especial",
        }
        for name, value in expected.items():
            member = getattr(Rito, name)
            assert member.name == name
            assert member.value == value

    def test_nao_aceita_texto_livre(self):
        with pytest.raises(ValueError):
            Rito("Ordinar")


class TestStatusProcessoEnum:
    def test_valores_validos(self):
        expected = {
            "CADASTRADO": "Cadastrado",
            "EM_ANDAMENTO": "Em Andamento",
            "CONCLUIDO": "Concluido",
            "ARQUIVADO": "Arquivado",
        }
        for name, value in expected.items():
            member = getattr(StatusProcesso, name)
            assert member.name == name
            assert member.value == value

    def test_nao_aceita_texto_livre(self):
        with pytest.raises(ValueError):
            StatusProcesso("INDEFINIDO")


_PAYLOAD_AREA_CIVEL = "Civel"


def payload_base():
    from uuid import uuid4
    return {
        "id_cliente": str(uuid4()),
        "id_reclamado": str(uuid4()),
        "numero_processo": "0001234-56.2026.8.06.0001",
        "data_autua": "2026-11-09",
        "valor_causa": Decimal("12345.67"),
        "id_area": "Civel",
        "id_rito": "Ordinario",
        "status": "Cadastrado",
    }


class TestProcessoSchema:
    def test_valido(self):
        s = ProcessoSchema(**payload_base())
        assert s.id_area.value == "Civel"
        assert s.id_rito.value == "Ordinario"
        assert s.status.value == "Cadastrado"

    def test_numero_processo_range(self):
        p = payload_base()
        p["numero_processo"] = ""
        with pytest.raises(Exception):
            ProcessoSchema(**p)
        p["numero_processo"] = "x" * 31
        with pytest.raises(Exception):
            ProcessoSchema(**p)

    def test_valor_causa_range(self):
        p = payload_base()
        p["valor_causa"] = -1
        with pytest.raises(Exception):
            ProcessoSchema(**p)
        p["valor_causa"] = 100_000_000.00
        with pytest.raises(Exception):
            ProcessoSchema(**p)

    def test_nested_check_literal_only(self):
        p = payload_base()
        p["id_area"] = "NaoArea"
        with pytest.raises(Exception):
            ProcessoSchema(**p)
        p["id_rito"] = "NaoRito"
        with pytest.raises(Exception):
            ProcessoSchema(**p)

    def test_observacao_max(self):
        p = payload_base()
        p["status"] = "Cadastrado"
        p["observacao"] = "a" * 2001
        with pytest.raises(Exception):
            ProcessoSchema(**p)

    def test_extra_forbid(self):
        p = payload_base()
        p["odd_extra"] = "bs"
        with pytest.raises(Exception):
            ProcessoSchema(**p)


class TestProcessoModel:
    def test_uuid_pk_audit(self):
        r = Processo(**{
            "id_cliente": UUID(payload_base()["id_cliente"]),
            "id_reclamado": UUID(payload_base()["id_reclamado"]),
            "numero_processo": "0001234-56.2026.8.06.0001",
            "data_autua": date(2026, 11, 9),
            "valor_causa": Decimal("12345.67"),
            "id_area": Area.CIVEL,
            "id_rito": Rito.ORDINARIO,
            "status": StatusProcesso.CADASTRADO,
        })
        assert isinstance(r.processo_id, UUID)
        assert isinstance(r.created_at, datetime)
        assert isinstance(r.updated_at, datetime)

    def test_defaults_status(self):
        r = Processo(**{
            "id_cliente": UUID(payload_base()["id_cliente"]),
            "id_reclamado": UUID(payload_base()["id_reclamado"]),
            "numero_processo": "0001234-56.2026.8.06.0001",
            "data_autua": date(2026, 11, 9),
            "valor_causa": Decimal("100.00"),
            "id_area": Area.CIVEL,
            "id_rito": Rito.ORDINARIO,
        })
        assert r.status == StatusProcesso.CADASTRADO

    def test_ddl_not_null(self):
        table = Processo.__table__
        cols = {c.name: c for c in table.columns}
        assert cols["numero_processo"].nullable is False
        assert cols["id_area"].nullable is False
        assert cols["id_rito"].nullable is False
        assert cols["status"].nullable is False

    def test_data_autua_opcional(self):
        r = Processo(**{
            "id_cliente": UUID(payload_base()["id_cliente"]),
            "id_reclamado": UUID(payload_base()["id_reclamado"]),
            "numero_processo": "0001234-56.2026.8.06.0001",
            "valor_causa": Decimal("100.00"),
            "id_area": Area.CIVEL,
            "id_rito": Rito.ORDINARIO,
        })
        assert r.data_autua is None


class TestObservacaoRange:
    def test_max_length(self):
        p = payload_base()
        p["observacao"] = "x" * 2000
        ProcessoSchema(**p)  # deve passar
        p["observacao"] = "x" * 2001
        with pytest.raises(Exception):
            ProcessoSchema(**p)
