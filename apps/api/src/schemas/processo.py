from pydantic import BaseModel, ConfigDict, Field, field_validator
from decimal import Decimal
from typing import Optional
from datetime import date
from uuid import UUID

from apps.api.src.domain.value_objects import NumeroProcesso
from apps.api.src.models.processo import Area, Rito, StatusProcesso

__all__ = ["ProcessoSchema", "MovimentoProcessualSchema", "Area", "Rito", "StatusProcesso"]


class ProcessoSchema(BaseModel):
    """Processo (raiz do agregado). ADR-0001, GLOSSARY 4.1.1."""
    model_config = ConfigDict(extra="forbid")

    id_cliente: UUID
    id_reclamado: UUID
    numero_processo: str = Field(min_length=25, max_length=25,
                               pattern=(r"^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$"))
    data_autua: Optional[date] = None
    valor_causa: Decimal = Field(ge=Decimal("0.00"), le=Decimal("99999999.99"))

    @field_validator("valor_causa")
    @classmethod
    def validate_valor_causa_dp(cls, v: Decimal) -> Decimal:
        if v.as_tuple().exponent < -2:
            raise ValueError("valor_causa com mais de 2 casas decimais")
        return v.quantize(Decimal("0.01"))

    @field_validator("numero_processo")
    @classmethod
    def validate_numero_cnj(cls, v: str) -> str:
        return NumeroProcesso(v).valor
    id_area: Area
    id_rito: Rito
    status: StatusProcesso = Field(default=StatusProcesso.CADASTRADO)
    observacao: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("observacao")
    @classmethod
    def validate_observacao(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (len(v.strip()) < 2 or len(v) > 2000):
            raise ValueError("observacao 2..2000 caracteres")
        return v


class MovimentoProcessualSchema(BaseModel):
    """MovimentoProcessual — entidade interna ao agregado Processo.

    Glossário 4.1.1: subordinated não raiz independente."""
    model_config = ConfigDict(extra="forbid")

    processo_id: UUID
    data_movimento: date
    tipo: str = Field(min_length=2, max_length=50)
    descricao: Optional[str] = Field(default=None, min_length=2, max_length=2000)
    status_anterior: Optional[StatusProcesso] = None
    status_novo: Optional[StatusProcesso] = None

    @field_validator("descricao")
    @classmethod
    def validate_descricao(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (len(v.strip()) < 2 or len(v) > 2000):
            raise ValueError("descricao 2..2000 caracteres")
        return v
