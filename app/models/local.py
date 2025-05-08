# app/models/local.py
# Importações padrão
from typing import List, Optional, TYPE_CHECKING, Any
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
import datetime
from decimal import Decimal

# Importar o Enum definido anteriormente
from .enums import TipoLocal

# Adelanta declaraciones para type hints dentro de if TYPE_CHECKING
if TYPE_CHECKING:
    from .obra import Obras
    from .modulo import Modulo
    from .bloco import Bloco
    from .apartamento import Apartamentos
    from .preco import PrecosTarefaLocal
    from .tarefa import Tarefa

# --- Classe Base ---
class Locais(SQLModel, table=True):
    """
    Tabela base para todos os tipos de locais. Contém informações comuns
    e o tipo específico (discriminador).
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo_local: TipoLocal = Field(
        sa_column=sa.Column(PgEnum(TipoLocal, name='tipo_local_enum', create_type=False), nullable=False, index=True),
        description="Discriminador que indica o tipo específico de local."
    )
    nome_display: str = Field(max_length=350, nullable=False)
    obra_id: int = Field(foreign_key="obras.obra_id", index=True, nullable=False)
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    )

    __mapper_args__ = {
        "polymorphic_identity": "locais_base",
        "polymorphic_on": "tipo_local",
    }

    # Relacionamentos - Usar strings para forward references
    obra: "Obras" = Relationship(back_populates="locais")
    precos_tarefa_local: List["PrecosTarefaLocal"] = Relationship(back_populates="local")
    tarefas: List["Tarefa"] = Relationship(back_populates="local")
    # <<<--- GARANTIR QUE NÃO HÁ NENHUM Relationship para Apartamentos AQUI ---<<<


# --- Classes Específicas ---

class LocalAmbienteInternoApartamento(Locais, table=True):
    """Local específico: Ambiente dentro de um Apartamento."""
    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    apartamento_id: int = Field(foreign_key="apartamentos.id", index=True, nullable=False)
    nome_ambiente: str = Field(max_length=150, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoLocal.AMBIENTE_INTERNO_APARTAMENTO}

    apartamento: "Apartamentos" = Relationship(back_populates="locais_ambiente_interno")


class LocalApartamento(Locais, table=True):
    """Local específico: Referência a um Apartamento como um todo."""
    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    apartamento_id: int = Field(foreign_key="apartamentos.id", index=True, nullable=False)
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    )

    __mapper_args__ = {"polymorphic_identity": TipoLocal.APARTAMENTO}

    apartamento: "Apartamentos" = Relationship(back_populates="locais_apartamento")


class LocalAreaComumInternaBloco(Locais, table=True):
    """Local específico: Área comum interna de um Bloco."""
    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    bloco_id: int = Field(foreign_key="blocos.id", index=True, nullable=False)
    nome_area: str = Field(max_length=150, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_INTERNA_BLOCO}

    bloco: "Bloco" = Relationship(back_populates="locais_area_interna")


class LocalAreaComumFachadaBloco(Locais, table=True):
    """Local específico: Fachada de um Bloco."""
    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    bloco_id: int = Field(foreign_key="blocos.id", index=True, nullable=False)
    pano_vertical: str = Field(max_length=100, nullable=False)
    pavimento_referencia: str = Field(max_length=50, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_FACHADA_BLOCO}

    bloco: "Bloco" = Relationship(back_populates="locais_fachada")


class LocalAreaComumExternaBloco(Locais, table=True):
    """Local específico: Área comum externa de um Bloco."""
    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    bloco_id: int = Field(foreign_key="blocos.id", index=True, nullable=False)
    nome_area: str = Field(max_length=150, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_EXTERNA_BLOCO}

    bloco: "Bloco" = Relationship(back_populates="locais_area_externa")


class LocalAreaComumModulo(Locais, table=True):
    """Local específico: Área comum de um Módulo."""
    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    modulo_id: int = Field(foreign_key="modulos.id", index=True, nullable=False)
    nome_area: str = Field(max_length=150, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_MODULO}

    modulo: "Modulo" = Relationship(back_populates="locais_area_comum")


class LocalRua(Locais, table=True):
    """Local específico: Rua."""
    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    nome_rua: str = Field(max_length=255, index=True, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoLocal.RUA}

