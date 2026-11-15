"""Argon2, sessão opaca no servidor e CSRF vinculado ao cookie da sessão."""
import hashlib
import hmac
import os
import secrets
from dotenv import load_dotenv
load_dotenv()
from datetime import timedelta
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from .database import get_db
from .models import Usuario, Sessao, utcnow

hasher = PasswordHasher()
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"  # true com HTTPS real
SECRET_KEY = os.getenv("APP_SECRET_KEY") or secrets.token_hex(32)
COOKIE_SESSION = "sr_session"
COOKIE_CSRF = "sr_csrf"
IDLE_MINUTES = 30
ABSOLUTE_HOURS = 8


def hash_password(pw: str) -> str:
    return hasher.hash(pw)


def verify_password(hashed: str, pw: str) -> bool:
    try:
        return hasher.verify(hashed, pw)
    except (VerifyMismatchError, VerificationError):
        return False


def token_digest(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def csrf_for(raw_sid: str) -> str:
    return hmac.new(SECRET_KEY.encode(), raw_sid.encode(), hashlib.sha256).hexdigest()


def create_session(db: Session, user: Usuario):
    from datetime import timedelta
    raw = secrets.token_urlsafe(40)
    now = utcnow()
    record = Sessao(usuario_id=user.id, token_hash=token_digest(raw), ultimo_acesso_em=now,
                    expira_em=now + timedelta(hours=ABSOLUTE_HOURS))
    db.add(record)
    db.flush()
    return raw, csrf_for(raw)


def current_user(request: Request, db: Session = Depends(get_db)) -> Usuario:
    raw = request.cookies.get(COOKIE_SESSION)
    if not raw:
        raise HTTPException(status_code=401, detail="Faça login para continuar.")
    record = db.scalar(select(Sessao).where(Sessao.token_hash == token_digest(raw)))
    now = utcnow()
    if record is None:
        raise HTTPException(status_code=401, detail="Sessão inválida. Faça login novamente.")
    if record.expira_em <= now or record.ultimo_acesso_em + timedelta(minutes=IDLE_MINUTES) <= now:
        db.delete(record)
        db.commit()  # invalida de fato; a excecao de autorizacao nao pode desfazer a exclusao
        raise HTTPException(status_code=401, detail="Sessão expirada. Faça login novamente.")
    record.ultimo_acesso_em = now
    user = db.get(Usuario, record.usuario_id)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")
    return user


def protected(request: Request, user: Usuario = Depends(current_user)) -> None:
    if request.method in {"POST", "PATCH", "PUT", "DELETE"}:
        raw = request.cookies.get(COOKIE_SESSION)
        cookie = request.cookies.get(COOKIE_CSRF)
        header = request.headers.get("X-CSRF-Token")
        expected = csrf_for(raw or "")
        if not cookie or not header or not hmac.compare_digest(cookie, header) or not hmac.compare_digest(header, expected):
            raise HTTPException(status_code=403, detail="Token CSRF inválido. Atualize a sessão.")


def set_session_cookies(response, sid: str, csrf: str):
    response.set_cookie(COOKIE_SESSION, sid, httponly=True, secure=COOKIE_SECURE, samesite="lax", max_age=ABSOLUTE_HOURS*3600, path="/")
    response.set_cookie(COOKIE_CSRF, csrf, httponly=False, secure=COOKIE_SECURE, samesite="lax", max_age=ABSOLUTE_HOURS*3600, path="/")


def clear_session_cookies(response):
    response.delete_cookie(COOKIE_SESSION, path="/", secure=COOKIE_SECURE, httponly=True, samesite="lax")
    response.delete_cookie(COOKIE_CSRF, path="/", secure=COOKIE_SECURE, httponly=False, samesite="lax")
