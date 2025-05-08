# app/models/tarefa_responsavel.py
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
from decimal import Decimal

# Adelanta declaraciones
if TYPE_CHECKING:
    from .tarefa import Tarefa
    from .responsavel import Responsavel

class TarefaResponsaveis(SQLModel, table=True):
    """
    Modelo para a tabela de junção entre Tarefas e Responsaveis.
    Armazena o percentual de responsabilidade e indica o principal.
    """
    # __tablename__ = 'tarefa_responsaveis' # Inferido

    # Constraints
    # O CHECK constraint é definido diretamente no Field ou via __table_args__
    # A PK composta é definida nos Fields com primary_key=True
    __table_args__ = (
        sa.CheckConstraint('percentual > 0 AND percentual <= 100.00', name='tarefa_responsaveis_percentual_check'),
        # Trigger para soma 100% é definido separadamente no DB
    )

    # Colunas que formam a Chave Primária Composta e são Chaves Estrangeiras
    tarefa_id: int = Field(
        foreign_key="tarefas.id",
        primary_key=True, # Parte da PK composta
        index=True, # Baseado no idx_tarefarespon_tarefa_id
        description="ID da tarefa (PK, FK)."
    )
    responsavel_id: int = Field(
        foreign_key="responsaveis.id",
        primary_key=True, # Parte da PK composta
        index=True, # Baseado no idx_tarefarespon_responsavel_id
        description="ID do responsável (PK, FK)."
    )

    # Atributos específicos da relação
    percentual: Decimal = Field(
        sa_column=sa.Column(sa.Numeric(5, 2), nullable=False, server_default=sa.text('100.00')),
        default=Decimal("100.00"), # Default Python
        description="Percentual de responsabilidade (0 < p <= 100.00)."
    )
    eh_principal: bool = Field(
        default=False, # Default Python
        sa_column=sa.Column(sa.Boolean, nullable=False, server_default=sa.text('false')),
        description="Indica se é o responsável principal pela tarefa."
    )

    # Relacionamentos para navegar a partir desta tabela de junção
    tarefa: "Tarefa" = Relationship(back_populates="responsaveis_link")
    responsavel: "Responsavel" = Relationship(back_populates="tarefas_atribuidas")

