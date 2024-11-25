from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Table, text , func
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import load_dotenv
import json
import os
    
"""
pip install psycopg2

Certifique-se de que o banco aeroporto já foi criado antes de conceder os privilégios:
CREATE DATABASE aeroporto;


CREATE USER vini WITH PASSWORD '123';
GRANT ALL PRIVILEGES ON DATABASE aeroporto TO vini;

GRANT USAGE ON SCHEMA public TO vini;
GRANT CREATE ON SCHEMA public TO vini;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO vini;


"""
Base = declarative_base()

# Definição das tabelas e modelos

class Passageiro(Base):
    __tablename__ = 'passageiro'

    codigo_passageiro = Column(Integer, primary_key=True)
    nome = Column(String)
    documento = Column(String)
    contato = Column(Integer)
    ControleSeguranca = Column(Boolean)

    bilhetes = relationship('BilheteVoo', back_populates='passageiro')

class BilheteVoo(Base):
    __tablename__ = 'bilhete_voo'

    numero_bilhete = Column(Integer, primary_key=True)
    classe = Column(String)
    nome_passageiro = Column(String)
    status = Column(String)
    fk_Passageiro_codigo_passageiro = Column(Integer, ForeignKey('passageiro.codigo_passageiro', ondelete='CASCADE'))
    fk_Voo_numero_voo = Column(Integer, ForeignKey('voo.numero_voo', ondelete='CASCADE'))

    passageiro = relationship('Passageiro', back_populates='bilhetes')
    voo = relationship('Voo', back_populates='bilhetes')

class Voo(Base):
    __tablename__ = 'voo'

    numero_voo = Column(Integer, primary_key=True)
    horario_chegada = Column(String)
    horario_partida = Column(String)
    fk_Area_Bagagem_codigo_bagagem = Column(Integer, ForeignKey('area_bagagem.codigo_bagagem', ondelete='CASCADE'))
    fk_Aeronave_prefixo_aeronave = Column(String, ForeignKey('aeronave.prefixo_aeronave', ondelete='CASCADE'))
    fk_Destinos_numero_destino = Column(Integer, ForeignKey('destinos.numero_destino', ondelete='CASCADE'))

    area_bagagem = relationship('AreaBagagem', back_populates='voos')
    aeronave = relationship('Aeronave', back_populates='voos')
    destino = relationship('Destinos', back_populates='voos')
    bilhetes = relationship('BilheteVoo', back_populates='voo')
    tripulantes = relationship('Tripulante', secondary='operaciona_table', back_populates='voos')
    portoes_embarque = relationship('PortaoEmbarque', secondary='usa_table', back_populates='voos')

class Aeronave(Base):
    __tablename__ = 'aeronave'

    prefixo_aeronave = Column(String, primary_key=True)
    modelo = Column(String)
    capacidade = Column(Integer)
    fk_Empresa_Aerea_cod_empresa = Column(String, ForeignKey('empresa_aerea.cod_empresa', ondelete='CASCADE'))

    empresa_aerea = relationship('EmpresaAerea', back_populates='aeronaves')
    voos = relationship('Voo', back_populates='aeronave')
    manutencoes = relationship('Manutencao', secondary='operaciona_manutencao_table', back_populates='aeronaves')

class EmpresaAerea(Base):
    __tablename__ = 'empresa_aerea'

    cod_empresa = Column(String, primary_key=True)
    Nome = Column(String)
    Pais = Column(String)

    aeronaves = relationship('Aeronave', back_populates='empresa_aerea')

class PortaoEmbarque(Base):
    __tablename__ = 'portao_embarque'

    codigo_portao = Column(String, primary_key=True)
    localizacao = Column(String)
    status = Column(String)

    voos = relationship('Voo', secondary='usa_table', back_populates='portoes_embarque')

class AreaBagagem(Base):
    __tablename__ = 'area_bagagem'

    codigo_bagagem = Column(Integer, primary_key=True)
    status = Column(String)

    voos = relationship('Voo', back_populates='area_bagagem')

class Tripulante(Base):
    __tablename__ = 'tripulantes'

    id_funcionario = Column(Integer, primary_key=True)
    nome = Column(String)
    cargo = Column(String)
    setor = Column(String)

    voos = relationship('Voo', secondary='operaciona_table', back_populates='tripulantes')

class Destinos(Base):
    __tablename__ = 'destinos'

    numero_destino = Column(Integer, primary_key=True)
    Origem = Column(String)
    Destino = Column(String)

    voos = relationship('Voo', back_populates='destino')

class Manutencao(Base):
    __tablename__ = 'manutencao'

    ID_Manutencao = Column(Integer, primary_key=True)
    Data = Column(String)
    Tipo = Column(String)

    aeronaves = relationship('Aeronave', secondary='operaciona_manutencao_table', back_populates='manutencoes')

# Tabelas de associação para relacionamentos muitos-para-muitos

usa_table = Table('usa_table', Base.metadata,
    Column('fk_Voo_numero_voo', Integer, ForeignKey('voo.numero_voo', ondelete='SET NULL')),
    Column('fk_Portao_Embarque_codigo_portao', String, ForeignKey('portao_embarque.codigo_portao', ondelete='SET NULL')),
    extend_existing=True
)

operaciona_table = Table('operaciona_table', Base.metadata,
    Column('fk_Tripulantes_id_funcionario', Integer, ForeignKey('tripulantes.id_funcionario', ondelete='SET NULL')),
    Column('fk_Voo_numero_voo', Integer, ForeignKey('voo.numero_voo', ondelete='SET NULL')),
    extend_existing=True
)

