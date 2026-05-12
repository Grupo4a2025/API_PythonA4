from flask import request, Blueprint, jsonify
import controlador_ficheros
import os

bp = Blueprint('ficheros', __name__)

# Configuración de seguridad para archivos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['POST']) 
def upload():
    try:
        if 'fichero' not in request.files:
            return jsonify({"status": "ERROR", "mensaje": "Falta archivo"}), 400
            
        contenido = request.files['fichero'] 
        nombre = request.form.get("nombre")
        
        if not nombre or not allowed_file(nombre) or len(nombre) > 100:
            return jsonify({"status": "ERROR", "mensaje": "Nombre o extensión no válida"}), 400

        # Verificar tamaño del archivo (leyendo el cursor de la petición)
        contenido.seek(0, os.SEEK_END)
        file_length = contenido.tell()
        contenido.seek(0, 0) # Reiniciar el cursor tras medir

        if file_length > MAX_FILE_SIZE:
            return jsonify({"status": "ERROR", "mensaje": "Archivo demasiado grande"}), 413

        respuesta, code = controlador_ficheros.guardar_fichero(nombre, contenido)
        
    except Exception as e:
        print(f"Error subiendo archivo: {e}", flush=True)
        respuesta, code = {"status": "ERROR"}, 500
        
    return jsonify(respuesta), code
