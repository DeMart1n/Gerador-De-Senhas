from app.gerador import gerar_senha
import unittest

class TestGerador(unittest.TestCase):

    def test_geradorDeSenhas_1(self):
        """
        Test that geradorDeSenhas generates a password of the specified length.
        """
        tamanho = 16
        senha = gerar_senha(tamanho)
        self.assertEqual(len(senha), tamanho)
        self.assertTrue(all(c.isalnum() for c in senha))

    def test_geradorDeSenhas_negative_length(self):
        """
        Test geradorDeSenhas function with negative length input.
        This tests the edge case of generating a password with a negative length,
        which should result in an empty string.
        """
        result = gerar_senha(-5)
        self.assertEqual(result, '')

    def test_geradorDeSenhas_zero_length(self):
        """
        Test geradorDeSenhas function with zero length input.
        This tests the edge case of generating a password with zero length,
        which should result in an empty string.
        """
        result = gerar_senha(0)
        self.assertEqual(result, '')
