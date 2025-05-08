import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carga las variables del archivo .env en la raíz del proyecto
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    """Configuraciones de la aplicación cargadas desde .env"""
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    # Añade otras variables de entorno aquí si las necesitas
    # OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Puedes añadir configuraciones que no vengan de .env también
    PROJECT_NAME: str = "Backend MCP"
    API_V1_STR: str = "/api/v1" # Si usas API REST adicional

settings = Settings()