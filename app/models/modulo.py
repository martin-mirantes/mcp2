# app/models/modulo.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
import datetime

# Adelanta declaraciones
if TYPE_CHECKING:
    from .obra import Obra
    from .bloco import Bloco
    from .local import LocalAreaComumModulo # Importa a classe específica

class Modulo(SQLModel, table=True):
    """Representa um módulo dentro de uma obra."""
    # __tablename__ = 'modulos'

    # Define constraints multi-coluna aqui
    __table_args__ = (
        sa.UniqueConstraint("obra_id", "nome", name="unique_obra_nome"),
    )

    # Colunas
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID único do módulo (PK)."
    )
    nome: str = Field(
        sa_column=sa.Column(sa.Text, nullable=False),
        description="Nome do módulo (NOT NULL, unique within obra)."
    )
    obra_id: int = Field(
        foreign_key="obras.obra_id", # Referencia a PK correta de Obras
        index=True, # Baseado no índice idx_modulos_obra_id
        nullable=False,
        description="ID da obra à qual pertence (FK, NOT NULL)."
    )
    # O dump não mostrava created_at, mas vamos adicionar por consistência
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        description="Timestamp de criação."
    )


    # Relacionamentos
    obra: "Obra" = Relationship(back_populates="modulos")
    blocos: List["Bloco"] = Relationship(back_populates="modulo")
    # A relação com LocalAreaComumModulo está na outra classe
    locais_area_comum: List["LocalAreaComumModulo"] = Relationship(back_populates="modulo")

