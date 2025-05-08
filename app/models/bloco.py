# app/models/bloco.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
import datetime

# Adelanta declaraciones
if TYPE_CHECKING:
    from .modulo import Modulo
    from .pavimento import Pavimento
    from .local import ( # Importa las clases específicas que se relacionan con Bloco
        LocalAreaComumExternaBloco,
        LocalAreaComumFachadaBloco,
        LocalAreaComumInternaBloco
    )

class Bloco(SQLModel, table=True):
    """Representa um bloco dentro de um módulo."""
    # __tablename__ = 'blocos'

    # Constraints multi-coluna
    __table_args__ = (
        sa.UniqueConstraint("modulo_id", "nome", name="unique_modulo_nome"),
    )

    # Colunas
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID único do bloco (PK)."
    )
    nome: str = Field(
        sa_column=sa.Column(sa.Text, nullable=False),
        description="Nome do bloco (NOT NULL, unique within modulo)."
    )
    modulo_id: int = Field(
        foreign_key="modulos.id",
        index=True, # Baseado no idx_blocos_modulo_id
        nullable=False,
        description="ID do módulo ao qual pertence (FK, NOT NULL)."
    )
    # O dump não mostrava created_at, mas vamos adicionar por consistência
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        description="Timestamp de criação."
    )

    # Relacionamentos
    modulo: "Modulo" = Relationship(back_populates="blocos")
    pavimentos: List["Pavimento"] = Relationship(back_populates="bloco")
    # Relacionamentos com os tipos de locais específicos
    locais_area_externa: List["LocalAreaComumExternaBloco"] = Relationship(back_populates="bloco")
    locais_fachada: List["LocalAreaComumFachadaBloco"] = Relationship(back_populates="bloco")
    locais_area_interna: List["LocalAreaComumInternaBloco"] = Relationship(back_populates="bloco")