operaciona_manutencao_table = Table('operaciona_manutencao_table', Base.metadata,
    Column('fk_Manutencao_ID_Manutencao', Integer, ForeignKey('manutencao.ID_Manutencao', ondelete='SET NULL')),
    Column('fk_Aeronave_prefixo_aeronave', String, ForeignKey('aeronave.prefixo_aeronave', ondelete='SET NULL')),
    extend_existing=True
)

##########################################
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


def imprimir_dados():
    modelos = [Passageiro, BilheteVoo, Voo, Aeronave, EmpresaAerea, Destinos, AreaBagagem, PortaoEmbarque, Tripulante, Manutencao]
    for modelo in modelos:
        registros = session.query(modelo).all()
        print(f"\n--- {modelo.__name__} ---")
        for registro in registros:
            atributos = vars(registro)
            atributos_limpos = {chave: valor for chave, valor in atributos.items() if not chave.startswith('_')}
            print(atributos_limpos)
            
            
def carregar_dados_iniciais():
    # Inserir dados na tabela Passageiro
    criar_registro(session, Passageiro, codigo_passageiro=1, nome="João Silva", documento="123456789", contato=999999999, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=2, nome="Maria Souza", documento="987654321", contato=888888888, ControleSeguranca=False)
    
    criar_registro(session, Passageiro, codigo_passageiro=3, nome="Pedro Mendes", documento="456789123", contato=777777777, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=4, nome="Ana Pereira", documento="789456123", contato=666666666, ControleSeguranca=False)
    criar_registro(session, Passageiro, codigo_passageiro=5, nome="Lucas Rodrigues", documento="234567891", contato=555555555, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=6, nome="Carla Farias", documento="567891234", contato=444444444, ControleSeguranca=False)
    criar_registro(session, Passageiro, codigo_passageiro=7, nome="Rafaela Costa", documento="891234567", contato=333333333, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=8, nome="Carlos Oliveira", documento="951753456", contato=555555555, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=9, nome="Ana Maria", documento="753159654", contato=666666666, ControleSeguranca=False)
    criar_registro(session, Passageiro, codigo_passageiro=10, nome="Pedro Sousa", documento="357951852", contato=777777777, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=11, nome="Marta Pereira", documento="159753456", contato=888888888, ControleSeguranca=False)
    criar_registro(session, Passageiro, codigo_passageiro=12, nome="Ricardo Almeida", documento="543216789", contato=999999999, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=13, nome="Juliana Santos", documento="741852963", contato=111111111, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=14, nome="Fernando Lima", documento="258963147", contato=222222222, ControleSeguranca=False)
    criar_registro(session, Passageiro, codigo_passageiro=15, nome="Isabela Ferreira", documento="852369741", contato=333333333, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=16, nome="Eduardo Lopes", documento="963852741", contato=444444444, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=17, nome="Patrícia Lima", documento="147258369", contato=555555555, ControleSeguranca=False)
    criar_registro(session, Passageiro, codigo_passageiro=18, nome="Felipe Andrade", documento="321654987", contato=666666666, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=19, nome="Luciana Alves", documento="789123456", contato=777777777, ControleSeguranca=False)
    criar_registro(session, Passageiro, codigo_passageiro=20, nome="Gustavo Barros", documento="456123789", contato=888888888, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=21, nome="Larissa Costa", documento="951753258", contato=999999999, ControleSeguranca=True)
    criar_registro(session, Passageiro, codigo_passageiro=22, nome="Victor Santos", documento="753951456", contato=222222222, ControleSeguranca=False)
    
    # Inserir dados na tabela EmpresaAerea
    criar_registro(session, EmpresaAerea, cod_empresa="AA", Nome="American Airlines", Pais="EUA")
    criar_registro(session, EmpresaAerea, cod_empresa="TP", Nome="TAP Portugal", Pais="Portugal")
    criar_registro(session, EmpresaAerea, cod_empresa="EM", Nome="Emirates", Pais="Emirados Árabes Unidos")
    criar_registro(session, EmpresaAerea, cod_empresa="BA", Nome="British Airways", Pais="Reino Unido")
    criar_registro(session, EmpresaAerea, cod_empresa="DL", Nome="Delta Air Lines", Pais="EUA")
    criar_registro(session, EmpresaAerea, cod_empresa="AF", Nome="Air France", Pais="França")
    criar_registro(session, EmpresaAerea, cod_empresa="LH", Nome="Lufthansa", Pais="Alemanha")
    criar_registro(session, EmpresaAerea, cod_empresa="QF", Nome="Qantas Airways", Pais="Austrália")
    criar_registro(session, EmpresaAerea, cod_empresa="AZ", Nome="Alitalia", Pais="Itália")
    criar_registro(session, EmpresaAerea, cod_empresa="SA", Nome="South African Airways", Pais="África do Sul")
    criar_registro(session, EmpresaAerea, cod_empresa="IB", Nome="Iberia", Pais="Espanha")

    
    
     #Inserir dados na tabela Aeronave
    criar_registro(session, Aeronave, prefixo_aeronave="AA-123", modelo="Boeing 737", capacidade=150, fk_Empresa_Aerea_cod_empresa="AA")
    criar_registro(session, Aeronave, prefixo_aeronave="TP-456", modelo="Airbus A320", capacidade=180, fk_Empresa_Aerea_cod_empresa="TP")
    criar_registro(session, Aeronave, prefixo_aeronave="AA-456", modelo="Boeing 747", capacidade=250, fk_Empresa_Aerea_cod_empresa="AA")
    criar_registro(session, Aeronave, prefixo_aeronave="TP-789", modelo="Airbus A330", capacidade=200, fk_Empresa_Aerea_cod_empresa="TP")
    criar_registro(session, Aeronave, prefixo_aeronave="EM-101", modelo="Boeing 787", capacidade=220, fk_Empresa_Aerea_cod_empresa="EM")
    criar_registro(session, Aeronave, prefixo_aeronave="BA-234", modelo="Airbus A350", capacidade=240, fk_Empresa_Aerea_cod_empresa="BA")
    criar_registro(session, Aeronave, prefixo_aeronave="DL-555", modelo="Airbus A220", capacidade=130, fk_Empresa_Aerea_cod_empresa="DL")
    criar_registro(session, Aeronave, prefixo_aeronave="AF-888", modelo="Boeing 777", capacidade=300, fk_Empresa_Aerea_cod_empresa="AF")
    criar_registro(session, Aeronave, prefixo_aeronave="LH-100", modelo="Airbus A380", capacidade=850, fk_Empresa_Aerea_cod_empresa="LH")
    criar_registro(session, Aeronave, prefixo_aeronave="QF-200", modelo="Boeing 787", capacidade=300, fk_Empresa_Aerea_cod_empresa="QF")
    criar_registro(session, Aeronave, prefixo_aeronave="AZ-300", modelo="Airbus A319", capacidade=150, fk_Empresa_Aerea_cod_empresa="AZ")
    criar_registro(session, Aeronave, prefixo_aeronave="SA-400", modelo="Boeing 747", capacidade=450, fk_Empresa_Aerea_cod_empresa="SA")
    criar_registro(session, Aeronave, prefixo_aeronave="IB-500", modelo="Airbus A321", capacidade=200, fk_Empresa_Aerea_cod_empresa="IB")
    criar_registro(session, Aeronave, prefixo_aeronave="LH-200", modelo="Airbus A380", capacidade=850, fk_Empresa_Aerea_cod_empresa="LH")
    criar_registro(session, Aeronave, prefixo_aeronave="QF-300", modelo="Boeing 787", capacidade=300, fk_Empresa_Aerea_cod_empresa="QF")
    criar_registro(session, Aeronave, prefixo_aeronave="AZ-400", modelo="Airbus A319", capacidade=150, fk_Empresa_Aerea_cod_empresa="AZ")
    criar_registro(session, Aeronave, prefixo_aeronave="SA-500", modelo="Boeing 747", capacidade=450, fk_Empresa_Aerea_cod_empresa="SA")
    criar_registro(session, Aeronave, prefixo_aeronave="IB-600", modelo="Airbus A321", capacidade=200, fk_Empresa_Aerea_cod_empresa="IB")

    

    # Inserir dados na tabela Destinos
    criar_registro(session, Destinos, numero_destino=1, Origem="São Paulo", Destino="Nova York")
    criar_registro(session, Destinos, numero_destino=2, Origem="Lisboa", Destino="Rio de Janeiro")
    criar_registro(session, Destinos, numero_destino=3, Origem="Madrid", Destino="São Paulo")
    criar_registro(session, Destinos, numero_destino=4, Origem="Paris", Destino="Rio de Janeiro")
    criar_registro(session, Destinos, numero_destino=5, Origem="Lisboa", Destino="Madrid")
    criar_registro(session, Destinos, numero_destino=6, Origem="Londres", Destino="Tóquio")
    criar_registro(session, Destinos, numero_destino=7, Origem="Roma", Destino="São Paulo")
    criar_registro(session, Destinos, numero_destino=8, Origem="Los Angeles", Destino="Tóquio")
    criar_registro(session, Destinos, numero_destino=9, Origem="São Paulo", Destino="Cidade do Cabo")
    criar_registro(session, Destinos, numero_destino=10, Origem="Berlim", Destino="Paris")
    criar_registro(session, Destinos, numero_destino=11, Origem="Lisboa", Destino="Dublin")
    criar_registro(session, Destinos, numero_destino=12, Origem="Sydney", Destino="Londres")
    criar_registro(session, Destinos, numero_destino=13, Origem="Nova York", Destino="Frankfurt")


    # Inserir dados na tabela AreaBagagem
    criar_registro(session, AreaBagagem, codigo_bagagem=3, status="Operacional")
    criar_registro(session, AreaBagagem, codigo_bagagem=4, status="Manutenção")

    # Inserir dados na tabela AreaBagagem
    criar_registro(session, AreaBagagem, codigo_bagagem=1, status="Operacional")
    criar_registro(session, AreaBagagem, codigo_bagagem=2, status="Manutenção")
    criar_registro(session, AreaBagagem, codigo_bagagem=5, status="Operacional")
    criar_registro(session, AreaBagagem, codigo_bagagem=6, status="Manutenção")
    criar_registro(session, AreaBagagem, codigo_bagagem=7, status="Operacional")
    criar_registro(session, AreaBagagem, codigo_bagagem=8, status="Manutenção")
    criar_registro(session, AreaBagagem, codigo_bagagem=9, status="Operacional")


    # Inserir dados na tabela Voo
    criar_registro(session, Voo, numero_voo=101, horario_chegada="12:00", horario_partida="08:00", fk_Area_Bagagem_codigo_bagagem=1, fk_Aeronave_prefixo_aeronave="AA-123", fk_Destinos_numero_destino=1)
    criar_registro(session, Voo, numero_voo=202, horario_chegada="18:30", horario_partida="14:00", fk_Area_Bagagem_codigo_bagagem=2, fk_Aeronave_prefixo_aeronave="TP-456", fk_Destinos_numero_destino=2)
    criar_registro(session, Voo, numero_voo=303, horario_chegada="14:00", horario_partida="10:00", fk_Area_Bagagem_codigo_bagagem=1, fk_Aeronave_prefixo_aeronave="AA-456", fk_Destinos_numero_destino=3)
    criar_registro(session, Voo, numero_voo=404, horario_chegada="20:00", horario_partida="16:00", fk_Area_Bagagem_codigo_bagagem=2, fk_Aeronave_prefixo_aeronave="TP-789", fk_Destinos_numero_destino=4)
    criar_registro(session, Voo, numero_voo=505, horario_chegada="11:00", horario_partida="07:00", fk_Area_Bagagem_codigo_bagagem=1, fk_Aeronave_prefixo_aeronave="EM-101", fk_Destinos_numero_destino=5)
    criar_registro(session, Voo, numero_voo=606, horario_chegada="06:00", horario_partida="22:00", fk_Area_Bagagem_codigo_bagagem=1, fk_Aeronave_prefixo_aeronave="DL-555", fk_Destinos_numero_destino=6)
    criar_registro(session, Voo, numero_voo=707, horario_chegada="10:00", horario_partida="02:00", fk_Area_Bagagem_codigo_bagagem=2, fk_Aeronave_prefixo_aeronave="AF-888", fk_Destinos_numero_destino=7)
    criar_registro(session, Voo, numero_voo=808, horario_chegada="09:00", horario_partida="05:00", fk_Area_Bagagem_codigo_bagagem=2, fk_Aeronave_prefixo_aeronave="LH-100", fk_Destinos_numero_destino=8)
    criar_registro(session, Voo, numero_voo=909, horario_chegada="13:00", horario_partida="09:00", fk_Area_Bagagem_codigo_bagagem=1, fk_Aeronave_prefixo_aeronave="QF-200", fk_Destinos_numero_destino=9)
    criar_registro(session, Voo, numero_voo=1010, horario_chegada="16:00", horario_partida="12:00", fk_Area_Bagagem_codigo_bagagem=2, fk_Aeronave_prefixo_aeronave="AZ-300", fk_Destinos_numero_destino=10)
    criar_registro(session, Voo, numero_voo=1111, horario_chegada="19:00", horario_partida="15:00", fk_Area_Bagagem_codigo_bagagem=1, fk_Aeronave_prefixo_aeronave="SA-400", fk_Destinos_numero_destino=11)
    criar_registro(session, Voo, numero_voo=1212, horario_chegada="22:00", horario_partida="18:00", fk_Area_Bagagem_codigo_bagagem=2, fk_Aeronave_prefixo_aeronave="IB-500", fk_Destinos_numero_destino=12)
   
    
    # Inserir dados na tabela BilheteVoo
    criar_registro(session, BilheteVoo, numero_bilhete=1001, classe="Economica", nome_passageiro="João Silva", status="Confirmado", fk_Passageiro_codigo_passageiro=1, fk_Voo_numero_voo=101)
    criar_registro(session, BilheteVoo, numero_bilhete=1002, classe="Executiva", nome_passageiro="Maria Souza", status="Pendente", fk_Passageiro_codigo_passageiro=2, fk_Voo_numero_voo=202)

    criar_registro(session, BilheteVoo, numero_bilhete=1003, classe="Economica", nome_passageiro="Carlos Oliveira", status="Confirmado", fk_Passageiro_codigo_passageiro=3, fk_Voo_numero_voo=101)
    criar_registro(session, BilheteVoo, numero_bilhete=1004, classe="Executiva", nome_passageiro="Ana Maria", status="Pendente", fk_Passageiro_codigo_passageiro=4, fk_Voo_numero_voo=202)
    criar_registro(session, BilheteVoo, numero_bilhete=1005, classe="Economica", nome_passageiro="Pedro Sousa", status="Confirmado", fk_Passageiro_codigo_passageiro=5, fk_Voo_numero_voo=303)
    criar_registro(session, BilheteVoo, numero_bilhete=1006, classe="Executiva", nome_passageiro="Marta Pereira", status="Pendente", fk_Passageiro_codigo_passageiro=6, fk_Voo_numero_voo=404)
    criar_registro(session, BilheteVoo, numero_bilhete=1007, classe="Economica", nome_passageiro="Ricardo Almeida", status="Confirmado", fk_Passageiro_codigo_passageiro=7, fk_Voo_numero_voo=505)
    criar_registro(session, BilheteVoo, numero_bilhete=1008, classe="Primeira Classe", nome_passageiro="Juliana Santos", status="Confirmado", fk_Passageiro_codigo_passageiro=13, fk_Voo_numero_voo=606)
    criar_registro(session, BilheteVoo, numero_bilhete=1009, classe="Executiva", nome_passageiro="Fernando Lima", status="Pendente", fk_Passageiro_codigo_passageiro=14, fk_Voo_numero_voo=707)
    criar_registro(session, BilheteVoo, numero_bilhete=1010, classe="Economica", nome_passageiro="Eduardo Lopes", status="Confirmado", fk_Passageiro_codigo_passageiro=16, fk_Voo_numero_voo=808)
    criar_registro(session, BilheteVoo, numero_bilhete=1011, classe="Executiva", nome_passageiro="Patrícia Lima", status="Confirmado", fk_Passageiro_codigo_passageiro=17, fk_Voo_numero_voo=909)
    criar_registro(session, BilheteVoo, numero_bilhete=1012, classe="Primeira Classe", nome_passageiro="Felipe Andrade", status="Pendente", fk_Passageiro_codigo_passageiro=18, fk_Voo_numero_voo=1010)
    criar_registro(session, BilheteVoo, numero_bilhete=1013, classe="Economica", nome_passageiro="Luciana Alves", status="Confirmado", fk_Passageiro_codigo_passageiro=19, fk_Voo_numero_voo=1111)
    criar_registro(session, BilheteVoo, numero_bilhete=1014, classe="Executiva", nome_passageiro="Gustavo Barros", status="Cancelado", fk_Passageiro_codigo_passageiro=20, fk_Voo_numero_voo=1212)
    criar_registro(session, BilheteVoo, numero_bilhete=1015, classe="Primeira Classe", nome_passageiro="Larissa Costa", status="Confirmado", fk_Passageiro_codigo_passageiro=21, fk_Voo_numero_voo=808)
    criar_registro(session, BilheteVoo, numero_bilhete=1016, classe="Economica", nome_passageiro="Victor Santos", status="Pendente", fk_Passageiro_codigo_passageiro=22, fk_Voo_numero_voo=909)

    # Inserir dados na tabela PortaoEmbarque
    criar_registro(session, PortaoEmbarque, codigo_portao="A1", localizacao="Terminal 1", status="Disponível")
    criar_registro(session, PortaoEmbarque, codigo_portao="B2", localizacao="Terminal 2", status="Ocupado")
    criar_registro(session, PortaoEmbarque, codigo_portao="C3", localizacao="Terminal 3", status="Disponível")
    criar_registro(session, PortaoEmbarque, codigo_portao="D4", localizacao="Terminal 4", status="Ocupado")
    criar_registro(session, PortaoEmbarque, codigo_portao="E5", localizacao="Terminal 5", status="Disponível")
    criar_registro(session, PortaoEmbarque, codigo_portao="F6", localizacao="Terminal 6", status="Disponível")
    criar_registro(session, PortaoEmbarque, codigo_portao="G7", localizacao="Terminal 7", status="Ocupado")
    criar_registro(session, PortaoEmbarque, codigo_portao="H8", localizacao="Terminal 8", status="Manutenção")
    criar_registro(session, PortaoEmbarque, codigo_portao="I9", localizacao="Terminal 9", status="Disponível")
    criar_registro(session, PortaoEmbarque, codigo_portao="J10", localizacao="Terminal 10", status="Ocupado")

    
    # Inserir dados na tabela Tripulante
    criar_registro(session, Tripulante, id_funcionario=100, nome="Carlos Santos", cargo="Piloto", setor="Operações")
    criar_registro(session, Tripulante, id_funcionario=101, nome="Ana Oliveira", cargo="Comissária", setor="Atendimento")
    criar_registro(session, Tripulante, id_funcionario=102, nome="Miguel Fernandes", cargo="Piloto", setor="Operações")
    criar_registro(session, Tripulante, id_funcionario=103, nome="Sofia Gomes", cargo="Comissário", setor="Atendimento")
    criar_registro(session, Tripulante, id_funcionario=104, nome="Mariana Silva", cargo="Piloto", setor="Operações")
    criar_registro(session, Tripulante, id_funcionario=105, nome="Thiago Ribeiro", cargo="Piloto", setor="Operações")
    criar_registro(session, Tripulante, id_funcionario=106, nome="Renata Carvalho", cargo="Comissária", setor="Atendimento")
    criar_registro(session, Tripulante, id_funcionario=107, nome="Gabriel Nunes", cargo="Piloto", setor="Operações")
    criar_registro(session, Tripulante, id_funcionario=108, nome="Camila Martins", cargo="Comissária", setor="Atendimento")
    criar_registro(session, Tripulante, id_funcionario=109, nome="André Gonçalves", cargo="Mecânico", setor="Manutenção")
    criar_registro(session, Tripulante, id_funcionario=110, nome="Júlia Amaral", cargo="Engenheira", setor="Manutenção")

    
    # Inserir dados na tabela Manutencao
    criar_registro(session, Manutencao, ID_Manutencao=1, Data="2023-01-10", Tipo="Preventiva")
    criar_registro(session, Manutencao, ID_Manutencao=2, Data="2023-02-15", Tipo="Corretiva")
    criar_registro(session, Manutencao, ID_Manutencao=3, Data="2023-03-20", Tipo="Preventiva")
    criar_registro(session, Manutencao, ID_Manutencao=4, Data="2023-04-15", Tipo="Corretiva")
    criar_registro(session, Manutencao, ID_Manutencao=5, Data="2023-05-10", Tipo="Preventiva")
    criar_registro(session, Manutencao, ID_Manutencao=6, Data="2023-06-15", Tipo="Preventiva")
    criar_registro(session, Manutencao, ID_Manutencao=7, Data="2023-07-20", Tipo="Corretiva")
    criar_registro(session, Manutencao, ID_Manutencao=8, Data="2023-08-25", Tipo="Preventiva")
    criar_registro(session, Manutencao, ID_Manutencao=9, Data="2023-09-30", Tipo="Corretiva")
    criar_registro(session, Manutencao, ID_Manutencao=10, Data="2023-10-05", Tipo="Preventiva")


    # Link tripulantes to voos through operaciona_table
    from sqlalchemy import insert
    session.execute(
        insert(operaciona_table),
        [
            {"fk_Tripulantes_id_funcionario": 100, "fk_Voo_numero_voo": 101},
            {"fk_Tripulantes_id_funcionario": 100, "fk_Voo_numero_voo": 303},
            {"fk_Tripulantes_id_funcionario": 101, "fk_Voo_numero_voo": 202},
            {"fk_Tripulantes_id_funcionario": 101, "fk_Voo_numero_voo": 404},
            {"fk_Tripulantes_id_funcionario": 102, "fk_Voo_numero_voo": 505},
            {"fk_Tripulantes_id_funcionario": 104, "fk_Voo_numero_voo": 606}, # Mariana Silva no voo 606
            {"fk_Tripulantes_id_funcionario": 103, "fk_Voo_numero_voo": 707}, # Sofia Gomes no voo 707
        ]
    )
    session.commit()

    # Link voos to portoes_embarque through usa_table
    session.execute(
        insert(usa_table),
        [
            {"fk_Voo_numero_voo": 101, "fk_Portao_Embarque_codigo_portao": "A1"},
            {"fk_Voo_numero_voo": 202, "fk_Portao_Embarque_codigo_portao": "B2"},
            {"fk_Voo_numero_voo": 303, "fk_Portao_Embarque_codigo_portao": "C3"},
            {"fk_Voo_numero_voo": 404, "fk_Portao_Embarque_codigo_portao": "D4"},
            {"fk_Voo_numero_voo": 505, "fk_Portao_Embarque_codigo_portao": "C3"},
            {"fk_Voo_numero_voo": 606, "fk_Portao_Embarque_codigo_portao": "E5"}, # Voo 606 no portão E5
            {"fk_Voo_numero_voo": 707, "fk_Portao_Embarque_codigo_portao": "A1"}, # Voo 707 no portão A1
        ]
    )
    session.commit()

    # Link manutencoes to aeronaves through operaciona_manutencao_table
    session.execute(
        insert(operaciona_manutencao_table),
        [
            {"fk_Manutencao_ID_Manutencao": 3, "fk_Aeronave_prefixo_aeronave": "AA-456"},
            {"fk_Manutencao_ID_Manutencao": 4, "fk_Aeronave_prefixo_aeronave": "TP-789"},
            {"fk_Manutencao_ID_Manutencao": 5, "fk_Aeronave_prefixo_aeronave": "DL-555"}, # Manutenção 5 na aeronave DL-555
        ]
    )
    session.commit()

