from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Usuario, Sessao
from ..schemas import UsuarioCreate, UsuarioOut, Login
from ..security import (
    current_user, protected, hash_password, verify_password, create_session,
    set_session_cookies, clear_session_cookies, token_digest, COOKIE_SESSION,
)
router = APIRouter(prefix="/auth", tags=["Acesso"])

@router.post("/register", response_model=UsuarioOut, status_code=201)
def register(body: UsuarioCreate, db: Session = Depends(get_db)):
    email = body.email.lower()
    if db.scalar(select(Usuario).where(Usuario.email == email)):
        raise HTTPException(status_code=409, detail="Este e-mail já está cadastrado.")
    user = Usuario(nome=body.nome, email=email, senha_hash=hash_password(body.senha))
    db.add(user)
    db.flush()
    db.refresh(user)
    return user

@router.post("/login", response_model=UsuarioOut)
def login(body: Login, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(Usuario).where(Usuario.email == body.email.lower()))
    if user is None or not verify_password(user.senha_hash, body.senha):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")
    sid, csrf = create_session(db, user)
    set_session_cookies(response, sid, csrf)
    return user

@router.get("/me", response_model=UsuarioOut)
def me(user: Usuario = Depends(current_user)):
    return user

@router.post("/logout", status_code=204, dependencies=[Depends(protected)])
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    row = db.scalar(select(Sessao).where(Sessao.token_hash == token_digest(request.cookies[COOKIE_SESSION])))
    if row: db.delete(row)
    clear_session_cookies(response)
