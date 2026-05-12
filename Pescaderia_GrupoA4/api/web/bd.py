import pymysql
import os

def obtener_conexion():
    """Establece la conexión con MariaDB usando las variables de entorno de Docker."""
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'mariadba4'),
        user=os.getenv('DB_USERNAME', 'root'),
        password=os.getenv('DB_PASSWORD', 'grupo4'),
        database=os.getenv('DB_DATABASE', 'ciber'),
        port=int(os.getenv('DB_PORT', 3306)),
        cursorclass=pymysql.cursors.Cursor
    )
