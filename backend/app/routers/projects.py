from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Usuario, Projeto
from .. import repositories as repo
from ..schemas import ProjetoCreate, ProjetoUpdate, ProjetoOut
from ..security import current_user, protected
from ..services import get_project
router = APIRouter(prefix="/projects", tags=["Projetos"], dependencies=[Depends(protected)])

@router.get("", response_model=list[ProjetoOut])
def list_projects(db: Session=Depends(get_db), user: Usuario=Depends(current_user)):
    return repo.projects(db,user.id)

@router.post("", status_code=201, response_model=ProjetoOut)
def create_project(body: ProjetoCreate, db: Session=Depends(get_db), user: Usuario=Depends(current_user)):
    project=Projeto(usuario_id=user.id, **body.model_dump())
    db.add(project);db.flush();db.refresh(project)
    return project

@router.get("/{project_id}", response_model=ProjetoOut)
def retrieve_project(project_id:int, db: Session=Depends(get_db), user: Usuario=Depends(current_user)):
    return get_project(db,user.id,project_id)

@router.patch("/{project_id}", response_model=ProjetoOut)
def patch_project(project_id:int, body:ProjetoUpdate, db: Session=Depends(get_db), user:Usuario=Depends(current_user)):
    project=get_project(db,user.id,project_id)
    for key,val in body.model_dump(exclude_unset=True).items():
        setattr(project,key,val)
    db.flush();db.refresh(project)
    return project

@router.delete("/{project_id}", status_code=204)
def delete_project(project_id:int, db:Session=Depends(get_db), user:Usuario=Depends(current_user)):
    project=get_project(db,user.id,project_id)
    db.delete(project);db.flush()
    return Response(status_code=204)
