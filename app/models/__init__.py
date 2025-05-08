# app/models/__init__.py (Ordem Revisada)

print("Importando: enums")
from .enums import TipoLocal
print("Importando: obra")
from .obra import Obra
print("Importando: modulo")
from .modulo import Modulo
print("Importando: bloco")
from .bloco import Bloco
print("Importando: pavimento")
from .pavimento import Pavimento
print("Importando: apartamento")
from .apartamento import Apartamentos # Importa Apartamentos ANTES de Local
print("Importando: responsavel")
from .responsavel import Responsavel
print("Importando: tipo_tarefa")
from .tipo_tarefa import TiposTarefa
# Preco depende de Local e TiposTarefa, importar depois de Local
# Tarefa depende de Local, TiposTarefa, Preco; importar depois de Preco
# TarefaResponsaveis depende de Tarefa e Responsavel; importar por último

# Importar Local e suas subclasses DEPOIS das dependências estruturais
print("Importando: local")
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

# Agora importar os que dependem de Local
print("Importando: preco")
from .preco import PrecosTarefaLocal
print("Importando: tarefa")
from .tarefa import Tarefa
print("Importando: tarefa_responsavel")
from .tarefa_responsavel import TarefaResponsaveis

print("Importações concluídas.")

# Opcional: Ajustar __all__
__all__ = [
    "TipoLocal", "Obra", "Modulo", "Bloco", "Pavimento", "Apartamentos",
    "Locais", 
    "LocalAreaComumExternaBloco", "LocalAreaComumFachadaBloco",
    "LocalAreaComumInternaBloco", "LocalAreaComumModulo", "LocalRua",
    "Responsavel", "TiposTarefa", "PrecosTarefaLocal", "Tarefa",
    "TarefaResponsaveis"
]
