from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

app = FastAPI(title="Judis-Advocacia API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from apps.api.src.schemas.cliente import ClienteSchema
from apps.api.src.schemas.processo import MovimentoProcessualSchema, ProcessoSchema
from apps.api.src.schemas.reclamado import ReclamadoSchema
from apps.api.src.infra.database import (
    create_movimento, create_processo, delete_processo, get_db, get_processo, list_movimentos,
    movimento_to_dict, processo_to_dict, update_processo,
)
from apps.api.src.models.cliente import StatusCliente  # exposto para testes
from apps.api.src.utils.lgpd_mask import mascara_cpf, mascara_cnpj, mascara_reclamado


@app.post("/clientes", status_code=201)
def criar_cliente(cliente: ClienteSchema):
    """ADR-0001: Cliente = PF com CPF + EstadoCivil + Endereco obrigatorios."""
    resp = cliente.model_dump(mode="json")
    resp["cpf"] = mascara_cpf(resp["cpf"])  # LGPD
    return {"status": "criado", "cliente": resp}

@app.get("/clientes/{id}")
def consultar_cliente(id: int):
    return {"status": "consultado", "cliente": {"id": id, "cpf": "***.***.***-**"}}

@app.put("/clientes/{id}")
def atualizar_cliente(id: int, cliente: ClienteSchema):
    resp = cliente.model_dump(mode="json")
    resp["cpf"] = mascara_cpf(resp["cpf"])  # LGPD
    return {"status": "atualizado", "cliente": {**resp, "id": id}}

@app.delete("/clientes/{cpf}")
def deletar_cliente(cpf: str):
    return {"status": "deletado", "cpf": mascara_cpf(cpf)}

# Rotas Reclamado
@app.post("/reclamados", status_code=201)
def criar_reclamado(r: ReclamadoSchema):
    """ADR-0001: Reclamado PF/PJ; CNPJ mascarado na resposta LGPD."""
    resp = r.model_dump(mode="json")
    resp = mascara_reclamado(resp)
    return {"status": "criado", "reclamado": resp}

@app.get("/reclamados/{id}")
def consultar_reclamado(id: str):
    return {"status": "consultado", "reclamado": {"id": id, "tipo": "***", "cpf": "***.***.***-**", "cnpj": "***.***.***/***-**"}}

@app.put("/reclamados/{id}")
def atualizar_reclamado(id: str, r: ReclamadoSchema):
    resp = r.model_dump(mode="json")
    resp = mascara_reclamado(resp)
    return {"status": "atualizado", "reclamado": {**resp, "id": id}}

@app.delete("/reclamados/{id}")
def deletar_reclamado(id: str):
    return {"status": "deletado", "reclamado": {"id": id}}

# Rotas Processo
@app.post("/processos", status_code=201)
def criar_processo(p: ProcessoSchema, db: Session = Depends(get_db)):
    """Processo (raiz do agregado). observacao logada; id_area/id_rito via enums."""
    row = create_processo(db, p)
    return {"status": "criado", "processo": {**processo_to_dict(row), "id": row.processo_id}}

@app.get("/processos/{id}")
def consultar_processo(id: str, db: Session = Depends(get_db)):
    row = get_processo(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="processo nao encontrado")
    return {"status": "consultado", "processo": {**processo_to_dict(row), "id": row.processo_id}}

@app.put("/processos/{id}")
def atualizar_processo(id: str, p: ProcessoSchema, db: Session = Depends(get_db)):
    row = update_processo(db, id, p)
    if row is None:
        raise HTTPException(status_code=404, detail="processo nao encontrado")
    return {"status": "atualizado", "processo": {**processo_to_dict(row), "id": row.processo_id}}

@app.delete("/processos/{id}")
def deletar_processo(id: str, db: Session = Depends(get_db)):
    ok = delete_processo(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="processo nao encontrado")
    return {"status": "deletado", "processo": {"id": id}}

# Rotas MovimentoProcessual — encadeamento máquina de estados (GLOSSARY 4.1.3)
@app.post("/movimentos", status_code=201)
def criar_movimento(m: MovimentoProcessualSchema, db: Session = Depends(get_db)):
    from apps.api.src.models.processo import Processo as _ProcModel, StatusProcesso as _SP
    from apps.api.src.services.processo import transicionar_status
    payload = MovimentoProcessualSchema.model_validate(m.model_dump())
    proc = get_processo(db, str(payload.processo_id))
    if proc is None:
        raise HTTPException(status_code=404, detail="processo nao encontrado")
    if payload.status_novo is not None:
        try:
            target = transicionar_status(proc.status, payload.status_novo)
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc))
        if target != proc.status:
            proc.status = target
            from datetime import datetime as _dt
            proc.updated_at = _dt.now().astimezone()
    row = create_movimento(db, payload)
    return {"status": "criado", "movimento": {**movimento_to_dict(row), "id": row.movimento_id}}

@app.get("/movimentos")
def listar_movimentos(processo_id: str | None = None, db: Session = Depends(get_db)):
    rows = list_movimentos(db, processo_id)
    return {"status": "listado", "movimentos": [movimento_to_dict(r) for r in rows]}

@app.get("/health")
def health():
    return {"status": "ok", "project": "judis-advocacia"}
