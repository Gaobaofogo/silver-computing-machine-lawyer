"""Modelo Auth — User e Role (ADR-0006/0007).

- Role: advogado (acesso completo, exceto gestão de usuários), assistente (sem valor_causa), admin (tudo).
- Administrador no UI, role code `admin` no banco/JWT — convenção ADR-0001."""
from datetime import datetime, timezone
import enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Role(str, enum.Enum):
    ADVOGADO = "advogado"
    ASSISTENTE = "assistente"
    ADMIN = "admin"


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: UUID = Field(default_factory=uuid4, primary_key=True)
    login: str = Field(min_length=3, max_length=80, unique=True, index=True)
    nome: str = Field(min_length=2, max_length=120)
    role: Role
    senha_hash: str = Field(min_length=60, max_length=200)  # bcrypt digest ~60 chars
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
