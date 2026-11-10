"""Ticket 02 — Auth backend: POST /auth/login + GET /me (ticket 01 seed)."""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from apps.api.src.main import app
from apps.api.src.infra import database
from apps.api.src.models.auth import Role
from apps.api.src.services.auth import create_user

PW = "Admin#2026a"
LOGIN = "admin@test"
NOME = "Administrador"


@pytest.fixture()
def client_and_user():
    test_engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    original = database.engine
    database.engine = test_engine

    def override_db():
        with Session(test_engine) as session:
            yield session

    database.init_db()
    with Session(test_engine) as s:
        create_user(s, LOGIN, NOME, Role.ADMIN, PW)

    app.dependency_overrides[database.get_db] = override_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()
        database.engine = original


def test_login_ok_com_credenciais_validas(client_and_user):
    r = client_and_user.post("/auth/login", json={"login": LOGIN, "password": PW})
    assert r.status_code == 200
    assert "access_token" in r.cookies
    assert r.json()["user"]["login"] == LOGIN
    assert r.json()["user"]["role"] == Role.ADMIN.value


def test_login_err_senha_errada(client_and_user):
    r = client_and_user.post("/auth/login", json={"login": LOGIN, "password": "Errada#2026"})
    assert r.status_code == 401


def test_me_sem_cookie_retorna_401(client_and_user):
    r = client_and_user.get("/me")
    assert r.status_code == 401


def test_me_com_cookie_retorna_user(client_and_user):
    login = client_and_user.post("/auth/login", json={"login": LOGIN, "password": PW})
    cookie = login.cookies.get("access_token")
    assert cookie is not None
    r = client_and_user.get("/me", cookies={"access_token": cookie})
    assert r.status_code == 200
    assert r.json()["sub"] is not None
    assert r.json()["role"] == Role.ADMIN.value


def test_me_cookie_token_invalido(client_and_user):
    r = client_and_user.get("/me", cookies={"access_token": "invalid.jwt.token"})
    assert r.status_code == 401
