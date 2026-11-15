"""Regras de negócio independentes dos endpoints (services + consultas de repositório)."""
from decimal import Decimal, ROUND_HALF_UP
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from . import models as m, schemas as s, repositories as repo


def get_project(db: Session, user_id: int, project_id: int) -> m.Projeto:
    project = repo.owned_project(db, user_id, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado ou acesso negado.")
    return project


def product_backlog(db: Session, project_id: int, required=True) -> m.ProductBacklog | None:
    pb = repo.product_backlog(db, project_id)
    if required and pb is None:
        raise HTTPException(status_code=409, detail="Crie o Product Backlog antes de cadastrar histórias.")
    return pb


def get_sprint(db: Session, project_id: int, sid: int) -> m.SprintBacklog:
    sp = repo.sprint(db, project_id, sid)
    if not sp: raise HTTPException(status_code=404, detail="Sprint não encontrada neste projeto.")
    return sp


def get_epic(db: Session, project_id: int, eid: int) -> m.Epico:
    ep = repo.epic(db, project_id, eid)
    if not ep: raise HTTPException(status_code=404, detail="Épico não encontrado neste projeto.")
    return ep


def get_story(db: Session, project_id: int, stid: int) -> m.HistoriaUsuario:
    st = repo.story(db, project_id, stid)
    if not st: raise HTTPException(status_code=404, detail="História não encontrada neste projeto.")
    return st


def get_criterion(db: Session, story_id: int, criterion_id: int) -> m.CriterioAceitacao:
    cr = repo.criterion(db, story_id, criterion_id)
    if not cr: raise HTTPException(status_code=404, detail="Critério não encontrado nesta história.")
    return cr


def validate_story_refs(db: Session, project_id: int, sprint_id: int | None, epic_id: int | None):
    if sprint_id is not None: get_sprint(db, project_id, sprint_id)
    if epic_id is not None: get_epic(db, project_id, epic_id)


def rice(reach, impact, confidence, effort) -> tuple[str | None,str]:
    """Pontuação derivada (não persistida), com 2 casas e tratamento de E=0."""
    if any(v is None for v in (reach,impact,confidence,effort)):
        return None, "PENDENTE"
    if effort == 0:
        return None, "NAO_CALCULAVEL"
    value = (Decimal(reach) * Decimal(str(impact)) * Decimal(confidence) / Decimal(100)) / Decimal(effort)
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)), "CALCULADO"


def story_out(story: m.HistoriaUsuario) -> s.HistoriaOut:
    score, state = rice(story.rice_reach, story.rice_impact, story.rice_confidence, story.rice_effort)
    return s.HistoriaOut(
        id=story.id, product_backlog_id=story.product_backlog_id, sprint_backlog_id=story.sprint_backlog_id,
        epico_id=story.epico_id, papel=story.papel, acao=story.acao, beneficio=story.beneficio,
        story_points=story.story_points, moscow=story.moscow, rice_reach=story.rice_reach,
        rice_impact=story.rice_impact, rice_confidence=story.rice_confidence, rice_effort=story.rice_effort,
        status=story.status, criado_em=story.criado_em,
        texto=f"Como um {story.papel}, eu quero {story.acao}, para {story.beneficio}.",
        rice_score=score, rice_estado=state,
        epico_nome=story.epico.nome if story.epico else None,
        sprint_nome=story.sprint_backlog.nome if story.sprint_backlog else None,
        criterios=[s.CriterioOut.model_validate(c) for c in story.criterios],
    )


def tally(db: Session, model, column, val: int) -> int:
    return repo.count_by(db,model,column,val)
