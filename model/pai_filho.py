from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

from  model import Base

class PaiFilho(Base):
    __tablename__ = 'paifilho'

    id = Column("pk_pai", Integer, primary_key=True)
    id_base = Column(Integer)    
    id_filho = Column(Integer)
    nome_pai = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, id_base:int, id_filho:int, nome_pai:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Membro da Árvore

        Arguments:
            id_base: idendificador do membro base 
            id_filho: id do membro filho
            nome: nome do pai
            data_insercao: data de quando o membro da árvore foi inserido à base
        """
        self.id_base = id_base
        self.id_filho = id_filho 
        self.nome_pai = nome_pai

        if data_insercao:
            self.data_insercao = data_insercao
