from __future__ import print_function
import os
import sys
import subprocess
import stat

# Ruta interna donde Python guardará las cosas
RUTA_MONTAJE = "/app/static/archivos"

def guardar_fichero(nombre, contenido):
    try:
        print("--- INICIO GUARDADO ---", flush=True)
        
        # 1. Crear carpeta si no existe
        if not os.path.exists(RUTA_MONTAJE):
            os.makedirs(RUTA_MONTAJE, exist_ok=True)
            # Permisos 777 a la carpeta
            try:
                os.chmod(RUTA_MONTAJE, 0o777)
            except:
                pass

        # 2. Ruta final
        ruta_final = os.path.join(RUTA_MONTAJE, nombre) 
        print(f"Guardando en: {ruta_final}", flush=True)
        
        # 3. Guardar
        contenido.save(ruta_final)
        
        # 4. QUITAR CANDADO (Permisos al archivo)
        try:
            os.chmod(ruta_final, 0o666)
            print("Permisos actualizados.", flush=True)
        except Exception as e:
            print(f"Error permisos: {e}", flush=True)

        # 5. Confirmación
        if os.path.exists(ruta_final):
            respuesta = {"status": "OK"}
            code = 200
        else:
            respuesta = {"status": "ERROR"}
            code = 500
            
    except Exception as e:
        print(f"EXCEPCION: {str(e)}", flush=True)  
        respuesta = {"status": "ERROR"}
        code = 500
    return respuesta, code

def ver_fichero(nombre):
    # Esta función se mantiene para compatibilidad, aunque visualizamos por Apache
    try:
        ruta_fichero = os.path.join(RUTA_MONTAJE, nombre)
        salida = subprocess.getoutput("cat " + ruta_fichero)
        respuesta = {"contenido": salida, "status": "OK"}
        code = 200
    except:
        respuesta = {"contenido": "", "status": "ERROR"}
        code = 500
    return respuesta, code