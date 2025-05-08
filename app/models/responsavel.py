# app/models/responsavel.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
import datetime
from decimal import Decimal

# Adelanta declaraciones
if TYPE_CHECKING:
    from .obra import Obras
    from .tarefa_responsavel import TarefaResponsaveis # Importa el modelo de enlace

class Responsavel(SQLModel, table=True):
    """Representa um trabalhador ou responsável."""
    # __tablename__ = 'responsaveis' # Inferido

    # Constraints
    __table_args__ = (
        sa.UniqueConstraint("nome", name="responsaveis_nome_key"),
    )

    # Colunas
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID único do responsável (PK)."
    )
    nome: str = Field(
        sa_column=sa.Column(sa.Text, nullable=False),
        # unique=True, # <<-- REMOVIDO daqui (já está em __table_args__)
        description="Nome completo do responsável (NOT NULL, UNIQUE)."
    )
    matricula: Optional[Decimal] = Field(
        default=None,
        sa_column=sa.Column(sa.Numeric),
        description="Matrícula do funcionário."
    )
    funcao: Optional[str] = Field(
        default=None,
        sa_column=sa.Column(sa.Text),
        description="Cargo/Função do responsável."
    )
    data_admissao: Optional[datetime.date] = Field(
        default=None,
        description="Data de admissão."
    )
    situacao: Optional[str] = Field(
        default=None,
        sa_column=sa.Column(sa.Text),
        description="Situação atual (ex: 'Ativo', 'Afastado')."
    )
    salario_categoria: Optional[Decimal] = Field(
        default=None,
        sa_column=sa.Column(sa.Numeric),
        description="Salário base da categoria."
    )
    obra_id: Optional[int] = Field(
        default=None,
        foreign_key="obras.obra_id",
        index=True, # Baseado no idx_responsaveis_obra_id
        description="ID da obra principal à qual está associado (FK, NULL)."
    )
    # created_at não estava no dump original, mas pode ser adicionado se necessário
    # created_at: Optional[datetime.datetime] = Field(...)

    # Relacionamentos
    obra: Optional["Obras"] = Relationship(back_populates="responsaveis")
    # Relação com a tabela de junção TarefaResponsaveis
    tarefas_atribuidas: List["TarefaResponsaveis"] = Relationship(back_populates="responsavel")

