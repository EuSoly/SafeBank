import os

def carregar_dados(arquivo):
    dados = {}
    try:
        with open(arquivo, 'r') as file:
            linhas = file.readlines()
            if len(linhas) % 4 != 0:
                print("Formato do arquivo inválido.")
                return dados
            
            for i in range(0, len(linhas), 4):  # Cada usuário tem 4 linhas
                nome = linhas[i].strip().split(' = ')[1]
                cpf = linhas[i + 1].strip().split(' = ')[1]
                senha = linhas[i + 2].strip().split(' = ')[1]
                saldo = float(linhas[i + 3].strip().split(' = ')[1])
                dados[cpf] = {'Nome': nome, 'Senha': senha, 'Saldo': saldo}
    except FileNotFoundError:
        print("Arquivo não encontrado. Um novo arquivo será criado.")
    except (ValueError, IndexError) as e:
        print("Erro ao ler os dados do arquivo:", e)
    return dados

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def realizar_login(dados):
    cpf_input = input("Digite seu CPF: ")
    senha_input = input("Digite sua Senha: ")

    if cpf_input in dados and dados[cpf_input]['Senha'] == senha_input:
        print("Login bem-sucedido!")
        return cpf_input
    else:
        print("CPF ou senha incorretos.")
        input("Pressione Enter para continuar...")
        return None

def adicionar_usuario(arquivo):
    nome = input("Digite seu nome: ")
    cpf = input("Digite seu CPF: ")
    senha = input("Digite sua Senha: ")
    saldo = 0.0  # Saldo inicial

    with open(arquivo, 'a') as file:
        file.write(f"Nome = {nome}\n")
        file.write(f"Cpf = {cpf}\n")
        file.write(f"Senha = {senha}\n")
        file.write(f"Saldo = {saldo:.2f}\n")  # Saldo formatado
    print("Usuário adicionado com sucesso!")
    input("Pressione Enter para continuar...")
    limpar_tela()

def exibir_hud(dados, cpf):
    nome = dados[cpf]['Nome']
    saldo = dados[cpf]['Saldo']
    print("=========== SafeBank =============")
    print(f"Olá, {nome}")
    print(f"Seu saldo atual é de: R$ {saldo:.2f}")
    print("===================================")

def fazer_deposito(dados, cpf):
    valor = float(input("Digite o valor a depositar: R$ "))
    dados[cpf]['Saldo'] += valor
    print("Depósito realizado com sucesso!")
    input("Pressione Enter para continuar...")
    limpar_tela()

def fazer_saque(dados, cpf):
    valor = float(input("Digite o valor a sacar: R$ "))
    if valor > dados[cpf]['Saldo']:
        print("Saldo insuficiente para realizar o saque.")
    else:
        dados[cpf]['Saldo'] -= valor
        print("Saque realizado com sucesso!")
    input("Pressione Enter para continuar...")
    limpar_tela()

def fazer_transferencia(dados, cpf):
    print("Escolha para quem deseja transferir:")
    lista_usuarios = [(user_cpf, info) for user_cpf, info in dados.items() if user_cpf != cpf]  # Filtra para não incluir o próprio usuário
    for idx, (user_cpf, info) in enumerate(lista_usuarios):
        print(f"{idx + 1}. {info['Nome']} (CPF: {user_cpf})")
    
    escolha = int(input("Escolha o número da pessoa: ")) - 1
    if 0 <= escolha < len(lista_usuarios):
        destinatario_cpf = lista_usuarios[escolha][0]
        valor = float(input("Digite o valor a transferir: R$ "))
        
        if valor > dados[cpf]['Saldo']:
            print("Saldo insuficiente para realizar a transferência.")
        else:
            dados[cpf]['Saldo'] -= valor
            dados[destinatario_cpf]['Saldo'] += valor
            print("Transferência realizada com sucesso!")
    else:
        print("Opção inválida.")
    
    input("Pressione Enter para continuar...")
    limpar_tela()

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w') as file:
        for cpf, info in dados.items():
            file.write(f"Nome = {info['Nome']}\n")
            file.write(f"Cpf = {cpf}\n")
            file.write(f"Senha = {info['Senha']}\n")
            file.write(f"Saldo = {info['Saldo']:.2f}\n")  # Saldo formatado

def main():
    arquivo = 'dados.txt'  # Nome do arquivo .txt
    dados = carregar_dados(arquivo)

    while True:
        limpar_tela()
        print("1. Fazer login")
        print("2. Adicionar novo usuário")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cpf = realizar_login(dados)
            if cpf:
                while True:
                    limpar_tela()
                    exibir_hud(dados, cpf)
                    print("1. Fazer depósito")
                    print("2. Fazer saque")
                    print("3. Fazer transferência")
                    print("4. Sair do sistema")
                    escolha = input("Escolha uma opção: ")

                    if escolha == '1':
                        fazer_deposito(dados, cpf)
                        salvar_dados(arquivo, dados)  # Salvar saldo após depósito
                    elif escolha == '2':
                        fazer_saque(dados, cpf)
                        salvar_dados(arquivo, dados)  # Salvar saldo após saque
                    elif escolha == '3':
                        fazer_transferencia(dados, cpf)
                        salvar_dados(arquivo, dados)  # Salvar saldo após transferência
                    elif escolha == '4':
                        break
                    else:
                        print("Opção inválida. Tente novamente.")
                        input("Pressione Enter para continuar...")
                        limpar_tela()
        elif opcao == '2':
            adicionar_usuario(arquivo)
            dados = carregar_dados(arquivo)  # Recarregar os dados
        elif opcao == '3':
            salvar_dados(arquivo, dados)  # Salvar ao sair
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar...")
            limpar_tela()

if __name__ == "__main__":
    main()
