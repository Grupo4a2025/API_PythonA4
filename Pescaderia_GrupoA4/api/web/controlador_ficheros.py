import os
import sys
from werkzeug.utils import secure_filename

# 1. Configuración por entorno: recuperamos la ruta o usamos la de la estructura del proyecto
# En Docker suele ser /app/api/web/static/archivos
RUTA_MONTAJE = os.getenv('STORAGE_PATH', '/app/static/archivos')

def guardar_fichero(nombre, contenido):
    """Guarda un fichero de forma segura aplicando sanitización de nombres."""
    try:
        print("--- INICIO GUARDADO SEGURO ---", flush=True)
        
        # 2. Crear carpeta si no existe con permisos restrictivos (755 en lugar de 777)
        if not os.path.exists(RUTA_MONTAJE):
            os.makedirs(RUTA_MONTAJE, mode=0o755, exist_ok=True)

        # 3. Sanitización: Evita Path Traversal (ej. nombre="../etc/passwd")
        nombre_seguro = secure_filename(nombre)
        ruta_final = os.path.join(RUTA_MONTAJE, nombre_seguro) 
        
        print(f"Guardando de forma segura en: {ruta_final}", flush=True)
        
        # 4. Guardar el archivo
        contenido.save(ruta_final)
        
        # 5. Ajustar permisos a 644 (lectura para todos, escritura solo para el dueño)
        try:
            os.chmod(ruta_final, 0o644)
            print("Permisos ajustados a 644.", flush=True)
        except Exception as e:
            print(f"Error ajustando permisos: {e}", flush=True)

        return {"status": "OK", "filename": nombre_seguro}, 200
            
    except Exception as e:
        print(f"EXCEPCIÓN EN GUARDADO: {str(e)}", flush=True)  
        return {"status": "ERROR", "msg": str(e)}, 500

def ver_fichero(nombre):
    """Lee un fichero de forma segura sin usar comandos de sistema."""
    try:
        # Sanitizar el nombre para evitar que lean archivos fuera de la carpeta permitida
        nombre_seguro = secure_filename(nombre)
        ruta_fichero = os.path.join(RUTA_MONTAJE, nombre_seguro)
        
        # 6. EVITAR COMMAND INJECTION: Usamos open() nativo en lugar de subprocess/cat
        if os.path.exists(ruta_fichero):
            with open(ruta_fichero, 'r', errors='ignore') as f:
                salida = f.read()
            return {"contenido": salida, "status": "OK"}, 200
        else:
            return {"contenido": "", "status": "FILE_NOT_FOUND"}, 404
            
    except Exception as e:
        print(f"Error al leer fichero: {e}", flush=True)
        return {"contenido": "", "status": "ERROR"}, 500
