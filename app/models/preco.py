# app/models/preco.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
import datetime
from decimal import Decimal

# Adelanta declaraciones
if TYPE_CHECKING:
    from .local import Locais
    from .tipo_tarefa import TiposTarefa
    from .tarefa import Tarefa

class PrecosTarefaLocal(SQLModel, table=True):
    """Armazena os preços padrão para uma combinação de tipo de tarefa e local."""
    # __tablename__ = 'precos_tarefa_local' # Inferido

    # Constraints
    __table_args__ = (
        sa.CheckConstraint('preco >= 0', name='precos_tarefa_local_preco_check'),
        # A constraint UNIQUE é complexa para definir aqui por causa do DEFERRABLE,
        # mas o SQLAlchemy geralmente a cria corretamente baseado no schema.
        # Se necessário, pode ser adicionada manualmente via Alembic.
        sa.UniqueConstraint('tipos_tarefa_id', 'local_id', 'unidade_medida', name='uq_preco_tipo_local_unidade', deferrable=True, initially="DEFERRED"),
    )

    # Colunas
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID único do registro de preço (PK)."
    )
    tipos_tarefa_id: int = Field(
        foreign_key="tipos_tarefas.id",
        index=True, # Baseado no idx_precos_tipo_tarefa
        nullable=False,
        description="ID do tipo de tarefa (FK, NOT NULL)."
    )
    local_id: int = Field(
        foreign_key="locais.id",
        index=True, # Baseado no idx_precos_local
        nullable=False,
        description="ID do local (FK, NOT NULL)."
    )
    preco: Decimal = Field(
        sa_column=sa.Column(sa.Numeric(12, 2), nullable=False),
        description="Preço definido para esta combinação (NOT NULL, >= 0)."
    )
    unidade_medida: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Unidade de medida para o preço (ex: 'm²', 'unidade', 'hora')."
    )
    validade_inicio: Optional[datetime.date] = Field(
        default=None, # O default CURRENT_DATE é do DB, não do modelo Python
        sa_column=sa.Column(sa.Date, server_default=sa.text('CURRENT_DATE')),
        index=True, # Parte do idx_precos_validade
        description="Início da validade do preço."
    )
    validade_fim: Optional[datetime.date] = Field(
        default=None,
        index=True, # Parte do idx_precos_validade
        description="Fim da validade do preço (NULL = vigente)."
    )
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        description="Timestamp de criação."
    )

    # Relacionamentos
    local: "Locais" = Relationship(back_populates="precos_tarefa_local")
    tipos_tarefa: "TiposTarefa" = Relationship(back_populates="precos_tarefa_local")
    tarefas: List["Tarefa"] = Relationship(back_populates="preco_tarefa_local") # Relação inversa com Tarefa

