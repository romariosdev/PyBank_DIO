import os
from typing import List, Optional
from datetime import datetime, timedelta, date
import zoneinfo

def limpar_terminal() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def formatar_float(valor: float) -> str:
    return f"{valor:,.2f}".replace(",", "x").replace(".", ",").replace("x", ".")

def formatar_data(data: datetime) -> str:
    return data.strftime("%d/%m/%Y %H:%M:%S")

def input_valor(prompt: str) -> float:
    while True:
        try:
            entrada = input(prompt).replace(',', '.')
            valor = float(entrada)
            if valor > 0:
                return valor
        except ValueError:
                print("Operação falhou! O valor informado é inválido.")

def input_opcoes(prompt: str) -> str:
    while True:
        try:
            entrada = input(prompt).strip().upper()
            if not entrada.isalpha():
                return entrada
        except ValueError:
            print("Operação falhou! Informe uma opção válida.")    

class Sistema_banco:
    def __init__(self):
        pass

    def menu_login(self) -> str:
        self.opcao = input_opcoes("""
_____________________________________  

    Selecione a operação desejada:
_____________________________________

[A] Abrir Conta     [L] Login
________________    _________________

 """)
        while True:
            if self.opcao in ["A", "L"]:
                return str(self.opcao)
            else:
                print("Operação falhou! Informe uma opção válida.")

    def menu_principal(self) -> str:
        self.opcao = input_opcoes("""
___________________________________
   
    Selecione a opção desejada:
___________________________________

[D] Depositar       [E] Extrato
_______________     _______________

[S] Sacar           [Q] Sair
_______________     _______________

 """)
        while True:
            if self.opcao in ["D", "E", "S", "Q"]:
                return str(self.opcao)
            else:
                print("Operação falhou! Informe uma opção válida.")

    def logar_conta(self, conta, agencia, senha) -> int:
        self.nemero_conta = conta
        self.numero_agencia = agencia
        self.senha = senha
        self.conta_logada = self.nemero_conta
        return self.conta_logada

class Banco:
    def __init__(self):
        self.contas = []
    
    def criar_conta(self, nome: str, senha: str, saldo_inicial: float = 0.0, limite_inicial: float = 500.0) -> Conta:
        nova_conta = Conta(nome=nome, saldo=saldo_inicial, limite=limite_inicial, senha=senha)
        self.contas.append(nova_conta)
        return nova_conta
    
    def exibir_contas(self) -> None:
        for conta in self.contas:
            print(f"Nome: {Conta.nome}, Saldo: {formatar_float(Conta.saldo)}, Limite: {formatar_float(Conta.limite)}")

class Conta:
    def __init__(self, nome: str, saldo: float, senha: str, limite: float = 500) -> None:
        self.numero_conta = 1 
        self.agencia = 1
        self.nome = nome
        self.senha = senha
        self.saldo = saldo
        self.limite = limite
        self.extrato: list[str] = []
        self.limite_saques_dia = 10
        self.numero_saques_hoje = 0
        self.data_utimo_saque: Optional[date] = None

    def depositar(self, valor: float) -> None:
        if valor > 0:
            self.saldo += valor
            data_operacao = datetime.now()
            self.extrato.append(f"Deposito de R$: {formatar_float(valor)} {formatar_data(data_operacao)}")
            print (f"Depósito de: R${formatar_float(valor)} realizado com sucesso.")
        else:
            print("Operação falhou! O valor informado é inválido.")

    def sacar(self, valor: float) -> None:
        if self.data_utimo_saque != datetime.now():
            self.numero_saques_hoje = 0
            self.data_utimo_saque = datetime.now()
        else:
            print ("Operação falhou! Número máximo de saques excedido.")
        
        excedeu_saldo_total = valor > (self.saldo + self.limite)
        
        if excedeu_saldo_total:
            print ("Operação falhou! Você não tem saldo suficiente nem limite disponível.")
        else:
            if valor <= self.saldo:
                self.saldo -= valor
            else:
                restante = self.limite - valor
                self.saldo = 0
                self.limite = restante
            data_operacao = datetime.now()
            self.extrato.append(f"Saque de R$: {formatar_float(valor)} {formatar_data(data_operacao)}")

    def imprimir_extrato(self) -> str:
       if not self.extrato:
           print ("Não foram realizadas movimentações.")
       else:
            limpar_terminal()
            enunciado = (" EXTRATO ")
            print (enunciado.center(47,"="))
            print ("Movimentações realizadas: \n")
            print (f"{"\n".join(self.extrato)} \n")
            print (47 * "-")
            print (formatar_data(datetime.now()))
            print (f"O seu Saldo atual é de: R$ {formatar_float(self.saldo)}")
            print (f"O seu limite atual é de: R$ {formatar_float(self.limite)}")
            print (47 * "=")

           

if __name__ == "__main__":
    