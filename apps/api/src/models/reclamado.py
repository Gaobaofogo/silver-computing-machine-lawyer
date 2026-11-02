from sqlmodel import SQLModel, Field, String
from typing import Optional

class Reclamado(SQLModel, table=True):
    __tablename__ = "reclamados"
    id: int | None = Field(default=None, primary_key=True)
    tipo: str = Field(index=True)
    cpf: Optional[str] = Field(default=None, index=True)
    cnpj: Optional[str] = Field(default=None, index=True)
    razao: Optional[str] = None
