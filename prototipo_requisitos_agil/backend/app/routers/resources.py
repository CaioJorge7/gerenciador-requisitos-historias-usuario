"""Backlogs, sprints, epicos, historias e criterios sob propriedade do projeto."""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from ..database import get_db
from .. import models as m, schemas as s, repositories as repo
from ..security import current_user, protected
from ..services import get_project, product_backlog, get_sprint, get_epic, get_story, get_criterion, validate_story_refs, story_out, tally

router = APIRouter(prefix="/projects/{project_id}", tags=["Requisitos"], dependencies=[Depends(protected)])

def own(db, user, project_id): return get_project(db, user.id, project_id)

@router.get("/product-backlog", response_model=s.BacklogOut | None)
def get_pb(project_id:int, db:Session=Depends(get_db), user:m.Usuario=Depends(current_user)):
    own(db,user,project_id)
    pb=product_backlog(db,project_id,required=False)
    if not pb: return None
    return s.BacklogOut.model_validate(pb).model_copy(update={"total_historias":tally(db,m.HistoriaUsuario,m.HistoriaUsuario.product_backlog_id,pb.id)})

@router.post("/product-backlog", response_model=s.BacklogOut, status_code=201)
def create_pb(project_id:int, body:s.BacklogCreate, db:Session=Depends(get_db), user:m.Usuario=Depends(current_user)):
    own(db,user,project_id)
    if product_backlog(db,project_id,required=False):
        raise HTTPException(status_code=409,detail="Este projeto já possui um Product Backlog.")
    pb=m.ProductBacklog(projeto_id=project_id,nome=body.nome)
    db.add(pb);db.flush();db.refresh(pb)
    return s.BacklogOut.model_validate(pb)

@router.patch("/product-backlog", response_model=s.BacklogOut)
def patch_pb(project_id:int,body:s.BacklogUpdate,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);pb=product_backlog(db,project_id)
    pb.nome=body.nome;db.flush();db.refresh(pb)
    return s.BacklogOut.model_validate(pb).model_copy(update={"total_historias":tally(db,m.HistoriaUsuario,m.HistoriaUsuario.product_backlog_id,pb.id)})

@router.delete("/product-backlog",status_code=204)
def delete_pb(project_id:int,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);pb=product_backlog(db,project_id)
    db.delete(pb);db.flush();return Response(status_code=204)

@router.get("/sprints",response_model=list[s.SprintOut])
def list_sprints(project_id:int,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id)
    items=repo.sprints(db,project_id)
    return [s.SprintOut.model_validate(x).model_copy(update={"total_historias":tally(db,m.HistoriaUsuario,m.HistoriaUsuario.sprint_backlog_id,x.id)}) for x in items]

@router.post("/sprints",response_model=s.SprintOut,status_code=201)
def create_sprint(project_id:int,body:s.SprintCreate,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);sp=m.SprintBacklog(projeto_id=project_id,**body.model_dump())
    db.add(sp);db.flush();db.refresh(sp);return s.SprintOut.model_validate(sp)

@router.get("/sprints/{sid}",response_model=s.SprintOut)
def retrieve_sprint(project_id:int,sid:int,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);sp=get_sprint(db,project_id,sid)
    return s.SprintOut.model_validate(sp).model_copy(update={"total_historias":tally(db,m.HistoriaUsuario,m.HistoriaUsuario.sprint_backlog_id,sp.id)})

@router.patch("/sprints/{sid}",response_model=s.SprintOut)
def patch_sprint(project_id:int,sid:int,body:s.SprintUpdate,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);sp=get_sprint(db,project_id,sid)
    for key,val in body.model_dump().items(): setattr(sp,key,val)
    db.flush();db.refresh(sp)
    return s.SprintOut.model_validate(sp).model_copy(update={"total_historias":tally(db,m.HistoriaUsuario,m.HistoriaUsuario.sprint_backlog_id,sp.id)})

@router.delete("/sprints/{sid}",status_code=204)
def delete_sprint(project_id:int,sid:int,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);sp=get_sprint(db,project_id,sid)
    db.delete(sp);db.flush();return Response(status_code=204)

@router.get("/epics",response_model=list[s.EpicoOut])
def list_epics(project_id:int,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id)
    items=repo.epics(db,project_id)
    return [s.EpicoOut.model_validate(x).model_copy(update={"total_historias":tally(db,m.HistoriaUsuario,m.HistoriaUsuario.epico_id,x.id)}) for x in items]

@router.post("/epics",response_model=s.EpicoOut,status_code=201)
def create_epic(project_id:int,body:s.EpicoCreate,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);ep=m.Epico(projeto_id=project_id,**body.model_dump())
    db.add(ep);db.flush();db.refresh(ep);return s.EpicoOut.model_validate(ep)

