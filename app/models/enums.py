# app/models/enums.py
from enum import Enum

class TipoLocal(str, Enum):
    """
    Define os tipos válidos para a coluna 'tipo_local' na tabela 'locais'.
    Corresponde ao ENUM 'tipo_local_enum' no PostgreSQL.
    """
    AMBIENTE_INTERNO_APARTAMENTO = "AMBIENTE_INTERNO_APARTAMENTO"
    AREA_COMUM_INTERNA_BLOCO = "AREA_COMUM_INTERNA_BLOCO"
    AREA_COMUM_FACHADA_BLOCO = "AREA_COMUM_FACHADA_BLOCO"
    AREA_COMUM_EXTERNA_BLOCO = "AREA_COMUM_EXTERNA_BLOCO"
    AREA_COMUM_MODULO = "AREA_COMUM_MODULO"
    RUA = "RUA"
    APARTAMENTO = "APARTAMENTO"
    # Adicione outros valores aqui se o ENUM no banco for modificado
