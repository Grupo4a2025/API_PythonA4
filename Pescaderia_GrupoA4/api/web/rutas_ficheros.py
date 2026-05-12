from flask import request, Blueprint, jsonify
import controlador_ficheros

bp = Blueprint('ficheros', __name__)

@bp.route('/', methods=['POST']) 
def upload():
    """Recibe un archivo y un nombre para almacenarlo en el sistema."""
    try:
        # Verificación básica de la existencia del archivo en la petición
        if 'fichero' not in request.files:
            return jsonify({"status": "ERROR", "mensaje": "No se ha enviado ningún archivo"}), 400
            
        contenido = request.files['fichero'] 
        nombre = request.form.get("nombre")
        
        if not nombre:
            return jsonify({"status": "ERROR", "mensaje": "Falta el nombre del archivo"}), 400

        # Llamada al controlador que ya aplica secure_filename
        respuesta, code = controlador_ficheros.guardar_fichero(nombre, contenido)
        
    except Exception as e:
        print(f"Error crítico subiendo archivo: {e}", flush=True)
        respuesta = {"status": "ERROR", "mensaje": "Error interno del servidor"}
        code = 500
        
    return jsonify(respuesta), code

@bp.route('/<archivo>', methods=['GET']) 
def ver(archivo):
    """Solicita la visualización del contenido de un archivo específico."""
    try:
        # El controlador se encarga de la apertura segura del archivo
        respuesta, code = controlador_ficheros.ver_fichero(archivo)
    except Exception as e:
        print(f"Error al visualizar archivo: {e}", flush=True)
        respuesta = {"status": "ERROR"}
        code = 500
        
    return jsonify(respuesta), code
