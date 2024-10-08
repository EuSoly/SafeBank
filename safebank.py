import os
import json

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def carregar_dados(arquivo):
    dados = {}
    try:
        with open(arquivo, 'r') as file:
            dados = json.load(file)
    except FileNotFoundError:
        print("Arquivo não encontrado. Um novo arquivo será criado.")
    except json.JSONDecodeError:
        print("Erro ao ler os dados do arquivo. O formato pode estar incorreto.")
    return dados

def adicionar_usuario(arquivo, dados):
    nome = input("Digite seu nome: ")
    cpf = input("Digite seu CPF: ")
    
    # Verifica se o CPF já está cadastrado
    if cpf in dados:
        print("CPF já cadastrado. Tente novamente.")
        return
    
    senha = input("Digite sua Senha: ")
    senha_emergencia = input("Digite sua Senha de Emergência: ")
    saldo = 0.0  # Saldo inicial

    dados[cpf] = {
        'Nome': nome,
        'Senha': senha,
        'SenhaEmergencia': senha_emergencia,
        'Saldo': saldo
    }
    
    salvar_dados(arquivo, dados)  # Salvar os dados após adicionar o usuário
    print("Usuário adicionado com sucesso!")
    input("Pressione Enter para continuar...")
    limpar_tela()

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w') as file:
        json.dump(dados, file, indent=4)  # Salva os dados no formato JSON

def realizar_login(dados):
    cpf_input = input("Digite seu CPF: ")
    
    if cpf_input not in dados:
        print("CPF não encontrado.")
        input("Pressione Enter para continuar...")
        return None, None

    senha_input = input("Digite sua Senha (ou Senha de Emergência para simulação): ")

    # Verifica se a senha é de emergência ou normal
    info = dados[cpf_input]
    if info['Senha'] == senha_input:
        print("Login bem-sucedido!")
        return cpf_input, False  # Modo normal
    elif info['SenhaEmergencia'] == senha_input:
        print("Login em modo de simulação!")
        return cpf_input, True  # Modo simulação

    print("Senha incorreta.")
    input("Pressione Enter para continuar...")
    return None, None

def exibir_hud(dados, cpf, modo_simulacao):
    nome = dados[cpf]['Nome']
    saldo = dados[cpf]['Saldo']
    print("=========== SafeBank =============")
    print(f"Olá, {nome}")
    print(f"Seu saldo atual é de: R$ {saldo:.2f}")
    if modo_simulacao:
        print("Você está no modo de simulação.")
    print("===================================")

def fazer_deposito(dados, cpf, modo_simulacao):
    valor = float(input("Digite o valor a depositar: R$ "))
    if modo_simulacao:
        print(f"Depósito simulado de R$ {valor:.2f} realizado com sucesso!")
    else:
        dados[cpf]['Saldo'] += valor
        print("Depósito realizado com sucesso!")
        gerar_comprovante_deposito(dados[cpf]['Nome'], cpf, valor)

def gerar_comprovante_deposito(nome, cpf, valor):
    print("\n======= COMPROVANTE =======")
    print(f"Nome: {nome}")
    print(f"CPF: {cpf}")
    print(f"Valor Depositado: R$ {valor:.2f}")
    print("============================\n")
    input("Pressione Enter para continuar...")

def fazer_saque(dados, cpf, modo_simulacao):
    valor = float(input("Digite o valor a sacar: R$ "))
    if modo_simulacao:
        print(f"Saque simulado de R$ {valor:.2f} realizado com sucesso!")
    else:
        if valor > dados[cpf]['Saldo']:
            print("Saldo insuficiente para realizar o saque.")
        else:
            dados[cpf]['Saldo'] -= valor
            print("Saque realizado com sucesso!")

def fazer_transferencia(dados, cpf, modo_simulacao):
    print("Escolha para quem deseja transferir:")
    lista_usuarios = [(user_cpf, info) for user_cpf, info in dados.items() if user_cpf != cpf]
    for idx, (user_cpf, info) in enumerate(lista_usuarios):
        print(f"{idx + 1}. {info['Nome']} (CPF: {user_cpf})")
    
    escolha = int(input("Escolha o número da pessoa: ")) - 1
    if 0 <= escolha < len(lista_usuarios):
        destinatario_cpf = lista_usuarios[escolha][0]
        valor = float(input("Digite o valor a transferir: R$ "))
        
        if modo_simulacao:
            print(f"Transferência simulada de R$ {valor:.2f} para {dados[destinatario_cpf]['Nome']} realizada com sucesso!")
        else:
            if valor > dados[cpf]['Saldo']:
                print("Saldo insuficiente para realizar a transferência.")
            else:
                dados[cpf]['Saldo'] -= valor
                dados[destinatario_cpf]['Saldo'] += valor
                print("Transferência realizada com sucesso!")
                gerar_comprovante_transferencia(dados[cpf]['Nome'], cpf, valor, dados[destinatario_cpf]['Nome'])

    else:
        print("Opção inválida.")
    
    input("Pressione Enter para continuar...")
    limpar_tela()

def gerar_comprovante_transferencia(nome_remetente, cpf_remetente, valor, nome_destinatario):
    print("\n======= COMPROVANTE =======")
    print(f"Nome Remetente: {nome_remetente}")
    print(f"CPF Remetente: {cpf_remetente}")
    print(f"Valor Transferido: R$ {valor:.2f}")
    print(f"Nome Destinatário: {nome_destinatario}")
    print("============================\n")
    input("Pressione Enter para continuar...")

def main():
    arquivo = 'dados.json'  # Nome do arquivo JSON
    dados = carregar_dados(arquivo)

    while True:
        limpar_tela()
        print("1. Fazer login")
        print("2. Adicionar novo usuário")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cpf, modo_simulacao = realizar_login(dados)
            if cpf:
                while True:
                    limpar_tela()
                    exibir_hud(dados, cpf, modo_simulacao)
                    print("1. Fazer depósito")
                    print("2. Fazer saque")
                    print("3. Fazer transferência")
                    print("4. Sair do sistema")
                    escolha = input("Escolha uma opção: ")

                    if escolha == '1':
                        fazer_deposito(dados, cpf, modo_simulacao)
                        salvar_dados(arquivo, dados)  # Salvar saldo após depósito
                    elif escolha == '2':
                        fazer_saque(dados, cpf, modo_simulacao)
                        salvar_dados(arquivo, dados)  # Salvar saldo após saque
                    elif escolha == '3':
                        fazer_transferencia(dados, cpf, modo_simulacao)
                        salvar_dados(arquivo, dados)  # Salvar saldo após transferência
                    elif escolha == '4':
                        break
                    else:
                        print("Opção inválida. Tente novamente.")
                        input("Pressione Enter para continuar...")
                        limpar_tela()
        elif opcao == '2':
            adicionar_usuario(arquivo, dados)
        elif opcao == '3':
            salvar_dados(arquivo, dados)  # Salvar ao sair
            break
        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione Enter para continuar...")
            limpar_tela()

if __name__ == "__main__":
    main()
{
    "801": {
        "Nome": "elizeu",
        "Senha": "5451",
        "SenhaEmergencia": "0000",
        "Saldo": 0.0
    }
}
