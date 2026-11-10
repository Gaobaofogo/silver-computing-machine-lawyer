"""Ticket 01 — ./scripts/manage.py create-admin (bootstrap admin)."""
import os
import subprocess
import sys
import pytest
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool

from apps.api.src.models.auth import User, Role

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MANAGE = os.path.join(ROOT, "scripts", "manage.py")


def _env(db_file, login="admin@x", pw="Admin#2026", extra=None):
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{db_file}"
    env["ADMIN_LOGIN"] = login
    env["ADMIN_PASSWORD"] = pw
    env["PYTHONPATH"] = f"{ROOT}:{ROOT}/.vendor:" + env.get("PYTHONPATH", "")
    if extra:
        env.update(extra)
    return env


def test_manage_help_blocks_no_args():
    proc = subprocess.run([sys.executable, MANAGE, "--help"], capture_output=True, text=True, cwd=ROOT)
    assert proc.returncode == 0
    assert "create-admin" in proc.stdout


def test_manage_create_admin_requires_env(tmp_path):
    env = os.environ.copy()
    env.pop("ADMIN_LOGIN", None)
    env.pop("ADMIN_PASSWORD", None)
    env["DATABASE_URL"] = f"sqlite:///{tmp_path}/m.db"
    proc = subprocess.run([sys.executable, MANAGE, "create-admin"], capture_output=True, text=True, env=env, cwd=ROOT)
    assert proc.returncode == 1
    assert "ADMIN_LOGIN" in proc.stdout or "ADMIN_PASSWORD" in proc.stdout


def test_manage_create_admin_senha_fraca_rejeitada(tmp_path):
    env = _env(tmp_path / "m.db", "admin@x", "fraca")  # sem símbolo/número/maiúscula; <10
    proc = subprocess.run([sys.executable, MANAGE, "create-admin"], capture_output=True, text=True, env=env, cwd=ROOT)
    assert proc.returncode == 2


def test_manage_create_admin_cria_admin(tmp_path):
    db_file = tmp_path / "m.db"
    pw = "Admin#2026a"
    env = _env(db_file, "admin@x", pw)
    proc = subprocess.run([sys.executable, MANAGE, "create-admin"],
                          capture_output=True, text=True, env=env, cwd=ROOT)
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    engine = create_engine(f"sqlite:///{db_file}", poolclass=StaticPool,
                           connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        rows = s.exec(select(User).where(User.login == "admin@x")).all()
        assert len(rows) == 1
        assert rows[0].role == Role.ADMIN


def test_manage_create_admin_idempotente(tmp_path):
    db_file = tmp_path / "m.db"
    pw = "Admin#2026a"
    env = _env(db_file, "admin@x", pw)
    subprocess.run([sys.executable, MANAGE, "create-admin"], capture_output=True, text=True, env=env, cwd=ROOT)
    proc2 = subprocess.run([sys.executable, MANAGE, "create-admin"],
                           capture_output=True, text=True, env=env)
    assert proc2.returncode == 0
    assert "admin" in proc2.stdout.lower() and ("exist" in proc2.stdout.lower() or "presente" in proc2.stdout.lower())
