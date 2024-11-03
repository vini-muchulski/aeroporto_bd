# models.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Configuração do banco de dados
engine = create_engine('sqlite:///aeroporto.db', echo=True)

# Declarar a base
Base = declarative_base()

# Definição das classes que representam as tabelas

class Passageiro(Base):
    __tablename__ = 'Passageiro'
    codigo_passageiro = Column(Integer, primary_key=True)
    nome = Column(String)
    documento = Column(String)
    contato = Column(String)

    # Relações
    bilhetes = relationship('BilheteVoo', secondary='Compra', back_populates='passageiros')
    controles_seguranca = relationship('ControleSeguranca', secondary='Passa_por', back_populates='passageiros')
    areas_bagagem = relationship('AreaBagagem', secondary='Despacha', back_populates='passageiros')

class BilheteVoo(Base):
    __tablename__ = 'Bilhete_Voo'
    numero_bilhete = Column(Integer, primary_key=True)
    classe = Column(Integer)
    nome_passageiro = Column(String)
    status = Column(String)

    # Relações
    passageiros = relationship('Passageiro', secondary='Compra', back_populates='bilhetes')
    voos = relationship('Voo', secondary='relaciona_se', back_populates='bilhetes')

class Voo(Base):
    __tablename__ = 'Voo'
    numero_voo = Column(Integer, primary_key=True)
    origem = Column(String)
    destino = Column(String)
    horario_chegada = Column(String)
    horario_partida = Column(String)

    # Relações
    bilhetes = relationship('BilheteVoo', secondary='relaciona_se', back_populates='voos')
    area_bagagem = relationship('AreaBagagem', secondary='esta_associado_a', back_populates='voos')
    companhia_aerea = relationship('CompanhiaAerea', secondary='e_operado_por', back_populates='voos')
    portao_embarque = relationship('PortaoEmbarque', secondary='usa', back_populates='voos')
    aeronaves = relationship('Aeronave', secondary='usava', back_populates='voos')

class Aeronave(Base):
    __tablename__ = 'Aeronave'
    prefixo_aeronave = Column(String, primary_key=True)
    modelo = Column(String)
    capacidade = Column(Integer)

    # Relações
    voos = relationship('Voo', secondary='usava', back_populates='aeronaves')

class PortaoEmbarque(Base):
    __tablename__ = 'Portao_Embarque'
    codigo_portao = Column(Integer, primary_key=True)
    localizacao = Column(String)
    status = Column(String)

    # Relações
    voos = relationship('Voo', secondary='usa', back_populates='portao_embarque')

class CompanhiaAerea(Base):
    __tablename__ = 'Companhia_Aerea'
    codigo_companhia = Column(Integer, primary_key=True)
    nome = Column(String)
    pais = Column(String)

    # Relações
    voos = relationship('Voo', secondary='e_operado_por', back_populates='companhia_aerea')

class AreaBagagem(Base):
    __tablename__ = 'Area_Bagagem'
    codigo_bagagem = Column(Integer, primary_key=True)
    status = Column(String)

    # Relações
    passageiros = relationship('Passageiro', secondary='Despacha', back_populates='areas_bagagem')
    voos = relationship('Voo', secondary='esta_associado_a', back_populates='area_bagagem')

class ControleSeguranca(Base):
    __tablename__ = 'Controle_Seguranca'
    codigo_seguranca = Column(Integer, primary_key=True)
    inspecao = Column(String)
    status = Column(String)

    # Relações
    passageiros = relationship('Passageiro', secondary='Passa_por', back_populates='controles_seguranca')

class Funcionario(Base):
    __tablename__ = 'Funcionario'
    id_funcionario = Column(Integer, primary_key=True)
    nome = Column(String)
    cargo = Column(String)
    setor = Column(String)

    # Relações
    servicos = relationship('ServicosAeroportuarios', secondary='Realiza', back_populates='funcionarios')

