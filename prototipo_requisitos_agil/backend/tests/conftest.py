"""Testes em SQLite temporário, sem substituir o PostgreSQL do ambiente de produção."""
import os
import tempfile
from pathlib import Path
from urllib.parse import quote

_DB=Path(tempfile.mkdtemp(prefix="requisitos_tests_"))/"tests.db"
os.environ["DATABASE_URL"]="sqlite:///"+str(_DB)
os.environ["COOKIE_SECURE"]="false"

import pytest
from fastapi.testclient import TestClient
from app.database import engine, Base
from app import models
from app.main import app

@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def logged(client):
    r=client.post("/api/v1/auth/register",json={"nome":"Pessoa A","email":"a@example.org","senha":"senhaSuper123"})
    assert r.status_code==201,r.text
    r=client.post("/api/v1/auth/login",json={"email":"a@example.org","senha":"senhaSuper123"})
    assert r.status_code==200,r.text
    return client

@pytest.fixture
def csrf(logged):
    return {"X-CSRF-Token":logged.cookies.get("sr_csrf")}

@pytest.fixture
def project(logged,csrf):
    response=logged.post("/api/v1/projects",json={"nome":"Projeto A","descricao":"Teste"},headers=csrf)
    assert response.status_code==201,response.text
    return response.json()
