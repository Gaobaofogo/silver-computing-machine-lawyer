"""Modelo SQLModel — Reclamado (PF/PJ cadastro). PK UUID + audit (ADR-0001 dual nature)."""
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel

from apps.api.src.models.cliente import Endereco


class Reclamado(SQLModel, table=True):
    __tablename__ = "reclamados"

    reclamado_id: UUID = Field(default_factory=uuid4, primary_key=True)
    tipo: str = Field(index=True)
    cpf: str | None = Field(default=None, index=True)
    cnpj: str | None = Field(default=None, index=True)
    razao: str | None = None
    endereco: Endereco = Field(sa_column=Column(JSON, nullable=False))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
