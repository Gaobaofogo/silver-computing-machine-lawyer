"""Conftest compartilhado — cada teste roda com engine SQLite in-memory
isolada, tabelas criadas automaticamente. auth_override/admin idempotente
pode ser mais granular sobrescrito pelos testes que exigem roles específicas
(e.g. test_require_role.py)."""
import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from apps.api.src.infra import database
from apps.api.src.main import app
from apps.api.src.auth.dependencies import current_user


@pytest.fixture(autouse=True)
def _isolated_db():
    test_engine = create_engine(
        "sqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    original = database.engine
    database.engine = test_engine
    # DDL todas tables (auth, audit, clientes, processos, reclamados)
    database.init_db()

    def _override_db():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[database.get_db] = _override_db
    try:
        yield test_engine
    finally:
        app.dependency_overrides.pop(current_user, None)
        app.dependency_overrides.clear()
        database.engine = original
