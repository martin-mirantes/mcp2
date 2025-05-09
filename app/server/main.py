# app/server/main.py
from typing import List, Optional, Dict, Any
from fastmcp import FastMCP, Context
from sqlmodel import Session, select
from pydantic import BaseModel, Field as PydanticField # Para modelos de API/JSON

# Importa a configuração e a função de sessão
from app.core.config import settings
from app.db.session import get_session # Para obter a sessão da DB
# Importa seus modelos SQLModel
from app.models.all_models import Obra, Pessoa # Adicionando Pessoa

# --- Modelos Pydantic para validação dos dados JSON ---
class PessoaObraAssociada(BaseModel):
    obra_id_ref: int
    obra_nome_ref: Optional[str] = None
    matricula_obra: Optional[str] = None
    funcao_na_obra: Optional[str] = None

class PessoaDados(BaseModel):
    nome_completo: str
    cpf: Optional[str] = PydanticField(default=None, pattern=r"^\d{3}\.\d{3}\.\d{3}-\d{2}$")
    telefone_whatsapp: Optional[str] = None
    email: Optional[str] = PydanticField(default=None, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    situacao_atual: Optional[str] = "Ativo"
    obras_associadas: Optional[List[PessoaObraAssociada]] = []

class PessoaCriar(PessoaDados):
    pass

class PessoaRead(BaseModel):
    id: int
    dados: PessoaDados
    created_at: str

class ObraDados(BaseModel):
    nome: str
    codigo: Optional[str] = None
    status: Optional[str] = None

class ObraCriar(ObraDados):
    pass

class ObraRead(BaseModel):
    id: int
    dados: ObraDados
    created_at: str

# Cria a instancia principal do servidor FastMCP
mcp = FastMCP(
    name=settings.PROJECT_NAME,
    instructions="Servidor MCP para gestão de tarefas de obra."
)

# --- Tools e Resources para Obras ---
@mcp.tool()
def criar_obra(
    nome_obra: str,
    codigo: Optional[str] = None,
    status: Optional[str] = None,
    ctx: Context = None
) -> ObraRead:
    """
    Cria uma nova obra na base de dados.
    O campo 'nome' da obra é obrigatório.
    """
    if ctx:
        ctx.info(f"Tentando criar obra: {nome_obra}")

    json_data = ObraCriar(nome=nome_obra, codigo=codigo, status=status).model_dump(exclude_none=True)

    db: Session = next(get_session())
    try:
        nova_obra = Obra(dados=json_data)
        db.add(nova_obra)
        db.commit()
        db.refresh(nova_obra)
        if ctx:
            ctx.info(f"Obra '{json_data.get('nome')}' criada com ID: {nova_obra.id}")
        return ObraRead(id=nova_obra.id, dados=ObraDados(**nova_obra.dados), created_at=str(nova_obra.created_at))
    except Exception as e:
        db.rollback()
        if ctx:
            ctx.error(f"Erro ao criar obra {nome_obra}: {e}")
        raise ValueError(f"Não foi possível criar a obra: {e}")
    finally:
        db.close()

# REFACTORIZADO: De Tool para Resource Template
@mcp.resource("obras://id/{obra_id}")
def obter_obra_por_id(obra_id: int, ctx: Context = None) -> Optional[ObraRead]:
    """Obtém os detalhes de uma obra pelo seu ID."""
    # A lógica interna da função permanece a mesma
    db: Session = next(get_session())
    try:
        # obra_id é convertido para int automaticamente pelo FastMCP a partir da URI
        obra_db = db.get(Obra, obra_id)
        if obra_db:
            if ctx: ctx.info(f"Obra encontrada: ID {obra_id}")
            return ObraRead(id=obra_db.id, dados=ObraDados(**obra_db.dados), created_at=str(obra_db.created_at))
        else:
            if ctx: ctx.warning(f"Obra com ID {obra_id} não encontrada.")
            # Para Resources, retornar None ou uma lista vazia é comum para "não encontrado"
            # Ou pode-se levantar uma exceção específica que o cliente MCP possa interpretar.
            # Por simplicidade, retornamos None, o cliente MCP verá um resultado vazio.
            return None
    except Exception as e:
        if ctx: ctx.error(f"Erro ao obter obra {obra_id}: {e}")
        # Em um Resource, levantar um erro pode ser traduzido para um erro MCP.
        raise ValueError(f"Erro ao buscar obra: {e}")
    finally:
        db.close()

@mcp.resource("obras://todas")
def listar_obras(ctx: Context = None) -> List[ObraRead]:
    """Lista todas as obras cadastradas."""
    db: Session = next(get_session())
    try:
        statement = select(Obra)
        results = db.exec(statement).all()
        obras_list = [
            ObraRead(id=obra.id, dados=ObraDados(**obra.dados), created_at=str(obra.created_at))
            for obra in results
        ]
        if ctx:
            ctx.info(f"Listando {len(obras_list)} obras.")
        return obras_list
    except Exception as e:
        if ctx: ctx.error(f"Erro ao listar obras: {e}")
        raise ValueError(f"Erro ao listar obras: {e}")
    finally:
        db.close()

# --- Tools e Resources para Pessoas ---
@mcp.tool()
def criar_pessoa(
    dados_pessoa: PessoaCriar,
    ctx: Context = None
) -> PessoaRead:
    """
    Cria uma nova pessoa na base de dados.
    Os dados da pessoa são fornecidos como um objeto JSON.
    """
    if ctx:
        ctx.info(f"Tentando criar pessoa: {dados_pessoa.nome_completo}")

    json_data_para_db = dados_pessoa.model_dump(exclude_none=True)

    db: Session = next(get_session())
    try:
        nova_pessoa = Pessoa(dados=json_data_para_db)
        db.add(nova_pessoa)
        db.commit()
        db.refresh(nova_pessoa)
        if ctx:
            ctx.info(f"Pessoa '{nova_pessoa.dados.get('nome_completo')}' criada com ID: {nova_pessoa.id}")
        return PessoaRead(id=nova_pessoa.id, dados=PessoaDados(**nova_pessoa.dados), created_at=str(nova_pessoa.created_at))
    except Exception as e:
        db.rollback()
        if ctx:
            ctx.error(f"Erro ao criar pessoa {dados_pessoa.nome_completo}: {e}")
        raise ValueError(f"Não foi possível criar a pessoa: {e}")
    finally:
        db.close()

# REFACTORIZADO: De Tool para Resource Template
@mcp.resource("pessoas://id/{pessoa_id}")
def obter_pessoa_por_id(pessoa_id: int, ctx: Context = None) -> Optional[PessoaRead]:
    """Obtém os detalhes de uma pessoa pelo seu ID."""
    # A lógica interna da função permanece a mesma
    db: Session = next(get_session())
    try:
        # pessoa_id é convertido para int automaticamente pelo FastMCP a partir da URI
        pessoa_db = db.get(Pessoa, pessoa_id)
        if pessoa_db:
            if ctx: ctx.info(f"Pessoa encontrada: ID {pessoa_id}")
            dados_parseados = PessoaDados(**pessoa_db.dados)
            return PessoaRead(id=pessoa_db.id, dados=dados_parseados, created_at=str(pessoa_db.created_at))
        else:
            if ctx: ctx.warning(f"Pessoa com ID {pessoa_id} não encontrada.")
            return None
    except Exception as e:
        if ctx: ctx.error(f"Erro ao obter pessoa {pessoa_id}: {e}")
        raise ValueError(f"Erro ao buscar pessoa: {e}")
    finally:
        db.close()

@mcp.resource("pessoas://todas")
def listar_pessoas(ctx: Context = None) -> List[PessoaRead]:
    """Lista todas as pessoas cadastradas."""
    db: Session = next(get_session())
    try:
        statement = select(Pessoa)
        results = db.exec(statement).all()
        pessoas_list = []
        for pessoa_db in results:
            dados_parseados = PessoaDados(**pessoa_db.dados)
            pessoas_list.append(
                PessoaRead(id=pessoa_db.id, dados=dados_parseados, created_at=str(pessoa_db.created_at))
            )
        if ctx:
            ctx.info(f"Listando {len(pessoas_list)} pessoas.")
        return pessoas_list
    except Exception as e:
        if ctx: ctx.error(f"Erro ao listar pessoas: {e}")
        raise ValueError(f"Erro ao listar pessoas: {e}")
    finally:
        db.close()

# --- Exemplo de Tool Ping (mantido) ---
@mcp.tool()
def ping() -> str:
    """Responde 'pong' para verificar que el servidor está activo."""
    return "pong"

# --- Exemplo de Resource server_info (mantido) ---
@mcp.resource("resource://server_info")
def get_server_info(ctx: Context = None) -> dict:
     """Devuelve información básica del servidor."""
     client_id_info = "N/A"
     request_id_info = "N/A"
     if ctx:
         client_id_info = ctx.client_id or "N/A"
         request_id_info = ctx.request_id
     return {
         "server_name": mcp.name,
         "request_id": request_id_info,
         "client_id": client_id_info
     }

# --- Punto de entrada para ejecutar el servidor ---
if __name__ == "__main__":
    print(f"Iniciando servidor FastMCP '{mcp.name}'...")
    # Para testes locais, pode ser útil rodar com HTTP
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, path="/mcp")
    mcp.run() # Default para STDIO
