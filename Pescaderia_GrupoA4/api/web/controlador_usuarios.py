from bd import obtener_conexion
import sys

def login_usuario(username, password):
    """Valida las credenciales de un usuario de forma segura."""
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # ✅ CORRECTO: Consulta parametrizada para evitar bypass de login
            sql = "SELECT perfil FROM usuarios WHERE usuario = %s AND clave = %s"
            cursor.execute(sql, (username, password))
            usuario_encontrado = cursor.fetchone()
            
            if usuario_encontrado is None:
                ret = {"status": "ERROR", "mensaje": "Usuario o clave incorrectos"}
            else:
                ret = {"status": "OK", "perfil": usuario_encontrado[0]}
        
        code = 200
    except Exception as e:
        print(f"Excepción al validar al usuario: {e}", flush=True)   
        ret = {"status": "ERROR"}
        code = 500
    finally:
        if conexion:
            conexion.close() # Cierre garantizado de la conexión
    return ret, code

def alta_usuario(username, password, perfil):
    """Registra un nuevo usuario verificando duplicados."""
    conexion = None
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            # Comprobación de existencia previa
            cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s", (username,))
            if cursor.fetchone() is None:
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
    except Exception as e:
        print(f"Excepción al registrar al usuario: {e}", flush=True)   
        ret = {"status": "ERROR"}
        code = 500
    finally:
        if conexion:
            conexion.close()
    return ret, code     

def logout():
    """Finaliza la sesión del usuario."""
    return {"status": "OK"}, 200
