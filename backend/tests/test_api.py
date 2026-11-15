from sqlalchemy import select, text
from app.database import SessionLocal
from app.models import Usuario, HistoriaUsuario, ProductBacklog, CriterioAceitacao
from app.services import rice


def req(client,method,url,body=None):
    h={"X-CSRF-Token":client.cookies.get("sr_csrf") or ""}
    return client.request(method,url,json=body,headers=h)


def create_pb(client,pid):
    r=req(client,"POST",f"/api/v1/projects/{pid}/product-backlog",{"nome":"Backlog principal"})
    assert r.status_code==201,r.text
    return r.json()


def create_story(client,pid,**kwargs):
    data={"papel":"analista","acao":"organizar requisitos","beneficio":"planejar melhor o produto","story_points":8,"moscow":"M","rice_reach":200,"rice_impact":2,"rice_confidence":80,"rice_effort":8}
    data.update(kwargs)
    return req(client,"POST",f"/api/v1/projects/{pid}/stories",data)


def test_auth_cookies_logout_and_csrf(client):
    assert client.get("/api/v1/projects").status_code==401
    assert client.post("/api/v1/auth/register",json={"nome":" ","email":"bad","senha":"123"}).status_code==422
    assert client.post("/api/v1/auth/register",json={"nome":"Ana","email":"Ana@example.org","senha":"senhaSuper123"}).status_code==201
    assert client.post("/api/v1/auth/register",json={"nome":"B","email":"ana@example.org","senha":"senhaSuper123"}).status_code==409
    assert client.post("/api/v1/auth/login",json={"email":"ana@example.org","senha":"errada"}).status_code==401
    assert client.post("/api/v1/auth/login",json={"email":"ana@example.org","senha":"senhaSuper123"}).status_code==200
    assert client.cookies.get("sr_session")
    assert client.get("/api/v1/auth/me").json()["nome"]=="Ana"
    assert client.post("/api/v1/projects",json={"nome":"Teste"}).status_code==403
    raw=client.cookies.get("sr_session")
    assert req(client,"POST","/api/v1/projects",{"nome":"Teste"}).status_code==201
    assert req(client,"POST","/api/v1/auth/logout").status_code==204
    assert client.get("/api/v1/projects").status_code==401
    client.cookies.set("sr_session",raw)
    assert client.get("/api/v1/projects").status_code==401


def test_project_crud_and_user_isolation(logged,project):
    client=logged
    p=project['id']
    assert client.get("/api/v1/projects").json()[0]['id']==p
    r=req(client,'PATCH',f'/api/v1/projects/{p}',{"nome":"Renomeado","descricao":"Nova"})
    assert r.status_code==200 and r.json()['nome']=='Renomeado'
    other_client=__import__('fastapi').testclient.TestClient(__import__('app.main',fromlist=['app']).app)
    with other_client as o:
        assert o.post('/api/v1/auth/register',json={'nome':'B','email':'b@example.org','senha':'senhaSuper123'}).status_code==201
        assert o.post('/api/v1/auth/login',json={'email':'b@example.org','senha':'senhaSuper123'}).status_code==200
        assert o.get(f'/api/v1/projects/{p}').status_code==404
        assert req(o,'DELETE',f'/api/v1/projects/{p}').status_code==404
    assert req(client,'DELETE',f'/api/v1/projects/{p}').status_code==204
    assert client.get('/api/v1/projects').json()==[]


def test_pb_uniqueness_and_story_requires_backlog(logged,project):
    p=project['id']
    r=create_story(logged,p)
    assert r.status_code==409
    create_pb(logged,p)
    assert req(logged,'POST',f'/api/v1/projects/{p}/product-backlog',{'nome':'Outro'}).status_code==409
    with SessionLocal() as db:
        assert len(db.scalars(select(ProductBacklog)).all())==1
    assert req(logged,'PATCH',f'/api/v1/projects/{p}/product-backlog',{'nome':'Nome novo'}).status_code==200


