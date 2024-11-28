from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

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
