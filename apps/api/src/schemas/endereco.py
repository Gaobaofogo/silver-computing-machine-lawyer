"""Shared `EnderecoSchema` reused by ClienteSchema and ReclamadoSchema."""
from pydantic import BaseModel, ConfigDict, Field
from apps.api.src.models.cliente import UF


class EnderecoSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    logradouro: str = Field(min_length=3, max_length=200)
    numero: str = Field(min_length=1, max_length=10)
    complemento: str | None = Field(default=None, max_length=100)
    bairro: str = Field(min_length=2, max_length=100)
    cidade: str = Field(min_length=2, max_length=100)
    uf: UF
    cep: str = Field(min_length=8, max_length=9)
