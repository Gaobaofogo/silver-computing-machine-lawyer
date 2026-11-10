"""Auditoria LGPD — tabela logs_acesso (ADR-0001, ADR-0007).

Registra todo acesso (read/write) a dados sensíveis com hora, IP, userId, role,
op, path. Não guarda conteúdo (CPF/CNPJ) — apenas metadados de acesso."""
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class LogsAcesso(SQLModel, table=True):
    __tablename__ = "logs_acesso"

    log_id: UUID = Field(default_factory=uuid4, primary_key=True)
    ts: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ip: str | None = Field(default=None, max_length=60)
    user_id: UUID | None = Field(default=None, index=True)
    role: str | None = Field(default=None, max_length=20)
    op: str = Field(max_length=10)
    path: str = Field(max_length=500)
    status_code: int | None = Field(default=None)
