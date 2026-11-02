from sqlmodel import SQLModel, Field
class Processo(SQLModel, table=True):
    __tablename__ = "processos"
    id: int | None = Field(default=None, primary_key=True)
    id_processo: str = Field(index=True)
    data_autua: str
    valor_causa: float = 0.0
    id_area: str
    id_rito: str
    id_reclamado: str
    observacoes: str | None = None
