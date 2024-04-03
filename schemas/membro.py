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

class MembroAlteraPaiSchema(BaseModel):
    """ Define como um membro da árvore a ser alterado deve ser representado
    """
    id_pai: int = 0
    id_filho: int = 0
    nome: str = "Nome do pai"

class MembroAlteraMaeSchema(BaseModel):
    """ Define como um membro da árvore a ser alterado deve ser representado
    """
    id_mae: int = 0
    id_filho: int = 0
    nome: str = "Nome da Mãe"

class MembroAlteraFilhoSchema(BaseModel):
    """ Define como um membro da árvore a ser alterado deve ser representado
    """
    id_filho: int = 0
    nome: str = "Nome"


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
    id: int 
    id_base: int

class MembroGetSchemaId(BaseModel):
    """ Define o filtro dos membros baseado no id
    """
    id: int 


class RetornoMembroSchema(BaseModel):
    """ Define com um membro será retornado.
    """
    membro: MembroViewModel

class ListagemMembrosSchema(BaseModel):
    """ Define como uma listagem de membros será retornada.
    """
    membros:List[MembroViewModel]

class RetornoPostEsquema(BaseModel):
    """ Define sucesso ou não em um post.
    """
    sucesso: bool
    mensagem: str
    


