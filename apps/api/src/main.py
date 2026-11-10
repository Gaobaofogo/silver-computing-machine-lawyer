import os
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
    create_cliente, delete_cliente, get_cliente, update_cliente,
    create_reclamado, delete_reclamado, get_reclamado, update_reclamado,
    cliente_to_dict, reclamado_to_dict,
    movimento_to_dict, processo_to_dict, update_processo,
)
from apps.api.src.models.cliente import StatusCliente  # exposto para testes
from apps.api.src.models.auth import Role as UserRole
from apps.api.src.auth.dependencies import require_role, current_user
from apps.api.src.models.processo import Processo
from apps.api.src.middleware.lgpd_audit import LGPDAuditMiddleware
from apps.api.src.services.auth import (
    decode_token, encode_token, get_user_by_login, hash_password, verify_password,
)
from fastapi import Request
from fastapi.responses import JSONResponse
from apps.api.src.utils.lgpd_mask import mascara_cpf, mascara_cnpj, mascara_reclamado


app.add_middleware(LGPDAuditMiddleware)


# Rotas Cliente — requer auth; assistente vede CPF pseudonimizado
@app.post("/clientes", status_code=201, dependencies=[Depends(require_role("advogado", "assistente", "admin"))])
def criar_cliente(cliente: ClienteSchema, user=Depends(current_user), db: Session = Depends(get_db)):
    """ADR-0001: Cliente sempre PF; CPF via middleware LGPD."""
    row = create_cliente(db, cliente)
    body = {"status": "criado", "cliente": {**cliente_to_dict(row), "id": str(row.cliente_id)}}
    if user["role"] == "assistente":
        body["cliente"]["cpf"] = mascara_cpf(body["cliente"]["cpf"])
    return body

@app.get("/clientes/{id}", dependencies=[Depends(require_role("advogado", "assistente", "admin"))])
def consultar_cliente(id: str, user=Depends(current_user), db: Session = Depends(get_db)):
    row = get_cliente(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="cliente nao encontrado")
    body = {"status": "consultado", "cliente": {**cliente_to_dict(row), "id": str(row.cliente_id)}}
    if user["role"] == "assistente":
        body["cliente"]["cpf"] = mascara_cpf(body["cliente"]["cpf"])
    return body

@app.put("/clientes/{id}", dependencies=[Depends(require_role("advogado", "assistente", "admin"))])
def atualizar_cliente(id: str, cliente: ClienteSchema, user=Depends(current_user), db: Session = Depends(get_db)):
    if user["role"] == "assistente":
        current = get_cliente(db, id)
        if current is None:
            raise HTTPException(status_code=404, detail="cliente nao encontrado")
        if cliente.cpf and cliente.cpf != current.cpf:
            raise HTTPException(status_code=403, detail="assistente nao pode alterar CPF")
    row = update_cliente(db, id, cliente)
    if row is None:
        raise HTTPException(status_code=404, detail="cliente nao encontrado")
    body = {"status": "atualizado", "cliente": {**cliente_to_dict(row), "id": str(row.cliente_id)}}
    if user["role"] == "assistente":
        body["cliente"]["cpf"] = mascara_cpf(body["cliente"]["cpf"])
    return body

@app.delete("/clientes/{id}", dependencies=[Depends(require_role("advogado", "admin"))])
def deletar_cliente(id: str, db: Session = Depends(get_db)):
    ok = delete_cliente(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="cliente nao encontrado")
    return {"status": "deletado", "cliente": {"id": id}}

# Rotas Reclamado — requer auth; assistente vede CPF/CNPJ mascarado
@app.post("/reclamados", status_code=201, dependencies=[Depends(require_role("advogado", "assistente", "admin"))])
def criar_reclamado(r: ReclamadoSchema, user=Depends(current_user), db: Session = Depends(get_db)):
    row = create_reclamado(db, r)
    body = {"status": "criado", "reclamado": {**reclamado_to_dict(row), "id": str(row.reclamado_id)}}
    if user["role"] == "assistente":
        body["reclamado"] = mascara_reclamado(body["reclamado"])
    return body

@app.get("/reclamados/{id}", dependencies=[Depends(require_role("advogado", "assistente", "admin"))])
def consultar_reclamado(id: str, user=Depends(current_user), db: Session = Depends(get_db)):
    row = get_reclamado(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="reclamado nao encontrado")
    body = {"status": "consultado", "reclamado": {**reclamado_to_dict(row), "id": str(row.reclamado_id)}}
    if user["role"] == "assistente":
        body["reclamado"] = mascara_reclamado(body["reclamado"])
    return body

