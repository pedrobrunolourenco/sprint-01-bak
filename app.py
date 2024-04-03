from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from schemas.membro import MembroAddSchema, MembroAlteraFilhoSchema, MembroAlteraMaeSchema, MembroAlteraPaiSchema, MembroComumGetSchema, MembroGetSchema, MembroGetSchemaId, RetornoMembroSchema, RetornoPostEsquema
from sqlalchemy.exc import IntegrityError

from model import Session, Membro
from logger import logger
from schemas import *
from flask_cors import CORS

from sqlalchemy.orm import aliased


#######################################
from pydantic import BaseModel
from typing import Optional, List
from model.membro import Membro
from model.membro_view_model import MembroViewModel
from sqlalchemy import AliasedReturnsRows, func, update;

info = Info(title="API para criação de um MVP de Árvore Genealógica - Sprint-01", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
membro_tag = Tag(name="Membro", description="Adição, Edição, visualização e remoção de membros à base")

def  verifica_se_ja_existe_membro_base(nome: str) -> str :
    session = Session()
    try :
        membro = session.query(Membro).filter(func.lower(Membro.nome) == nome.lower(), Membro.id_base == 0).first()
        if membro :
          result = True
        else :
          result = False          
        return result
    except Exception as e:
        logger.warning(e)
            

def busca_membros_comuns(id_base) -> List[MembroViewModel] :
    session = Session()    

    Pai = aliased(Membro)
    Mae = aliased(Membro)
    
    membros = session.query(Membro, Pai.nome.label('nome_pai'), Mae.nome.label('nome_mae')) \
                 .outerjoin(Pai, Membro.pai == Pai.id) \
                 .outerjoin(Mae, Membro.mae == Mae.id) \
                 .filter((Membro.id_base == id_base) | (Membro.id == id_base)) \
                 .order_by(Membro.nivel, Membro.id) \
                 .all()

    result = []
    for membro, pai_nome, mae_nome in membros:
        membro_dict = {
            "id": membro.id,
            "id_base": membro.id_base,
            "nivel": membro.nivel,
            "nome": membro.nome,
            "pai": membro.pai,
            "nome_pai": pai_nome if pai_nome else "Informe o Pai",
            "mae": membro.mae,
            "nome_mae": mae_nome if mae_nome else "Informe a Mãe"
        }
        result.append(membro_dict)

    return {"membros": result}

def busca_membros_base() -> List[MembroViewModel] :
    session = Session()    

    Pai = aliased(Membro)
    Mae = aliased(Membro)
    
    membros = session.query(Membro, Pai.nome.label('nome_pai'), Mae.nome.label('nome_mae')) \
                 .outerjoin(Pai, Membro.pai == Pai.id) \
                 .outerjoin(Mae, Membro.mae == Mae.id) \
                 .filter((Membro.id_base == 0)) \
                 .order_by(Membro.nivel, Membro.id) \
                 .all()

    result = []
    for membro, pai_nome, mae_nome in membros:
        membro_dict = {
            "id": membro.id,
            "id_base": membro.id_base,
            "nivel": membro.nivel,
            "nome": membro.nome,
            "pai": membro.pai,
            "nome_pai": pai_nome if pai_nome else "Informe o Pai",
            "mae": membro.mae,
            "nome_mae": mae_nome if mae_nome else "Informe a Mãe"
        }
        result.append(membro_dict)

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
        return {"message": error_msg}, 400
    
@app.get('/membro_por_id', tags=[membro_tag],
          responses={"200": RetornoMembroSchema, "409": ErrorSchema, "400": ErrorSchema, "404": ErrorSchema})
def obter_por_id(query: MembroGetSchemaId):
    """Obtém um membro 

    Retorna uma representação de um membro
    """
    try:
        session = Session()    

        Pai = aliased(Membro)
        Mae = aliased(Membro)
        
        membros = session.query(Membro, Pai.nome.label('nome_pai'), Mae.nome.label('nome_mae')) \
                    .outerjoin(Pai, Membro.pai == Pai.id) \
                    .outerjoin(Mae, Membro.mae == Mae.id) \
                    .filter((Membro.id == query.id)) \
                    .order_by(Membro.nivel, Membro.id) \
                    .first()
        
        
        if not membros :
          error_msg = "Membro não localizado :/"
          return {"message": error_msg}, 200
        
        result = []
        membro, pai_nome, mae_nome = membros  # Descompactando a tupla retornada
        membro_dict = {
            "id": membro.id,
            "id_base": membro.id_base,
            "nivel": membro.nivel,
            "nome": membro.nome,
            "pai": membro.pai,
            "nome_pai": pai_nome if pai_nome else "Informe o Pai",
            "mae": membro.mae,
            "nome_mae": mae_nome if mae_nome else "Informe a Mãe"
        }
        result.append(membro_dict)
        return {"membro": result}
        
    except Exception as e:
        error_msg = "Não foi possível obter um membro por id:/"
        logger.warning(f"Erro ao buscar membro por id ', {error_msg}")
        return {"message": error_msg}, 400
        
@app.get('/membro_comum', tags=[membro_tag],
          responses={"200": ListagemMembrosSchema, "404": ErrorSchema, "400": ErrorSchema})
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
        return {"message": error_msg}, 400


@app.post('/membro_base', tags=[membro_tag],
          responses={"200": RetornoPostEsquema, "400": RetornoPostEsquema})
def add_membro_base(form: MembroBaseAddSchema):
    """Adiciona um novo membro à base de dados

    Retorna uma verificacao de sucesso ou falha.
    """
    membro = Membro(
      id_base = 0,
      nivel = 0,    
      nome = form.nome,
      pai = 0,
      mae = 0
    )

    try:
        if membro.nome != "" :
            jaexiste = verifica_se_ja_existe_membro_base(membro.nome)
            if jaexiste == True :
                return {"sucesso": False, "mensagem": "Membro já existe na base"}, 404
            else :            
                session = Session()
                session.add(membro)
                session.commit()
                return {"sucesso": True, "mensagem": "Membro base cadastrado com sucesso"}, 200
        else :
            return {"sucesso": False, "mensagem": "Necessário informar o nome"}, 400

    except Exception as e:
            return {"sucesso": False, "mensagem": "Erro ao cadastrar membro base"}, 400
       
          

@app.post('/add_membro_comum_pai', tags=[membro_tag],
          responses={"200": RetornoPostEsquema, "409": ErrorSchema, "400": ErrorSchema})
def add_membro_comum_pai(form: MembroAddSchema):
    """Adiciona um novo membro comum à base de dados

    Retorna uma verificação de sucesso ou falha
    """
    membro = Membro(
      id_base = form.id_base,
      nivel = form.nivel,    
      nome = form.nome,
      pai = form.pai,
      mae = form.mae
    )

    logger.debug(f"Adicionando membro comum de nome: '{membro.nome}'")
    try:
        session = Session()
        session.add(membro)
        session.commit()

        novo_pai = membro.id
        stmt = update(Membro).where(Membro.id == form.id_origem).values(pai=novo_pai)
        session.execute(stmt)
        session.commit() 

        return {"sucesso": True}, 200
    except Exception as e:
        error_msg = "Não foi possível salvar novo membro comum :/"
        logger.warning(f"Erro ao adicionar membro comum '{membro.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.put('/altera_membro_comum_pai', tags=[membro_tag],
          responses={"200": RetornoPostEsquema, "409": ErrorSchema, "400": ErrorSchema})
def altera_membro_comum_pai(form: MembroAlteraPaiSchema):
    """altera um membro comum na base de dados

       Retorna uma verificação de sucesso ou falha
    """

    try:
        session = Session()
        stmt01 = update(Membro).where(Membro.id == form.id_pai).values(nome=form.nome)
        session.execute(stmt01)
        session.commit() 
        return {"sucesso": True}, 200
    except Exception as e:
        logger.warning("Erro ao alterar um membro")
        return {"message": "Erro ao alterar um membro"}, 400


@app.post('/add_membro_comum_mae', tags=[membro_tag],
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

        nova_mae = membro.id
        stmt = update(Membro).where(Membro.id == form.id_origem).values(mae=nova_mae)
        session.execute(stmt)
        session.commit() 


        return {"sucesso": True}, 200
    except Exception as e:
        error_msg = "Não foi possível salvar novo membro comum :/"
        logger.warning(f"Erro ao adicionar membro comum '{membro.nome}', {error_msg}")
        return {"message": error_msg}, 400

@app.put('/altera_membro_comum_mae', tags=[membro_tag],
          responses={"200": RetornoPostEsquema, "409": ErrorSchema, "400": ErrorSchema})
def altera_membro_comum_mae(form: MembroAlteraMaeSchema):
    """altera um membro comum na base de dados

       Retorna uma verificação de sucesso ou falha
    """
    try:
        session = Session()
        stmt01 = update(Membro).where(Membro.id == form.id_mae).values(nome=form.nome)
        session.execute(stmt01)
        session.commit() 
        return {"sucesso": True}, 200
    except Exception as e:
        logger.warning("Erro ao alterar um membro")
        return {"message": "Erro ao alterar um membro"}, 400

@app.get('/membro_pai', tags=[membro_tag],
          responses={"200": RetornoMembroSchema, "409": ErrorSchema, "400": ErrorSchema, "404": ErrorSchema})
def obter_membro_pai(query: MembroGetSchemaId):
    """Obtém um membro 

    Retorna uma representação de um membro
    """
    """Obtém um membro 

    Retorna uma representação de um membro
    """
    try:
        session = Session()    
        Pai = aliased(Membro)
        Mae = aliased(Membro)
        membros = session.query(Membro, Pai.nome.label('nome_pai'), Mae.nome.label('nome_mae')) \
                    .outerjoin(Pai, Membro.pai == Pai.id) \
                    .outerjoin(Mae, Membro.mae == Mae.id) \
                    .filter((Membro.pai == query.id)) \
                    .order_by(Membro.nivel, Membro.id) \
                    .first()
        
        if not membros :
          error_msg = "Membro não localizado :/"
          return {"message": error_msg}, 200
        
        result = []
        membro, pai_nome, mae_nome = membros  # Descompactando a tupla retornada
        membro_dict = {
            "id": membro.id,
            "id_base": membro.id_base,
            "nivel": membro.nivel,
            "nome": membro.nome,
            "pai": membro.pai,
            "nome_pai": pai_nome if pai_nome else "Informe o Pai",
            "mae": membro.mae,
            "nome_mae": mae_nome if mae_nome else "Informe a Mãe"
        }
        result.append(membro_dict)
        return {"membro": result}
    except Exception as e:
        error_msg = "Não foi possível obter um membro:/"
        logger.warning(f"Erro ao buscar membro', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/membro_mae', tags=[membro_tag],
          responses={"200": RetornoMembroSchema, "409": ErrorSchema, "400": ErrorSchema, "404": ErrorSchema})
def obter_membro_mae(query: MembroGetSchemaId):
    """Obtém um membro 

    Retorna uma representação de um membro
    """
    try:
        session = Session()    
        Pai = aliased(Membro)
        Mae = aliased(Membro)
        membros = session.query(Membro, Pai.nome.label('nome_pai'), Mae.nome.label('nome_mae')) \
                    .outerjoin(Pai, Membro.pai == Pai.id) \
                    .outerjoin(Mae, Membro.mae == Mae.id) \
                    .filter((Membro.mae == query.id)) \
                    .order_by(Membro.nivel, Membro.id) \
                    .first()
        
        if not membros :
          error_msg = "Membro não localizado :/"
          return {"message": error_msg}, 200
        
        result = []
        membro, pai_nome, mae_nome = membros  # Descompactando a tupla retornada
        membro_dict = {
            "id": membro.id,
            "id_base": membro.id_base,
            "nivel": membro.nivel,
            "nome": membro.nome,
            "pai": membro.pai,
            "nome_pai": pai_nome if pai_nome else "Informe o Pai",
            "mae": membro.mae,
            "nome_mae": mae_nome if mae_nome else "Informe a Mãe"
        }
        result.append(membro_dict)        
        return {"membro": result}
    except Exception as e:
        error_msg = "Não foi possível obter um membro:/"
        logger.warning(f"Erro ao buscar membro', {error_msg}")
        return {"message": error_msg}, 400
    

@app.post('/add_membro_comum_filho', tags=[membro_tag],
          responses={"200": RetornoPostEsquema, "409": ErrorSchema, "400": ErrorSchema})
def add_membro_comum_filho(form: MembroAddSchema):
    """Adiciona um novo membro comum à base de dados

    Retorna uma verificação de sucesso ou falha
    """
    membro = Membro(
      id_base = form.id_base,
      nivel = form.nivel,    
      nome = form.nome,
      pai = form.pai,
      mae = form.mae
    )

    try:
        session = Session()
        session.add(membro)
        session.commit()

        return {"sucesso": True}, 200
    except Exception as e:
        error_msg = "Não foi possível salvar novo membro comum :/"
        logger.warning(f"Erro ao adicionar membro comum '{membro.nome}', {error_msg}")
        return {"message": error_msg}, 400

