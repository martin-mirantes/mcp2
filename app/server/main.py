# app/server/main.py
from typing import List, Optional, Dict, Any
from fastmcp import FastMCP, Context
from sqlmodel import Session, select
from pydantic import BaseModel, Field as PydanticField # Para modelos de API/JSON

# Importa a configuração e a função de sessão
from app.core.config import settings
from app.db.session import get_session # Para obter a sessão da DB
# Importa seus modelos SQLModel
from app.models.all_models import Obra, Pessoa

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
    nome: str # Mantido como 'nome' para consistência interna do modelo Pydantic
    codigo: Optional[str] = None
    status: Optional[str] = None
    # Adicione outros campos que espera no JSON de Obra

class ObraCriar(ObraDados): # Este modelo será usado como parâmetro do Tool
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
    dados_obra: ObraCriar, # <<-- MUDANÇA: Agora aceita o modelo Pydantic diretamente
    ctx: Context = None
) -> ObraRead:
    """
    Cria uma nova obra na base de dados.
    Os dados da obra são fornecidos como um objeto JSON que corresponde ao schema de ObraCriar.
    O campo 'nome' dentro de dados_obra é obrigatório.
    """
    if ctx:
        ctx.info(f"Tentando criar obra: {dados_obra.nome}")

    # model_dump() converte o modelo Pydantic para um dict
    # exclude_none=True remove campos que não foram enviados (são None)
    json_data_para_db = dados_obra.model_dump(exclude_none=True)

    db: Session = next(get_session())
    try:
        nova_obra = Obra(dados=json_data_para_db)
        db.add(nova_obra)
        db.commit()
        db.refresh(nova_obra)
        if ctx:
            ctx.info(f"Obra '{json_data_para_db.get('nome')}' criada com ID: {nova_obra.id}")
        # Ao retornar, parseamos o dicionário 'dados' de volta para ObraDados para consistência
        return ObraRead(id=nova_obra.id, dados=ObraDados(**nova_obra.dados), created_at=str(nova_obra.created_at))
    except Exception as e:
        db.rollback()
        if ctx:
            ctx.error(f"Erro ao criar obra {dados_obra.nome}: {e}")
        raise ValueError(f"Não foi possível criar a obra: {e}")
    finally:
        db.close()

@mcp.resource("obras://id/{obra_id}")
def obter_obra_por_id(obra_id: int, ctx: Context = None) -> Optional[ObraRead]:
    """Obtém os detalhes de uma obra pelo seu ID."""
    db: Session = next(get_session())
    try:
        obra_db = db.get(Obra, obra_id)
        if obra_db:
            if ctx: ctx.info(f"Obra encontrada: ID {obra_id}")
            return ObraRead(id=obra_db.id, dados=ObraDados(**obra_db.dados), created_at=str(obra_db.created_at))
        else:
            if ctx: ctx.warning(f"Obra com ID {obra_id} não encontrada.")
            return None
    except Exception as e:
        if ctx: ctx.error(f"Erro ao obter obra {obra_id}: {e}")
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
    Os dados da pessoa são fornecidos como um objeto JSON que corresponde ao schema de PessoaCriar.
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

@mcp.resource("pessoas://id/{pessoa_id}")
def obter_pessoa_por_id(pessoa_id: int, ctx: Context = None) -> Optional[PessoaRead]:
    """Obtém os detalhes de uma pessoa pelo seu ID."""
    db: Session = next(get_session())
    try:
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
# --- Punto de entrada para ejecutar el servidor ---
if __name__ == "__main__":
    # Para permitir escolher o transporte via argumento de linha de comando
    import sys
    transport_mode = "stdio" # Default
    port = 8000 # Default para HTTP
    if len(sys.argv) > 1 and sys.argv[1] == "http":
        transport_mode = "streamable-http"
        print(f"Iniciando servidor FastMCP '{mcp.name}' em modo Streamable HTTP na porta {port}...")
        mcp.run(transport=transport_mode, host="0.0.0.0", port=port, path="/mcp")
    else:
        print(f"Iniciando servidor FastMCP '{mcp.name}' em modo STDIO...")
        mcp.run(transport=transport_mode) # Default para STDIO
