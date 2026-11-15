"""Repository: consultas ORM parametrizadas, isoladas das regras do domínio.

Camada: Router -> Service -> Repository -> SQLAlchemy -> PostgreSQL.
"""
from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload
from . import models as m


def owned_project(db:Session,user_id:int,pid:int):
    return db.scalar(select(m.Projeto).where(m.Projeto.id==pid,m.Projeto.usuario_id==user_id))

def projects(db:Session,user_id:int):
    return db.scalars(select(m.Projeto).where(m.Projeto.usuario_id==user_id).order_by(m.Projeto.id.desc())).all()

def product_backlog(db:Session,pid:int):
    return db.scalar(select(m.ProductBacklog).where(m.ProductBacklog.projeto_id==pid))

def sprint(db:Session,pid:int,sid:int):
    return db.scalar(select(m.SprintBacklog).where(m.SprintBacklog.id==sid,m.SprintBacklog.projeto_id==pid))

def sprints(db:Session,pid:int):
    return db.scalars(select(m.SprintBacklog).where(m.SprintBacklog.projeto_id==pid).order_by(m.SprintBacklog.id.desc())).all()

def epic(db:Session,pid:int,eid:int):
    return db.scalar(select(m.Epico).where(m.Epico.id==eid,m.Epico.projeto_id==pid))

def epics(db:Session,pid:int):
    return db.scalars(select(m.Epico).where(m.Epico.projeto_id==pid).order_by(m.Epico.id.desc())).all()

def story(db:Session,pid:int,stid:int):
    return db.scalar(select(m.HistoriaUsuario)
        .join(m.ProductBacklog,m.HistoriaUsuario.product_backlog_id==m.ProductBacklog.id)
        .where(m.HistoriaUsuario.id==stid,m.ProductBacklog.projeto_id==pid))

def stories(db:Session,pb_id:int,sprint_id:int|None=None,epic_id:int|None=None,available:bool=False):
    stmt=select(m.HistoriaUsuario).where(m.HistoriaUsuario.product_backlog_id==pb_id)
    if sprint_id is not None:stmt=stmt.where(m.HistoriaUsuario.sprint_backlog_id==sprint_id)
    if epic_id is not None:stmt=stmt.where(m.HistoriaUsuario.epico_id==epic_id)
    if available:stmt=stmt.where(m.HistoriaUsuario.sprint_backlog_id.is_(None))
    stmt=stmt.options(selectinload(m.HistoriaUsuario.criterios),selectinload(m.HistoriaUsuario.epico),selectinload(m.HistoriaUsuario.sprint_backlog)).order_by(m.HistoriaUsuario.id.desc())
    return db.scalars(stmt).all()

def criterion(db:Session,stid:int,cid:int):
    return db.scalar(select(m.CriterioAceitacao).where(m.CriterioAceitacao.id==cid,m.CriterioAceitacao.historia_usuario_id==stid))

def criteria(db:Session,stid:int):
    return db.scalars(select(m.CriterioAceitacao).where(m.CriterioAceitacao.historia_usuario_id==stid).order_by(m.CriterioAceitacao.id)).all()

def count_by(db:Session,model,column,value:int)->int:
    return db.scalar(select(func.count()).select_from(model).where(column==value)) or 0
