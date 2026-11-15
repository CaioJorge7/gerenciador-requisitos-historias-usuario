"""Contratos Pydantic para formulario e API. Rejeicao uniforme de valores invalidos."""
from datetime import datetime, date
from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator

class Out(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)

    @field_validator("nome")
    @classmethod
    def nonempty(cls, value: str):
        if not value.strip(): raise ValueError("Nome é obrigatório")
        return value.strip()

class Login(BaseModel):
    email: EmailStr
    senha: str

class UsuarioOut(Out):
    id: int
    nome: str
    email: EmailStr
    criado_em: datetime

class NomeNotBlank(BaseModel):
    @field_validator("nome", check_fields=False)
    @classmethod
    def valid_name(cls, value: str | None):
        if value is None or not value.strip(): raise ValueError("O nome não pode estar vazio")
        return value.strip()

class ProjetoCreate(NomeNotBlank):
    nome: str = Field(min_length=1, max_length=120)
    descricao: str | None = None

class ProjetoUpdate(NomeNotBlank):
    nome: str | None = Field(default=None, min_length=1, max_length=120)
    descricao: str | None = None

class ProjetoOut(Out):
    id: int
    usuario_id: int
    nome: str
    descricao: str | None
    criado_em: datetime

class BacklogCreate(NomeNotBlank):
    nome: str = Field(min_length=1, max_length=120)

class BacklogUpdate(NomeNotBlank):
    nome: str = Field(min_length=1, max_length=120)

class BacklogOut(Out):
    id: int
    projeto_id: int
    nome: str
    criado_em: datetime
    total_historias: int = 0

class SprintBase(NomeNotBlank):
    nome: str = Field(min_length=1, max_length=120)
    objetivo: str | None = None
    data_inicio: date | None = None
    data_fim: date | None = None

    @model_validator(mode="after")
    def valid_dates(self):
        if self.data_inicio and self.data_fim and self.data_fim < self.data_inicio:
            raise ValueError("A data final não pode anteceder a data inicial")
        return self

class SprintCreate(SprintBase):
    pass
class SprintUpdate(SprintBase):
    pass
class SprintOut(Out):
    id: int
    projeto_id: int
    nome: str
    objetivo: str | None
    data_inicio: date | None
    data_fim: date | None
    criado_em: datetime
    total_historias: int = 0

class EpicoCreate(NomeNotBlank):
    nome: str = Field(min_length=1, max_length=150)
    descricao: str | None = None
class EpicoUpdate(EpicoCreate):
    pass
class EpicoOut(Out):
    id: int
    projeto_id: int
    nome: str
    descricao: str | None
    criado_em: datetime
    total_historias: int = 0

STORY_POINTS = {0,1,2,3,5,8,13,21,34,55}
IMPACTS = {Decimal("3.00"),Decimal("2.00"),Decimal("1.00"),Decimal("0.50"),Decimal("0.25")}
CONFIDENCES = {100,80,50}
MOSCOW = {"M","S","C","W"}
STATUS = {"A_FAZER","EM_ANDAMENTO","CONCLUIDA"}

class HistoriaBase(BaseModel):
    papel: str = Field(min_length=1, max_length=100)
    acao: str = Field(min_length=1, max_length=255)
    beneficio: str = Field(min_length=1, max_length=255)
    epico_id: int | None = None
    sprint_backlog_id: int | None = None
    story_points: int | None = None
    moscow: str | None = None
    rice_reach: int | None = Field(default=None, ge=0)
    rice_impact: Decimal | None = None
    rice_confidence: int | None = None
    rice_effort: int | None = None
    status: str = "A_FAZER"

    @field_validator("papel", "acao", "beneficio")
    @classmethod
    def non_blank(cls, v: str):
        if not v.strip(): raise ValueError("Campo obrigatório")
        return v.strip()

    @field_validator("story_points", "rice_effort")
    @classmethod
    def valid_points(cls, v):
        if v is not None and v not in STORY_POINTS: raise ValueError("Valores permitidos: 0, 1, 2, 3, 5, 8, 13, 21, 34, 55")
        return v
    @field_validator("moscow")
    @classmethod
    def valid_moscow(cls, v):
        if v is not None and v not in MOSCOW: raise ValueError("Valores permitidos: M, S, C, W")
        return v
    @field_validator("rice_impact")
    @classmethod
    def valid_impact(cls, v):
        if v is not None and v not in IMPACTS: raise ValueError("Valores permitidos: 3, 2, 1, 0.5, 0.25")
        return v
    @field_validator("rice_confidence")
    @classmethod
    def valid_confidence(cls, v):
        if v is not None and v not in CONFIDENCES: raise ValueError("Valores permitidos: 100, 80, 50")
        return v
    @field_validator("status")
    @classmethod
    def valid_status(cls, v):
        if v not in STATUS: raise ValueError("Valores permitidos: A_FAZER, EM_ANDAMENTO, CONCLUIDA")
        return v

class HistoriaCreate(HistoriaBase):
    pass
class HistoriaUpdate(HistoriaBase):
    pass
class MoveStory(BaseModel):
    sprint_backlog_id: int | None = None
class CriterioCreate(BaseModel):
    dado: str = Field(min_length=1, max_length=255)
    quando: str = Field(min_length=1, max_length=255)
    entao: str = Field(min_length=1, max_length=255)

    @field_validator("dado", "quando", "entao")
    @classmethod
    def trim(cls, v):
        if not v.strip(): raise ValueError("Campo obrigatório")
        return v.strip()
class CriterioUpdate(CriterioCreate):
    pass
class CriterioOut(Out):
    id: int
    historia_usuario_id: int
    dado: str
    quando: str
    entao: str
    criado_em: datetime

class HistoriaOut(Out):
    id: int
    product_backlog_id: int
    sprint_backlog_id: int | None
    epico_id: int | None
    papel: str
    acao: str
    beneficio: str
    story_points: int | None
    moscow: str | None
    rice_reach: int | None
    rice_impact: Decimal | None
    rice_confidence: int | None
    rice_effort: int | None
    status: str
    criado_em: datetime
    texto: str
    rice_score: str | None
    rice_estado: str
    epico_nome: str | None = None
    sprint_nome: str | None = None
    criterios: list[CriterioOut] = Field(default_factory=list)
