# app/models/pavimento.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
import datetime

# Adelanta declaraciones
if TYPE_CHECKING:
    from .bloco import Bloco
    from .apartamento import Apartamento

class Pavimento(SQLModel, table=True):
    """Representa um pavimento (piso) dentro de um bloco."""
    # __tablename__ = 'pavimentos'

    # Constraints multi-coluna
    __table_args__ = (
        sa.UniqueConstraint("bloco_id", "nome", name="unique_bloco_nome"),
    )

    # Colunas
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID único do pavimento (PK)."
    )
    nome: str = Field(
        sa_column=sa.Column(sa.Text, nullable=False),
        description="Nome/Número do pavimento (ex: 'Térreo', '01', NOT NULL, unique within bloco)."
    )
    bloco_id: int = Field(
        foreign_key="blocos.id",
        index=True, # Baseado no idx_pavimentos_bloco_id
        nullable=False,
        description="ID do bloco ao qual pertence (FK, NOT NULL)."
    )
    # O dump não mostrava created_at, mas vamos adicionar por consistência
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        description="Timestamp de criação."
    )

    # Relacionamentos
    bloco: "Bloco" = Relationship(back_populates="pavimentos")
    apartamentos: List["Apartamento"] = Relationship(back_populates="pavimento")

