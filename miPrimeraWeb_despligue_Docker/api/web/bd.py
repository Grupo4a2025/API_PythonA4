import pymysql
import os

def obtener_conexion():
    return pymysql.connect(
        # El host debe ser el nombre del servicio en docker-compose: 'mariadb'
        host=os.environ.get('DB_HOST', 'localhost'),
        
        # Nombre de la base de datos: 'ciber'
        database=os.environ.get('DB_DATABASE', 'ciber'),
        
        # Usuario y contraseña definidos en el environment de docker-compose
        user=os.environ.get('DB_USERNAME', 'root'),
        password=os.environ.get('DB_PASSWORD', 'example')
    )