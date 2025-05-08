# app/models/all_models.py
# -*- coding: utf-8 -*-
# (PARA DIAGNÓSTICO FINAL - TODAS as Classes Específicas de Local Comentadas)

# --- Importaciones Necesarias ---
from typing import List, Optional, Any
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
import datetime
from decimal import Decimal
from enum import Enum

# --- Enum Definido Primero ---
class TipoLocal(str, Enum):
    AMBIENTE_INTERNO_APARTAMENTO = "AMBIENTE_INTERNO_APARTAMENTO"
    AREA_COMUM_INTERNA_BLOCO = "AREA_COMUM_INTERNA_BLOCO"
    AREA_COMUM_FACHADA_BLOCO = "AREA_COMUM_FACHADA_BLOCO"
    AREA_COMUM_EXTERNA_BLOCO = "AREA_COMUM_EXTERNA_BLOCO"
    AREA_COMUM_MODULO = "AREA_COMUM_MODULO"
    RUA = "RUA"
    APARTAMENTO = "APARTAMENTO"

# --- Tablas Independientes o de Primer Nivel ---
class Obra(SQLModel, table=True):
    __tablename__ = 'obras'
    obra_id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(sa_column=sa.Column(sa.Text, nullable=False))
    modulos: List["Modulo"] = Relationship(back_populates="obra")
    locais: List["Locais"] = Relationship(back_populates="obra")
    responsaveis: List["Responsavel"] = Relationship(back_populates="obra")

