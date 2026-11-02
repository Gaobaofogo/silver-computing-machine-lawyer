from pydantic import BaseModel, field_validator, ConfigDict
from typing import Literal
import re

CPF_REGEX = r"^(\d{3}\.\d{3}\.\d{3}-\d{2})$"
CNPJ_REGEX = r"^[A-Z0-9]{2}\.[A-Z0-9]{3}\.[A-Z0-9]{3}/[A-Z0-9]{4}-\d{2}$"

class ReclamadoSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tipo: Literal["pf", "pj"]
    cpf: str | None = None
    cnpj: str | None = None
    razao: str | None = None
    estado_civil: str | None = None

    @field_validator("tipo")
    @classmethod
    def validate_tipo(cls, v: str):
        if v not in ("pf", "pj"):
            raise ValueError("tipo deve ser 'pf' ou 'pj'")
        return v

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str | None, info):
        if info.data.get("tipo") == "pf" and (not v or not re.match(CPF_REGEX, v)):
            raise ValueError("CPF obrigatorio para PF")
        return v

    @field_validator("cnpj")
    @classmethod
    def validate_cnpj(cls, v: str | None, info):
        if info.data.get("tipo") == "pj" and (not v or not re.match(CNPJ_REGEX, v)):
            raise ValueError("CNPJ obrigatorio para PJ")
        return v