def test_sprints_epics_story_criteria_movement_and_cascades(logged,project):
    p=project['id'];create_pb(logged,p)
    sp=req(logged,'POST',f'/api/v1/projects/{p}/sprints',{'nome':'Sprint 1','objetivo':'Entrega MVP','data_inicio':'2026-11-14','data_fim':'2026-11-21'})
    ep=req(logged,'POST',f'/api/v1/projects/{p}/epics',{'nome':'Autenticação','descricao':'Login e conta'})
    assert sp.status_code==201 and ep.status_code==201
    sid=sp.json()['id']; eid=ep.json()['id']
    r=create_story(logged,p,sprint_backlog_id=sid,epico_id=eid)
    assert r.status_code==201,r.text
    st=r.json(); tid=st['id']
    assert st['rice_score']=='40.00' and st['rice_estado']=='CALCULADO'
    assert 'Como um analista' in st['texto']
    cr=req(logged,'POST',f'/api/v1/projects/{p}/stories/{tid}/criteria',{'dado':'usuário autenticado','quando':'abre o backlog','entao':'vê suas histórias'})
    assert cr.status_code==201,cr.text
    cid=cr.json()['id']
    assert len(logged.get(f'/api/v1/projects/{p}/stories/{tid}').json()['criterios'])==1
    assert req(logged,'PATCH',f'/api/v1/projects/{p}/stories/{tid}/criteria/{cid}',{'dado':'outro contexto','quando':'abre','entao':'vê'}).status_code==200
    moved=req(logged,'POST',f'/api/v1/projects/{p}/stories/{tid}/move',{'sprint_backlog_id':None})
    assert moved.status_code==200 and moved.json()['sprint_backlog_id'] is None
    assert moved.json()['rice_score']=='40.00' and moved.json()['epico_id']==eid
    assert req(logged,'POST',f'/api/v1/projects/{p}/stories/{tid}/move',{'sprint_backlog_id':sid}).status_code==200
    assert req(logged,'DELETE',f'/api/v1/projects/{p}/sprints/{sid}').status_code==204
    assert logged.get(f'/api/v1/projects/{p}/stories/{tid}').json()['sprint_backlog_id'] is None
    assert req(logged,'DELETE',f'/api/v1/projects/{p}/epics/{eid}').status_code==204
    st=logged.get(f'/api/v1/projects/{p}/stories/{tid}').json()
    assert st['epico_id'] is None and st['criterios'][0]['dado']=='outro contexto'
    assert req(logged,'DELETE',f'/api/v1/projects/{p}/stories/{tid}/criteria/{cid}').status_code==204
    assert logged.get(f'/api/v1/projects/{p}/stories/{tid}/criteria').json()==[]
    assert req(logged,'DELETE',f'/api/v1/projects/{p}/product-backlog').status_code==204
    assert logged.get(f'/api/v1/projects/{p}/stories').json()==[]


def test_cross_project_blocked(logged,project):
    p1=project['id'];create_pb(logged,p1)
    p2=req(logged,'POST','/api/v1/projects',{'nome':'Projeto B'}).json()['id'];create_pb(logged,p2)
    foreign_sprint=req(logged,'POST',f'/api/v1/projects/{p2}/sprints',{'nome':'Outra sprint'}).json()['id']
    foreign_epic=req(logged,'POST',f'/api/v1/projects/{p2}/epics',{'nome':'Outro épico'}).json()['id']
    assert create_story(logged,p1,sprint_backlog_id=foreign_sprint).status_code==404
    assert create_story(logged,p1,epico_id=foreign_epic).status_code==404
    story=create_story(logged,p1).json()['id']
    assert req(logged,'POST',f'/api/v1/projects/{p1}/stories/{story}/move',{'sprint_backlog_id':foreign_sprint}).status_code==404
    assert logged.get(f'/api/v1/projects/{p2}/stories/{story}').status_code==404


def test_validations_rice_zero_and_not_persisted(logged,project):
    p=project['id'];create_pb(logged,p)
    assert create_story(logged,p,story_points=4).status_code==422
    assert create_story(logged,p,moscow='Z').status_code==422
    assert create_story(logged,p,rice_impact='5').status_code==422
    assert create_story(logged,p,rice_confidence=65).status_code==422
    assert create_story(logged,p,rice_effort=7).status_code==422
    assert create_story(logged,p,rice_reach=-1).status_code==422
    assert create_story(logged,p,papel='  ').status_code==422
    zero=create_story(logged,p,rice_effort=0).json()
    assert zero['rice_score'] is None and zero['rice_estado']=='NAO_CALCULAVEL'
    assert create_story(logged,p,rice_confidence=None).json()['rice_estado']=='PENDENTE'
    with SessionLocal() as db:
        assert 'rice_score' not in HistoriaUsuario.__table__.columns
    assert rice(200,2,80,8)==('40.00','CALCULADO')


