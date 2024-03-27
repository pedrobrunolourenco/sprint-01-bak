from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from model.mae_filho import MaeFilho
from model.pai_filho import PaiFilho
from schemas.membro import MembroAddSchema, MembroComumGetSchema, RetornoPostEsquema
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
from sqlalchemy import update;



info = Info(title="API para criação de um MVP de Árvore Genealógica - Sprint-01", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
membro_tag = Tag(name="Membro", description="Adição, Edição, visualização e remoção de membros à base")

# def  verifica_se_ja_existe_membro_base(nome: str) -> str :
#     session = Session()
#     membro = session.query(Membro).filter(Membro.nome.lower() == nome.lower() and Membro.id_base==0).first()
#     result = False
#     if membro != None and membro.id > 0 :
#       result = True
#     return result

def busca_pai_por_id_array(id, pais ) -> str :
    result = "Informe o Pai"
    if id > 0 :
        for pai in pais:
            if pai.id_filho == id :
                result = pai.nome_pai
                break
    return result            

def busca_pai_por_id(id) -> str :
    result = "Informe o Pai"
    if id > 0 :
        session = Session()
        membroPai = session.query(PaiFilho).filter(PaiFilho.id_filho == id).first()
        if membroPai != None and membroPai.id > 0 :
            result =  membroPai.nome_pai
        return result
    else :
        return result
    
def busca_mae_por_id(id) -> str :
    result = "Informe a Mãe"
    if id > 0 :
        session = Session()
        membroMae = session.query(MaeFilho).filter(MaeFilho.id_filho == id).first()
        if membroMae != None and membroMae.id > 0 :
            result =  membroMae.nome_mae
        return result
    else :
        return result


def busca_membros_comuns(id_base) -> List[MembroViewModel] :
    session = Session()

    membros = session.query(Membro)\
                .filter((Membro.id_base == id_base) | (Membro.id == id_base))\
                .order_by(Membro.nivel, Membro.id)\
                .all()
    
    pais = session.query(PaiFilho)\
                .filter(PaiFilho.id_base == id_base)\
                .all()

    maes = session.query(MaeFilho)\
                .filter(MaeFilho.id_base == id_base)\
                .all()

    result = []
    for membro in membros:
        result.append({
        "id": membro.id,    
        "id_base" : membro.id_base,
        "nivel" : membro.nivel,
        "nome" : membro.nome,
        "pai" : membro.pai,
        "nome_pai" : busca_pai_por_id_array(membro.id, pais ), ##busca_pai_por_id(membro.id),
        "mae" : membro.mae,
        "nome_mae" : "mae" ##busca_mae_por_id(membro.id),
        })
    return {"membros": result}

def busca_membros_base() -> List[MembroViewModel] :
    session = Session()
    membros = session.query(Membro).filter(Membro.id_base == 0).order_by(Membro.nome)
    result = []
    for membro in membros:
        result.append({
        "id": membro.id,    
        "id_base" : membro.id_base,
        "nivel" : membro.nivel,
        "nome" : membro.nome,
        "pai" : membro.pai,
        "nome_pai" : busca_pai_por_id(membro.id),
        "mae" : membro.mae,
        "nome_mae" : busca_mae_por_id(membro.id),
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
        return {"mesage": error_msg}, 400
    
@app.get('/membro_comun', tags=[membro_tag],
          responses={"200": ListagemMembrosSchema, "409": ErrorSchema, "400": ErrorSchema})
def obter_membros_comuns(query: MembroComumGetSchema):
    """Obtém uma lista de membros relacionados a um membro base

    Retorna uma lista de representação dos membros 
    """
    try:
        membros = busca_membros_comuns(query.id_base)      
        return membros, 200
    except Exception as e:
        error_msg = "Não foi possível obter listagem de membros :/"
        logger.warning(f"Erro ao listar membros base ', {error_msg}")
        return {"mesage": error_msg}, 400


@app.post('/membro_base', tags=[membro_tag],
          responses={"200": RetornoPostEsquema, "400": ErrorSchema})
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
        return {"sucesso": True}, 200

    except Exception as e:
        error_msg = "Não foi possível salvar novo membro :/"
        logger.warning(f"Erro ao adicionar membro '{membro.nome}', {error_msg}")
        return {"mesage": error_msg}, 400
        
            

@app.post('/membro_comum_pai', tags=[membro_tag],
          responses={"200": RetornoPostEsquema, "409": ErrorSchema, "400": ErrorSchema})
def add_membro_comum_pai(form: MembroAddSchema):
    """Adiciona um novo membro comum à base de dados

    Retorna uma lista de representação dos membros comuns.
    """
    membro = Membro(
      id_base = form.id_base,
      nivel = form.nivel,    
      nome = form.nome,
      pai = form.pai,
      mae = form.mae
    )

    paifilho = PaiFilho(
        id_base = form.id_base,
        id_filho = form.id_origem,
        nome_pai= form.nome
    )

    logger.debug(f"Adicionando membro comum de nome: '{membro.nome}'")
    try:
        session = Session()
        session.add(membro)
        session.commit()

        paifilho = PaiFilho(
            id_base = form.id_base,
            id_filho = form.id_origem,
            nome_pai= form.nome
        )

        pPai = busca_pai_por_id(paifilho.id_filho)
        if pPai == "Informe o Pai" :
            session.add(paifilho)
            session.commit()

        
        novo_pai = membro.id
        stmt = update(Membro).where(Membro.id == form.id_origem).values(pai=novo_pai)
        session.execute(stmt)
        session.commit() 

        return {"sucesso": True}, 200
    except Exception as e:
        error_msg = "Não foi possível salvar novo membro comum :/"
        logger.warning(f"Erro ao adicionar membro comum '{membro.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.post('/membro_comum_mae', tags=[membro_tag],
          responses={"200": RetornoPostEsquema, "409": ErrorSchema, "400": ErrorSchema})
def add_membro_comum_mae(form: MembroAddSchema):
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

        maefilho = MaeFilho(
            id_base = form.id_base,
            id_filho = form.id_origem,
            nome_mae = form.nome
        )


        pMae = busca_mae_por_id(maefilho.id_filho)
        if pMae == "Informe a Mãe" :
            session.add(maefilho)
            session.commit()

        nova_mae = membro.id
        stmt = update(Membro).where(Membro.id == form.id_origem).values(mae=nova_mae)
        session.execute(stmt)
        session.commit()       

        return {"sucesso": True}, 200
    except Exception as e:
        error_msg = "Não foi possível salvar novo membro comum :/"
        logger.warning(f"Erro ao adicionar membro comum '{membro.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


