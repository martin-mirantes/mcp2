# app/models/__init__.py (Ultra-Simplificado)

print("Importando modelos de app.models.all_models...")
# Importa tudo do arquivo consolidado
from .all_models import Obra, Pessoa, Tarefa # Apenas os modelos que agora existem

print("Importações concluídas.")

# Lista __all__ refletindo os modelos atuais
__all__ = [
    "Obra", "Pessoa", "Tarefa",
]
