from bd import obtener_conexion
from funciones_auxiliares import sanitize_field
import sys

def convertir_comentario_a_json(comentario):
    return {
        'id': comentario[0],
        'usuario': sanitize_field(comentario[1]),
        'descripcion': sanitize_field(comentario[2])
    }

def insertar_comentario(usuario, descripcion):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO comentarios(usuario, descripcion) VALUES (%s, %s)"
            cursor.execute(query, (usuario, descripcion))
            conexion.commit()
        ret, code = {"status": "OK"}, 200
    except Exception as e:
        print(f"Excepcion al insertar un comentario: {e}", flush=True)
        ret, code = {"status": "ERROR"}, 500
    finally:
        if conexion:
            conexion.close()
    return ret, code

def obtener_comentarios():
    comentariosjson = []
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, usuario, descripcion FROM comentarios")
            comentarios = cursor.fetchall()
            if comentarios:
                comentariosjson = [convertir_comentario_a_json(c) for c in comentarios]
        code = 200
    except Exception as e:
        print(f"Excepcion al consultar todas los comentarios: {e}", flush=True)
        code = 500
    finally:
        if conexion:
            conexion.close()
    return comentariosjson, code