@router.get("/epics/{eid}",response_model=s.EpicoOut)
def retrieve_epic(project_id:int,eid:int,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);ep=get_epic(db,project_id,eid)
    return s.EpicoOut.model_validate(ep).model_copy(update={"total_historias":tally(db,m.HistoriaUsuario,m.HistoriaUsuario.epico_id,ep.id)})

@router.patch("/epics/{eid}",response_model=s.EpicoOut)
def patch_epic(project_id:int,eid:int,body:s.EpicoUpdate,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);ep=get_epic(db,project_id,eid)
    for key,val in body.model_dump().items():setattr(ep,key,val)
    db.flush();db.refresh(ep)
    return s.EpicoOut.model_validate(ep).model_copy(update={"total_historias":tally(db,m.HistoriaUsuario,m.HistoriaUsuario.epico_id,ep.id)})

@router.delete("/epics/{eid}",status_code=204)
def delete_epic(project_id:int,eid:int,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);ep=get_epic(db,project_id,eid)
    db.delete(ep);db.flush();return Response(status_code=204)

@router.get("/stories",response_model=list[s.HistoriaOut])
def list_stories(project_id:int, sprint_id:int|None=None, epico_id:int|None=None, available:bool=False,
                 db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id)
    pb=product_backlog(db,project_id,required=False)
    if not pb: return []
    if sprint_id is not None: get_sprint(db,project_id,sprint_id)
    if epico_id is not None: get_epic(db,project_id,epico_id)
    return [story_out(x) for x in repo.stories(db,pb.id,sprint_id,epico_id,available)]

@router.post("/stories",response_model=s.HistoriaOut,status_code=201)
def create_story(project_id:int,body:s.HistoriaCreate,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id)
    pb=product_backlog(db,project_id)
    validate_story_refs(db,project_id,body.sprint_backlog_id,body.epico_id)
    st=m.HistoriaUsuario(product_backlog_id=pb.id,**body.model_dump())
    db.add(st);db.flush();db.refresh(st)
    return story_out(st)

@router.get("/stories/{stid}",response_model=s.HistoriaOut)
def retrieve_story(project_id:int,stid:int,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);return story_out(get_story(db,project_id,stid))

@router.patch("/stories/{stid}",response_model=s.HistoriaOut)
def patch_story(project_id:int,stid:int,body:s.HistoriaUpdate,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);st=get_story(db,project_id,stid)
    validate_story_refs(db,project_id,body.sprint_backlog_id,body.epico_id)
    for key,val in body.model_dump().items():setattr(st,key,val)
    db.flush();db.refresh(st)
    return story_out(st)

@router.post("/stories/{stid}/move",response_model=s.HistoriaOut)
def move_story(project_id:int,stid:int,body:s.MoveStory,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);st=get_story(db,project_id,stid)
    if body.sprint_backlog_id is not None: get_sprint(db,project_id,body.sprint_backlog_id)
    st.sprint_backlog_id=body.sprint_backlog_id
    db.flush();db.refresh(st)
    return story_out(st)

@router.delete("/stories/{stid}",status_code=204)
def delete_story(project_id:int,stid:int,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);st=get_story(db,project_id,stid)
    db.delete(st);db.flush();return Response(status_code=204)

@router.get("/stories/{stid}/criteria",response_model=list[s.CriterioOut])
def list_criteria(project_id:int,stid:int,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);get_story(db,project_id,stid)
    return repo.criteria(db,stid)

@router.post("/stories/{stid}/criteria",response_model=s.CriterioOut,status_code=201)
def create_criterion(project_id:int,stid:int,body:s.CriterioCreate,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);get_story(db,project_id,stid)
    cr=m.CriterioAceitacao(historia_usuario_id=stid,**body.model_dump())
    db.add(cr);db.flush();db.refresh(cr);return cr

@router.patch("/stories/{stid}/criteria/{cid}",response_model=s.CriterioOut)
def patch_criterion(project_id:int,stid:int,cid:int,body:s.CriterioUpdate,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);get_story(db,project_id,stid);cr=get_criterion(db,stid,cid)
    for key,val in body.model_dump().items():setattr(cr,key,val)
    db.flush();db.refresh(cr);return cr

@router.delete("/stories/{stid}/criteria/{cid}",status_code=204)
def delete_criterion(project_id:int,stid:int,cid:int,db:Session=Depends(get_db),user:m.Usuario=Depends(current_user)):
    own(db,user,project_id);get_story(db,project_id,stid);cr=get_criterion(db,stid,cid)
    db.delete(cr);db.flush();return Response(status_code=204)
