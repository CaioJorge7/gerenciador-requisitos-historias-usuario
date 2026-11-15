"""Dados fictícios acadêmicos, persistidos no PostgreSQL pela aplicação.

Idempotente: não altera contas nem dados que já existam.
Conta: demo@requisitos.local / Demo123456! (APENAS ambiente local).
"""
import os
from decimal import Decimal
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Usuario, Projeto, ProductBacklog, SprintBacklog, Epico, HistoriaUsuario, CriterioAceitacao
from app.security import hash_password

EMAIL = os.getenv('SEED_EMAIL','demo@example.com')
PASSWORD = os.getenv('SEED_PASSWORD','Demo123456!')

with SessionLocal() as db:
    if db.scalar(select(Usuario).where(Usuario.email==EMAIL)):
        print('Conta de demonstração já existe. Nenhuma alteração realizada.')
    else:
        u=Usuario(nome='Conta de demonstração',email=EMAIL,senha_hash=hash_password(PASSWORD));db.add(u);db.flush()
        project=Projeto(usuario_id=u.id,nome='Plataforma de Gestão de Requisitos',descricao='Produto de demonstração para a disciplina de Engenharia de Software');db.add(project);db.flush()
        pb=ProductBacklog(projeto_id=project.id,nome='Backlog do Produto');db.add(pb)
        sp1=SprintBacklog(projeto_id=project.id,nome='Sprint 01 — Acesso',objetivo='Cadastro, autenticação e projetos')
        sp2=SprintBacklog(projeto_id=project.id,nome='Sprint 02 — Requisitos',objetivo='Histórias, critérios e priorização')
        db.add_all([sp1,sp2])
        ep1=Epico(projeto_id=project.id,nome='Identidade e acesso',descricao='Recursos de autenticação e autorização')
        ep2=Epico(projeto_id=project.id,nome='Planejamento do produto',descricao='Organização de histórias e prioridades')
        db.add_all([ep1,ep2]);db.flush()
        data=[
            ('usuário cadastrado','autenticar-me com e-mail e senha','acessar meus projetos',5,'M',250,'3.00',80,5,ep1.id,sp1.id,'CONCLUIDA'),
            ('analista de requisitos','criar histórias estruturadas','registrar necessidades com clareza',8,'M',140,'2.00',80,8,ep2.id,sp2.id,'EM_ANDAMENTO'),
            ('gerente de produto','priorizar histórias com RICE','planejar o backlog por valor',13,'S',300,'2.00',100,13,ep2.id,None,'A_FAZER'),
            ('integrante da equipe ágil','associar histórias às sprints','organizar cada iteração',5,'S',80,'1.00',80,5,ep2.id,None,'A_FAZER'),
            ('usuário autenticado','gerenciar meus projetos','manter os requisitos separados',3,'M',200,'3.00',100,3,ep1.id,sp1.id,'CONCLUIDA'),
        ]
        for papel,acao,beneficio,pts,moscow,reach,impact,confidence,effort,epid,sid,status in data:
            st=HistoriaUsuario(product_backlog_id=pb.id,papel=papel,acao=acao,beneficio=beneficio,story_points=pts,moscow=moscow,
                               rice_reach=reach,rice_impact=Decimal(impact),rice_confidence=confidence,rice_effort=effort,epico_id=epid,sprint_backlog_id=sid,status=status)
            db.add(st);db.flush()
            db.add(CriterioAceitacao(historia_usuario_id=st.id,dado='o usuário está autenticado',quando='realiza a ação descrita na história',entao='o resultado esperado é apresentado e persistido'))
        db.commit()
        print('Dados de demonstração criados no banco com sucesso.')
        print(f'Login local: {EMAIL} / {PASSWORD}')
        print('IMPORTANTE: não utilize essa senha em ambiente exposto à internet.')
