import os
from werkzeug.utils import secure_filename

RUTA_MONTAJE = os.getenv('STORAGE_PATH', '/app/static/archivos')

def guardar_fichero(nombre, contenido):
    try:
        if not os.path.exists(RUTA_MONTAJE):
            os.makedirs(RUTA_MONTAJE, mode=0o755, exist_ok=True)

        nombre_seguro = secure_filename(nombre)
        ruta_final = os.path.join(RUTA_MONTAJE, nombre_seguro) 
        
        contenido.save(ruta_final)
        
        try:
            os.chmod(ruta_final, 0o644)
        except Exception as e:
            print(f"Error ajustando permisos: {e}", flush=True)

        return {"status": "OK", "filename": nombre_seguro}, 200
            
    except Exception as e:
        print(f"EXCEPCION EN GUARDADO: {str(e)}", flush=True)  
        return {"status": "ERROR", "msg": "Error interno al guardar"}, 500

def ver_fichero(nombre):
    try:
        nombre_seguro = secure_filename(nombre)
        ruta_fichero = os.path.join(RUTA_MONTAJE, nombre_seguro)
        
        if os.path.exists(ruta_fichero):
            with open(ruta_fichero, 'r', errors='ignore') as f:
                salida = f.read()
            return {"contenido": salida, "status": "OK"}, 200
        else:
            return {"contenido": "", "status": "FILE_NOT_FOUND"}, 404
            
    except Exception as e:
        print(f"Error al leer fichero: {e}", flush=True)
        return {"contenido": "", "status": "ERROR"}, 500
