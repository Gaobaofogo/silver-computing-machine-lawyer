from datetime import datetime, timezone
import enum
from uuid import UUID, uuid4
from pydantic import model_validator
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class EstadoCivil(str, enum.Enum):
    SOLTEIRO = "Solteiro"
    CASADO = "Casado"
    DIVORCIADO = "Divorciado"
    VIUVO = "Viúvo"
    SEPARADO_JUDICIALMENTE = "Separado Judicialmente"


class StatusCliente(str, enum.Enum):
    ATIVO = "Ativo"
    INATIVO = "Inativo"
    BLOQUEADO = "Bloqueado"


class UF(str, enum.Enum):
    AC = "AC"; AL = "AL"; AM = "AM"; AP = "AP"; BA = "BA"
    CE = "CE"; DF = "DF"; ES = "ES"; GO = "GO"; MA = "MA"
    MG = "MG"; MS = "MS"; MT = "MT"; PA = "PA"; PB = "PB"
    PE = "PE"; PI = "PI"; PR = "PR"; RJ = "RJ"; RN = "RN"
    RO = "RO"; RR = "RR"; RS = "RS"; SC = "SC"; SP = "SP"
    SE = "SE"; TO = "TO"


class Endereco(SQLModel):
    logradouro: str = Field(min_length=3, max_length=200)
    numero: str = Field(min_length=1, max_length=10)
    complemento: str | None = Field(default=None, max_length=100)
    bairro: str = Field(min_length=2, max_length=100)
    cidade: str = Field(min_length=2, max_length=100)
    uf: UF
    cep: str = Field(min_length=8, max_length=9)


class Cliente(SQLModel, table=True):
    __tablename__ = "clientes"

    cliente_id: UUID = Field(default_factory=uuid4, primary_key=True)
    nome_completo: str = Field(min_length=2, max_length=100)
    cpf: str = Field(index=True)
    telefone: str | None = Field(default=None, min_length=8, max_length=20)
    email: str | None = Field(default=None, min_length=5, max_length=120)
    endereco: Endereco = Field(sa_column=Column(JSON, nullable=False))
    estado_civil: EstadoCivil
    status: StatusCliente = Field(default=StatusCliente.ATIVO)
    observacao: str | None = Field(default=None, min_length=2, max_length=2000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

    @model_validator(mode="after")
    def _validar_campos(self):
        if self.estado_civil is None:
            raise ValueError("estado_civil obrigatorio")
        if not isinstance(self.estado_civil, EstadoCivil):
            raise ValueError("estado_civil deve ser um valor enum")
        return self
