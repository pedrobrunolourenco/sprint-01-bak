from pydantic import BaseModel

class MembroViewModel(BaseModel):

    def __init__(self, id: int, id_base:int, nivel:int, nome:str, pai:int, nome_pai: str, mae:int, nome_mae:str):
        self.id = id,
        self.id_base = id_base
        self.nivel = nivel
        self.nome = nome
        self.pai = pai
        self.nome_pai = nome_pai,
        self.mae = mae
        self.nome_mae = nome_mae


