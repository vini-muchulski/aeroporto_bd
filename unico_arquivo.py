from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

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


def ler_registro(session, modelo, id_):
    chave_primaria = obter_nome_chave_primaria(modelo)
    filtro = {chave_primaria: id_}
    registro = session.query(modelo).filter_by(**filtro).first()
    return registro

def atualizar_registro(session, modelo, id_, **kwargs):
    chave_primaria = obter_nome_chave_primaria(modelo)
    filtro = {chave_primaria: id_}
    registro = session.query(modelo).filter_by(**filtro).first()
    if registro:
        for chave, valor in kwargs.items():
            setattr(registro, chave, valor)
        session.commit()
        print(f"{modelo.__name__} {id_} atualizado com sucesso.")
        return registro
    else:
        print(f"{modelo.__name__} {id_} não encontrado.")
        return None

def deletar_registro(session, modelo, id_):
    chave_primaria = obter_nome_chave_primaria(modelo)
    filtro = {chave_primaria: id_}
    registro = session.query(modelo).filter_by(**filtro).first()
    if registro:
        session.delete(registro)
        session.commit()
        print(f"{modelo.__name__} {id_} deletado com sucesso.")
    else:
        print(f"{modelo.__name__} {id_} não encontrado.")

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

    # Inserir dados na tabela EmpresaAerea
    criar_registro(session, EmpresaAerea, cod_empresa="AA", Nome="American Airlines", Pais="EUA")
    criar_registro(session, EmpresaAerea, cod_empresa="TP", Nome="TAP Portugal", Pais="Portugal")

    # Inserir dados na tabela Aeronave
    criar_registro(session, Aeronave, prefixo_aeronave="AA-123", modelo="Boeing 737", capacidade=150, fk_Empresa_Aerea_cod_empresa="AA")
    criar_registro(session, Aeronave, prefixo_aeronave="TP-456", modelo="Airbus A320", capacidade=180, fk_Empresa_Aerea_cod_empresa="TP")

    # Inserir dados na tabela Destinos
    criar_registro(session, Destinos, numero_destino=1, Origem="São Paulo", Destino="Nova York")
    criar_registro(session, Destinos, numero_destino=2, Origem="Lisboa", Destino="Rio de Janeiro")

    # Inserir dados na tabela AreaBagagem
    criar_registro(session, AreaBagagem, codigo_bagagem=1, status="Operacional")
    criar_registro(session, AreaBagagem, codigo_bagagem=2, status="Manutenção")

    # Inserir dados na tabela Voo
    criar_registro(session, Voo, numero_voo=101, horario_chegada="12:00", horario_partida="08:00", fk_Area_Bagagem_codigo_bagagem=1, fk_Aeronave_prefixo_aeronave="AA-123", fk_Destinos_numero_destino=1)
    criar_registro(session, Voo, numero_voo=202, horario_chegada="18:30", horario_partida="14:00", fk_Area_Bagagem_codigo_bagagem=2, fk_Aeronave_prefixo_aeronave="TP-456", fk_Destinos_numero_destino=2)

    # Inserir dados na tabela BilheteVoo
    criar_registro(session, BilheteVoo, numero_bilhete=1001, classe="Economica", nome_passageiro="João Silva", status="Confirmado", fk_Passageiro_codigo_passageiro=1, fk_Voo_numero_voo=101)
    criar_registro(session, BilheteVoo, numero_bilhete=1002, classe="Executiva", nome_passageiro="Maria Souza", status="Pendente", fk_Passageiro_codigo_passageiro=2, fk_Voo_numero_voo=202)

    # Inserir dados na tabela PortaoEmbarque
    criar_registro(session, PortaoEmbarque, codigo_portao="A1", localizacao="Terminal 1", status="Disponível")
    criar_registro(session, PortaoEmbarque, codigo_portao="B2", localizacao="Terminal 2", status="Ocupado")

    # Inserir dados na tabela Tripulante
    criar_registro(session, Tripulante, id_funcionario=100, nome="Carlos Santos", cargo="Piloto", setor="Operações")
    criar_registro(session, Tripulante, id_funcionario=101, nome="Ana Oliveira", cargo="Comissária", setor="Atendimento")

    # Inserir dados na tabela Manutencao
    criar_registro(session, Manutencao, ID_Manutencao=1, Data="2023-01-10", Tipo="Preventiva")
    criar_registro(session, Manutencao, ID_Manutencao=2, Data="2023-02-15", Tipo="Corretiva")



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
        12. Sair
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
            drop_tables()
        elif opcao == '12':
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

def consulta_01():
    print("\n--- CONSULTA 01: Lista de passageiros com bilhetes confirmados ---")
    resultado = session.query(Passageiro).join(BilheteVoo).filter(BilheteVoo.status == "Confirmado").all()
    for passageiro in resultado:
        print(f"Código: {passageiro.codigo_passageiro}, Nome: {passageiro.nome}")

def consulta_02():
    print("\n--- CONSULTA 02: Voos programados para hoje ---")
    # Supondo que 'horario_partida' seja uma string com a data e hora
    from datetime import datetime
    hoje = datetime.now().strftime('%Y-%m-%d')
    resultado = session.query(Voo).filter(Voo.horario_partida.contains(hoje)).all()
    for voo in resultado:
        print(f"Número do Voo: {voo.numero_voo}, Partida: {voo.horario_partida}")

def consulta_03():
    print("\n--- CONSULTA 03: Lista de Tripulantes e seus Voos ---")
    resultado = session.query(Tripulante).all()
    for tripulante in resultado:
        voos = ', '.join([str(voo.numero_voo) for voo in tripulante.voos])
        print(f"ID: {tripulante.id_funcionario}, Nome: {tripulante.nome}, Voos: {voos if voos else 'Nenhum'}")

def consulta_extra():
    print("\n--- CONSULTA EXTRA: Portões de Embarque Disponíveis e Voos Associados ---")
    portoes = session.query(PortaoEmbarque).filter(PortaoEmbarque.status == "Disponível").all()
    for portao in portoes:
        voos = ', '.join([str(voo.numero_voo) for voo in portao.voos])
        print(f"Código do Portão: {portao.codigo_portao}, Voos: {voos if voos else 'Nenhum'}")


def atualizar_valor_especifico():
    print("\n--- Atualizar valor específico ---")
    print("Selecione a tabela:")
    print("1. Passageiro")
    print("2. Voo")
    # Adicione outras tabelas conforme necessário
    tabela_opcao = input("Opção: ")

    if tabela_opcao == '1':
        model_class = Passageiro
    elif tabela_opcao == '2':
        model_class = Voo
    else:
        print("Opção inválida.")
        return

    chave_primaria = obter_nome_chave_primaria(model_class)
    id_ = input(f"Digite o valor da chave primária ({chave_primaria}): ")
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
                dados[atributo] = valor
        atualizar_registro(session, model_class, id_, **dados)
    else:
        print(f"{model_class.__name__} com {chave_primaria}={id_} não encontrado.")







# Configuração do banco de dados
def create_database():
    engine = create_engine('sqlite:///aeroporto.db')
    Base.metadata.create_all(engine)
    print("Banco de dados criado com sucesso.")
    return engine

def drop_tables():
    engine = create_engine('sqlite:///aeroporto.db')
    Base.metadata.drop_all(engine)
    print("Todas as tabelas foram eliminadas com sucesso.")


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

# Configuração da sessão
engine = create_engine('sqlite:///aeroporto.db')
session = get_session(engine)






 
if __name__ == "__main__":
    menu_principal()


