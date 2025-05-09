# inspect_tools.py
import asyncio
import json # Para imprimir el schema de forma legible

# Importa la instancia 'mcp' de tu servidor y el Cliente FastMCP
from app.server.main import mcp # Asegúrate que la ruta es correcta
from fastmcp import Client
from mcp import types as mcp_types # Para acceder a los tipos del protocolo MCP

async def print_tool_schemas():
    """
    Se conecta al servidor MCP en memoria, lista los tools,
    e imprime sus nombres y esquemas de argumentos.
    """
    print("Conectando al servidor MCP para inspeccionar Tools...\n")
    # Usamos el cliente en memoria apuntando directamente a tu instancia 'mcp'
    async with Client(mcp) as client:
        try:
            list_tools_result: mcp_types.ListToolsResult = await client.list_tools_mcp()

            if not list_tools_result.tools:
                print("No se encontraron tools en el servidor.")
                return

            print(f"--- Esquemas de Argumentos para {len(list_tools_result.tools)} Tool(s) ---")
            for tool in list_tools_result.tools:
                print(f"\nTool: {tool.name}")
                if hasattr(tool, 'description') and tool.description:
                    print(f"  Description: {tool.description}")

                schema_to_print = None
                # Priorizar 'inputSchema' ya que es el campo estándar de MCP para esto
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    schema_to_print = tool.inputSchema
                    print(f"  Arguments Schema (accessed via 'inputSchema'):")
                elif hasattr(tool, 'arguments_schema') and tool.arguments_schema:
                    # Fallback por si acaso
                    schema_to_print = tool.arguments_schema
                    print(f"  Arguments Schema (accessed via 'arguments_schema'):")
                elif hasattr(tool, 'argumentsSchema') and tool.argumentsSchema:
                    # Fallback para alias camelCase
                    schema_to_print = tool.argumentsSchema
                    print(f"  Arguments Schema (accessed via 'argumentsSchema'):")


                if schema_to_print:
                    try:
                        # Imprime el schema JSON de forma legible
                        # Pydantic v1 models might store schema as dict, v2 as JsonSchemaValue
                        # json.dumps can handle dicts directly.
                        # If schema_to_print is a Pydantic model itself, convert to dict.
                        if hasattr(schema_to_print, 'model_dump'): # Pydantic v2 JsonSchemaValue
                            # O schema pode ser um JsonSchemaValue que precisa ser convertido
                            # para um dict antes do json.dumps, ou já ser um dict.
                            # Se for um objeto complexo, model_dump() é o caminho.
                            # Se for um dict simples (como JSON Schema), json.dumps o manipula.
                            # A estrutura de inputSchema já deve ser um dict compatível com JSON Schema.
                            print(json.dumps(schema_to_print, indent=2))
                        elif isinstance(schema_to_print, dict): # Already a dict
                            print(json.dumps(schema_to_print, indent=2))
                        else: # Fallback
                             # Se for um objeto Pydantic representando o schema, tente model_dump
                            if hasattr(schema_to_print, 'model_dump_json'):
                                print(schema_to_print.model_dump_json(indent=2))
                            else:
                                print(str(schema_to_print))
                    except Exception as dump_error:
                        print(f"    Error al dumpear schema: {dump_error}")
                        print(f"    Schema (raw): {schema_to_print}")
                else:
                    print("  Arguments Schema: (No arguments or schema attribute not found)")
                    print(f"    Atributos disponibles en el objeto 'tool': {dir(tool)}")
                    if hasattr(type(tool), 'model_fields'): # Acessar da classe para Pydantic v2.11+
                         print(f"    Campos del modelo Pydantic v2: {list(type(tool).model_fields.keys())}")
                    elif hasattr(tool, '__fields__'): # Pydantic v1
                         print(f"    Campos del modelo Pydantic v1: {list(tool.__fields__.keys())}")

                print("-" * 30)

        except Exception as e:
            print(f"Ocurrió un error al interactuar con el servidor MCP: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(print_tool_schemas())
