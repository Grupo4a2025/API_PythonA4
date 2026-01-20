from bd import obtener_conexion
import sys

def login_usuario(username, password):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # CORREGIDO: Usamos %s para evitar errores con símbolos en las contraseñas
            sql = "SELECT perfil FROM usuarios WHERE usuario = %s AND clave = %s"
            cursor.execute(sql, (username, password))
            usuario_encontrado = cursor.fetchone()
            
            if usuario_encontrado is None:
                ret = {"status": "ERROR", "mensaje": "Usuario o clave incorrectos"}
            else:
                # Devolvemos también el perfil por si lo necesitas en el front
                ret = {"status": "OK", "perfil": usuario_encontrado[0]}
        
        code = 200
        conexion.close()
    except Exception as e:
        print("Excepcion al validar al usuario: " + str(e), flush=True)   
        ret = {"status": "ERROR"}
        code = 500
    return ret, code

def alta_usuario(username, password, perfil):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # 1. Comprobamos si ya existe
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s", (username,))
            usuario_existente = cursor.fetchone()
            
            if usuario_existente is None:
                # 2. Si no existe, lo creamos (Usando %s por seguridad)
                sql_insert = "INSERT INTO usuarios(usuario, clave, perfil) VALUES (%s, %s, %s)"
                cursor.execute(sql_insert, (username, password, perfil))
                
                if cursor.rowcount == 1:
                    conexion.commit()
                    ret = {"status": "OK"}
                    code = 200
                else:
                    ret = {"status": "ERROR"}
                    code = 500
            else:
                ret = {"status": "ERROR", "mensaje": "El usuario ya existe"}
                code = 200 # Devolvemos 200 para que el front pueda leer el mensaje de error
        conexion.close()
    except Exception as e:
        print("Excepcion al registrar al usuario: " + str(e), flush=True)   
        ret = {"status": "ERROR"}
        code = 500
    return ret, code    

def logout():
    # Como es una API sin estado (REST), el logout lo gestiona realmente el navegador borrando datos,
    # pero dejamos el endpoint por compatibilidad.
    return {"status": "OK"}, 200