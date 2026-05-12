from bd import obtener_conexion
from funciones_auxiliares import sanitize_field
import sys

def convertir_pescado_a_json(pescado):
    return {
        'id': pescado[0],
        'nombre': sanitize_field(pescado[1]),
        'descripcion': sanitize_field(pescado[2]),
        'precio': float(pescado[3]),
        'foto': sanitize_field(pescado[4]),
        'origen': sanitize_field(pescado[5])
    }

def insertar_pescado(nombre, descripcion, precio, foto, origen):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "INSERT INTO pescados(nombre, descripcion, precio, foto, origen) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (nombre, descripcion, precio, foto, origen))
            conexion.commit()
        ret, code = {"status": "OK"}, 200
    except Exception as e:
        print(f"Error al insertar pescado: {e}", flush=True)
        ret, code = {"status": "Failure"}, 500
    finally:
        if conexion:
            conexion.close()
    return ret, code

def obtener_pescados():
    pescadosjson = []
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio, foto, origen FROM pescados")
            pescados = cursor.fetchall()
            if pescados:
                pescadosjson = [convertir_pescado_a_json(p) for p in pescados]
        code = 200
    except Exception as e:
        print(f"Error al consultar todos los pescados: {e}", flush=True)
        code = 500
    finally:
        if conexion:
            conexion.close()
    return pescadosjson, code

def obtener_pescado_por_id(id):
    pescadojson = {}
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "SELECT id, nombre, descripcion, precio, foto, origen FROM pescados WHERE id = %s"
            cursor.execute(query, (id,))
            pescado = cursor.fetchone()
            if pescado:
                pescadojson = convertir_pescado_a_json(pescado)
        code = 200
    except Exception as e:
        print(f"Error al consultar el pescado {id}: {e}", flush=True)
        code = 500
    finally:
        if conexion:
            conexion.close()
    return pescadojson, code

def eliminar_pescado(id):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM pescados WHERE id = %s", (id,))
            ret = {"status": "OK"} if cursor.rowcount == 1 else {"status": "Failure"}
        conexion.commit()
        code = 200
    except Exception as e:
        print(f"Error al eliminar pescado: {e}", flush=True)
        ret, code = {"status": "Failure"}, 500
    finally:
        if conexion:
            conexion.close()
    return ret, code

def actualizar_pescado(id, nombre, descripcion, precio, foto, origen):
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = "UPDATE pescados SET nombre = %s, descripcion = %s, precio = %s, foto = %s, origen = %s WHERE id = %s"
            cursor.execute(query, (nombre, descripcion, precio, foto, origen, id))
            ret = {"status": "OK"} if cursor.rowcount == 1 else {"status": "Failure"}
        conexion.commit()
        code = 200
    except Exception as e:
        print(f"Error al actualizar pescado: {e}", flush=True)
        ret, code = {"status": "Failure"}, 500
    finally:
        if conexion:
            conexion.close()
    return ret, code
