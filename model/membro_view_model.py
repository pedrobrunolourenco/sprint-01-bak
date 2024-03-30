from pydantic import BaseModel

class MembroViewModel(BaseModel):
    id: int
    id_base: int
    nivel: int
    nome: str
    pai: int
    nome_pai: str
    mae: int
    nome_mae: str


