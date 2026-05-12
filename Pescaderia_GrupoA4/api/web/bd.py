import pymysql
import os

def obtener_conexion():
    """Establece la conexión con MariaDB usando las variables de entorno de Docker."""
    return pymysql.connect(
        # El host debe ser el nombre del servicio en docker-compose: 'mariadba4'
        host=os.getenv('DB_HOST', 'mariadba4'),
        
        # El usuario y la base de datos según tu .env
        user=os.getenv('DB_USERNAME', 'root'),
        password=os.getenv('DB_PASSWORD', 'grupo4'),
        database=os.getenv('DB_DATABASE', 'ciber'),
        
        # Es importante convertir el puerto a entero para pymysql
        port=int(os.getenv('DB_PORT', 3306)),
        
        # Opcional: Esto ayuda a que los resultados se manejen como tuplas estándar 
        # en tus controladores actuales
        cursorclass=pymysql.cursors.Cursor 
    )
