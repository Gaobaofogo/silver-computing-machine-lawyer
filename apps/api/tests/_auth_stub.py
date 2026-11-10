"""Helpers para testes de rotas — seed minimal admin via dependency_override."""
from apps.api.src.auth.dependencies import current_user
from apps.api.src.main import app

_ADMIN = {
    "user_id": "00000000-0000-0000-0000-000000000000",
    "login": "admin@test",
    "nome": "Administrador",
    "role": "admin",
}


def enable_admin_override():
    app.dependency_overrides[current_user] = lambda: dict(_ADMIN)


def disable_admin_override():
    app.dependency_overrides.pop(current_user, None)
