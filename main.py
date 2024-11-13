from crud_operations import criar_passageiro, ler_passageiro, atualizar_passageiro, deletar_passageiro

# Criar um novo passageiro
criar_passageiro(2, "Maria Souza", "987654321", 888888888, False)

# Ler informações do passageiro
passageiro = ler_passageiro(2)
print(f"Nome: {passageiro.nome}, Documento: {passageiro.documento}")

# Atualizar informações do passageiro
atualizar_passageiro(2, contato=777777777)

# Deletar o passageiro
deletar_passageiro(2)
