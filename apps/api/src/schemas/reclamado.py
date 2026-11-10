from pydantic import BaseModel, field_validator, ConfigDict, Field, model_validator
from typing import Literal
import re

from apps.api.src.models.cliente import EstadoCivil
from apps.api.src.schemas.endereco import EnderecoSchema

CPF_REGEX = r"^(\d{3}\.\d{3}\.\d{3}-\d{2})$"
CNPJ_REGEX = r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"


class ReclamadoSchema(BaseModel):
    """Schema Pydantic — Reclamado (PF ou PJ, ADR-0001).

    Regra cross-field:
      - tipo="pf": cpf obrigatório e (CPF ou CNPJ ausente no payload)
      - tipo="pj": cnpj obrigatório e (CNPJ ou CPF ausente no payload)
    ``extra=forbid``. Só aceita EstadoCivil enum (opcional, apenas PF)."""
    model_config = ConfigDict(extra="forbid")

    tipo: Literal["pf", "pj"]
    cpf: str | None = Field(default=None)
    cnpj: str | None = Field(default=None)
    razao: str | None = Field(default=None, min_length=2, max_length=100)
    endereco: EnderecoSchema
    estado_civil: EstadoCivil | None = Field(default=None)
    telefone: str | None = Field(default=None, min_length=8, max_length=20)
    email: str | None = Field(default=None, min_length=5, max_length=120)
    observacao: str | None = Field(default=None, min_length=2, max_length=2000)

    @model_validator(mode="after")
    def cross_field_pf_pj(self):
        if self.tipo == "pf":
            if not self.cpf or not re.match(CPF_REGEX, self.cpf):
                raise ValueError("CPF obrigatorio para tipo=pf (ADR-0001)")
            if self.cnpj:
                raise ValueError("tipo=pf nao pode entregar CNPJ")
        if self.tipo == "pj":
            if not self.cnpj or not re.match(CNPJ_REGEX, self.cnpj):
                raise ValueError("CNPJ obrigatorio para tipo=pj (ADR-0001)")
            if self.cpf:
                raise ValueError("tipo=pj nao pode entregar CPF")
            if not self.razao:
                raise ValueError("razao obrigatoria para tipo=pj (ADR-0001)")
        return self

    @field_validator("estado_civil")
    @classmethod
    def validate_estado_civil(cls, v: EstadoCivil | None):
        if v is not None and not isinstance(v, EstadoCivil):
            raise ValueError("EstadoCivil fora dos valores do dominio")
        return v
