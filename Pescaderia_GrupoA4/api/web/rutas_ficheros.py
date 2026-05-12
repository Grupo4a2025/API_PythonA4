from flask import request, Blueprint, jsonify
import controlador_ficheros
import os

bp = Blueprint('ficheros', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 MB limite

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['POST']) 
def upload():
    try:
        if 'fichero' not in request.files:
            return jsonify({"status": "ERROR", "mensaje": "Falta archivo"}), 400
            
        contenido = request.files['fichero'] 
        nombre = request.form.get("nombre")
        
        if not nombre or not isinstance(nombre, str) or not allowed_file(nombre) or len(nombre) > 100:
            return jsonify({"status": "ERROR", "mensaje": "Nombre o extension no valida"}), 400

        contenido.seek(0, os.SEEK_END)
        file_length = contenido.tell()
        contenido.seek(0, 0) 

        if file_length > MAX_FILE_SIZE:
            return jsonify({"status": "ERROR", "mensaje": "Archivo demasiado grande"}), 413

        respuesta, code = controlador_ficheros.guardar_fichero(nombre, contenido)
        
    except Exception as e:
        print(f"Error subiendo archivo: {e}", flush=True)
        respuesta, code = {"status": "ERROR"}, 500
        
    return jsonify(respuesta), code

@bp.route('/<archivo>', methods=['GET']) 
def ver(archivo):
    try:
        respuesta, code = controlador_ficheros.ver_fichero(archivo)
    except Exception as e:
        print(f"Error al visualizar archivo: {e}", flush=True)
        respuesta, code = {"status": "ERROR"}, 500
        
    return jsonify(respuesta), code