######################################### menu
def menu_principal():
    while True:
        print("""
        ---MENU---

        1.  Criar todas as tabelas
        2.  Inserir todos os valores
        3.  Atualizar valores (teste)
        4.  Deletar valores (teste)
        5.  CONSULTA 01 - consulta padrão pronta
        6.  CONSULTA 02 - consulta padrão pronta
        7.  CONSULTA 03 - consulta padrão pronta
        8.  CONSULTA EXTRA - consulta padrão pronta
        9.  Mostrar Tabelas
        10. Atualizar Valor Específico
        11. Limpar Todos os Dados
        12. Dropar Todas as Tabelas
        13. Sair
        """)

        opcao = input("Selecione uma opção: ")

        if opcao == '1':
            create_database()
        elif opcao == '2':
            carregar_dados_iniciais()
        elif opcao == '3':
            atualizar_valores_teste()
        elif opcao == '4':
            deletar_valores_teste()
        elif opcao == '5':
            consulta_01()
        elif opcao == '6':
            consulta_02()
        elif opcao == '7':
            consulta_03()
        elif opcao == '8':
            consulta_extra()
        elif opcao == '9':
            imprimir_dados()
        elif opcao == '10':
            atualizar_valor_especifico()
        elif opcao == '11':
            limpar_dados()
        elif opcao == '12':
            drop_tables()  # Chama a função para dropar as tabelas
        elif opcao == '13':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")


