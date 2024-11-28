from legado.models import * 
"""
(
    get_session, Passageiro, BilheteVoo, Voo, Aeronave,
    EmpresaAerea, Destinos, AreaBagagem, PortaoEmbarque, Tripulante, Manutencao
)
"""
from sqlalchemy import create_engine

# Configuração da sessão
engine = create_engine('sqlite:///aeroporto.db')
session = get_session(engine)

# Funções CRUD para a tabela Passageiro

def criar_passageiro(codigo, nome, documento, contato, controle_seguranca):
    passageiro = Passageiro(
        codigo_passageiro=codigo,
        nome=nome,
        documento=documento,
        contato=contato,
        ControleSeguranca=controle_seguranca
    )
    session.add(passageiro)
    session.commit()
    print(f"Passageiro {nome} criado com sucesso.")

def ler_passageiro(codigo):
    passageiro = session.query(Passageiro).filter_by(codigo_passageiro=codigo).first()
    return passageiro

def atualizar_passageiro(codigo, nome=None, documento=None, contato=None, controle_seguranca=None):
    passageiro = session.query(Passageiro).filter_by(codigo_passageiro=codigo).first()
    if passageiro:
        if nome:
            passageiro.nome = nome
        if documento:
            passageiro.documento = documento
        if contato:
            passageiro.contato = contato
        if controle_seguranca is not None:
            passageiro.ControleSeguranca = controle_seguranca
        session.commit()
        print(f"Passageiro {codigo} atualizado com sucesso.")
    else:
        print(f"Passageiro {codigo} não encontrado.")

def deletar_passageiro(codigo):
    passageiro = session.query(Passageiro).filter_by(codigo_passageiro=codigo).first()
    if passageiro:
        session.delete(passageiro)
        session.commit()
        print(f"Passageiro {codigo} deletado com sucesso.")
    else:
        print(f"Passageiro {codigo} não encontrado.")

# Funções CRUD para a tabela BilheteVoo

def criar_bilhete_voo(numero_bilhete, classe, nome_passageiro, status, fk_Passageiro_codigo_passageiro, fk_Voo_numero_voo):
    bilhete = BilheteVoo(
        numero_bilhete=numero_bilhete,
        classe=classe,
        nome_passageiro=nome_passageiro,
        status=status,
        fk_Passageiro_codigo_passageiro=fk_Passageiro_codigo_passageiro,
        fk_Voo_numero_voo=fk_Voo_numero_voo
    )
    session.add(bilhete)
    session.commit()
    print(f"Bilhete {numero_bilhete} criado com sucesso.")

def ler_bilhete_voo(numero_bilhete):
    bilhete = session.query(BilheteVoo).filter_by(numero_bilhete=numero_bilhete).first()
    return bilhete

def atualizar_bilhete_voo(numero_bilhete, classe=None, nome_passageiro=None, status=None, fk_Passageiro_codigo_passageiro=None, fk_Voo_numero_voo=None):
    bilhete = session.query(BilheteVoo).filter_by(numero_bilhete=numero_bilhete).first()
    if bilhete:
        if classe:
            bilhete.classe = classe
        if nome_passageiro:
            bilhete.nome_passageiro = nome_passageiro
        if status:
            bilhete.status = status
        if fk_Passageiro_codigo_passageiro:
            bilhete.fk_Passageiro_codigo_passageiro = fk_Passageiro_codigo_passageiro
        if fk_Voo_numero_voo:
            bilhete.fk_Voo_numero_voo = fk_Voo_numero_voo
        session.commit()
        print(f"Bilhete {numero_bilhete} atualizado com sucesso.")
    else:
        print(f"Bilhete {numero_bilhete} não encontrado.")

def deletar_bilhete_voo(numero_bilhete):
    bilhete = session.query(BilheteVoo).filter_by(numero_bilhete=numero_bilhete).first()
    if bilhete:
        session.delete(bilhete)
        session.commit()
        print(f"Bilhete {numero_bilhete} deletado com sucesso.")
    else:
        print(f"Bilhete {numero_bilhete} não encontrado.")

# Funções CRUD para a tabela Voo

