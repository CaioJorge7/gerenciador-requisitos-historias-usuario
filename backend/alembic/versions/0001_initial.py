"""Initial reviewed relational schema"""
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('senha_hash', sa.String(length=255), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=False),
    sa.CheckConstraint('length(trim(nome)) > 0', name='ck_usuario_nome'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('projeto',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=120), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('criado_em', sa.DateTime(), nullable=False),
    sa.CheckConstraint('length(trim(nome)) > 0', name='ck_projeto_nome'),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projeto_usuario_id'), 'projeto', ['usuario_id'], unique=False)
    op.create_table('sessao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('token_hash', sa.String(length=255), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=False),
    sa.Column('ultimo_acesso_em', sa.DateTime(), nullable=False),
    sa.Column('expira_em', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token_hash')
    )
    op.create_index(op.f('ix_sessao_usuario_id'), 'sessao', ['usuario_id'], unique=False)
    op.create_table('epico',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('projeto_id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=False),
    sa.Column('descricao', sa.Text(), nullable=True),
    sa.Column('criado_em', sa.DateTime(), nullable=False),
    sa.CheckConstraint('length(trim(nome)) > 0', name='ck_epico_nome'),
    sa.ForeignKeyConstraint(['projeto_id'], ['projeto.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_epico_projeto_id'), 'epico', ['projeto_id'], unique=False)
    op.create_table('product_backlog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('projeto_id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=120), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=False),
    sa.CheckConstraint('length(trim(nome)) > 0', name='ck_product_nome'),
    sa.ForeignKeyConstraint(['projeto_id'], ['projeto.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('projeto_id')
    )
    op.create_table('sprint_backlog',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('projeto_id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=120), nullable=False),
    sa.Column('objetivo', sa.Text(), nullable=True),
    sa.Column('data_inicio', sa.Date(), nullable=True),
    sa.Column('data_fim', sa.Date(), nullable=True),
    sa.Column('criado_em', sa.DateTime(), nullable=False),
    sa.CheckConstraint('data_inicio IS NULL OR data_fim IS NULL OR data_fim >= data_inicio', name='ck_sprint_datas'),
    sa.CheckConstraint('length(trim(nome)) > 0', name='ck_sprint_nome'),
    sa.ForeignKeyConstraint(['projeto_id'], ['projeto.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sprint_backlog_projeto_id'), 'sprint_backlog', ['projeto_id'], unique=False)
    op.create_table('historia_usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_backlog_id', sa.Integer(), nullable=False),
    sa.Column('sprint_backlog_id', sa.Integer(), nullable=True),
    sa.Column('epico_id', sa.Integer(), nullable=True),
    sa.Column('papel', sa.String(length=100), nullable=False),
    sa.Column('acao', sa.String(length=255), nullable=False),
    sa.Column('beneficio', sa.String(length=255), nullable=False),
    sa.Column('story_points', sa.SmallInteger(), nullable=True),
    sa.Column('moscow', sa.String(length=1), nullable=True),
    sa.Column('rice_reach', sa.Integer(), nullable=True),
    sa.Column('rice_impact', sa.Numeric(precision=3, scale=2), nullable=True),
    sa.Column('rice_confidence', sa.SmallInteger(), nullable=True),
    sa.Column('rice_effort', sa.SmallInteger(), nullable=True),
    sa.Column('status', sa.String(length=20), server_default='A_FAZER', nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=False),
    sa.CheckConstraint("moscow IS NULL OR moscow IN ('M','S','C','W')", name='ck_historia_moscow'),
    sa.CheckConstraint("status IN ('A_FAZER','EM_ANDAMENTO','CONCLUIDA')", name='ck_historia_status'),
    sa.CheckConstraint('length(trim(papel)) > 0 AND length(trim(acao)) > 0 AND length(trim(beneficio)) > 0', name='ck_historia_campos'),
    sa.CheckConstraint('rice_confidence IS NULL OR rice_confidence IN (100,80,50)', name='ck_historia_confidence'),
    sa.CheckConstraint('rice_effort IS NULL OR rice_effort IN (0,1,2,3,5,8,13,21,34,55)', name='ck_historia_effort'),
    sa.CheckConstraint('rice_impact IS NULL OR rice_impact IN (3,2,1,0.5,0.25)', name='ck_historia_impact'),
    sa.CheckConstraint('rice_reach IS NULL OR rice_reach >= 0', name='ck_historia_reach'),
    sa.CheckConstraint('story_points IS NULL OR story_points IN (0,1,2,3,5,8,13,21,34,55)', name='ck_historia_pontos'),
    sa.ForeignKeyConstraint(['epico_id'], ['epico.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['product_backlog_id'], ['product_backlog.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sprint_backlog_id'], ['sprint_backlog.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_historia_usuario_epico_id'), 'historia_usuario', ['epico_id'], unique=False)
    op.create_index(op.f('ix_historia_usuario_product_backlog_id'), 'historia_usuario', ['product_backlog_id'], unique=False)
    op.create_index(op.f('ix_historia_usuario_sprint_backlog_id'), 'historia_usuario', ['sprint_backlog_id'], unique=False)
    op.create_table('criterio_aceitacao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('historia_usuario_id', sa.Integer(), nullable=False),
    sa.Column('dado', sa.String(length=255), nullable=False),
    sa.Column('quando', sa.String(length=255), nullable=False),
    sa.Column('entao', sa.String(length=255), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=False),
    sa.CheckConstraint('length(trim(dado)) > 0 AND length(trim(quando)) > 0 AND length(trim(entao)) > 0', name='ck_criterio_campos'),
    sa.ForeignKeyConstraint(['historia_usuario_id'], ['historia_usuario.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_criterio_aceitacao_historia_usuario_id'), 'criterio_aceitacao', ['historia_usuario_id'], unique=False)
def downgrade():
    op.drop_index(op.f('ix_criterio_aceitacao_historia_usuario_id'), table_name='criterio_aceitacao')
    op.drop_table('criterio_aceitacao')
    op.drop_index(op.f('ix_historia_usuario_sprint_backlog_id'), table_name='historia_usuario')
    op.drop_index(op.f('ix_historia_usuario_product_backlog_id'), table_name='historia_usuario')
    op.drop_index(op.f('ix_historia_usuario_epico_id'), table_name='historia_usuario')
    op.drop_table('historia_usuario')
    op.drop_index(op.f('ix_sprint_backlog_projeto_id'), table_name='sprint_backlog')
    op.drop_table('sprint_backlog')
    op.drop_table('product_backlog')
    op.drop_index(op.f('ix_epico_projeto_id'), table_name='epico')
    op.drop_table('epico')
    op.drop_index(op.f('ix_sessao_usuario_id'), table_name='sessao')
    op.drop_table('sessao')
    op.drop_index(op.f('ix_projeto_usuario_id'), table_name='projeto')
    op.drop_table('projeto')
    op.drop_table('usuario')
