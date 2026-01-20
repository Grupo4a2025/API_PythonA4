import unittest
from funciones_auxiliares import calculariva

class TestCalculos(unittest.TestCase):
    
    def test_iva_de_100(self):
        print("--- Ejecutando Test de IVA ---")
        importe = 100
        esperado = 21.0
        
        resultado = calculariva(importe)
        
        self.assertEqual(resultado, esperado)
        print(f"Test Superado: {importe} * 0.21 = {resultado}")

if __name__ == '__main__':
    unittest.main()