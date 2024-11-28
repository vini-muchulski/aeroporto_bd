from crud import *
from models import *


def carregar_dados_iniciais(session):
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
    
    # Inserir dados na tabela EmpresaAerea
    criar_registro(session, EmpresaAerea, cod_empresa="AA", Nome="American Airlines", Pais="EUA")
    criar_registro(session, EmpresaAerea, cod_empresa="TP", Nome="TAP Portugal", Pais="Portugal")
    criar_registro(session, EmpresaAerea, cod_empresa="EM", Nome="Emirates", Pais="Emirados Árabes Unidos")
    criar_registro(session, EmpresaAerea, cod_empresa="BA", Nome="British Airways", Pais="Reino Unido")
    criar_registro(session, EmpresaAerea, cod_empresa="DL", Nome="Delta Air Lines", Pais="EUA")
    criar_registro(session, EmpresaAerea, cod_empresa="AF", Nome="Air France", Pais="França")
    
    
    # Inserir dados na tabela Aeronave
    criar_registro(session, Aeronave, prefixo_aeronave="AA-123", modelo="Boeing 737", capacidade=150, fk_Empresa_Aerea_cod_empresa="AA")
    criar_registro(session, Aeronave, prefixo_aeronave="TP-456", modelo="Airbus A320", capacidade=180, fk_Empresa_Aerea_cod_empresa="TP")
    criar_registro(session, Aeronave, prefixo_aeronave="AA-456", modelo="Boeing 747", capacidade=250, fk_Empresa_Aerea_cod_empresa="AA")
    criar_registro(session, Aeronave, prefixo_aeronave="TP-789", modelo="Airbus A330", capacidade=200, fk_Empresa_Aerea_cod_empresa="TP")
    criar_registro(session, Aeronave, prefixo_aeronave="EM-101", modelo="Boeing 787", capacidade=220, fk_Empresa_Aerea_cod_empresa="EM")
    criar_registro(session, Aeronave, prefixo_aeronave="BA-234", modelo="Airbus A350", capacidade=240, fk_Empresa_Aerea_cod_empresa="BA")
    criar_registro(session, Aeronave, prefixo_aeronave="DL-555", modelo="Airbus A220", capacidade=130, fk_Empresa_Aerea_cod_empresa="DL")
    criar_registro(session, Aeronave, prefixo_aeronave="AF-888", modelo="Boeing 777", capacidade=300, fk_Empresa_Aerea_cod_empresa="AF")
    

    # Inserir dados na tabela Destinos
    criar_registro(session, Destinos, numero_destino=1, Origem="São Paulo", Destino="Nova York")
    criar_registro(session, Destinos, numero_destino=2, Origem="Lisboa", Destino="Rio de Janeiro")
    criar_registro(session, Destinos, numero_destino=3, Origem="Madrid", Destino="São Paulo")
    criar_registro(session, Destinos, numero_destino=4, Origem="Paris", Destino="Rio de Janeiro")
    criar_registro(session, Destinos, numero_destino=5, Origem="Lisboa", Destino="Madrid")
    criar_registro(session, Destinos, numero_destino=6, Origem="Londres", Destino="Tóquio")
    criar_registro(session, Destinos, numero_destino=7, Origem="Roma", Destino="São Paulo")

    # Inserir dados na tabela AreaBagagem
    criar_registro(session, AreaBagagem, codigo_bagagem=3, status="Operacional")
    criar_registro(session, AreaBagagem, codigo_bagagem=4, status="Manutenção")

    # Inserir dados na tabela AreaBagagem
    criar_registro(session, AreaBagagem, codigo_bagagem=1, status="Operacional")
    criar_registro(session, AreaBagagem, codigo_bagagem=2, status="Manutenção")

    # Inserir dados na tabela Voo
    criar_registro(session, Voo, numero_voo=101, horario_chegada="12:00", horario_partida="08:00", fk_Area_Bagagem_codigo_bagagem=1, fk_Aeronave_prefixo_aeronave="AA-123", fk_Destinos_numero_destino=1)
    criar_registro(session, Voo, numero_voo=202, horario_chegada="18:30", horario_partida="14:00", fk_Area_Bagagem_codigo_bagagem=2, fk_Aeronave_prefixo_aeronave="TP-456", fk_Destinos_numero_destino=2)
    criar_registro(session, Voo, numero_voo=303, horario_chegada="14:00", horario_partida="10:00", fk_Area_Bagagem_codigo_bagagem=1, fk_Aeronave_prefixo_aeronave="AA-456", fk_Destinos_numero_destino=3)
    criar_registro(session, Voo, numero_voo=404, horario_chegada="20:00", horario_partida="16:00", fk_Area_Bagagem_codigo_bagagem=2, fk_Aeronave_prefixo_aeronave="TP-789", fk_Destinos_numero_destino=4)
    criar_registro(session, Voo, numero_voo=505, horario_chegada="11:00", horario_partida="07:00", fk_Area_Bagagem_codigo_bagagem=1, fk_Aeronave_prefixo_aeronave="EM-101", fk_Destinos_numero_destino=5)
    criar_registro(session, Voo, numero_voo=606, horario_chegada="06:00", horario_partida="22:00", fk_Area_Bagagem_codigo_bagagem=1, fk_Aeronave_prefixo_aeronave="DL-555", fk_Destinos_numero_destino=6)
    criar_registro(session, Voo, numero_voo=707, horario_chegada="10:00", horario_partida="02:00", fk_Area_Bagagem_codigo_bagagem=2, fk_Aeronave_prefixo_aeronave="AF-888", fk_Destinos_numero_destino=7)
    
    
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
    
    # Inserir dados na tabela PortaoEmbarque
    criar_registro(session, PortaoEmbarque, codigo_portao="A1", localizacao="Terminal 1", status="Disponível")
    criar_registro(session, PortaoEmbarque, codigo_portao="B2", localizacao="Terminal 2", status="Ocupado")
    criar_registro(session, PortaoEmbarque, codigo_portao="C3", localizacao="Terminal 3", status="Disponível")
    criar_registro(session, PortaoEmbarque, codigo_portao="D4", localizacao="Terminal 4", status="Ocupado")
    criar_registro(session, PortaoEmbarque, codigo_portao="E5", localizacao="Terminal 5", status="Disponível")
    
    # Inserir dados na tabela Tripulante
    criar_registro(session, Tripulante, id_funcionario=100, nome="Carlos Santos", cargo="Piloto", setor="Operações")
    criar_registro(session, Tripulante, id_funcionario=101, nome="Ana Oliveira", cargo="Comissária", setor="Atendimento")
    criar_registro(session, Tripulante, id_funcionario=102, nome="Miguel Fernandes", cargo="Piloto", setor="Operações")
    criar_registro(session, Tripulante, id_funcionario=103, nome="Sofia Gomes", cargo="Comissário", setor="Atendimento")
    criar_registro(session, Tripulante, id_funcionario=104, nome="Mariana Silva", cargo="Piloto", setor="Operações")
    
    # Inserir dados na tabela Manutencao
    criar_registro(session, Manutencao, ID_Manutencao=1, Data="2023-01-10", Tipo="Preventiva")
    criar_registro(session, Manutencao, ID_Manutencao=2, Data="2023-02-15", Tipo="Corretiva")
    criar_registro(session, Manutencao, ID_Manutencao=3, Data="2023-03-20", Tipo="Preventiva")
    criar_registro(session, Manutencao, ID_Manutencao=4, Data="2023-04-15", Tipo="Corretiva")
    criar_registro(session, Manutencao, ID_Manutencao=5, Data="2023-05-10", Tipo="Preventiva")

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

