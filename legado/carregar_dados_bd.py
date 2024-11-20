from crud_operations import *

def imprimir_dados():
    print("\n--- Passageiros ---")
    for passageiro in ler_todos_passageiros():
        print(f"Código: {passageiro.codigo_passageiro}, Nome: {passageiro.nome}, Documento: {passageiro.documento}, Contato: {passageiro.contato}, Controle de Segurança: {passageiro.ControleSeguranca}")

    print("\n--- Bilhetes de Voo ---")
    for bilhete in ler_todos_bilhetes_voo():
        print(f"Número: {bilhete.numero_bilhete}, Classe: {bilhete.classe}, Passageiro: {bilhete.nome_passageiro}, Status: {bilhete.status}, FK Passageiro: {bilhete.fk_Passageiro_codigo_passageiro}, FK Voo: {bilhete.fk_Voo_numero_voo}")

    print("\n--- Voos ---")
    for voo in ler_todos_voos():
        print(f"Número: {voo.numero_voo}, Chegada: {voo.horario_chegada}, Partida: {voo.horario_partida}, FK Área Bagagem: {voo.fk_Area_Bagagem_codigo_bagagem}, FK Aeronave: {voo.fk_Aeronave_prefixo_aeronave}, FK Destino: {voo.fk_Destinos_numero_destino}")

    print("\n--- Aeronaves ---")
    for aeronave in ler_todas_aeronaves():
        print(f"Prefixo: {aeronave.prefixo_aeronave}, Modelo: {aeronave.modelo}, Capacidade: {aeronave.capacidade}, FK Empresa Aérea: {aeronave.fk_Empresa_Aerea_cod_empresa}")

    print("\n--- Empresas Aéreas ---")
    for empresa in ler_todas_empresas_aereas():
        print(f"Código: {empresa.cod_empresa}, Nome: {empresa.Nome}, País: {empresa.Pais}")

    print("\n--- Destinos ---")
    for destino in ler_todos_destinos():
        print(f"Número: {destino.numero_destino}, Origem: {destino.Origem}, Destino: {destino.Destino}")

    print("\n--- Áreas de Bagagem ---")
    for area in ler_todas_areas_bagagem():
        print(f"Código: {area.codigo_bagagem}, Status: {area.status}")

    print("\n--- Portões de Embarque ---")
    for portao in ler_todos_portoes_embarque():
        print(f"Código: {portao.codigo_portao}, Localização: {portao.localizacao}, Status: {portao.status}")

    print("\n--- Tripulantes ---")
    for tripulante in ler_todos_tripulantes():
        print(f"ID: {tripulante.id_funcionario}, Nome: {tripulante.nome}, Cargo: {tripulante.cargo}, Setor: {tripulante.setor}")

    print("\n--- Manutenções ---")
    for manutencao in ler_todas_manutencoes():
        print(f"ID: {manutencao.ID_Manutencao}, Data: {manutencao.Data}, Tipo: {manutencao.Tipo}")
        
def carregar_dados_iniciais():
    # Inserir dados na tabela Passageiro
    criar_passageiro(1, "João Silva", "123456789", 999999999, True)
    criar_passageiro(2, "Maria Souza", "987654321", 888888888, False)

    # Inserir dados na tabela EmpresaAerea
    criar_empresa_aerea("AA", "American Airlines", "EUA")
    criar_empresa_aerea("TP", "TAP Portugal", "Portugal")

    # Inserir dados na tabela Aeronave
    criar_aeronave("AA-123", "Boeing 737", 150, "AA")
    criar_aeronave("TP-456", "Airbus A320", 180, "TP")

    # Inserir dados na tabela Destinos
    criar_destino(1, "São Paulo", "Nova York")
    criar_destino(2, "Lisboa", "Rio de Janeiro")

    # Inserir dados na tabela AreaBagagem
    criar_area_bagagem(1, "Operacional")
    criar_area_bagagem(2, "Manutenção")

    # Inserir dados na tabela Voo
    criar_voo(101, "12:00", "08:00", 1, "AA-123", 1)
    criar_voo(202, "18:30", "14:00", 2, "TP-456", 2)

    # Inserir dados na tabela BilheteVoo
    criar_bilhete_voo(1001, "Economica", "João Silva", "Confirmado", 1, 101)
    criar_bilhete_voo(1002, "Executiva", "Maria Souza", "Pendente", 2, 202)

    # Inserir dados na tabela PortaoEmbarque
    criar_portao_embarque("A1", "Terminal 1", "Disponível")
    criar_portao_embarque("B2", "Terminal 2", "Ocupado")

    # Inserir dados na tabela Tripulante
    criar_tripulante(100, "Carlos Santos", "Piloto", "Operações")
    criar_tripulante(101, "Ana Oliveira", "Comissária", "Atendimento")

    # Inserir dados na tabela Manutencao
    criar_manutencao(1, "2023-01-10", "Preventiva")
    criar_manutencao(2, "2023-02-15", "Corretiva")

if __name__ == "__main__":
    #carregar_dados_iniciais()
    #print("Dados iniciais carregados com sucesso.")
    imprimir_dados()