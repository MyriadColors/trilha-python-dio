import json

cidades_estados = json.load(open("./dados/cidades_estados.json", encoding="utf-8"))

siglas = []

for estado in cidades_estados["estados"]:
    siglas.append(estado["sigla"])

def cidade_existe_no_estado(sigla_estado, nome_cidade):
    for estado in cidades_estados["estados"]:
        if estado["sigla"] == sigla_estado:
            if nome_cidade in estado["cidades"]:
                return True
            else:
                return False

    # Se a sigla do estado não for encontrada
    return False

def listar_usuários(usuarios):
    print("==========================================")
    for usuario in usuarios:
            print(f"Nome: {usuario['nome']}")
            print("Endereço: ")
            print(f"Logradouro: {usuario['endereço']['logradouro']}")
            print(f"Número: {usuario['endereço']['numero']}")
            print(f"Bairro: {usuario['endereço']['bairro']}")
            print(f"Sigla da Cidade: {usuario['endereço']['sigla']}")
            print(f"Cidade: {usuario['endereço']['nome_cidade']}")
            print(f"Data de nascimento: {usuario['data_nascimento']}")
            print(f"CPF: {usuario['cpf']}")
            print("==========================================")


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
    sigla = ""
    nome_cidade = ""
    endereço = ""

    lista_cpfs = list(map(lambda usuario: usuario["cpf"], usuarios))

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
            # Verificar se o CPF existe
            if cpf in lista_cpfs:
                print("Operação falhou! O CPF deve ser único.")
                continue
            else:
                break
    
    
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
        sigla = input("Sigla: ")
        if validar_string(sigla, "sigla"):
            if sigla in siglas:
                break
            else:
                print("Operação falhou! Sigla inválida.")
                continue

    while True:
        nome_cidade = input("Cidade: ")
        if validar_string(nome_cidade):
            if cidade_existe_no_estado(sigla, nome_cidade):
                break
            else:
                print("Operação falhou! Cidade não encontrada.")
                continue
    
    # Formato: logradouro, numero - bairro - cidade/sigla
    endereço = str.join(" ", (logradouro, numero, bairro, nome_cidade, sigla))
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereço": endereço})
    return usuarios
def criar_conta(usuarios, contas):
    cpf = 0
    usuário = {}
    while True:
        cpf = input("Numero de cpf do usuário (-1 para lista de usuários, -2 para sair): ")
        usuario = {}
        if validar_string(cpf, "cpf"):
            # Verificar se o CPF existe
            for usuario in usuarios:
                if usuario["cpf"] == cpf:
                    usuários = usuario
                    break
                else:
                    print("Operação falhou! Usuário não encontrado.")
                    continue
        else:
            if int(cpf) == -1:
                listar_usuários(usuarios)
                continue
            elif int(cpf) == -2:
                return contas
        break
    
    usuario_selecionado: dict = {}

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuario_selecionado = usuario
            break
    print(f"Usuario selecionado: {usuario_selecionado["nome"]}")

    agencia = "0001"
    conta = len(contas) + 1
    contas.append({"agencia": agencia, "conta": conta, "usuario": usuario})

    return contas

def listar_contas(contas):
    print("==========================================")
    for conta in contas:
        print(f"Agência: {conta['agencia']}")
        print(f"Conta: {conta['conta']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print("==========================================")

def main():

    menu = """

    [u] Criar Usuário
    [lu] listar Usuários
    [c] Criar Conta
    [lc] Listar Contas
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
    # Usuários pre-criados para testes
    usuarios = [
        {
            "nome": "Guilherme",
            "data_nascimento": "01-01-2000",
            "cpf": "11111111111",
            "endereço": {
                "logradouro": "Rua das Laranjeiras",
                "numero": "123",
                "bairro": "Centro",
                "nome_cidade": "São Paulo",
                "sigla": "SP"
            }
        },
        {
            "nome": "Joaquim",
            "data_nascimento": "01-01-1990",
            "cpf": "22222222222",
            "endereço": {
                "logradouro": "Rua das Margaridas",
                "numero": "456",
                "bairro": "Centro",
                "nome_cidade": "São Paulo",
                "sigla": "SP"
            }
        }
    ]
    contas = []

    while True:

        opcao = input(menu)

        if opcao == "u":
            usuarios = criar_usuario(usuarios)
        elif opcao == "lu":
            listar_usuários(usuarios)
        elif opcao == "c":
            contas = criar_conta(usuarios, contas)
        elif opcao == "lc":
            listar_contas(contas)
            
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

if __name__ == "__main__":
    main()