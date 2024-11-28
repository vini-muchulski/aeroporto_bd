from sqlalchemy.orm import sessionmaker
from models import *

# CRUD Operations
def obter_nome_chave_primaria(modelo):
    return modelo.__mapper__.primary_key[0].name

def criar_registro(session, model_class, **kwargs):
    registro = model_class(**kwargs)
    session.add(registro)
    session.commit()
    print(f"{model_class.__name__} criado com sucesso.")
    return registro



def ler_registro(session, model_class, id_):
    chave_primaria = obter_nome_chave_primaria(model_class)
    filtro = {chave_primaria: id_}
    registro = session.query(model_class).filter_by(**filtro).first()
    return registro


def atualizar_registro(session, model_class, id_, **kwargs):
    chave_primaria = obter_nome_chave_primaria(model_class)
    filtro = {chave_primaria: id_}
    registro = session.query(model_class).filter_by(**filtro).first()
    if registro:
        for chave, valor in kwargs.items():
            setattr(registro, chave, valor)
        session.commit()
        print(f"{model_class.__name__} {id_} atualizado com sucesso.")
        return registro
    else:
        print(f"{model_class.__name__} {id_} não encontrado.")
        return None


def deletar_registro(session, model_class, id_):
    chave_primaria = obter_nome_chave_primaria(model_class)
    filtro = {chave_primaria: id_}
    registro = session.query(model_class).filter_by(**filtro).first()
    if registro:
        session.delete(registro)
        session.commit()
        print(f"{model_class.__name__} {id_} deletado com sucesso.")
    else:
        print(f"{model_class.__name__} {id_} não encontrado.")