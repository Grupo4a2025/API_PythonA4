import decimal
import json
import os
import html
import bleach

class Encoder(json.JSONEncoder):
    """Codificador para manejar objetos Decimal y sanitizar la salida si es necesario."""
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(Encoder, self).default(obj)

def calculariva(importe):
    """Calcula el IVA utilizando una variable de entorno."""
    iva_rate = float(os.getenv('IVA_RATE', 0.21))
    return importe * iva_rate

def sanitize_field(data):
    """Limpia y codifica caracteres peligrosos para evitar XSS recursivamente."""
    if isinstance(data, str):
        return bleach.clean(html.escape(data))
    if isinstance(data, dict):
        return {k: sanitize_field(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_field(v) for v in data]
    return data
