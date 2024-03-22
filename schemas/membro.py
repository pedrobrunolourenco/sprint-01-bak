from pydantic import BaseModel
from typing import Optional, List
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

class MembroBaseAddSchema(BaseModel):
    """ Define como um novo membro base da árvore a ser inserido deve ser representado
    """
    nome: str = "Nome Completo"


class ListagemMembrosSchema(BaseModel):
    """ Define como uma listagem de membros será retornada.
    """
    produtos:List[MembroViewModel]




