test.py

import unittest
from io import StringIO
import sys

class TestBanco(unittest.TestCase):

    def setUp(self):
        # Redirecionar stdout para capturar saídas para testes
        self.held, sys.stdout = sys.stdout, StringIO()
        self.banco = Banco("0001")
        self.banco.usuarios.append(Usuario("Teste User", "01-01-2000", "12345678900", "Rua Teste, 123 - Bairro - Cidade/UF"))
        self.banco.contas.append(Conta("0001", 1, self.banco.usuarios[0]))

    def tearDown(self):
        # Restaurar stdout
        sys.stdout = self.held

    def test_criar_usuario_existente(self):
        self.banco.criar_usuario = lambda: None
        self.banco.filtrar_usuario = lambda cpf: self.banco.usuarios[0]
        self.banco.criar_usuario()
        output = sys.stdout.getvalue().strip()
        self.assertIn("@@@ Já existe usuário com esse CPF! @@@", output)

    def test_criar_usuario_novo(self):
        self.banco.criar_usuario = lambda: None
        self.banco.filtrar_usuario = lambda cpf: None
        self.banco.criar_usuario()
        output = sys.stdout.getvalue().strip()
        self.assertIn("=== Usuário criado com sucesso! ===", output)

    def test_criar_conta_usuario_existente(self):
        self.banco.criar_conta = lambda: None
        self.banco.filtrar_usuario = lambda cpf: self.banco.usuarios[0]
        self.banco.criar_conta()
        output = sys.stdout.getvalue().strip()
        self.assertIn("=== Conta criada com sucesso! ===", output)

    def test_criar_conta_usuario_inexistente(self):
        self.banco.criar_conta = lambda: None
        self.banco.filtrar_usuario = lambda cpf: None
        self.banco.criar_conta()
        output = sys.stdout.getvalue().strip()
        self.assertIn("@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@", output)

    def test_depositar_valor_valido(self):
        conta = self.banco.contas[0]
        conta.depositar(100)
        self.assertEqual(conta.saldo, 100)
        self.assertIn("Depósito:\tR$ 100.00", conta.extrato)

    def test_depositar_valor_invalido(self):
        conta = self.banco.contas[0]
        conta.depositar(-100)
        self.assertEqual(conta.saldo, 0)
        output = sys.stdout.getvalue().strip()
        self.assertIn("@@@ Operação falhou! O valor informado é inválido. @@@", output)

    def test_sacar_valor_valido(self):
        conta = self.banco.contas[0]
        conta.depositar(200)
        conta.sacar(100)
        self.assertEqual(conta.saldo, 100)
        self.assertIn("Saque:\t\tR$ 100.00", conta.extrato)

    def test_sacar_valor_excede_saldo(self):
        conta = self.banco.contas[0]
        conta.sacar(100)
        output = sys.stdout.getvalue().strip()
        self.assertIn("@@@ Operação falhou! Você não tem saldo suficiente. @@@", output)

    def test_sacar_valor_excede_limite(self):
        conta = self.banco.contas[0]
        conta.depositar(600)
        conta.sacar(600)
        output = sys.stdout.getvalue().strip()
        self.assertIn("@@@ Operação falhou! O valor do saque excede o limite. @@@", output)

    def test_sacar_valor_excede_limite_saques(self):
        conta = self.banco.contas[0]
        conta.depositar(500)
        conta.sacar(100)
        conta.sacar(100)
        conta.sacar(100)
        conta.sacar(100)
        output = sys.stdout.getvalue().strip()
        self.assertIn("@@@ Operação falhou! Número máximo de saques excedido. @@@", output)

    def test_exibir_extrato_sem_movimentacoes(self):
        conta = self.banco.contas[0]
        conta.exibir_extrato()
        output = sys.stdout.getvalue().strip()
        self.assertIn("Não foram realizadas movimentações.", output)
        self.assertIn("Saldo:\t\tR$ 0.00", output)

    def test_exibir_extrato_com_movimentacoes(self):
        conta = self.banco.contas[0]
        conta.depositar(200)
        conta.sacar(100)
        conta.exibir_extrato()
        output = sys.stdout.getvalue().strip()
        self.assertIn("Depósito:\tR$ 200.00", output)
        self.assertIn("Saque:\t\tR$ 100.00", output)
        self.assertIn("Saldo:\t\tR$ 100.00", output)

if __name__ == "__main__":
    unittest.main()