def criar_voo(numero_voo, horario_chegada, horario_partida, fk_area_bagagem, fk_aeronave, fk_destino):
    voo = Voo(
        numero_voo=numero_voo,
        horario_chegada=horario_chegada,
        horario_partida=horario_partida,
        fk_Area_Bagagem_codigo_bagagem=fk_area_bagagem,
        fk_Aeronave_prefixo_aeronave=fk_aeronave,
        fk_Destinos_numero_destino=fk_destino
    )
    session.add(voo)
    session.commit()
    print(f"Voo {numero_voo} criado com sucesso.")

def ler_voo(numero_voo):
    voo = session.query(Voo).filter_by(numero_voo=numero_voo).first()
    return voo

def atualizar_voo(numero_voo, horario_chegada=None, horario_partida=None, fk_area_bagagem=None, fk_aeronave=None, fk_destino=None):
    voo = session.query(Voo).filter_by(numero_voo=numero_voo).first()
    if voo:
        if horario_chegada:
            voo.horario_chegada = horario_chegada
        if horario_partida:
            voo.horario_partida = horario_partida
        if fk_area_bagagem:
            voo.fk_Area_Bagagem_codigo_bagagem = fk_area_bagagem
        if fk_aeronave:
            voo.fk_Aeronave_prefixo_aeronave = fk_aeronave
        if fk_destino:
            voo.fk_Destinos_numero_destino = fk_destino
        session.commit()
        print(f"Voo {numero_voo} atualizado com sucesso.")
    else:
        print(f"Voo {numero_voo} não encontrado.")

def deletar_voo(numero_voo):
    voo = session.query(Voo).filter_by(numero_voo=numero_voo).first()
    if voo:
        session.delete(voo)
        session.commit()
        print(f"Voo {numero_voo} deletado com sucesso.")
    else:
        print(f"Voo {numero_voo} não encontrado.")

# Funções CRUD para a tabela Aeronave

def criar_aeronave(prefixo_aeronave, modelo, capacidade, fk_empresa_aerea):
    aeronave = Aeronave(
        prefixo_aeronave=prefixo_aeronave,
        modelo=modelo,
        capacidade=capacidade,
        fk_Empresa_Aerea_cod_empresa=fk_empresa_aerea
    )
    session.add(aeronave)
    session.commit()
    print(f"Aeronave {prefixo_aeronave} criada com sucesso.")

def ler_aeronave(prefixo_aeronave):
    aeronave = session.query(Aeronave).filter_by(prefixo_aeronave=prefixo_aeronave).first()
    return aeronave

def atualizar_aeronave(prefixo_aeronave, modelo=None, capacidade=None, fk_empresa_aerea=None):
    aeronave = session.query(Aeronave).filter_by(prefixo_aeronave=prefixo_aeronave).first()
    if aeronave:
        if modelo:
            aeronave.modelo = modelo
        if capacidade:
            aeronave.capacidade = capacidade
        if fk_empresa_aerea:
            aeronave.fk_Empresa_Aerea_cod_empresa = fk_empresa_aerea
        session.commit()
        print(f"Aeronave {prefixo_aeronave} atualizada com sucesso.")
    else:
        print(f"Aeronave {prefixo_aeronave} não encontrada.")

def deletar_aeronave(prefixo_aeronave):
    aeronave = session.query(Aeronave).filter_by(prefixo_aeronave=prefixo_aeronave).first()
    if aeronave:
        session.delete(aeronave)
        session.commit()
        print(f"Aeronave {prefixo_aeronave} deletada com sucesso.")
    else:
        print(f"Aeronave {prefixo_aeronave} não encontrada.")

# Funções CRUD para a tabela EmpresaAerea

def criar_empresa_aerea(cod_empresa, nome, pais):
    empresa = EmpresaAerea(
        cod_empresa=cod_empresa,
        Nome=nome,
        Pais=pais
    )
    session.add(empresa)
    session.commit()
    print(f"Empresa Aérea {nome} criada com sucesso.")

def ler_empresa_aerea(cod_empresa):
    empresa = session.query(EmpresaAerea).filter_by(cod_empresa=cod_empresa).first()
    return empresa

def atualizar_empresa_aerea(cod_empresa, nome=None, pais=None):
    empresa = session.query(EmpresaAerea).filter_by(cod_empresa=cod_empresa).first()
    if empresa:
        if nome:
            empresa.Nome = nome
        if pais:
            empresa.Pais = pais
        session.commit()
        print(f"Empresa Aérea {cod_empresa} atualizada com sucesso.")
    else:
        print(f"Empresa Aérea {cod_empresa} não encontrada.")

