from flask import request, Blueprint, jsonify
import controlador_comentarios

bp = Blueprint('comentarios', __name__)

@bp.route("/", methods=['POST'])
def crear_comentario():
    """Recibe un nuevo comentario en formato JSON y lo almacena."""
    if request.is_json:
        comentario_json = request.get_json()
        
        # Extracción segura con .get() para evitar errores si faltan campos
        usuario = comentario_json.get('usuario')
        descripcion = comentario_json.get('descripcion')
        
        if not usuario or not descripcion:
            return jsonify({"status": "ERROR", "mensaje": "Faltan campos obligatorios"}), 400

        # El controlador ya gestiona la conexión de forma segura
        respuesta, code = controlador_comentarios.insertar_comentario(usuario, descripcion)
    else:
        respuesta = {"status": "Bad request", "mensaje": "Se requiere Content-Type: application/json"}
        code = 400 # Error de petición mal formada
        
    return jsonify(respuesta), code

@bp.route("/", methods=['GET'])
def consulta_comentarios():
    """Devuelve el listado de todos los comentarios registrados."""
    respuesta, code = controlador_comentarios.obtener_comentarios()
    return jsonify(respuesta), code