class ServicosAeroportuarios(Base):
    __tablename__ = 'Servicoes_AeroPortuarios'
    codigo_servico = Column(Integer, primary_key=True)
    descricao = Column(String)

    # Relações
    funcionarios = relationship('Funcionario', secondary='Realiza', back_populates='servicos')

# Tabelas associativas

class Compra(Base):
    __tablename__ = 'Compra'
    fk_Passageiro_codigo_passageiro = Column(Integer, ForeignKey('Passageiro.codigo_passageiro', ondelete='SET NULL'), primary_key=True)
    fk_Bilhete_Voo_numero_bilhete = Column(Integer, ForeignKey('Bilhete_Voo.numero_bilhete', ondelete='SET NULL'), primary_key=True)

class PassaPor(Base):
    __tablename__ = 'Passa_por'
    fk_Passageiro_codigo_passageiro = Column(Integer, ForeignKey('Passageiro.codigo_passageiro', ondelete='SET NULL'), primary_key=True)
    fk_Controle_Seguranca_codigo_seguranca = Column(Integer, ForeignKey('Controle_Seguranca.codigo_seguranca', ondelete='SET NULL'), primary_key=True)

class Realiza(Base):
    __tablename__ = 'Realiza'
    fk_Funcionario_id_funcionario = Column(Integer, ForeignKey('Funcionario.id_funcionario', ondelete='SET NULL'), primary_key=True)
    fk_Servicoes_AeroPortuarios_codigo_servico = Column(Integer, ForeignKey('Servicoes_AeroPortuarios.codigo_servico', ondelete='SET NULL'), primary_key=True)

class Despacha(Base):
    __tablename__ = 'Despacha'
    fk_Passageiro_codigo_passageiro = Column(Integer, ForeignKey('Passageiro.codigo_passageiro', ondelete='SET NULL'), primary_key=True)
    fk_Area_Bagagem_codigo_bagagem = Column(Integer, ForeignKey('Area_Bagagem.codigo_bagagem', ondelete='SET NULL'), primary_key=True)

class EstaAssociadoA(Base):
    __tablename__ = 'esta_associado_a'
    fk_Voo_numero_voo = Column(Integer, ForeignKey('Voo.numero_voo', ondelete='SET NULL'), primary_key=True)
    fk_Area_Bagagem_codigo_bagagem = Column(Integer, ForeignKey('Area_Bagagem.codigo_bagagem', ondelete='SET NULL'), primary_key=True)

class EOperadoPor(Base):
    __tablename__ = 'e_operado_por'
    fk_Voo_numero_voo = Column(Integer, ForeignKey('Voo.numero_voo', ondelete='SET NULL'), primary_key=True)
    fk_Companhia_Aerea_codigo_companhia = Column(Integer, ForeignKey('Companhia_Aerea.codigo_companhia', ondelete='SET NULL'), primary_key=True)

class Usa(Base):
    __tablename__ = 'usa'
    fk_Voo_numero_voo = Column(Integer, ForeignKey('Voo.numero_voo', ondelete='SET NULL'), primary_key=True)
    fk_Portao_Embarque_codigo_portao = Column(Integer, ForeignKey('Portao_Embarque.codigo_portao', ondelete='SET NULL'), primary_key=True)

class Usava(Base):
    __tablename__ = 'usava'
    fk_Aeronave_prefixo_aeronave = Column(String, ForeignKey('Aeronave.prefixo_aeronave', ondelete='SET NULL'), primary_key=True)
    fk_Voo_numero_voo = Column(Integer, ForeignKey('Voo.numero_voo', ondelete='SET NULL'), primary_key=True)

class RelacionaSe(Base):
    __tablename__ = 'relaciona_se'
    fk_Bilhete_Voo_numero_bilhete = Column(Integer, ForeignKey('Bilhete_Voo.numero_bilhete', ondelete='SET NULL'), primary_key=True)
    fk_Voo_numero_voo = Column(Integer, ForeignKey('Voo.numero_voo', ondelete='SET NULL'), primary_key=True)

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)

# Criar uma fábrica de sessões
Session = sessionmaker(bind=engine)
