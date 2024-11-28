from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Table, text , func
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import matplotlib.pyplot as plt
import json


from crud import *
from models import *  
from data_loader import carregar_dados_iniciais
from llm_advice import gemini_interpretacao, local_llm_interpretacao
##########################################



def imprimir_dados():
    modelos = [Passageiro, BilheteVoo, Voo, Aeronave, EmpresaAerea, Destinos, AreaBagagem, PortaoEmbarque, Tripulante, Manutencao]
    for modelo in modelos:
        registros = session.query(modelo).all()
        print(f"\n--- {modelo.__name__} ---")
        for registro in registros:
            atributos = vars(registro)
            atributos_limpos = {chave: valor for chave, valor in atributos.items() if not chave.startswith('_')}
            print(atributos_limpos)
            
            

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
            carregar_dados_iniciais(session)
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
    
    #print(resultado)
    print("Resposta da LLM: ")  
    gemini_interpretacao(resultado,titulo_consulta="Número de Passageiros por Voo")
    # Gerar gráfico
    voos = [r[0] for r in resultado]
    passageiros = [r[1] for r in resultado]
    plt.bar(voos, passageiros, color='blue',width=7)
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

    #print(resultado)
    print("Resposta da LLM: ")
    gemini_interpretacao(resultado,titulo_consulta="Capacidade Média das Aeronaves por Empresa Aérea")
    
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

    print("Resposta da LLM: ")
    gemini_interpretacao(resultado,titulo_consulta="Número Total de Voos por Destino")
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

    print("Resposta da LLM: ")
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


