# app/models/__init__.py
from .enums import TipoLocal
from .obra import Obra
from .modulo import Modulo
from .bloco import Bloco
from .pavimento import Pavimento
from .apartamento import Apartamento
from .local import (
    Locais,
    LocalApartamento,
    LocalAmbienteInternoApartamento,
    LocalAreaComumExternaBloco,
    LocalAreaComumFachadaBloco,
    LocalAreaComumInternaBloco,
    LocalAreaComumModulo,
    LocalRua,
)
from .responsavel import Responsavel
from .tipo_tarefa import TiposTarefa
from .preco import PrecosTarefaLocal
from .tarefa import Tarefa                           # Añadido
from .tarefa_responsavel import TarefaResponsaveis # Añadido

# Opcional: Definir __all__ para controlar o que é importado com *
__all__ = [
    "TipoLocal", "Obra", "Modulo", "Bloco", "Pavimento", "Apartamento",
    "Locais", "LocalApartamento", "LocalAmbienteInternoApartamento",
    "LocalAreaComumExternaBloco", "LocalAreaComumFachadaBloco",
    "LocalAreaComumInternaBloco", "LocalAreaComumModulo", "LocalRua",
    "Responsavel", "TiposTarefa", "PrecosTarefaLocal", "Tarefa",
    "TarefaResponsaveis"
]