def atualizar_valores_teste():
    print("\n--- Atualizando valores para teste ---")
    # Exemplo: Atualizar o nome de um passageiro com código 1
    atualizar_registro(session, Passageiro, id_=1, nome="vini")
    # Exemplo: Atualizar o horário de partida de um voo com número 101
    atualizar_registro(session, Voo, id_=101, horario_partida="09:00")
    print("Valores atualizados com sucesso.")


def deletar_valores_teste():
    print("\n--- Deletando valores para teste ---")
    # Exemplo: Deletar um passageiro com código 2
    deletar_registro(session, Passageiro, id_=2)
    # Exemplo: Deletar um voo com número 202
    deletar_registro(session, Voo, id_=202)
    print("Valores deletados com sucesso.")

def atualizar_valor_especifico():
    print("\n--- Atualizar valor específico ---")
    print("Selecione a tabela:")
    print("1. Passageiro")
    print("2. BilheteVoo")
    print("3. Voo")
    print("4. Aeronave")
    print("5. EmpresaAerea")
    print("6. Destinos")
    print("7. Área de Bagagem")
    print("8. Portão de Embarque")
    print("9. Tripulante")
    print("10. Manutenção")
    tabela_opcao = input("Opção: ")

    if tabela_opcao == '1':
        model_class = Passageiro
    elif tabela_opcao == '2':
        model_class = BilheteVoo
    elif tabela_opcao == '3':
        model_class = Voo
    elif tabela_opcao == '4':
        model_class = Aeronave
    elif tabela_opcao == '5':
        model_class = EmpresaAerea
    elif tabela_opcao == '6':
        model_class = Destinos
    elif tabela_opcao == '7':
        model_class = AreaBagagem
    elif tabela_opcao == '8':
        model_class = PortaoEmbarque
    elif tabela_opcao == '9':
        model_class = Tripulante
    elif tabela_opcao == '10':
        model_class = Manutencao
    else:
        print("Opção inválida.")
        return

    chave_primaria = obter_nome_chave_primaria(model_class)
    id_ = input(f"Digite o valor da chave primária ({chave_primaria}): ")

    # Converter o ID para o tipo correto (inteiro ou string)
    coluna_chave = getattr(model_class, chave_primaria).property.columns[0]
    if isinstance(coluna_chave.type, Integer):
        id_ = int(id_)

    registro = ler_registro(session, model_class, id_)
    if registro:
        print("Registro atual:")
        atributos = vars(registro)
        atributos_limpos = {chave: valor for chave, valor in atributos.items() if not chave.startswith('_')}
        print(atributos_limpos)
        print("\nDigite os novos valores (deixe em branco para manter o valor atual):")
        dados = {}
        for atributo in atributos_limpos.keys():
            if atributo == chave_primaria:
                continue  # Não atualizar a chave primária
            valor_atual = getattr(registro, atributo)
            valor = input(f"{atributo} [{valor_atual}]: ")
            if valor:
                # Detectar o tipo da coluna e converter o valor adequadamente
                coluna = getattr(model_class, atributo).property.columns[0]
                if isinstance(coluna.type, Integer):
                    valor = int(valor)
                elif isinstance(coluna.type, Boolean):
                    valor = valor.lower() in ('true', '1', 'yes', 'sim')
                # Caso seja String, manter o valor como está
                dados[atributo] = valor
        atualizar_registro(session, model_class, id_, **dados)
    else:
        print(f"{model_class.__name__} com {chave_primaria}={id_} não encontrado.")


