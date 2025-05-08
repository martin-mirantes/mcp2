# app/models/apartamento.py
from typing import List, Optional, TYPE_CHECKING
# Certifique-se de importar Field, Relationship, SQLModel, Column, etc.
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
import datetime

# Adelanta declaraciones para type hints dentro de if TYPE_CHECKING
# Isso ajuda linters como Pylance a resolver as referências futuras
if TYPE_CHECKING:
    from .pavimento import Pavimento
    # Importa as classes específicas de Local que se relacionam com Apartamento
    from .local import LocalApartamento, LocalAmbienteInternoApartamento

class Apartamentos(SQLModel, table=True):
    """Representa um apartamento ou unidade dentro de um pavimento."""
    # __tablename__ = 'apartamentos' # Inferido

    # Constraints multi-coluna
    __table_args__ = (
        sa.UniqueConstraint("pavimento_id", "nome", name="unique_pavimento_nome"),
    )

    # --- Colunas ---
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID único do apartamento (PK)."
    )
    nome: str = Field(
        sa_column=sa.Column(sa.Text, nullable=False), # Usando sa.Column para Text
        description="Nome/Número do apartamento (ex: '101', '205B', NOT NULL, unique within pavimento)."
    )
    pavimento_id: int = Field(
        foreign_key="pavimentos.id",
        index=True, # Baseado no idx_apartamentos_pavimento_id
        nullable=False,
        description="ID do pavimento ao qual pertence (FK, NOT NULL)."
    )
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        description="Timestamp de criação."
    )

    # --- Relacionamentos ---
    # Usar strings para forward references e nomes de classe corretos
    pavimento: "Pavimento" = Relationship(back_populates="apartamentos")
    # Relação com os locais que são de tipo APARTAMENTO
# Em Apartamentos
    locais_apartamento: List["LocalApartamento"] = Relationship(back_populates="apartamento")
    locais_ambiente_interno: List["LocalAmbienteInternoApartamento"] = Relationship(back_populates="apartamento")

