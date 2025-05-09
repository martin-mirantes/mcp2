from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings # Importa la configuración

# echo=True muestra las querys SQL (útil en desarrollo, quitar en producción)
engine = create_engine(settings.DATABASE_URL, echo=False)

def create_db_and_tables():
    """
    Crea todas las tablas definidas por los modelos SQLModel.
    ¡Usar con precaución! Solo para configuración inicial si no se usa Alembic desde el principio.
    En producción/desarrollo continuo, usar Alembic para migraciones.
    """
    print("Intentando crear tablas (si no existen)...")
    # Asegúrate de que todos tus modelos SQLModel sean importados
    # antes de llamar a create_all para que sean registrados en los metadatos.
    # Esto usualmente se hace importándolos en app/models/__init__.py
    # y luego importando ese __init__ aquí o en main.py
    # from app import models # Ejemplo
    SQLModel.metadata.create_all(engine)
    print("Tablas verificadas/creadas.")

def get_session():
    """
    Generador para obtener una sesión de base de datos.
    Maneja el commit y rollback automáticamente.
    """
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

# También puedes definir una dependencia para FastAPI si planeas usarlo
# def get_session_dependency() -> Generator[Session, Any, None]:
#     with Session(engine) as session:
#         yield session