def consulta_01():
    print("\n--- CONSULTA 01: Número de Passageiros por Voo ---")
    from sqlalchemy import func

    resultado = session.query(
        Voo.numero_voo,
        func.count(Passageiro.codigo_passageiro).label('num_passageiros')
    ).join(BilheteVoo, Voo.numero_voo == BilheteVoo.fk_Voo_numero_voo)\
     .join(Passageiro, BilheteVoo.fk_Passageiro_codigo_passageiro == Passageiro.codigo_passageiro)\
     .group_by(Voo.numero_voo)\
     .all()

    for numero_voo, num_passageiros in resultado:
        print(f"Voo {numero_voo} tem {num_passageiros} passageiros.")
        
    #gemini_interpretacao(resultado)
    # Gerar gráfico
    voos = [r[0] for r in resultado]
    passageiros = [r[1] for r in resultado]
    plt.bar(voos, passageiros, color='blue')
    plt.xlabel('Número do Voo')
    plt.ylabel('Número de Passageiros')
    plt.title('Número de Passageiros por Voo')
    plt.show()


def consulta_02():
    print("\n--- CONSULTA 02: Capacidade Média das Aeronaves por Empresa Aérea ---")
    from sqlalchemy import func

    resultado = session.query(
        EmpresaAerea.Nome,
        func.avg(Aeronave.capacidade).label('capacidade_media')
    ).join(Aeronave, EmpresaAerea.cod_empresa == Aeronave.fk_Empresa_Aerea_cod_empresa)\
     .group_by(EmpresaAerea.Nome)\
     .all()

    for nome_empresa, capacidade_media in resultado:
        print(f"Empresa: {nome_empresa}, Capacidade Média: {capacidade_media:.2f}")

    gemini_interpretacao(resultado)
    
    # Gerar gráfico
    empresas = [r[0] for r in resultado]
    capacidades = [r[1] for r in resultado]
    plt.bar(empresas, capacidades, color='green')
    plt.xlabel('Empresa Aérea')
    plt.ylabel('Capacidade Média')
    plt.title('Capacidade Média das Aeronaves por Empresa Aérea')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



