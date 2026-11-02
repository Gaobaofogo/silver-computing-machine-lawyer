from pydantic import BaseModel, field_validator, ConfigDict

class ClienteSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")  # ADR-0001: rejeita CNPJ removido
    nome: str
    cpf: str
    estado_civil: str

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        if not v or len(v.strip()) < 11:
            raise ValueError("CPF obrigatorio (ADR-0001)")
        return v

    @field_validator("estado_civil")
    @classmethod
    def validate_estado_civil(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("EstadoCivil obrigatorio (ADR-0001)")
        return v
