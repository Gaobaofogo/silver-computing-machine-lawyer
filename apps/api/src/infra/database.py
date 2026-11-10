"""Infra de persistência — engine, sessão e DDL baseado em SQLModel.

Em produção `DATABASE_URL` (docker-compose) → Postgres.
Em testes, default in-memory SQLite com `StaticPool` para compartilhar o banco
entre conexões da mesma thread."""
import os
from decimal import Decimal
from datetime import date, datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

SQLITE_DEFAULT = "sqlite://"
URL = os.getenv("DATABASE_URL", SQLITE_DEFAULT)

IS_SQLITE = URL.startswith("sqlite")

engine = create_engine(
    URL,
    echo=False,
    connect_args={"check_same_thread": False} if IS_SQLITE else {},
    poolclass=StaticPool if IS_SQLITE else None,
)


def init_db() -> None:
    """Cria todas as tabelas registradas nos modelos SQLModel."""
    from apps.api.src.models import cliente, processo, reclamado  # noqa: F401

    SQLModel.metadata.create_all(engine)


def drop_db() -> None:
    from apps.api.src.models import cliente, processo, reclamado  # noqa: F401

    SQLModel.metadata.drop_all(engine)


def get_db():
    """FastAPI Dependency — yield Session; caller disposes."""
    with Session(engine) as session:
        yield session


# ------------------------------------------------------------------
# Helpers de persistência (consumo por rotas FastAPI)
# ------------------------------------------------------------------
def create_processo(session, payload):
    from apps.api.src.models.processo import Processo
    row = Processo(
        id_cliente=payload.id_cliente,
        id_reclamado=payload.id_reclamado,
        numero_processo=payload.numero_processo,
        data_autua=payload.data_autua,
        valor_causa=Decimal(str(payload.valor_causa)),
        id_area=payload.id_area,
        id_rito=payload.id_rito,
        status=payload.status,
        observacao=payload.observacao,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def get_processo(session, processo_id: str):
    from apps.api.src.models.processo import Processo
    from uuid import UUID
    try:
        pid = UUID(processo_id)
    except ValueError:
        return None
    try:
        return session.get(Processo, pid)
    except Exception:
        return None


def update_processo(session, processo_id: str, payload):
    from apps.api.src.models.processo import Processo
    from uuid import UUID
    try:
        pid = UUID(processo_id)
    except ValueError:
        return None
    row = session.get(Processo, pid)
    if row is None:
        return None
    row.id_cliente = payload.id_cliente
    row.id_reclamado = payload.id_reclamado
    row.numero_processo = payload.numero_processo
    row.data_autua = payload.data_autua
    row.valor_causa = Decimal(str(payload.valor_causa))
    row.id_area = payload.id_area
    row.id_rito = payload.id_rito
    row.status = payload.status
    row.observacao = payload.observacao
    row.updated_at = datetime.now().astimezone()
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def delete_processo(session, processo_id: str) -> bool:
    from apps.api.src.models.processo import Processo
    from uuid import UUID
    try:
        pid = UUID(processo_id)
    except ValueError:
        return False
    row = session.get(Processo, pid)
    if row is None:
        return False
    session.delete(row)
    session.commit()
    return True


def create_movimento(session, payload):
    from apps.api.src.models.processo import MovimentoProcessual
    row = MovimentoProcessual(
        processo_id=payload.processo_id,
        data_movimento=payload.data_movimento,
        tipo=payload.tipo,
        descricao=payload.descricao,
        status_anterior=payload.status_anterior,
        status_novo=payload.status_novo,
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def list_movimentos(session, processo_id=None):
    from apps.api.src.models.processo import MovimentoProcessual
    from uuid import UUID
    stmt = select(MovimentoProcessual)
    if processo_id is not None:
        try:
            pid = UUID(processo_id)
        except ValueError:
            return []
        stmt = stmt.where(MovimentoProcessual.processo_id == pid)
    return list(session.exec(stmt))


def processo_to_dict(row) -> dict:
    area_val = row.id_area.value if hasattr(row.id_area, "value") else str(row.id_area)
    rito_val = row.id_rito.value if hasattr(row.id_rito, "value") else str(row.id_rito)
    status_val = row.status.value if hasattr(row.status, "value") else str(row.status)
    return {
        "processo_id": str(row.processo_id),
        "id_cliente": str(row.id_cliente),
        "id_reclamado": str(row.id_reclamado),
        "numero_processo": row.numero_processo,
        "data_autua": row.data_autua.isoformat() if row.data_autua else None,
        "valor_causa": str(row.valor_causa),
        "id_area": area_val,
        "id_rito": rito_val,
        "status": status_val,
        "observacao": row.observacao,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }


def movimento_to_dict(row) -> dict:
    status_val = row.status_novo.value if (row.status_novo and hasattr(row.status_novo, "value")) else str(row.status_novo)
    status_a_val = row.status_anterior.value if (row.status_anterior and hasattr(row.status_anterior, "value")) else str(row.status_anterior)
    return {
        "movimento_id": str(row.movimento_id),
        "processo_id": str(row.processo_id),
        "data_movimento": row.data_movimento.isoformat() if row.data_movimento else None,
        "tipo": row.tipo,
        "descricao": row.descricao,
        "status_anterior": status_a_val,
        "status_novo": status_val,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "updated_at": row.updated_at.isoformat() if row.updated_at else None,
    }
