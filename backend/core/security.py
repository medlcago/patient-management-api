from datetime import timedelta, datetime, UTC

import bcrypt
import jwt
from jwt import PyJWTError

from core.settings import settings


def create_token(employee_id: int, token_type: str = "access", lifetime: timedelta | None = None) -> str:
    now = datetime.now(UTC)
    if lifetime is None:
        if token_type == "refresh":
            lifetime = settings.jwt.refresh_token_lifetime
        else:
            lifetime = settings.jwt.access_token_lifetime

    payload = {
        "iat": now,
        "exp": now + lifetime,
        "employee_id": employee_id,
        "token_type": token_type,
    }
    token = jwt.encode(
        payload=payload,
        key=settings.jwt.secret_key,
        algorithm=settings.jwt.token_algorithm
    )
    return token


def access_token(employee_id: int) -> str:
    token = create_token(employee_id=employee_id, token_type="access")
    return token


def refresh_token(employee_id: int) -> str:
    token = create_token(employee_id=employee_id, token_type="refresh")
    return token


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.token_algorithm])
    except PyJWTError:
        return {}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password=plain_password.encode(), hashed_password=hashed_password.encode())


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt()).decode()
