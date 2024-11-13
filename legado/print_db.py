# print_database.py

from models import Session, Passageiro, BilheteVoo, Voo, Aeronave, PortaoEmbarque, CompanhiaAerea, AreaBagagem, ControleSeguranca, Funcionario, ServicosAeroportuarios

# Criar uma sessão
session = Session()

def print_passageiros():
    passageiros = session.query(Passageiro).all()
    print("\nPassageiros:")
    for p in passageiros:
        print(f'Código: {p.codigo_passageiro}, Nome: {p.nome}, Documento: {p.documento}, Contato: {p.contato}')

def print_bilhetes():
    bilhetes = session.query(BilheteVoo).all()
    print("\nBilhetes de Voo:")
    for b in bilhetes:
        print(f'Número: {b.numero_bilhete}, Classe: {b.classe}, Nome Passageiro: {b.nome_passageiro}, Status: {b.status}')

def print_voos():
    voos = session.query(Voo).all()
    print("\nVoos:")
    for v in voos:
        print(f'Número: {v.numero_voo}, Origem: {v.origem}, Destino: {v.destino}, Horário Partida: {v.horario_partida}, Horário Chegada: {v.horario_chegada}')

def print_aeronaves():
    aeronaves = session.query(Aeronave).all()
    print("\nAeronaves:")
    for a in aeronaves:
        print(f'Prefixo: {a.prefixo_aeronave}, Modelo: {a.modelo}, Capacidade: {a.capacidade}')

def print_portoes_embarque():
    portoes = session.query(PortaoEmbarque).all()
    print("\nPortões de Embarque:")
    for p in portoes:
        print(f'Código: {p.codigo_portao}, Localização: {p.localizacao}, Status: {p.status}')

def print_companhias_aereas():
    companhias = session.query(CompanhiaAerea).all()
    print("\nCompanhias Aéreas:")
    for c in companhias:
        print(f'Código: {c.codigo_companhia}, Nome: {c.nome}, País: {c.pais}')

def print_areas_bagagem():
    areas = session.query(AreaBagagem).all()
    print("\nÁreas de Bagagem:")
    for a in areas:
        print(f'Código: {a.codigo_bagagem}, Status: {a.status}')

def print_controles_seguranca():
    controles = session.query(ControleSeguranca).all()
    print("\nControles de Segurança:")
    for c in controles:
        print(f'Código: {c.codigo_seguranca}, Inspeção: {c.inspecao}, Status: {c.status}')

def print_funcionarios():
    funcionarios = session.query(Funcionario).all()
    print("\nFuncionários:")
    for f in funcionarios:
        print(f'ID: {f.id_funcionario}, Nome: {f.nome}, Cargo: {f.cargo}, Setor: {f.setor}')

def print_servicos_aeroportuarios():
    servicos = session.query(ServicosAeroportuarios).all()
    print("\nServiços Aeroportuários:")
    for s in servicos:
        print(f'Código: {s.codigo_servico}, Descrição: {s.descricao}')

def print_todas_tabelas():
    print_passageiros()
""" print_bilhetes()
    print_voos()
    print_aeronaves()
    print_portoes_embarque()
    print_companhias_aereas()
    print_areas_bagagem()
    print_controles_seguranca()
    print_funcionarios()
    print_servicos_aeroportuarios()"""

if __name__ == '__main__':
    print_todas_tabelas()
    session.close()
