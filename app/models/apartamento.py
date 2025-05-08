# app/models/apartamento.py
from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
import datetime

# Adelanta declaraciones
if TYPE_CHECKING:
    from .pavimento import Pavimento
    # Importa las clases específicas de Local que se relacionan con Apartamento
    from .local import LocalApartamento, LocalAmbienteInternoApartamento

class Apartamento(SQLModel, table=True):
    """Representa um apartamento ou unidade dentro de um pavimento."""
    # __tablename__ = 'apartamentos'

    # Constraints multi-coluna
    __table_args__ = (
        sa.UniqueConstraint("pavimento_id", "nome", name="unique_pavimento_nome"),
    )

    # Colunas
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID único do apartamento (PK)."
    )
    nome: str = Field(
        sa_column=sa.Column(sa.Text, nullable=False),
        description="Nome/Número do apartamento (ex: '101', '205B', NOT NULL, unique within pavimento)."
    )
    pavimento_id: int = Field(
        foreign_key="pavimentos.id",
        index=True, # Baseado no idx_apartamentos_pavimento_id
        nullable=False,
        description="ID do pavimento ao qual pertence (FK, NOT NULL)."
    )
    # O dump não mostrava created_at, mas vamos adicionar por consistência
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        description="Timestamp de criação."
    )

    # Relacionamentos
    pavimento: "Pavimento" = Relationship(back_populates="apartamentos")
    # Relación con los locales que son de tipo APARTAMENTO
    locais_apartamento: List["LocalApartamento"] = Relationship(back_populates="apartamento")
    # Relación con los locales que son de tipo AMBIENTE_INTERNO_APARTAMENTO
    locais_ambiente_interno: List["LocalAmbienteInternoApartamento"] = Relationship(back_populates="apartamento")

