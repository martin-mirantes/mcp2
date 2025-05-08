from fastmcp import FastMCP, Context

# Importa la configuración si necesitas accederla aquí
from app.core.config import settings

# Crea la instancia principal del servidor FastMCP
mcp = FastMCP(
    name=settings.PROJECT_NAME,
    # Puedes añadir instrucciones generales aquí
    instructions="Servidor MCP para gestión de tarefas de obra."
)

# --- Añade tus Tools, Resources, Prompts aquí usando decoradores ---
# Ejemplo de Tool básico:
@mcp.tool()
def ping() -> str:
    """Responde 'pong' para verificar que el servidor está activo."""
    return "pong"

# Ejemplo de acceso a contexto (opcional)
@mcp.resource("resource://server_info")
def get_server_info(ctx: Context) -> dict:
     """Devuelve información básica del servidor."""
     return {
         "server_name": mcp.name,
         "request_id": ctx.request_id,
         "client_id": ctx.client_id or "N/A"
     }

# --- Punto de entrada para ejecutar el servidor ---
# Esta parte permite correr el servidor directamente con `python -m app.server.main`
# o usando `fastmcp run app.server.main:mcp`
if __name__ == "__main__":
    print(f"Iniciando servidor FastMCP '{mcp.name}'...")
    # Por defecto corre en modo STDIO, adecuado para clientes como Claude Desktop
    # o para pruebas locales con fastmcp.Client("python -m app.server.main")
    mcp.run()

    # Para correr en modo HTTP (ej: Streamable HTTP en puerto 8000):
    # print("Corriendo en modo Streamable HTTP en http://127.0.0.1:8000/mcp")
    # mcp.run(transport="streamable-http", host="127.0.0.1", port=8000, path="/mcp")
