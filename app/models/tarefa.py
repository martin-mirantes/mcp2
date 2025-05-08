# app/models/tarefa.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
import datetime
from decimal import Decimal # Importar se for usar Decimal para outras coisas

# Adelanta declaraciones
if TYPE_CHECKING:
    from .local import Locais
    from .tipo_tarefa import TiposTarefa
    from .preco import PrecosTarefaLocal
    from .tarefa_responsavel import TarefaResponsaveis # Importa o modelo de junção

class Tarefa(SQLModel, table=True):
    """Representa uma tarefa a ser realizada."""
    # __tablename__ = 'tarefas' # Inferido

    # Colunas
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID único da tarefa (PK)."
    )
    nome: str = Field(
        sa_column=sa.Column(sa.Text, nullable=False),
        description="Nome ou descrição curta da tarefa (NOT NULL)."
    )
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        description="Timestamp de criação."
    )
    inicio: Optional[datetime.date] = Field(
        default=None,
        description="Data de início planejada ou real."
    )
    fim: Optional[datetime.date] = Field(
        default=None,
        description="Data de fim planejada ou real."
    )
    local_id: Optional[int] = Field(
        default=None,
        foreign_key="locais.id",
        index=True, # Baseado no idx_tarefas_local_id
        description="ID do local onde a tarefa é realizada (FK, NULL)."
    )
    tipos_tarefa_id: Optional[int] = Field(
        default=None,
        foreign_key="tipos_tarefas.id",
        index=True, # Baseado no idx_tarefas_tipos_tarefa_id
        description="ID do tipo de tarefa (FK, NULL)."
    )
    preco_tarefa_local_id: Optional[int] = Field(
        default=None,
        foreign_key="precos_tarefa_local.id",
        index=True, # Baseado no idx_tarefas_preco_id
        description="ID da referência ao preço padrão aplicável (FK, NULL)."
    )

    # Relacionamentos
    local: Optional["Locais"] = Relationship(back_populates="tarefas")
    tipos_tarefa: Optional["TiposTarefa"] = Relationship(back_populates="tarefas")
    preco_tarefa_local: Optional["PrecosTarefaLocal"] = Relationship(back_populates="tarefas")
    # Relação com a tabela de junção TarefaResponsaveis
    responsaveis_link: List["TarefaResponsaveis"] = Relationship(back_populates="tarefa")

