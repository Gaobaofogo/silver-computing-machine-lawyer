from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProcessoSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id_processo: str
    data_autua: str
    valor_causa: float = 0.0
    id_area: str
    id_rito: str
    id_reclamado: str
    observacoes: Optional[str] = None
