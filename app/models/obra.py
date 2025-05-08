# app/models/obra.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa # Import sqlalchemy para usar text() ou tipos específicos

# Adelanta declaraciones para evitar importación circular en type hints
if TYPE_CHECKING:
    from .modulo import Modulo
    from .local import Locais
    from .responsavel import Responsavel

class Obra(SQLModel, table=True):
    """Representa uma obra ou projeto principal."""
    # __tablename__ = 'obras' # SQLModel infere 'obras' do nome da classe

    # Colunas
    obra_id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID único da obra (PK)."
    )
    nome: str = Field(
        sa_column=sa.Column(sa.Text, nullable=False), # Usando sa.Column para tipo TEXT
        description="Nome da obra (NOT NULL)."
    )

    # Relacionamentos (o back_populates deve coincidir com o nome do atributo na outra classe)
    modulos: List["Modulo"] = Relationship(back_populates="obra")
    locais: List["Locais"] = Relationship(back_populates="obra")
    responsaveis: List["Responsavel"] = Relationship(back_populates="obra")

