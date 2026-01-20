import unittest
# Importamos la función que acabamos de crear en el otro archivo
from funciones_auxiliares import calculariva

class TestCalculos(unittest.TestCase):
    
    # Las funciones de prueba deben empezar por la palabra 'test_'
    def test_iva_de_100(self):
        print("--- Ejecutando Test de IVA ---")
        importe = 100
        esperado = 21.0
        
        # Llamamos a tu función
        resultado = calculariva(importe)
        
        # Comprobamos si el resultado es igual al esperado (Assertion)
        self.assertEqual(resultado, esperado)
        print(f"Test Superado: {importe} * 0.21 = {resultado}")

if __name__ == '__main__':
    unittest.main()