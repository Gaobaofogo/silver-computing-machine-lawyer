from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Judis-Advocacia API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from apps.api.src.schemas.cliente import ClienteSchema

def validar_cliente_pf(cliente: ClienteSchema) -> ClienteSchema:
    """Seam: regra ADR-0001 — CPF obrigatorio (>=11 chars), EstadoCivil nao vazio."""
    if not cliente.cpf or len(cliente.cpf.strip()) < 11:
        raise ValueError("CPF do Cliente e obrigatorio (ADR-0001)")
    if not cliente.estado_civil or cliente.estado_civil.strip() == "":
        raise ValueError("EstadoCivil do Cliente e obrigatorio (ADR-0001)")
    return cliente

def mascara_cpf(cpf: str) -> str:
    """LGPD: mascara o CPF no retorno."""
    limpo = cpf.replace(".", "").replace("-", "").strip()
    if len(limpo) >= 11:
        return f"***.***.***-{limpo[-2:]}"
    return "***.***.***-**"

@app.post("/clientes")
def criar_cliente(cliente: ClienteSchema = Depends(validar_cliente_pf)):
    resp = cliente.model_dump()
    resp["cpf"] = mascara_cpf(resp["cpf"])  # LGPD
    return{"status":"criado","cliente":resp}

@app.get("/health")
def health():
    return {"status": "ok", "project": "judis-advocacia"}
