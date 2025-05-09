# alembic/env.py
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

# --- MODIFICACIÓN PARA CARGAR .ENV ---
project_dir = Path(__file__).parent.parent.resolve()
env_path = project_dir / ".env"
if env_path.is_file():
    #print(f"Cargando variables de entorno desde: {env_path}")
    load_dotenv(dotenv_path=env_path)
#else:
   #print(f"Advertencia: Archivo .env no encontrado en {env_path}")
# --- FIN MODIFICACIÓN .ENV ---

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- MODIFICACIÓN PARA SQLMODEL E IMPORTS INDIVIDUAIS ---
# Adiciona o diretório raiz do projeto ao sys.path
if str(project_dir) not in sys.path:
    #print(f"Adicionando {project_dir} ao sys.path")
     sys.path.insert(0, str(project_dir)) # <<-- Indentación corregida aquí

from sqlmodel import SQLModel # Importa SQLModel

# Importa o módulo único que contém todos os modelos
try:
   #print("Importando modelos de app.models.all_models...")
    from app.models import all_models # Importa o arquivo consolidado
   #print("Modelos SQLModel importados com sucesso.")
except ImportError as e:
   #print(f"Erro ao importar modelos de app.models.all_models: {e}")
   #print("Verifique o caminho e o arquivo __init__.py em app/models.")
    raise e

# Define os metadados dos seus modelos SQLModel como o alvo para Alembic
target_metadata = SQLModel.metadata
# --- FIN MODIFICACIÓN SQLMODEL ---

# ... (Resto do arquivo env.py como estava antes) ...

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL não definida no ambiente ou .env para modo offline")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL não definida no ambiente ou .env para modo online")

    connectable = create_engine(db_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            # compare_server_default=True, # Opcional
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
