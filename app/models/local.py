# app/models/local.py
from typing import List, Optional, TYPE_CHECKING, Any
from sqlmodel import SQLModel, Field, Relationship, Column
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM as PgEnum # Para mapear ao ENUM do PG
import datetime
from decimal import Decimal # Importar Decimal

# Importar o Enum definido anteriormente
from .enums import TipoLocal

# Adelanta declaraciones para type hints
if TYPE_CHECKING:
    from .obra import Obra
    from .modulo import Modulo
    from .bloco import Bloco
    from .apartamento import Apartamento
    from .preco import PrecosTarefaLocal
    from .tarefa import Tarefa

# --- Classe Base ---
class Locais(SQLModel, table=True):
    """
    Tabela base para todos os tipos de locais. Contém informações comuns
    e o tipo específico (discriminador).
    """
    # __tablename__ = 'locais' # Inferido

    # Colunas Comuns
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="ID único para qualquer tipo de local (PK)."
    )
    # Mapeia para o tipo ENUM do PostgreSQL e usa o Enum Python
    tipo_local: TipoLocal = Field(
        sa_column=sa.Column(PgEnum(TipoLocal, name='tipo_local_enum', create_type=False), nullable=False), # create_type=False porque já existe no DB
        index=True,
        description="Discriminador que indica o tipo específico de local (FK implícita para a tabela específica)."
    )
    nome_display: str = Field(
        max_length=350, # Baseado no VARCHAR(350) do seu schema
        nullable=False,
        description="Nome descritivo completo do local para exibição."
    )
    obra_id: int = Field(
        foreign_key="obras.obra_id", # FK para Obras
        index=True,
        nullable=False,
        description="ID da obra à qual o local pertence (FK, NOT NULL)."
    )
    # O dump não mostrava created_at, mas vamos adicionar por consistência
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        description="Timestamp de criação."
    )

    # Configuração de Herança Polimórfica (Joined Table Inheritance)
    __mapper_args__ = {
        "polymorphic_identity": "locais_base", # Identificador para esta classe base
        "polymorphic_on": "tipo_local",       # Coluna usada para determinar o tipo específico
    }

    # Relacionamentos (definidos na classe base, aplicáveis a todos os locais)
    obra: "Obra" = Relationship(back_populates="locais")
    precos_tarefa_local: List["PrecosTarefaLocal"] = Relationship(back_populates="local")
    tarefas: List["Tarefa"] = Relationship(back_populates="local")


# --- Classes Específicas ---

class LocalAmbienteInternoApartamento(Locais, table=True):
    """Local específico: Ambiente dentro de um Apartamento."""
    # __tablename__ = 'local_ambiente_interno_apartamento' # Inferido

    # Chave Primária / Estrangeira para a tabela base 'locais'
    local_id: Optional[int] = Field(
        default=None,
        foreign_key="locais.id",
        primary_key=True,
        description="ID que vincula à tabela base 'locais' (PK, FK)."
    )
    # Chave Estrangeira para 'apartamentos'
    apartamento_id: int = Field(
        foreign_key="apartamentos.id",
        index=True, # Baseado no índice idx_local_ambiente_apto_id
        nullable=False,
        description="ID do apartamento ao qual este ambiente pertence (FK, NOT NULL)."
    )
    # Campo específico
    nome_ambiente: str = Field(
        max_length=150,
        nullable=False,
        description="Nome do ambiente (ex: 'Sala', 'Cozinha')."
    )

    # Configuração Polimórfica
    __mapper_args__ = {"polymorphic_identity": TipoLocal.AMBIENTE_INTERNO_APARTAMENTO}

    # Relacionamento específico
    apartamento: "Apartamento" = Relationship(back_populates="locais_ambiente_interno")


class LocalApartamento(Locais, table=True):
    """Local específico: Referência a um Apartamento como um todo."""
    # __tablename__ = 'local_apartamento' # Inferido

    local_id: Optional[int] = Field(
        default=None,
        foreign_key="locais.id",
        primary_key=True,
        description="ID que vincula à tabela base 'locais' (PK, FK)."
    )
    apartamento_id: int = Field(
        foreign_key="apartamentos.id",
        index=True, # Baseado no idx_local_apto_apartamento_id
        nullable=False,
        description="ID do apartamento referenciado (FK, NOT NULL)."
    )
    # O dump não mostrava created_at, mas vamos adicionar por consistência
    created_at: Optional[datetime.datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        description="Timestamp de criação."
    )

    __mapper_args__ = {"polymorphic_identity": TipoLocal.APARTAMENTO}

    apartamento: "Apartamento" = Relationship(back_populates="locais_apartamento")


class LocalAreaComumInternaBloco(Locais, table=True):
    """Local específico: Área comum interna de um Bloco."""
    # __tablename__ = 'local_area_comum_interna_bloco' # Inferido

    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    bloco_id: int = Field(foreign_key="blocos.id", index=True, nullable=False)
    nome_area: str = Field(max_length=150, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_INTERNA_BLOCO}

    bloco: "Bloco" = Relationship(back_populates="locais_area_interna")


class LocalAreaComumFachadaBloco(Locais, table=True):
    """Local específico: Fachada de um Bloco."""
    # __tablename__ = 'local_area_comum_fachada_bloco' # Inferido

    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    bloco_id: int = Field(foreign_key="blocos.id", index=True, nullable=False)
    pano_vertical: str = Field(max_length=100, nullable=False)
    pavimento_referencia: str = Field(max_length=50, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_FACHADA_BLOCO}

    bloco: "Bloco" = Relationship(back_populates="locais_fachada")


class LocalAreaComumExternaBloco(Locais, table=True):
    """Local específico: Área comum externa de um Bloco."""
    # __tablename__ = 'local_area_comum_externa_bloco' # Inferido

    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    bloco_id: int = Field(foreign_key="blocos.id", index=True, nullable=False)
    nome_area: str = Field(max_length=150, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_EXTERNA_BLOCO}

    bloco: "Bloco" = Relationship(back_populates="locais_area_externa")


class LocalAreaComumModulo(Locais, table=True):
    """Local específico: Área comum de um Módulo."""
    # __tablename__ = 'local_area_comum_modulo' # Inferido

    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    modulo_id: int = Field(foreign_key="modulos.id", index=True, nullable=False)
    nome_area: str = Field(max_length=150, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoLocal.AREA_COMUM_MODULO}

    modulo: "Modulo" = Relationship(back_populates="locais_area_comum")


class LocalRua(Locais, table=True):
    """Local específico: Rua."""
    # __tablename__ = 'local_rua' # Inferido

    local_id: Optional[int] = Field(default=None, foreign_key="locais.id", primary_key=True)
    nome_rua: str = Field(max_length=255, index=True, nullable=False)

    __mapper_args__ = {"polymorphic_identity": TipoLocal.RUA}

    # Se houver relação M-N com Modulo, seria definida aqui com link_model
    # modulos: List["Modulo"] = Relationship(back_populates="ruas", link_model=ModuloRuaLink)

