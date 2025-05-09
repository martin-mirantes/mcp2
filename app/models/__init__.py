# app/models/__init__.py (Ultra-Simplificado - Sin Prints de Debug)

# Importa tudo do arquivo consolidado
from .all_models import Obra, Pessoa, Tarefa # Apenas os modelos que agora existem

# Lista __all__ refletindo os modelos atuais
__all__ = [
    "Obra", "Pessoa", "Tarefa",
]
