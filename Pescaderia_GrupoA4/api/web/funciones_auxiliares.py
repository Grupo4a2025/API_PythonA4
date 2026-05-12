import decimal
import json
import os

class Encoder(json.JSONEncoder):
    """
    Codificador personalizado para manejar objetos Decimal de MariaDB.
    Convierte tipos Decimal a float para que jsonify no de error.
    """
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(Encoder, self).default(obj)

def calculariva(importe):
    """
    Calcula el IVA utilizando una variable de entorno. 
    Si no está definida en el .env, usa el 21% por defecto.
    """
    iva_rate = float(os.getenv('IVA_RATE', 0.21))
    return importe * iva_rate
