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

from apps.api.src.schemas.reclamado import ReclamadoSchema
from apps.api.src.schemas.processo import ProcessoSchema

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

# Rotas Cliente
@app.get("/clientes/{id}")
def consultar_cliente(id: int):
    return {"status":"consultado","cliente":{"id":id,"cpf":"***.***.***-**"}}

@app.put("/clientes")
def atualizar_cliente(cliente: ClienteSchema = Depends(validar_cliente_pf)):
    return {"status":"atualizado","cliente":cliente.model_dump()}

@app.delete("/clientes/{cpf}")
def deletar_cliente(cpf: str):
    return {"status":"deletado","cpf":mascara_cpf(cpf)}

# Rotas Reclamado
@app.post("/reclamados")
def criar_reclamado(r: ReclamadoSchema):
    return{"status":"criado","reclamado":r.model_dump()}

@app.get("/reclamados/{tipo}/{id}")
def consultar_reclamado(tipo: str, id: str):
    return{"status":"consultado","reclamado":{"tipo":tipo,"id":id}}

@app.put("/reclamados")
def atualizar_reclamado(r: ReclamadoSchema):
    return{"status":"atualizado","reclamado":r.model_dump()}

@app.delete("/reclamados/{tipo}/{id}")
def deletar_reclamado(tipo: str, id: str):
    return{"status":"deletado","tipo":tipo,"id":id}

# Rotas Processo
@app.post("/processos")
def criar_processo(p: ProcessoSchema):
    return{"status":"criado","processo":p.model_dump()}

@app.get("/processos/{id_processo}")
def consultar_processo(id_processo: str):
    return{"status":"consultado","processo":{"id_processo":id_processo}}

@app.put("/processos")
def atualizar_processo(p: ProcessoSchema):
    return{"status":"atualizado","processo":p.model_dump()}

@app.delete("/processos/{id_processo}")
def deletar_processo(id_processo: str):
    return{"status":"deletado","id_processo":id_processo}

@app.get("/health")
def health():
    return {"status": "ok", "project": "judis-advocacia"}
