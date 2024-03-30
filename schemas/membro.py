from pydantic import BaseModel
from typing import List
from model.membro import Membro
from model.membro_view_model import MembroViewModel

class MembroAddSchema(BaseModel):
    """ Define como um novo membro da árvore a ser inserido deve ser representado
    """
    id_base: int = 0 
    nivel: int = 0
    nome: str = "Nome Completo"
    pai: int = 0
    mae: int = 0
    id_origem: int = 0

class MembroBaseAddSchema(BaseModel):
    """ Define como um novo membro base da árvore a ser inserido deve ser representado
    """
    nome: str = "Nome Completo"

class MembroComumGetSchema(BaseModel):
    """ Define o filtro dos membros baseado no membro base
    """
    id_base: int = 1

class MembroGetSchema(BaseModel):
    """ Define o filtro dos membros baseado no id
    """
    id: int = 1

class RetornoMembroSchema(BaseModel):
    """ Define com um membro será retornado.
    """
    membro: MembroViewModel

class ListagemMembrosSchema(BaseModel):
    """ Define como uma listagem de membros será retornada.
    """
    membros:List[MembroViewModel]

class RetornoPostEsquema(BaseModel):
    """ Define sucesso ou não da inclusão do membro base.
    """
    sucesso: bool
    