def consulta_03():
    print("\n--- CONSULTA 03: Número Total de Voos por Destino ---")
    from sqlalchemy import func

    resultado = session.query(
        Destinos.Destino,
        func.count(Voo.numero_voo).label('num_voos')
    ).join(Voo, Voo.fk_Destinos_numero_destino == Destinos.numero_destino)\
     .group_by(Destinos.Destino)\
     .all()

    for destino, num_voos in resultado:
        print(f"Destino: {destino}, Número de Voos: {num_voos}")

    gemini_interpretacao(resultado)
    # Gerar gráfico
    destinos = [r[0] for r in resultado]
    num_voos = [r[1] for r in resultado]
    plt.bar(destinos, num_voos, color='orange')
    plt.xlabel('Destino')
    plt.ylabel('Número de Voos')
    plt.title('Número Total de Voos por Destino')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def consulta_extra():
    print("\n--- CONSULTA EXTRA: Número de Voos por Portão de Embarque Disponível e Capacidade Média das Aeronaves ---")

    resultado = session.query(
        PortaoEmbarque.codigo_portao,
        func.count(Voo.numero_voo).label('num_voos'),
        func.avg(Aeronave.capacidade).label('capacidade_media')
    ).join(
        usa_table, PortaoEmbarque.codigo_portao == usa_table.c.fk_Portao_Embarque_codigo_portao
    ).join(
        Voo, Voo.numero_voo == usa_table.c.fk_Voo_numero_voo
    ).join(
        Aeronave, Voo.fk_Aeronave_prefixo_aeronave == Aeronave.prefixo_aeronave
    ).filter(
        PortaoEmbarque.status == "Disponível"
    ).group_by(
        PortaoEmbarque.codigo_portao
    ).all()

    resultado_serializavel = [
        {
            "codigo_portao": row[0],
            "num_voos": row[1],
            "capacidade_media": float(row[2]) if row[2] is not None else None
        }
        for row in resultado
    ]

    for item in resultado_serializavel:
        print(f"Portão: {item['codigo_portao']}, Número de Voos: {item['num_voos']}, Capacidade Média das Aeronaves: {item['capacidade_media']:.2f}")

    # Passar o resultado serializável para o LLM

    local_llm_interpretacao(json.dumps(resultado_serializavel))
    #gemini_interpretacao(resultado)
    # Gerar gráfico
    """portoes = [r[0] for r in resultado]
    num_voos = [r[1] for r in resultado]
    capacidades = [r[2] for r in resultado]

    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Código do Portão')
    ax1.set_ylabel('Número de Voos', color=color)
    ax1.bar(portoes, num_voos, color=color, alpha=0.6)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # Instancia um segundo eixo que compartilha o mesmo eixo x

    color = 'tab:red'
    ax2.set_ylabel('Capacidade Média', color=color)
    ax2.plot(portoes, capacidades, color=color, marker='o')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Número de Voos e Capacidade Média por Portão de Embarque Disponível')
    plt.tight_layout()
    plt.show()"""





