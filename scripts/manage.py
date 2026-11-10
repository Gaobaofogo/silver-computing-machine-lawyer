#!/usr/bin/env python3
"""manage.py — CLI utilitário administrativo do MVP.

Comandos:
  create-admin   Cria/atualiza o primeiro usuário admin via env ADMIN_LOGIN/ADMIN_PASSWORD."""
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _connect(db_url=None):
    db_url = db_url or os.getenv("DATABASE_URL", "sqlite://")
    from sqlmodel import Session, create_engine
    is_sqlite = db_url.startswith("sqlite")
    return create_engine(
        db_url,
        echo=False,
        connect_args={"check_same_thread": False} if is_sqlite else {},
    )


def _all_models():
    from apps.api.src.infra import database as database_infra
    database_infra.init_db()  # cria tabelas


def cmd_create_admin(args):
    from apps.api.src.models.auth import Role, User
    from apps.api.src.services.auth import hash_password, password_policy
    from sqlmodel import Session, select

    login = os.getenv("ADMIN_LOGIN")
    password = os.getenv("ADMIN_PASSWORD")
    if not login or not password:
        print("ADMIN_LOGIN/ADMIN_PASSWORD ausentes — configure antes de rodar create-admin.")
        return 1

    issues = password_policy(password)
    if issues:
        print("Senha fraca:")
        for i in issues:
            print(f" - {i}")
        return 2

    engine = _connect()
    _all_models()
    with Session(engine) as s:
        existing = s.exec(select(User).where(User.login == login)).first()
        if existing is not None:
            print(f"Admin já existe (login={login}). Nothing to do.")
            return 0
        admin = User(
            login=login,
            nome="Administrador",
            role=Role.ADMIN,
            senha_hash=hash_password(password),
        )
        s.add(admin)
        s.commit()
        print(f"Admin criado (login={login}). Troque a senha no primeiro login.")
    return 0


def main():
    parser = argparse.ArgumentParser(prog="manage.py", description="Utilitário administrativo")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("create-admin", help="Cria o primeiro user admin")

    args = parser.parse_args()
    if args.command == "create-admin":
        sys.exit(cmd_create_admin(args))
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
