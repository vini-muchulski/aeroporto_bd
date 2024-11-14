from crud_operations import *

def main():
    # Exemplo de uso das funções CRUD
    criar_passageiro(1, "João Silva", "123456789", 999999999, True)
    passageiro = ler_passageiro(1)
    if passageiro:
        print(f"Passageiro: {passageiro.nome}, Documento: {passageiro.documento}")
    else:
        print("Passageiro não encontrado.")

    # ... restante da lógica da aplicação ...

if __name__ == "__main__":
    main()