@app.put("/reclamados/{id}", dependencies=[Depends(require_role("advogado", "assistente", "admin"))])
def atualizar_reclamado(id: str, r: ReclamadoSchema, user=Depends(current_user), db: Session = Depends(get_db)):
    row = update_reclamado(db, id, r)
    if row is None:
        raise HTTPException(status_code=404, detail="reclamado nao encontrado")
    body = {"status": "atualizado", "reclamado": {**reclamado_to_dict(row), "id": str(row.reclamado_id)}}
    if user["role"] == "assistente":
        body["reclamado"] = mascara_reclamado(body["reclamado"])
    return body

@app.delete("/reclamados/{id}", dependencies=[Depends(require_role("advogado", "admin"))])
def deletar_reclamado(id: str, db: Session = Depends(get_db)):
    ok = delete_reclamado(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="reclamado nao encontrado")
    return {"status": "deletado", "reclamado": {"id": id}}

# Rotas Processo
@app.post("/processos", status_code=201, dependencies=[Depends(require_role("advogado", "assistente", "admin"))])
def criar_processo(p: ProcessoSchema, db: Session = Depends(get_db)):
    """Processo (raiz do agregado). observacao logada; id_area/id_rito via enums."""
    row = create_processo(db, p)
    return {"status": "criado", "processo": {**processo_to_dict(row), "id": row.processo_id}}

@app.get("/processos/{id}", dependencies=[Depends(require_role("advogado", "assistente", "admin"))])
def consultar_processo(id: str, db: Session = Depends(get_db)):
    row = get_processo(db, id)
    if row is None:
        raise HTTPException(status_code=404, detail="processo nao encontrado")
    return {"status": "consultado", "processo": {**processo_to_dict(row), "id": row.processo_id}}

@app.put("/processos/{id}", dependencies=[Depends(require_role("advogado", "assistente", "admin"))])
def atualizar_processo(id: str, p: ProcessoSchema, user=Depends(current_user), db: Session = Depends(get_db)):
    if user["role"] == "assistente":
        current = get_processo(db, id)
        if current is None:
            raise HTTPException(status_code=404, detail="processo nao encontrado")
        if float(current.valor_causa) != float(p.valor_causa):
            raise HTTPException(status_code=403, detail="assistente nao pode alterar valor_causa")
    row = update_processo(db, id, p)
    if row is None:
        raise HTTPException(status_code=404, detail="processo nao encontrado")
    return {"status": "atualizado", "processo": {**processo_to_dict(row), "id": row.processo_id}}

@app.delete("/processos/{id}", dependencies=[Depends(require_role("admin"))])
def deletar_processo(id: str, db: Session = Depends(get_db)):
    ok = delete_processo(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="processo nao encontrado")
    return {"status": "deletado", "processo": {"id": id}}

# Rotas MovimentoProcessual — encadeamento máquina de estados (GLOSSARY 4.1.3)
@app.post("/movimentos", status_code=201, dependencies=[Depends(require_role("advogado", "assistente", "admin"))])
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

@app.get("/movimentos", dependencies=[Depends(require_role("advogado", "assistente", "admin"))])
def listar_movimentos(processo_id: str | None = None, db: Session = Depends(get_db)):
    rows = list_movimentos(db, processo_id)
    return {"status": "listado", "movimentos": [movimento_to_dict(r) for r in rows]}

@app.post("/auth/login")
def auth_login(payload: dict, response: JSONResponse = None, db: Session = Depends(get_db)):
    login = str(payload.get("login", "") or "")
    password = str(payload.get("password", "") or "")
    if not login or not password:
        raise HTTPException(status_code=400, detail="login/password obrigatorios")
    user = get_user_by_login(db, login)
    if user is None or not verify_password(password, user.senha_hash):
        raise HTTPException(status_code=401, detail="credenciais invalidas")
    token = encode_token(user.user_id, user.nome, user.role.value)
    secure = (os.getenv("COOKIE_SECURE", "true").lower() != "false")
    resp = JSONResponse({"user": {"login": user.login, "nome": user.nome, "role": user.role.value}})
    resp.set_cookie(
        "access_token", token,
        httponly=True, samesite="strict", secure=secure,
        max_age=28800, path="/",
    )
    return resp


@app.get("/me")
def me(request: Request, db: Session = Depends(get_db)):
    cookie = request.cookies.get("access_token")
    if not cookie:
        raise HTTPException(status_code=401, detail="nao autenticado")
    try:
        payload = decode_token(cookie)
    except Exception:
        raise HTTPException(status_code=401, detail="token invalido")
    return {"sub": payload["sub"], "nome": payload["nome"], "role": payload["role"]}


@app.get("/health")
def health():
    return {"status": "ok", "project": "judis-advocacia"}
