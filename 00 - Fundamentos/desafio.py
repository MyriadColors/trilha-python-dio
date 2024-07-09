import json

cidades_estados = json.load(open("./dados/cidades_estados.json", encoding="utf-8"))
siglas = list(cidades_estados["estados"][0].keys())[1:]
nomes_estados = list(cidades_estados["estados"][1].values())[1:]

def procurar_cidades(sigla):
    return cidades_estados["estados"][siglas.index(sigla) + 1]["cidades"]

def validar_string(string, tipo_de_dado = ""):
    if not string:
        print("Operação falhou! O campo é obrigatório.")
        return False
        
    if tipo_de_dado == "int":
        try:
            int(string)
        except ValueError:
            print("Operação falhou! O campo deve ser numero inteiro.")
            return False
    
    if tipo_de_dado == "float":
        try:
            float(string)
        except ValueError:
            print("Operação falhou! O campo deve ser numero decimal.")
            return False
    
    if tipo_de_dado == "nome":
        if not string.isalpha():
            print("Operação falhou! O campo deve ser texto.")
            return False
        if " " not in string:
            print("Operação falhou! O campo deve conter um nome e sobrenome.")
            return False
    
    if tipo_de_dado == "data":
        try:
            data = string.split("-")
            if len(data) != 3:
                raise ValueError
            dia, mes, ano = data
            if not dia.isdigit() or not mes.isdigit() or not ano.isdigit():
                raise ValueError
            if int(dia) > 31 or int(mes) > 12:
                raise ValueError
        except ValueError:
            print("Operação falhou! O campo deve conter uma data no formato dd-mm-aaaa.")
            return False
    
    if tipo_de_dado == "cpf":
        try:
            if len(string) != 11:
                raise ValueError
            if not string.isdigit():
                raise ValueError
        except ValueError:
            print("Operação falhou! O campo deve conter apenas 11 números.")
            return False
    
    if tipo_de_dado == "logradouro":
        if " " not in string:
            print("Operação falhou! O campo deve conter um logradouro.")
            return False
            return False
        if "rua" not in string.lower():
            print("Operação falhou! O campo deve conter a palavra 'rua'.")
            return False
    
    if tipo_de_dado == "sigla_estado":
        if len(string) != 2:
            print("Operação falhou! O campo deve conter 2 letras.")
            return False
        if string not in siglas:
            print("Operação falhou! O campo deve conter uma sigla de estado.")
            print("Segue a lista de siglas disponíveis: \n", siglas)
            return False
        
    if tipo_de_dado == "estado":
        if string not in nomes_estados:
            print("Operação falhou! O campo deve conter o nome de um estado brasileiro.")
            print("Segue a lista de estados disponíveis: \n", nomes_estados)
            return False
        
    if tipo_de_dado == "endereço":
        # Formato: logradouro, numero - bairro - cidade/sigla estado
        if str.count(string, "-") != 2 and str.count(string, ",") != 1 and str.count(string, " ") != 6 and str.count(string, "/") != 1:
            print("Operação falhou! O campo deve conter o seguinte formato: logradouro, numero - bairro - cidade/sigla estado")
            return False
        
    
    return True

def mostrar_extrato(extrato, saldo):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def depositar(valor, saldo, extrato):
    if valor > 0:
        saldo += valor
        extrato += f"Deposito: R$ {valor:.2f}\n"
        return extrato, saldo
    else:
        print("Operação falhou! O valor informado é inválido.")

def sacar(valor, saldo, limite, extrato, numero_saques, LIMITE_SAQUES):
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return extrato, saldo, numero_saques

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return extrato, saldo, numero_saques

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return extrato, saldo, numero_saques

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        return extrato, saldo, numero_saques

    else:
        print("Operação falhou! O valor informado é inválido.")

def criar_usuario(usuarios):
    nome = ""
    data_nascimento = ""
    cpf = ""
    logradouro = ""
    numero = ""
    bairro = ""
    cidade = ""
    sigla = ""
    estado = ""
    endereço = ""

    lista_cpfs = list(map(lambda usuario: usuario["cpf"], usuarios)) if not len(usuarios) else None

    while True:
        nome = input("Nome completo: ")
        if validar_string(nome):
            break

    while True:
        data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
        if validar_string(data_nascimento, "data"):
            break

    while True:
        cpf = input("CPF: ")
        if validar_string(cpf, "cpf"):
            break
    
    # Verificar se o CPF existe
    if cpf in lista_cpfs:
        print("Operação falhou! O CPF deve ser único.")
        return usuarios

    while True:
        logradouro = input("Logradouro: ")
        if validar_string(logradouro, "logradouro"):
            break

    while True:
        numero = input("Número: ")
        if validar_string(numero, "int"):
            break
    
    while True:
        bairro = input("Bairro: ")
        if validar_string(bairro):
            break

    while True:
        cidade = input("Cidade: ")
        if validar_string(cidade):
            break

    while True:
        sigla = input("Sigla: ")
        if validar_string(sigla, "sigla"):
            break

    while True:
        estado = input("Estado: ")
        if validar_string(estado, "estado"):
            break

    while True:
        endereço = str.join(" ", (logradouro, numero, bairro, cidade, sigla, estado))
        if validar_string(endereço, "endereço"):
            break
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereço": endereço})
    return usuarios

    
menu = """

[u] Criar Usuário
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []

while True:

    opcao = input(menu)

    if opcao == "u":
        usuarios = criar_usuario(usuarios)
    elif opcao == "d":
        valor = ""
        while True:
            valor = input("Informe o valor do depósito: ")
            if validar_string(valor, "float"):
                break
        extrato, saldo = depositar(float(valor), saldo, extrato)

    elif opcao == "s":
        valor = ""
        while True:
            valor = input("Informe o valor do saque: ")
            if validar_string(valor, "float"):
                break
        extrato, saldo, numero_saques = sacar(float(valor), saldo, limite, extrato, numero_saques, LIMITE_SAQUES)

    elif opcao == "e":
        mostrar_extrato(extrato, saldo)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
