from bd import obtener_conexion
import sys

def convertir_pescado_a_json(pescado):
    """Convierte la tupla de MariaDB en un diccionario para la API."""
    return {
        'id': pescado[0],
        'nombre': pescado[1],
        'descripcion': pescado[2],
        'precio': float(pescado[3]),
        'foto': pescado[4],
        'origen': pescado[5]
    }

def insertar_pescado(nombre, descripcion, precio, foto, origen):
    """Inserta un nuevo registro de forma segura."""
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # ✅ YA ERA CORRECTO: Consulta parametrizada
            query = "INSERT INTO pescados(nombre, descripcion, precio, foto, origen) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (nombre, descripcion, precio, foto, origen))
            conexion.commit()
        ret = {"status": "OK"}
        code = 200
    except Exception as e:
        print(f"Error al insertar pescado: {e}", flush=True)
        ret = {"status": "Failure"}
        code = 500
    finally:
        if conexion:
            conexion.close() # Cierre garantizado de la conexión
    return ret, code

def obtener_pescados():
    """Recupera la lista completa de productos."""
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
    """Busca un pescado específico por su ID primario."""
    pescadojson = {}
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # ✅ CORRECTO: El ID se pasa como tupla (id,) para evitar inyecciones
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
    """Elimina un registro verificando que se haya afectado una fila."""
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
        ret = {"status": "Failure"}
        code = 500
    finally:
        if conexion:
            conexion.close()
    return ret, code

def actualizar_pescado(id, nombre, descripcion, precio, foto, origen):
    """Actualiza los datos de un pescado existente."""
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            query = """UPDATE pescados 
                       SET nombre = %s, descripcion = %s, precio = %s, foto = %s, origen = %s 
                       WHERE id = %s"""
            cursor.execute(query, (nombre, descripcion, precio, foto, origen, id))
            ret = {"status": "OK"} if cursor.rowcount == 1 else {"status": "Failure"}
        conexion.commit()
        code = 200
    except Exception as e:
        print(f"Error al actualizar pescado: {e}", flush=True)
        ret = {"status": "Failure"}
        code = 500
    finally:
        if conexion:
            conexion.close()
    return ret, code