def deletar_empresa_aerea(cod_empresa):
    empresa = session.query(EmpresaAerea).filter_by(cod_empresa=cod_empresa).first()
    if empresa:
        session.delete(empresa)
        session.commit()
        print(f"Empresa Aérea {cod_empresa} deletada com sucesso.")
    else:
        print(f"Empresa Aérea {cod_empresa} não encontrada.")

# Funções CRUD para a tabela Destinos

def criar_destino(numero_destino, origem, destino):
    destino_obj = Destinos(
        numero_destino=numero_destino,
        Origem=origem,
        Destino=destino
    )
    session.add(destino_obj)
    session.commit()
    print(f"Destino {numero_destino} criado com sucesso.")

def ler_destino(numero_destino):
    destino = session.query(Destinos).filter_by(numero_destino=numero_destino).first()
    return destino

def atualizar_destino(numero_destino, origem=None, destino_nome=None):
    destino = session.query(Destinos).filter_by(numero_destino=numero_destino).first()
    if destino:
        if origem:
            destino.Origem = origem
        if destino_nome:
            destino.Destino = destino_nome
        session.commit()
        print(f"Destino {numero_destino} atualizado com sucesso.")
    else:
        print(f"Destino {numero_destino} não encontrado.")

def deletar_destino(numero_destino):
    destino = session.query(Destinos).filter_by(numero_destino=numero_destino).first()
    if destino:
        session.delete(destino)
        session.commit()
        print(f"Destino {numero_destino} deletado com sucesso.")
    else:
        print(f"Destino {numero_destino} não encontrado.")

#####

# Funções CRUD para a tabela AreaBagagem

def criar_area_bagagem(codigo_bagagem, status):
    area_bagagem = AreaBagagem(
        codigo_bagagem=codigo_bagagem,
        status=status
    )
    session.add(area_bagagem)
    session.commit()
    print(f"Área de Bagagem {codigo_bagagem} criada com sucesso.")

def ler_area_bagagem(codigo_bagagem):
    area_bagagem = session.query(AreaBagagem).filter_by(codigo_bagagem=codigo_bagagem).first()
    return area_bagagem

def atualizar_area_bagagem(codigo_bagagem, status=None):
    area_bagagem = session.query(AreaBagagem).filter_by(codigo_bagagem=codigo_bagagem).first()
    if area_bagagem:
        if status:
            area_bagagem.status = status
        session.commit()
        print(f"Área de Bagagem {codigo_bagagem} atualizada com sucesso.")
    else:
        print(f"Área de Bagagem {codigo_bagagem} não encontrada.")

def deletar_area_bagagem(codigo_bagagem):
    area_bagagem = session.query(AreaBagagem).filter_by(codigo_bagagem=codigo_bagagem).first()
    if area_bagagem:
        session.delete(area_bagagem)
        session.commit()
        print(f"Área de Bagagem {codigo_bagagem} deletada com sucesso.")
    else:
        print(f"Área de Bagagem {codigo_bagagem} não encontrada.")

# Funções CRUD para a tabela PortaoEmbarque

def criar_portao_embarque(codigo_portao, localizacao, status):
    portao_embarque = PortaoEmbarque(
        codigo_portao=codigo_portao,
        localizacao=localizacao,
        status=status
    )
    session.add(portao_embarque)
    session.commit()
    print(f"Portão de Embarque {codigo_portao} criado com sucesso.")

def ler_portao_embarque(codigo_portao):
    portao_embarque = session.query(PortaoEmbarque).filter_by(codigo_portao=codigo_portao).first()
    return portao_embarque

def atualizar_portao_embarque(codigo_portao, localizacao=None, status=None):
    portao_embarque = session.query(PortaoEmbarque).filter_by(codigo_portao=codigo_portao).first()
    if portao_embarque:
        if localizacao:
            portao_embarque.localizacao = localizacao
        if status:
            portao_embarque.status = status
        session.commit()
        print(f"Portão de Embarque {codigo_portao} atualizado com sucesso.")
    else:
        print(f"Portão de Embarque {codigo_portao} não encontrado.")

