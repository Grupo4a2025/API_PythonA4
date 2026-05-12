from bd import obtener_conexion
import sys
import datetime as dt

def convertir_comentario_a_json(comentario):
    """Convierte una tupla de la base de datos a un diccionario JSON."""
    return {
        'id': comentario[0],
        'usuario': comentario[1],
        'descripcion': comentario[2]
    }

def insertar_comentario(usuario, descripcion):
    """Inserta un comentario usando consultas parametrizadas para evitar Inyección SQL."""
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # ✅ CORRECTO: Consulta parametrizada con %s
            # El conector se encarga de escapar caracteres peligrosos.
            query = "INSERT INTO comentarios(usuario, descripcion) VALUES (%s, %s)"
            cursor.execute(query, (usuario, descripcion))
            conexion.commit()
        
        ret = {"status": "OK"}
        code = 200
    except Exception as e:
        # Es mejor capturar la excepción específica para depuración
        print(f"Excepción al insertar un comentario: {e}", flush=True)
        ret = {"status": "ERROR"}
        code = 500
    finally:
        if conexion:
            conexion.close() # Aseguramos el cierre de la conexión
            
    return ret, code

def obtener_comentarios():
    """Recupera todos los comentarios de la base de datos."""
    comentariosjson = []
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Esta consulta es estática, pero se mantiene la estructura segura.
            cursor.execute("SELECT id, usuario, descripcion FROM comentarios")
            comentarios = cursor.fetchall()
            
            if comentarios:
                for comentario in comentarios:
                    comentariosjson.append(convertir_comentario_a_json(comentario))
        code = 200
    except Exception as e:
        print(f"Excepción al consultar todos los comentarios: {e}", flush=True)
        code = 500
    finally:
        if conexion:
            conexion.close()
            
    return comentariosjson, code
