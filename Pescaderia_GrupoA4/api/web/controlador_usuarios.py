from bd import obtener_conexion
import sys

def login_usuario(username, password):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = "SELECT perfil FROM usuarios WHERE usuario = %s AND clave = %s"
            cursor.execute(sql, (username, password))
            usuario_encontrado = cursor.fetchone()
            
            if usuario_encontrado is None:
                ret = {"status": "ERROR", "mensaje": "Usuario o clave incorrectos"}
            else:
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
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s", (username,))
            usuario_existente = cursor.fetchone()
            
            if usuario_existente is None:
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
                code = 200 
        conexion.close()
    except Exception as e:
        print("Excepcion al registrar al usuario: " + str(e), flush=True)   
        ret = {"status": "ERROR"}
        code = 500
    return ret, code    

def logout():
    return {"status": "OK"}, 200