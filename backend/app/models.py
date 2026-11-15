"""Modelo fisico do Artefato 7, incluidas constraints no banco."""
from datetime import datetime, timezone, date
from decimal import Decimal
from sqlalchemy import (
    String, Text, Integer, SmallInteger, ForeignKey, UniqueConstraint,
    CheckConstraint, DateTime, Date, Numeric, func, Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Usuario(Base):
    __tablename__ = "usuario"
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    projetos: Mapped[list["Projeto"]] = relationship(back_populates="usuario", passive_deletes=True)
    sessoes: Mapped[list["Sessao"]] = relationship(back_populates="usuario", passive_deletes=True)
    __table_args__ = (CheckConstraint("length(trim(nome)) > 0", name="ck_usuario_nome"),)


class Sessao(Base):
    __tablename__ = "sessao"
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    ultimo_acesso_em: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    expira_em: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    usuario: Mapped["Usuario"] = relationship(back_populates="sessoes")


class Projeto(Base):
    __tablename__ = "projeto"
    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    usuario: Mapped["Usuario"] = relationship(back_populates="projetos")
    product_backlog: Mapped["ProductBacklog | None"] = relationship(back_populates="projeto", uselist=False, passive_deletes=True)
    sprints: Mapped[list["SprintBacklog"]] = relationship(back_populates="projeto", passive_deletes=True)
    epicos: Mapped[list["Epico"]] = relationship(back_populates="projeto", passive_deletes=True)
    __table_args__ = (CheckConstraint("length(trim(nome)) > 0", name="ck_projeto_nome"),)


class ProductBacklog(Base):
    __tablename__ = "product_backlog"
    id: Mapped[int] = mapped_column(primary_key=True)
    projeto_id: Mapped[int] = mapped_column(ForeignKey("projeto.id", ondelete="CASCADE"), unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    projeto: Mapped["Projeto"] = relationship(back_populates="product_backlog")
    historias: Mapped[list["HistoriaUsuario"]] = relationship(back_populates="product_backlog", passive_deletes=True)
    __table_args__ = (CheckConstraint("length(trim(nome)) > 0", name="ck_product_nome"),)


class SprintBacklog(Base):
    __tablename__ = "sprint_backlog"
    id: Mapped[int] = mapped_column(primary_key=True)
    projeto_id: Mapped[int] = mapped_column(ForeignKey("projeto.id", ondelete="CASCADE"), nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    objetivo: Mapped[str | None] = mapped_column(Text)
    data_inicio: Mapped[date | None] = mapped_column(Date)
    data_fim: Mapped[date | None] = mapped_column(Date)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    projeto: Mapped["Projeto"] = relationship(back_populates="sprints")
    historias: Mapped[list["HistoriaUsuario"]] = relationship(back_populates="sprint_backlog", passive_deletes=True)
    __table_args__ = (
        CheckConstraint("length(trim(nome)) > 0", name="ck_sprint_nome"),
        CheckConstraint("data_inicio IS NULL OR data_fim IS NULL OR data_fim >= data_inicio", name="ck_sprint_datas"),
    )


class Epico(Base):
    __tablename__ = "epico"
    id: Mapped[int] = mapped_column(primary_key=True)
    projeto_id: Mapped[int] = mapped_column(ForeignKey("projeto.id", ondelete="CASCADE"), nullable=False, index=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    projeto: Mapped["Projeto"] = relationship(back_populates="epicos")
    historias: Mapped[list["HistoriaUsuario"]] = relationship(back_populates="epico", passive_deletes=True)
    __table_args__ = (CheckConstraint("length(trim(nome)) > 0", name="ck_epico_nome"),)


class HistoriaUsuario(Base):
    __tablename__ = "historia_usuario"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_backlog_id: Mapped[int] = mapped_column(ForeignKey("product_backlog.id", ondelete="CASCADE"), nullable=False, index=True)
    sprint_backlog_id: Mapped[int | None] = mapped_column(ForeignKey("sprint_backlog.id", ondelete="SET NULL"), index=True)
    epico_id: Mapped[int | None] = mapped_column(ForeignKey("epico.id", ondelete="SET NULL"), index=True)
    papel: Mapped[str] = mapped_column(String(100), nullable=False)
    acao: Mapped[str] = mapped_column(String(255), nullable=False)
    beneficio: Mapped[str] = mapped_column(String(255), nullable=False)
    story_points: Mapped[int | None] = mapped_column(SmallInteger)
    moscow: Mapped[str | None] = mapped_column(String(1))
    rice_reach: Mapped[int | None] = mapped_column(Integer)
    rice_impact: Mapped[Decimal | None] = mapped_column(Numeric(3, 2))
    rice_confidence: Mapped[int | None] = mapped_column(SmallInteger)
    rice_effort: Mapped[int | None] = mapped_column(SmallInteger)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="A_FAZER", server_default="A_FAZER")
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    product_backlog: Mapped["ProductBacklog"] = relationship(back_populates="historias")
    sprint_backlog: Mapped["SprintBacklog | None"] = relationship(back_populates="historias")
    epico: Mapped["Epico | None"] = relationship(back_populates="historias")
    criterios: Mapped[list["CriterioAceitacao"]] = relationship(back_populates="historia", passive_deletes=True, order_by="CriterioAceitacao.id")
    __table_args__ = (
        CheckConstraint("length(trim(papel)) > 0 AND length(trim(acao)) > 0 AND length(trim(beneficio)) > 0", name="ck_historia_campos"),
        CheckConstraint("story_points IS NULL OR story_points IN (0,1,2,3,5,8,13,21,34,55)", name="ck_historia_pontos"),
        CheckConstraint("moscow IS NULL OR moscow IN ('M','S','C','W')", name="ck_historia_moscow"),
        CheckConstraint("rice_reach IS NULL OR rice_reach >= 0", name="ck_historia_reach"),
        CheckConstraint("rice_impact IS NULL OR rice_impact IN (3,2,1,0.5,0.25)", name="ck_historia_impact"),
        CheckConstraint("rice_confidence IS NULL OR rice_confidence IN (100,80,50)", name="ck_historia_confidence"),
        CheckConstraint("rice_effort IS NULL OR rice_effort IN (0,1,2,3,5,8,13,21,34,55)", name="ck_historia_effort"),
        CheckConstraint("status IN ('A_FAZER','EM_ANDAMENTO','CONCLUIDA')", name="ck_historia_status"),
    )


class CriterioAceitacao(Base):
    __tablename__ = "criterio_aceitacao"
    id: Mapped[int] = mapped_column(primary_key=True)
    historia_usuario_id: Mapped[int] = mapped_column(ForeignKey("historia_usuario.id", ondelete="CASCADE"), nullable=False, index=True)
    dado: Mapped[str] = mapped_column(String(255), nullable=False)
    quando: Mapped[str] = mapped_column(String(255), nullable=False)
    entao: Mapped[str] = mapped_column(String(255), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    historia: Mapped["HistoriaUsuario"] = relationship(back_populates="criterios")
    __table_args__ = (CheckConstraint("length(trim(dado)) > 0 AND length(trim(quando)) > 0 AND length(trim(entao)) > 0", name="ck_criterio_campos"),)
