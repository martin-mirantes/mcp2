# app/models/all_models.py
# -*- coding: utf-8 -*-
# (Modelos Ultra-Simplificados com JSONB)

from typing import Optional, Dict, Any, List # Adicionar List se necessário para JSON
from sqlmodel import SQLModel, Field, Column # Relationship não é mais usado aqui
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
import datetime
# from decimal import Decimal # Não mais necessário se preços estão no JSON como float/str

# --- Definição de Classes ---

class Obra(SQLModel, table=True):
    __tablename__ = "obras" # Boa prática especificar

    id: Optional[int] = Field(default=None, primary_key=True)
    dados: Optional[Dict[str, Any]] = Field(
        default_factory=dict, # Para garantir que seja um dict se não fornecido
        sa_column=sa.Column(JSONB)
    )
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    )

class Pessoa(SQLModel, table=True): # Nome da classe no singular
    __tablename__ = "pessoas"

    id: Optional[int] = Field(default=None, primary_key=True)
    dados: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        sa_column=sa.Column(JSONB)
    )
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    )

class Tarefa(SQLModel, table=True):
    __tablename__ = "tarefas"

    id: Optional[int] = Field(default=None, primary_key=True)
    dados: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        sa_column=sa.Column(JSONB)
    )
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    )

# Não há mais TiposTarefa, PrecosTarefaLocal, nem tabelas de junção como modelos SQLModel diretos.
# As relações e os dados específicos estão agora embutidos nos campos 'dados' JSONB.