class TiposTarefa(SQLModel, table=True):
    __tablename__ = 'tipos_tarefas'
    __table_args__: Any = (sa.UniqueConstraint("nome", name="tipos_tarefas_nome_key"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=255, nullable=False, unique=True, index=True)
    funcao: Optional[str] = Field(default=None, sa_column=sa.Column(sa.Text))
    created_at: Optional[datetime.datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")))
    precos_tarefa_local: List["PrecosTarefaLocal"] = Relationship(back_populates="tipos_tarefa")
    tarefas: List["Tarefa"] = Relationship(back_populates="tipos_tarefa")

# --- Tablas con Dependencias (Jerarquía) ---
class Modulo(SQLModel, table=True):
    __tablename__ = 'modulos'
    __table_args__: Any = (sa.UniqueConstraint("obra_id", "nome", name="unique_obra_nome"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(sa_column=sa.Column(sa.Text, nullable=False))
    obra_id: int = Field(foreign_key="obras.obra_id", index=True, nullable=False)
    created_at: Optional[datetime.datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")))
    obra: Obra = Relationship(back_populates="modulos")
    blocos: List["Bloco"] = Relationship(back_populates="modulo")
    # locais_area_comum: List["LocalAreaComumModulo"] = Relationship(back_populates="modulo") # Comentado por dependencia

class Bloco(SQLModel, table=True):
    __tablename__ = 'blocos'
    __table_args__: Any = (sa.UniqueConstraint("modulo_id", "nome", name="unique_modulo_nome"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(sa_column=sa.Column(sa.Text, nullable=False))
    modulo_id: int = Field(foreign_key="modulos.id", index=True, nullable=False)
    created_at: Optional[datetime.datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")))
    modulo: Modulo = Relationship(back_populates="blocos")
    pavimentos: List["Pavimento"] = Relationship(back_populates="bloco")
    # locais_area_externa: List["LocalAreaComumExternaBloco"] = Relationship(back_populates="bloco") # Comentado por dependencia
    # locais_fachada: List["LocalAreaComumFachadaBloco"] = Relationship(back_populates="bloco") # Comentado por dependencia
    # locais_area_interna: List["LocalAreaComumInternaBloco"] = Relationship(back_populates="bloco") # Comentado por dependencia

class Pavimento(SQLModel, table=True):
    __tablename__ = 'pavimentos'
    __table_args__: Any = (sa.UniqueConstraint("bloco_id", "nome", name="unique_bloco_nome"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(sa_column=sa.Column(sa.Text, nullable=False))
    bloco_id: int = Field(foreign_key="blocos.id", index=True, nullable=False)
    created_at: Optional[datetime.datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")))
    bloco: Bloco = Relationship(back_populates="pavimentos")
    apartamentos: List["Apartamentos"] = Relationship(back_populates="pavimento")

class Apartamentos(SQLModel, table=True):
    __tablename__ = 'apartamentos'
    __table_args__: Any = (sa.UniqueConstraint("pavimento_id", "nome", name="unique_pavimento_nome"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(sa_column=sa.Column(sa.Text, nullable=False))
    pavimento_id: int = Field(foreign_key="pavimentos.id", index=True, nullable=False)
    created_at: Optional[datetime.datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")))
    pavimento: Pavimento = Relationship(back_populates="apartamentos")
    # locais_apartamento: List["LocalApartamento"] = Relationship(back_populates="apartamento") # Comentado por dependencia
    # locais_ambiente_interno: List["LocalAmbienteInternoApartamento"] = Relationship(back_populates="apartamento") # Comentado por dependencia

class Responsavel(SQLModel, table=True):
    __tablename__ = 'responsaveis'
    __table_args__: Any = (sa.UniqueConstraint("nome", name="responsaveis_nome_key"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(sa_column=sa.Column(sa.Text, nullable=False))
    matricula: Optional[Decimal] = Field(default=None, sa_column=sa.Column(sa.Numeric))
    funcao: Optional[str] = Field(default=None, sa_column=sa.Column(sa.Text))
    data_admissao: Optional[datetime.date] = Field(default=None)
    situacao: Optional[str] = Field(default=None, sa_column=sa.Column(sa.Text))
    salario_categoria: Optional[Decimal] = Field(default=None, sa_column=sa.Column(sa.Numeric))
    obra_id: Optional[int] = Field(default=None, foreign_key="obras.obra_id", index=True)
    obra: Optional[Obra] = Relationship(back_populates="responsaveis")
    tarefas_atribuidas: List["TarefaResponsaveis"] = Relationship(back_populates="responsavel")

# --- Hierarquia Polimórfica de Locais (Base) ---
class Locais(SQLModel, table=True):
    __tablename__ = 'locais'
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo_local: TipoLocal = Field(
        sa_column=sa.Column(PgEnum(TipoLocal, name='tipo_local_enum', create_type=False), nullable=False, index=True),
        description="Discriminador que indica o tipo específico de local."
    )
    nome_display: str = Field(max_length=350, nullable=False)
    obra_id: int = Field(foreign_key="obras.obra_id", index=True, nullable=False)
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    )
    # __mapper_args__ pode precisar ser comentado se causar problemas sem as classes filhas
    # __mapper_args__ = {
    #     "polymorphic_identity": "locais_base",
    #     "polymorphic_on": "tipo_local",
    # }
    obra: Obra = Relationship(back_populates="locais")
    precos_tarefa_local: List["PrecosTarefaLocal"] = Relationship(back_populates="local")
    tarefas: List["Tarefa"] = Relationship(back_populates="local")

# --- Classes Específicas de Local (COMENTADAS PARA DIAGNÓSTICO) ---
# class LocalAmbienteInternoApartamento(Locais, table=True):
#     __tablename__ = 'local_ambiente_interno_apartamento'
#     local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
#     apartamento_id: int = Field(foreign_key="apartamentos.id", index=True, nullable=False)
#     nome_ambiente: str = Field(max_length=150, nullable=False)
#     __mapper_args__ = {"polymorphic_identity": TipoLocal.AMBIENTE_INTERNO_APARTAMENTO}
#     apartamento: Apartamentos = Relationship(back_populates="locais_ambiente_interno")

# class LocalApartamento(Locais, table=True):
#     __tablename__ = 'local_apartamento'
#     local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
#     apartamento_id: int = Field(foreign_key="apartamentos.id", index=True, nullable=False)
#     created_at: Optional[datetime.datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")))
#     __mapper_args__ = {"polymorphic_identity": TipoLocal.APARTAMENTO}
#     apartamento: Apartamentos = Relationship(back_populates="locais_apartamento")

# class LocalAreaComumInternaBloco(Locais, table=True):
#     __tablename__ = 'local_area_comum_interna_bloco'
#     local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
#     bloco_id: int = Field(foreign_key="blocos.id", index=True, nullable=False)
#     nome_area: str = Field(max_length=150, nullable=False)
#     __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_INTERNA_BLOCO}
#     bloco: Bloco = Relationship(back_populates="locais_area_interna")

# class LocalAreaComumFachadaBloco(Locais, table=True):
#     __tablename__ = 'local_area_comum_fachada_bloco'
#     local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
#     bloco_id: int = Field(foreign_key="blocos.id", index=True, nullable=False)
#     pano_vertical: str = Field(max_length=100, nullable=False)
#     pavimento_referencia: str = Field(max_length=50, nullable=False)
#     __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_FACHADA_BLOCO}
#     bloco: Bloco = Relationship(back_populates="locais_fachada")

# class LocalAreaComumExternaBloco(Locais, table=True):
#     __tablename__ = 'local_area_comum_externa_bloco'
#     local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
#     bloco_id: int = Field(foreign_key="blocos.id", index=True, nullable=False)
#     nome_area: str = Field(max_length=150, nullable=False)
#     __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_EXTERNA_BLOCO}
#     bloco: Bloco = Relationship(back_populates="locais_area_externa")

# class LocalAreaComumModulo(Locais, table=True):
#     __tablename__ = 'local_area_comum_modulo'
#     local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
#     modulo_id: int = Field(foreign_key="modulos.id", index=True, nullable=False)
#     nome_area: str = Field(max_length=150, nullable=False)
#     __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_MODULO}
#     modulo: Modulo = Relationship(back_populates="locais_area_comum")

# class LocalRua(Locais, table=True):
#     __tablename__ = 'local_rua'
#     local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
#     nome_rua: str = Field(max_length=255, index=True, nullable=False)
#     __mapper_args__ = {"polymorphic_identity": TipoLocal.RUA}

# --- Tabelas Finais com Dependências ---
class PrecosTarefaLocal(SQLModel, table=True):
    __tablename__ = 'precos_tarefa_local'
    __table_args__: Any = (
        sa.CheckConstraint('preco >= 0', name='precos_tarefa_local_preco_check'),
        sa.UniqueConstraint('tipos_tarefa_id', 'local_id', 'unidade_medida', name='uq_preco_tipo_local_unidade', deferrable=True, initially="DEFERRED"),
        sa.Index('idx_precos_validade', 'validade_inicio', 'validade_fim'),
    )
    id: Optional[int] = Field(default=None, primary_key=True)
    tipos_tarefa_id: int = Field(foreign_key="tipos_tarefas.id", index=True, nullable=False)
    local_id: int = Field(foreign_key="locais.id", index=True, nullable=False)
    preco: Decimal = Field(sa_column=sa.Column(sa.Numeric(12, 2), nullable=False))
    unidade_medida: Optional[str] = Field(default=None, max_length=50)
    validade_inicio: Optional[datetime.date] = Field(default=None, sa_column=sa.Column(sa.Date, server_default=sa.text('CURRENT_DATE')))
    validade_fim: Optional[datetime.date] = Field(default=None)
    created_at: Optional[datetime.datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")))
    local: Locais = Relationship(back_populates="precos_tarefa_local")
    tipos_tarefa: TiposTarefa = Relationship(back_populates="precos_tarefa_local")
    tarefas: List["Tarefa"] = Relationship(back_populates="preco_tarefa_local")

class Tarefa(SQLModel, table=True):
    __tablename__ = 'tarefas'
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(sa_column=sa.Column(sa.Text, nullable=False))
    created_at: Optional[datetime.datetime] = Field(default=None, sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")))
    inicio: Optional[datetime.date] = Field(default=None)
    fim: Optional[datetime.date] = Field(default=None)
    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", index=True)
    tipos_tarefa_id: Optional[int] = Field(default=None, foreign_key="tipos_tarefas.id", index=True)
    preco_tarefa_local_id: Optional[int] = Field(default=None, foreign_key="precos_tarefa_local.id", index=True)
    local: Optional[Locais] = Relationship(back_populates="tarefas")
    tipos_tarefa: Optional[TiposTarefa] = Relationship(back_populates="tarefas")
    preco_tarefa_local: Optional[PrecosTarefaLocal] = Relationship(back_populates="tarefas")
    responsaveis_link: List["TarefaResponsaveis"] = Relationship(back_populates="tarefa")

class TarefaResponsaveis(SQLModel, table=True):
    __tablename__ = 'tarefa_responsaveis'
    __table_args__: Any = (
        sa.CheckConstraint('percentual > 0 AND percentual <= 100.00', name='tarefa_responsaveis_percentual_check'),
        sa.PrimaryKeyConstraint('tarefa_id', 'responsavel_id', name='tarefa_responsaveis_pkey'),
    )
    tarefa_id: int = Field(foreign_key="tarefas.id", primary_key=True, index=True)
    responsavel_id: int = Field(foreign_key="responsaveis.id", primary_key=True, index=True)
    percentual: Decimal = Field(sa_column=sa.Column(sa.Numeric(5, 2), nullable=False, server_default=sa.text('100.00')), default=Decimal("100.00"))
    eh_principal: bool = Field(default=False, sa_column=sa.Column(sa.Boolean, nullable=False, server_default=sa.text('false')))
    tarefa: Tarefa = Relationship(back_populates="responsaveis_link")
    responsavel: Responsavel = Relationship(back_populates="tarefas_atribuidas")

