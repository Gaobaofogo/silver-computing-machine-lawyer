from pydantic import BaseModel, field_validator, ConfigDict
import re

CPF_REGEX = r"^(\d{3}\.\d{3}\.\d{3}-\d{2})$"
CNPJ_REGEX = r"^[A-Z0-9]{2}\.[A-Z0-9]{3}\.[A-Z0-9]{3}/[A-Z0-9]{4}-\d{2}$"

class ClienteSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")  # ADR-0001: rejeita CNPJ removido
    nome: str
    cpf: str
    estado_civil: str
    observacoes: str | None = None

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        if not v or len(v.strip()) < 11:
            raise ValueError("CPF obrigatorio (ADR-0001)")
        if not re.match(CPF_REGEX, v):
            raise ValueError("CPF fora do pattern ^(\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2})$")
        return v

    @field_validator("estado_civil")
    @classmethod
    def validate_estado_civil(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("EstadoCivil obrigatorio (ADR-0001)")
        return v
