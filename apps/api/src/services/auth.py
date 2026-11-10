"""Helpers de Auth: bcrypt hash/verify + JWT HS256 (ADR-0006)."""
from datetime import datetime, timedelta, timezone
from uuid import UUID

import bcrypt
import jwt

SECRET = "MVP_SECRET_KEY_FALLBACK_INSECURE_DEFAULT"  # ser overriderado via env em produção
ALGORITHM = "HS256"
EXPIRES_IN_SECONDS = 8 * 3600


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=12)).decode()


def verify_password(plain: str, digest: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), digest.encode())
    except ValueError:
        return False


def encode_token(user_id: UUID, nome: str, role: str) -> str:
    import os
    key = os.getenv("SECRET_KEY", SECRET)
    payload = {
        "sub": str(user_id),
        "nome": nome,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=EXPIRES_IN_SECONDS),
    }
    return jwt.encode(payload, key, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    import os
    key = os.getenv("SECRET_KEY", SECRET)
    return jwt.decode(token, key, algorithms=[ALGORITHM])


def password_policy(plain: str) -> list[str]:
    """Lista de violações da política mínima (ADR-0006 §5)."""
    issues = []
    if len(plain) < 10:
        issues.append("senha deve ter ao menos 10 caracteres")
    if not any(c.isdigit() for c in plain):
        issues.append("senha deve conter ao menos 1 número")
    if not any(not c.isalnum() for c in plain):
        issues.append("senha deve conter ao menos 1 símbolo")
    if not any(c.isupper() for c in plain):
        issues.append("senha deve conter ao menos 1 letra maiúscula")
    return issues


from sqlmodel import Session, select
from apps.api.src.models.auth import Role, User


def create_user(session, login: str, nome: str, role, password: str) -> User:
    row = User(
        login=login,
        nome=nome,
        role=role,
        senha_hash=hash_password(password),
    )
    session.add(row)
    session.commit()
    session.refresh(row)
    return row


def get_user_by_login(session, login: str):
    return session.exec(select(User).where(User.login == login)).first()