def test_integrity_constraints_on_db(logged,project):
    p=project['id'];pb=create_pb(logged,p)
    from sqlalchemy.exc import IntegrityError
    import pytest
    with SessionLocal() as db:
        with pytest.raises(IntegrityError):
            db.execute(text('INSERT INTO product_backlog(projeto_id,nome,criado_em) VALUES (:id,:name,CURRENT_TIMESTAMP)'),{'id':p,'name':'Duplicado'})
            db.commit()
        db.rollback()
        with pytest.raises(IntegrityError):
            db.execute(text("INSERT INTO historia_usuario(product_backlog_id,papel,acao,beneficio,story_points,status,criado_em) VALUES (:pb,'p','a','b',4,'A_FAZER',CURRENT_TIMESTAMP)"),{'pb':pb['id']})
            db.commit()
        db.rollback()
        with pytest.raises(IntegrityError):
            db.execute(text("INSERT INTO historia_usuario(product_backlog_id,papel,acao,beneficio,status,criado_em) VALUES (99999,'p','a','b','A_FAZER',CURRENT_TIMESTAMP)"))
            db.commit()
        db.rollback()


def test_full_crud_product_backlog_sprints_epics_and_stories(logged,project):
    p=project['id']; pb=create_pb(logged,p)
    assert logged.get(f'/api/v1/projects/{p}/product-backlog').json()['nome']=='Backlog principal'
    sprint=req(logged,'POST',f'/api/v1/projects/{p}/sprints',{'nome':'Sprint nova'})
    assert sprint.status_code==201
    sid=sprint.json()['id']
    assert req(logged,'PATCH',f'/api/v1/projects/{p}/sprints/{sid}',{'nome':'Sprint atualizada','objetivo':'Entregar','data_inicio':None,'data_fim':None}).json()['nome']=='Sprint atualizada'
    assert req(logged,'POST',f'/api/v1/projects/{p}/sprints',{'nome':'Datas inválidas','data_inicio':'2026-12-01','data_fim':'2026-11-01'}).status_code==422
    eid=req(logged,'POST',f'/api/v1/projects/{p}/epics',{'nome':'Épico 1'}).json()['id']
    assert req(logged,'PATCH',f'/api/v1/projects/{p}/epics/{eid}',{'nome':'Épico alterado','descricao':'Novo texto'}).json()['nome']=='Épico alterado'
    story=create_story(logged,p).json();stid=story['id']
    patch={k:story[k] for k in ['papel','acao','beneficio','epico_id','sprint_backlog_id','story_points','moscow','rice_reach','rice_impact','rice_confidence','rice_effort','status']}
    patch.update({'acao':'escrever requisitos claros','status':'EM_ANDAMENTO','epico_id':eid})
    r=req(logged,'PATCH',f'/api/v1/projects/{p}/stories/{stid}',patch)
    assert r.status_code==200,r.text
    assert r.json()['acao']=='escrever requisitos claros'
    assert r.json()['status']=='EM_ANDAMENTO'
    assert len(logged.get(f'/api/v1/projects/{p}/stories').json())==1
    assert len(logged.get(f'/api/v1/projects/{p}/stories?epico_id={eid}').json())==1
    assert req(logged,'DELETE',f'/api/v1/projects/{p}/stories/{stid}').status_code==204
    assert logged.get(f'/api/v1/projects/{p}/stories').json()==[]


def test_session_idle_expiration_and_cookie_exposure(logged):
    from datetime import timedelta
    from sqlalchemy import select
    from app.models import Sessao, utcnow
    with SessionLocal() as db:
        sess=db.scalar(select(Sessao))
        assert sess is not None
        sess.ultimo_acesso_em=utcnow()-timedelta(minutes=31)
        db.commit()
    r=logged.get('/api/v1/projects')
    assert r.status_code==401 and 'expirada' in r.json()['detail']
    with SessionLocal() as db:
        assert db.scalar(select(Sessao)) is None


def test_fast_list_500_stories_in_test_environment(logged,project):
    from time import perf_counter
    from app.models import ProductBacklog
    p=project['id'];pb=create_pb(logged,p)
    with SessionLocal() as db:
        db.add_all([HistoriaUsuario(product_backlog_id=pb['id'],papel='analista',acao=f'priorizar requisito {i}',beneficio='organizar o backlog',status='A_FAZER') for i in range(500)])
        db.commit()
    start=perf_counter()
    response=logged.get(f'/api/v1/projects/{p}/stories')
    took=perf_counter()-start
    assert response.status_code==200
    assert len(response.json())==500
    assert took<3.0, f'{took:.3f}s (somente ambiente de teste SQLite, não valida desempenho no PostgreSQL de produção)'
