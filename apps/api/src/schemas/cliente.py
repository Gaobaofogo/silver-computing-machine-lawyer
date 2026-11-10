"""Schema Pydantic — Cliente (pessoa física, ADR-0001)."""
from pydantic import BaseModel, ConfigDict, Field, field_validator
import re

from apps.api.src.models.cliente import EstadoCivil, StatusCliente
from apps.api.src.schemas.endereco import EnderecoSchema

CPF_REGEX = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
CNPJ_REGEX = r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"

__all__ = ["ClienteSchema", "EnderecoSchema", "CPF_REGEX", "CNPJ_REGEX"]


class ClienteSchema(BaseModel):
    r"""Schema Pydantic — Cliente (pessoa física, ADR-0001).
    CPF obrigatório + formato \\d{3}\\.\\d{3}\\.\\d{3}-\\d{2},
    EstadoCivil por enum, extra=forbid (ADR-0001: CNPJ removido)."""
    model_config = ConfigDict(extra="forbid")

    nome_completo: str = Field(min_length=2, max_length=100)
    cpf: str
    telefone: str | None = Field(default=None, min_length=8, max_length=20)
    email: str | None = Field(default=None, min_length=5, max_length=120)
    endereco: EnderecoSchema
    estado_civil: EstadoCivil
    status: StatusCliente = Field(default=StatusCliente.ATIVO)
    observacao: str | None = Field(default=None, min_length=2, max_length=2000)

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        if not v:
            raise ValueError("CPF obrigatorio (ADR-0001)")
        if not re.match(CPF_REGEX, v):
            raise ValueError("CPF fora do pattern ^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$")
        return v

    @field_validator("estado_civil")
    @classmethod
    def validate_estado_civil(cls, v: EstadoCivil) -> EstadoCivil:
        if not isinstance(v, EstadoCivil):
            raise ValueError("EstadoCivil fora dos valores do dominio")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: StatusCliente) -> StatusCliente:
        if not isinstance(v, StatusCliente):
            raise ValueError("StatusCliente fora dos valores do dominio")
        return v

    @field_validator("observacao")
    @classmethod
    def validate_observacao(cls, v: str | None) -> str | None:
        if v is not None and (len(v.strip()) < 2 or len(v) > 2000):
            raise ValueError("observacao 2..2000 caracteres")
        return v
