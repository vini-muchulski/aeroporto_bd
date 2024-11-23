# crud_operations.py

from legado.models import Session, Passageiro, BilheteVoo, Compra, Voo, RelacionaSe
from sqlalchemy.orm import sessionmaker

# Criar uma sessão
session = Session()

# Funções de CRUD

# Create (Criar)
def create_passageiro(codigo_passageiro, nome, documento, contato):
    passageiro = Passageiro(
        codigo_passageiro=codigo_passageiro,
        nome=nome,
        documento=documento,
        contato=contato
    )
    session.add(passageiro)
    session.commit()
    return passageiro

def create_bilhete(numero_bilhete, classe, nome_passageiro, status):
    bilhete = BilheteVoo(
        numero_bilhete=numero_bilhete,
        classe=classe,
        nome_passageiro=nome_passageiro,
        status=status
    )
    session.add(bilhete)
    session.commit()
    return bilhete

# Read (Ler)
def get_passageiro_by_nome(nome):
    return session.query(Passageiro).filter_by(nome=nome).first()

def get_all_passageiros():
    return session.query(Passageiro).all()

# Update (Atualizar)
def update_passageiro(codigo_passageiro, nome=None, documento=None, contato=None):
    passageiro = session.query(Passageiro).filter_by(codigo_passageiro=codigo_passageiro).first()
    if passageiro:
        if nome:
            passageiro.nome = nome
        if documento:
            passageiro.documento = documento
        if contato:
            passageiro.contato = contato
        session.commit()
        return passageiro
    else:
        return None

# Delete (Excluir)
def delete_passageiro(codigo_passageiro):
    passageiro = session.query(Passageiro).filter_by(codigo_passageiro=codigo_passageiro).first()
    if passageiro:
        session.delete(passageiro)
        session.commit()
        return True
    else:
        return False

# Exemplo de uso
if __name__ == '__main__':
    # Criar dados de exemplo
    create_passageiro(1, 'João Silva', '123456789', 'joao@example.com')
    create_bilhete(1001, 1, 'João Silva', 'Confirmado')

    # Ler dados
    passageiros = get_all_passageiros()
    for p in passageiros:
        print(f'Passageiro: {p.nome}, Documento: {p.documento}')

    # Atualizar dados
    #update_passageiro(1, contato='joao.silva@novoemail.com')

    # Excluir dados
    #delete_passageiro(1)
