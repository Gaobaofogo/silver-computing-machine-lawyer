from sqlmodel import SQLModel, Field, String

class Cliente(SQLModel, table=True):
    __tablename__ = "clientes"

    id: int | None = Field(default=None, primary_key=True)
    nome: str
    cpf: str = Field(index=True)
    estado_civil: str
    observacoes: str | None = None
