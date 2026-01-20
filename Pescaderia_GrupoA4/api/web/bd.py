import pymysql
import os

def obtener_conexion():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        
        database=os.environ.get('DB_DATABASE', 'ciber'),
        
        user=os.environ.get('DB_USERNAME', 'root'),
        password=os.environ.get('DB_PASSWORD', 'example')
    )