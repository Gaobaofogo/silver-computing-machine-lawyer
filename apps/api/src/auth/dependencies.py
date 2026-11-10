"""Dependencies do MVP: require_role, current_user, auditoria middleware."""
from datetime import datetime, timezone
from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException, Request
from sqlmodel import Session

from apps.api.src.infra.database import get_db
from apps.api.src.models.auth import Role, User
from apps.api.src.models.audit import LogsAcesso
from apps.api.src.services.auth import decode_token


def current_user(request: Request, db: Session = Depends(get_db)):
    cookie = request.cookies.get("access_token")
    if not cookie:
        raise HTTPException(status_code=401, detail="nao autenticado")
    try:
        payload = decode_token(cookie)
    except Exception:
        raise HTTPException(status_code=401, detail="token invalido")
    try:
        u = db.get(User, UUID(payload["sub"]))
    except Exception:
        raise HTTPException(status_code=401, detail="usuario nao encontrado")
    if not u:
        raise HTTPException(status_code=401, detail="usuario nao encontrado")
    return {"user_id": u.user_id, "login": u.login, "nome": u.nome, "role": u.role.value}


def require_role(*allowed: str):
    def check(user=Depends(current_user)):
        if user["role"] not in allowed:
            raise HTTPException(status_code=403, detail="acesso negado")
        return user
    return check


def lgpd_audit(request: Request, response_status: int = 200, db: Session = None):
    # placeholder (nunca chamado diretamente; middleware faz tudo)
    return


def middleware_log(request: Request, response_status: int):
    """Escreve uma linha em logs_acesso — usado pelo middleware."""
    path = request.url.path
    if not _tracked_path(path):
        return
    role, user_id = None, None
    try:
        cookie = request.cookies.get("access_token")
        if cookie:
            payload = decode_token(cookie)
            role = payload.get("role")
            try:
                user_id = UUID(payload["sub"])
            except Exception:
                user_id = None
    except Exception:
        role, user_id = None, None
    from apps.api.src.infra.database import engine as _engine
    with Session(_engine) as s:
        s.add(LogsAcesso(
            ts=datetime.now(timezone.utc),
            ip=(request.client.host if request.client else None),
            user_id=user_id,
            role=role,
            op=request.method,
            path=path,
            status_code=response_status,
        ))
        s.commit()


def _tracked_path(path: str) -> bool:
    return path.startswith(("/clientes", "/reclamados", "/processos", "/movimentos"))
