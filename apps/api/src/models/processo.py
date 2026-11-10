from decimal import Decimal
from datetime import date, datetime, timezone
from uuid import UUID, uuid4
import enum
from typing import Optional

from sqlmodel import SQLModel, Field


class Area(str, enum.Enum):
    TRABALHISTA = "Trabalhista"
    CIVEL = "Civel"
    PREVIDENCIARIO = "Previdenciario"
    TRIBUTARIO = "Tributario"
    PENAL = "Penal"


class Rito(str, enum.Enum):
    ORDINARIO = "Ordinario"
    SUMARIO = "Sumario"
    ESPECIAL = "Especial"


class StatusProcesso(str, enum.Enum):
    CADASTRADO = "Cadastrado"
    EM_ANDAMENTO = "Em Andamento"
    CONCLUIDO = "Concluido"
    ARQUIVADO = "Arquivado"


class MovimentoProcessual(SQLModel, table=True):
    """Movimento processual — entidade interna ao agregado Processo."""

    __tablename__ = "movimentos_processuais"

    movimento_id: UUID = Field(default_factory=uuid4, primary_key=True)
    processo_id: UUID = Field(index=True)
    data_movimento: date
    tipo: str = Field(min_length=2, max_length=50)
    descricao: str | None = Field(default=None, min_length=2, max_length=2000)
    status_anterior: StatusProcesso | None = Field(default=None)
    status_novo: StatusProcesso | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )


class Processo(SQLModel, table=True):
    __tablename__ = "processos"

    processo_id: UUID = Field(default_factory=uuid4, primary_key=True)
    id_cliente: UUID = Field(index=True)
    id_reclamado: UUID = Field(index=True)
    numero_processo: str = Field(min_length=2, max_length=30, index=True)
    data_autua: Optional[date] = None
    valor_causa: Decimal = Field(default=Decimal("0.00"), max_digits=10, decimal_places=2)
    id_area: Area = Field()
    id_rito: Rito = Field()
    status: StatusProcesso = Field(default=StatusProcesso.CADASTRADO)
    observacao: Optional[str] = Field(default=None, min_length=2, max_length=2000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
