# app/models/__init__.py
from .all_models import *

# O __all__ pode ser definido aqui ou no all_models.py
# Se definido em all_models.py, esta linha não é estritamente necessária
# mas pode ser útil para clareza ou se você quiser re-exportar seletivamente.
__all__ = [
    "TipoLocal", "Obra", "Modulo", "Bloco", "Pavimento", "Apartamentos",
    "Locais", "LocalApartamento", "LocalAmbienteInternoApartamento",
    "LocalAreaComumExternaBloco", "LocalAreaComumFachadaBloco",
    "LocalAreaComumInternaBloco", "LocalAreaComumModulo", "LocalRua",
    "Responsavel", "TiposTarefa", "PrecosTarefaLocal", "Tarefa",
    "TarefaResponsaveis"
]