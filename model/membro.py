from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

from  model import Base

class Membro(Base):
    __tablename__ = 'membro'

    id = Column("pk_membro", Integer, primary_key=True)
    id_base = Column(Integer)    
    nivel = Column(Integer)    
    nome = Column(String(140))
    pai = Column(Integer)
    mae = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, id_base:int, nivel:int, nome:str, pai:int, mae:int,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Membro da Árvore

        Arguments:
            id_base: idendificador do membro base (se 0 indica que é membro base do início da construção da árvore)
            nivel: indica o nivel hierárquico do membro (se 0 indica que é membro base do início da construção da árvore)
            nome: nome do membro da árvore.
            pai: valor inteiro que indica a relação do membro pai
            pai: valor inteiro que indica a relação do membro mãe
            data_insercao: data de quando o membro da árvore foi inserido à base
        """
        self.id_base = id_base
        self.nivel = nivel
        self.nome = nome
        self.pai = pai
        self.mae = mae

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

