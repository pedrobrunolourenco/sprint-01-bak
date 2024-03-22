from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from schemas.membro import MembroAddSchema
from sqlalchemy.exc import IntegrityError

from model import Session, Membro
from logger import logger
from schemas import *
from flask_cors import CORS


#######################################
from pydantic import BaseModel
from typing import Optional, List
from model.membro import Membro
from model.membro_view_model import MembroViewModel



info = Info(title="API para criação de uma árvore genealógica", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
membro_tag = Tag(name="Membro", description="Adição, Edição, visualização e remoção de membros à base")

def  busca_nome_por_id(id) -> str :
    session = Session()
    membro = session.query(Membro).filter(Membro.id == id).first()
    result = "Informar"
    if membro != None and membro.id > 0 :
      result = membro.nome
    return result

def  busca_membros_comuns(id_base) -> List[MembroViewModel] :
    session = Session()
    membros = session.query(Membro).filter(Membro.id_base == id_base).order_by(Membro.nivel)
    result = []
    for membro in membros:
        result.append({
        "id": membro.id,    
        "id_base" : membro.id_base,
        "nivel" : membro.nivel,
        "nome" : membro.nome,
        "pai" : membro.pai,
        "nome_pai" : busca_nome_por_id(membro.pai),
        "mae" : membro.mae,
        "nome_mae" : busca_nome_por_id(membro.mae),
        })
    return {"membros": result}

def  busca_membros_base() -> List[MembroViewModel] :
    session = Session()
    membros = session.query(Membro).filter(Membro.id_base == 0).order_by(Membro.nivel)
    result = []
    for membro in membros:
        result.append({
        "id": membro.id,    
        "id_base" : membro.id_base,
        "nivel" : membro.nivel,
        "nome" : membro.nome,
        "pai" : membro.pai,
        "nome_pai" : busca_nome_por_id(membro.pai),
        "mae" : membro.mae,
        "nome_mae" : busca_nome_por_id(membro.mae),
        })
    return {"membros": result}



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.get('/membro_base', tags=[membro_tag],
          responses={"200": ListagemMembrosSchema, "409": ErrorSchema, "400": ErrorSchema})
def obter_membros_base():
    """Obtém uma lista de membros base

    Retorna uma lista de representação dos membros base
    """
    try:
        membros = busca_membros_base()        
        return membros, 200

    except Exception as e:
        error_msg = "Não foi possível obter listagem de membros base :/"
        logger.warning(f"Erro ao listar membros base ', {error_msg}")
        membros = busca_membros_base()        

@app.post('/membro_base', tags=[membro_tag],
          responses={"200": ListagemMembrosSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_membro_base(form: MembroBaseAddSchema):
    """Adiciona um novo membro à base de dados

    Retorna uma representação dos membros base.
    """
    membro = Membro(
      id_base = 0,
      nivel = 0,    
      nome = form.nome,
      pai = 0,
      mae = 0
    )
    
    logger.debug(f"Adicionando membro base de nome: '{membro.nome}'")
    try:
        session = Session()
        session.add(membro)
        session.commit()
        logger.debug(f"Adicionado membro base de nome: '{membro.nome}'")
        membros = busca_membros_base()        
        return membros, 200
    except Exception as e:
        error_msg = "Não foi possível salvar novo membro :/"
        logger.warning(f"Erro ao adicionar membro '{membro.nome}', {error_msg}")
        membros = busca_membros_base(membro.id_base)        



@app.post('/membro_comum', tags=[membro_tag],
          responses={"200": ListagemMembrosSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_membro_comum(form: MembroAddSchema):
    """Adiciona um novo membro comum à base de dados

    Retorna uma lista de representação dos membros comuns.
    """
    membro = Membro(
      id_base = form.id_base,
      nivel = form. nivel,    
      nome = form.nome,
      pai = form.pai,
      mae = form.mae
    )
    
    logger.debug(f"Adicionando membro comum de nome: '{membro.nome}'")
    try:
        session = Session()
        session.add(membro)
        session.commit()
        logger.debug(f"Adicionado membro comum de nome: '{membro.nome}'")
        membros = busca_membros_comuns(membro.id_base)        
        return membros, 200
        

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo membro comum :/"
        logger.warning(f"Erro ao adicionar membro comum '{membro.nome}', {error_msg}")
        membros = busca_membros_comuns(membro.id_base)        
    


        

  

