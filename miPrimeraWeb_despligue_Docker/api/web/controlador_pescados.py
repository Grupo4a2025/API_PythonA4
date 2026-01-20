from bd import obtener_conexion
import sys


def convertir_pescado_a_json(pescado):
    d = {}
    d['id'] = pescado[0]
    d['nombre'] = pescado[1]
    d['descripcion'] = pescado[2]
    d['precio'] = float(pescado[3])
    d['foto'] = pescado[4]
    d['origen'] = pescado[5]  # CAMBIO: Antes ingredientes
    return d

def insertar_pescado(nombre, descripcion, precio, foto, origen):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # CAMBIO: Tabla pescados y columna origen
        cursor.execute("INSERT INTO pescados(nombre, descripcion, precio, foto, origen) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, descripcion, precio, foto, origen))
    conexion.commit()
    conexion.close()
    ret = {"status": "OK"}
    code = 200
    return ret, code

def obtener_pescados():
    pescadosjson = []
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # CAMBIO: Select con origen
            cursor.execute("SELECT id, nombre, descripcion, precio, foto, origen FROM pescados")
            pescados = cursor.fetchall()
            if pescados:
                for pescado in pescados:
                    pescadosjson.append(convertir_pescado_a_json(pescado))
        conexion.close()
        code = 200
    except Exception as e:
        print("Excepcion al consultar todos los pescados: " + str(e), flush=True)
        code = 500
    return pescadosjson, code

def obtener_pescado_por_id(id):
    pescadojson = {}
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # CAMBIO: Select con origen
            cursor.execute("SELECT id, nombre, descripcion, precio, foto, origen FROM pescados WHERE id = %s", (id,))
            pescado = cursor.fetchone()
            if pescado is not None:
                pescadojson = convertir_pescado_a_json(pescado)
        conexion.close()
        code = 200
    except Exception as e:
        print("Excepcion al consultar un pescado: " + str(e), flush=True)
        code = 500
    return pescadojson, code

def eliminar_pescado(id):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM pescados WHERE id = %s", (id,))
            if cursor.rowcount == 1:
                ret = {"status": "OK"}
            else:
                ret = {"status": "Failure"}
        conexion.commit()
        conexion.close()
        code = 200
    except Exception as e:
        print("Excepcion al eliminar un pescado: " + str(e), flush=True)
        ret = {"status": "Failure"}
        code = 500
    return ret, code

def actualizar_pescado(id, nombre, descripcion, precio, foto, origen):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # CAMBIO: Update con origen y tabla pescados
            cursor.execute("UPDATE pescados SET nombre = %s, descripcion = %s, precio = %s, foto = %s, origen = %s WHERE id = %s",
                       (nombre, descripcion, precio, foto, origen, id))
            if cursor.rowcount == 1:
                ret = {"status": "OK"}
            else:
                ret = {"status": "Failure"}
        conexion.commit()
        conexion.close()
        code = 200
    except Exception as e:
        print("Excepcion al actualizar un pescado: " + str(e), flush=True)
        ret = {"status": "Failure"}
        code = 500
    return ret, code