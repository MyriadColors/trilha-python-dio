import textwrap
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class FormatoData:
    _ano: int
    _mes: int
    _dia: int

    def __str__(self) -> str:
        return f"{self.dia}-{self.mes}-{self.ano}"
    
    @property
    def ano(self) -> int:
        return self._ano
    
    @property
    def mes(self) -> int:
        return self._mes
    
    @property
    def dia(self) -> int:
        return self._dia

class PessoaFisica:

    def __init__(self, nome: str, cpf: str, data_nascimento: FormatoData):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

@dataclass
class ContaCorrente:
    _limite: float
    _limite_saques: int

    def __str__(self) -> str:
        return f"Limite: {self.limite} - Limite de saques: {self.limite_saques}"

    @property
    def limite(self) -> float:
        return self._limite
    
    @property
    def limite_saques(self) -> int:
        return self._limite_saques

class Cliente:
    def __init__(self, endereço: str, contas: list['Conta']):
        self._endereço = endereço
        self._contas = contas
    
    @property
    def endereço(self) -> str:
        return self._endereço

    @property
    def contas(self) -> list['Conta']:
        return self._contas
    
    def realizar_transferencia(conta_origem: 'Conta', valor: float, conta_destino: 'Conta'):
        conta_origem.sacar(valor)
        conta_destino.depositar(valor)

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self) -> float:
        pass

    @abstractmethod
    def registrar(conta: 'Conta'):
        pass

    @abstractmethod
    def __str__(self):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: 'Conta'):
        sucesso = conta.depositar(self._valor)
        if not sucesso:
            print('Falha na operação de depósito.')
        else:
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f'Depósito de R${self._valor:.2f}'

class Saque(Transacao):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    def registrar(self, conta: 'Conta'):
        sucesso = conta.sacar(self._valor)
        if not sucesso:
            print('Falha na operação de saque.')
        else:
            conta.set_saldo(conta.saldo - self._valor)
            conta.historico.adicionar_transacao(self)
    
    def __str__(self):
        return f'Saque de R${self._valor:.2f}'

@dataclass
class Historico:
    _transacoes: list['Transacao']
    
    @classmethod
    def adicionar_transacao(self, transacao: 'Transacao'):
        self._transacoes.append(transacao)

    @property
    def transacoes(self) -> list['Transacao']:
        return self._transacoes

class Conta:
    def __init__(self):
        self._saldo: float = 0
        self._numero: int = 0
        self._agencia: str = '0001'
        self._historico: 'Historico' = None
        self._cliente: 'Cliente' = None

    @property
    def saldo(self) -> float:
        return self._saldo

    def set_saldo(self, valor: float):
        self._saldo = valor

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia
    
    @property
    def historico(self) -> 'Historico':
        return self._historico
    
    @property
    def cliente(self) -> 'Cliente':
        return self._cliente

    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: int) -> 'Conta':
        conta = cls()
        conta._numero = numero
        conta._cliente = cliente
        return conta
    
    def sacar(self, valor: float) -> bool:
        if self._saldo < valor:
            return False
        else:
            return True
    
    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            print("Valor inválido para depósito: deve ser um decimal positivo.")
            return False
        else:
            return True

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