def deletar_portao_embarque(codigo_portao):
    portao_embarque = session.query(PortaoEmbarque).filter_by(codigo_portao=codigo_portao).first()
    if portao_embarque:
        session.delete(portao_embarque)
        session.commit()
        print(f"Portão de Embarque {codigo_portao} deletado com sucesso.")
    else:
        print(f"Portão de Embarque {codigo_portao} não encontrado.")

# Funções CRUD para a tabela Tripulante

def criar_tripulante(id_funcionario, nome, cargo, setor):
    tripulante = Tripulante(
        id_funcionario=id_funcionario,
        nome=nome,
        cargo=cargo,
        setor=setor
    )
    session.add(tripulante)
    session.commit()
    print(f"Tripulante {nome} criado com sucesso.")

def ler_tripulante(id_funcionario):
    tripulante = session.query(Tripulante).filter_by(id_funcionario=id_funcionario).first()
    return tripulante

def atualizar_tripulante(id_funcionario, nome=None, cargo=None, setor=None):
    tripulante = session.query(Tripulante).filter_by(id_funcionario=id_funcionario).first()
    if tripulante:
        if nome:
            tripulante.nome = nome
        if cargo:
            tripulante.cargo = cargo
        if setor:
            tripulante.setor = setor
        session.commit()
        print(f"Tripulante {id_funcionario} atualizado com sucesso.")
    else:
        print(f"Tripulante {id_funcionario} não encontrado.")

def deletar_tripulante(id_funcionario):
    tripulante = session.query(Tripulante).filter_by(id_funcionario=id_funcionario).first()
    if tripulante:
        session.delete(tripulante)
        session.commit()
        print(f"Tripulante {id_funcionario} deletado com sucesso.")
    else:
        print(f"Tripulante {id_funcionario} não encontrado.")

# Funções CRUD para a tabela Manutencao

def criar_manutencao(ID_Manutencao, Data, Tipo):
    manutencao = Manutencao(
        ID_Manutencao=ID_Manutencao,
        Data=Data,
        Tipo=Tipo
    )
    session.add(manutencao)
    session.commit()
    print(f"Manutenção {ID_Manutencao} criada com sucesso.")

def ler_manutencao(ID_Manutencao):
    manutencao = session.query(Manutencao).filter_by(ID_Manutencao=ID_Manutencao).first()
    return manutencao

def atualizar_manutencao(ID_Manutencao, Data=None, Tipo=None):
    manutencao = session.query(Manutencao).filter_by(ID_Manutencao=ID_Manutencao).first()
    if manutencao:
        if Data:
            manutencao.Data = Data
        if Tipo:
            manutencao.Tipo = Tipo
        session.commit()
        print(f"Manutenção {ID_Manutencao} atualizada com sucesso.")
    else:
        print(f"Manutenção {ID_Manutencao} não encontrada.")

def deletar_manutencao(ID_Manutencao):
    manutencao = session.query(Manutencao).filter_by(ID_Manutencao=ID_Manutencao).first()
    if manutencao:
        session.delete(manutencao)
        session.commit()
        print(f"Manutenção {ID_Manutencao} deletada com sucesso.")
    else:
        print(f"Manutenção {ID_Manutencao} não encontrada.")



def ler_todos_passageiros():
    passageiros = session.query(Passageiro).all()
    return passageiros

def ler_todos_bilhetes_voo():
    bilhetes = session.query(BilheteVoo).all()
    return bilhetes

def ler_todos_voos():
    voos = session.query(Voo).all()
    return voos

def ler_todas_aeronaves():
    aeronaves = session.query(Aeronave).all()
    return aeronaves

def ler_todas_empresas_aereas():
    empresas = session.query(EmpresaAerea).all()
    return empresas

def ler_todos_destinos():
    destinos = session.query(Destinos).all()
    return destinos

def ler_todas_areas_bagagem():
    areas = session.query(AreaBagagem).all()
    return areas

def ler_todos_portoes_embarque():
    portoes = session.query(PortaoEmbarque).all()
    return portoes

def ler_todos_tripulantes():
    tripulantes = session.query(Tripulante).all()
    return tripulantes

def ler_todas_manutencoes():
    manutencoes = session.query(Manutencao).all()
    return manutencoes