def local_llm_interpretacao(user_message):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    messages = [
        {"role": "system", "content": (
                "Você é um assistente especializado em interpretar consultas de banco de dados. "
                "O banco de dados 'aeroporto' contém informações sobre voos, passageiros, aeronaves, empresas aéreas, etc. "
                "As tabelas incluem: passageiro, bilhete_voo, voo, aeronave, empresa_aerea, portao_embarque, area_bagagem, tripulantes, destinos e manutencao. "
                "Essas tabelas se relacionam por meio de chaves estrangeiras, como 'bilhete_voo' que se conecta com 'passageiro' e 'voo'. "
                "Seu trabalho é fornecer explicações claras e úteis em português sobre consultas SQL e seus resultados, destacando insights acionáveis "
                "que ajudem na tomada de decisões. Responda de forma concisa, clara e sem formatação especial."
            )},
        
        {"role": "user", "content": user_message}
    ]
    
    print("\n")
    print(client.chat.completions.create(
        model="model-identifier",
        messages=messages,
        temperature=0.7
    ).choices[0].message.content)

def gemini_interpretacao(consulta_resultado, model_name="gemini-1.5-flash-002"):
    
    load_dotenv()

    api_key=os.getenv("GEMINI_API_KEY")
    client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
    )

    schema_description = """
    O banco de dados 'aeroporto' contém informações sobre voos, passageiros, aeronaves, empresas aéreas, etc.
    As tabelas incluem: passageiro, bilhete_voo, voo, aeronave, empresa_aerea, portao_embarque, area_bagagem, tripulantes, destinos e manutencao.  
    Elas se relacionam por meio de chaves estrangeiras. Por exemplo, 'bilhete_voo' se relaciona com 'passageiro' e 'voo'.
    """
    # Converter o resultado da consulta para JSON para facilitar o processamento pelo modelo
    json_result = json.dumps(consulta_resultado, indent=4, default=str)  # default=str para lidar com tipos de dados do SQLAlchemy

    response = client.chat.completions.create(
        model="gemini-1.5-flash-002",
        #model="gemini-1.5-pro-002",
        n=1,
        messages=[
            {
                "role": "system",
                "content": f"""Você é um assistente útil para interpretar consultas de banco de dados.
                {schema_description}
                Seu trabalho é fornecer uma breve explicação em português do significado de uma consulta SQL, com foco em insights acionáveis que ajudem na tomada de decisões.  
                Seja conciso e direto ao ponto. Concentre-se no que os dados revelam e nas possíveis implicações.
                """
            },
            {
                "role": "user",
                "content": f"Aqui está o resultado de uma consulta no banco de dados 'aeroporto':\n```json\n{json_result}\n```\nExplique o significado desta consulta e forneça insights acionáveis."
            }
        ]
    )

    print(response.choices[0].message.content)



