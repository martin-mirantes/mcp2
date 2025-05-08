# app/models/tipo_tarefa.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
import datetime

# Adelanta declaraciones
if TYPE_CHECKING:
    from .preco import PrecosTarefaLocal
    from .tarefa import Tarefa

class TiposTarefa(SQLModel, table=True):
    """Define os diferentes tipos de tarefas que podem ser realizadas."""
    # __tablename__ = 'tipos_tarefas' # Inferido

    # Constraints
    __table_args__ = (
        sa.UniqueConstraint("nome", name="tipos_tarefas_nome_key"),
    )

    # Colunas
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID único do tipo de tarefa (PK)."
    )
    nome: str = Field(
        max_length=255, # Baseado no VARCHAR(255)
        nullable=False,
        unique=True, # Já coberto pelo UniqueConstraint
        index=True, # Baseado no idx_tipos_tarefas_nome
        description="Nome do tipo de tarefa (NOT NULL, UNIQUE)."
    )
    funcao: Optional[str] = Field(
        default=None,
        sa_column=sa.Column(sa.Text),
        description="Função geralmente associada a este tipo de tarefa (ex: 'PINTOR')."
    )
    # Adicionando created_at para consistência
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        description="Timestamp de criação."
    )

    # Relacionamentos
    precos_tarefa_local: List["PrecosTarefaLocal"] = Relationship(back_populates="tipos_tarefa")
    tarefas: List["Tarefa"] = Relationship(back_populates="tipos_tarefa")