# Configuração do banco de dados
def create_database():
    engine = create_engine('postgresql+psycopg2://vini:123@localhost:5432/aeroporto')

    Base.metadata.create_all(engine)
    print("Banco de dados criado com sucesso.")
    return engine



def limpar_dados():
    print("\n--- Limpando todos os dados do banco de dados ---")
    try:
        # Truncar tabelas de associação primeiro
        session.execute(text('TRUNCATE TABLE operaciona_table, usa_table, operaciona_manutencao_table RESTART IDENTITY CASCADE;'))
        # Truncar tabelas principais
        session.execute(text('TRUNCATE TABLE passageiro, bilhete_voo, voo, aeronave, empresa_aerea, destinos, area_bagagem, portao_embarque, tripulantes, manutencao RESTART IDENTITY CASCADE;'))
        session.commit()
        print("Todos os dados foram removidos com sucesso.")
    except Exception as e:
        session.rollback()
        print("Erro ao limpar os dados:", e)

def drop_tables():
    print("\n--- Eliminando todas as tabelas do banco de dados ---")
    try:
        session.commit()
        Base.metadata.drop_all(bind=engine)
        session.commit()
        print("Todas as tabelas foram eliminadas com sucesso.")
    except Exception as e:
        session.rollback()
        print("Erro ao eliminar as tabelas:", e)



def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

# Configuração da sessão
engine = create_engine('postgresql+psycopg2://vini:123@localhost:5432/aeroporto')

session = get_session(engine)


if __name__ == "__main__":
    menu_principal()


