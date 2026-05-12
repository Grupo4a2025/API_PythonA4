from flask import request, Blueprint, jsonify, make_response
import json
import controlador_comentarios
from funciones_auxiliares import Encoder

bp = Blueprint('comentarios', __name__)

@bp.route("/", methods=['POST'])
def crear_comentario():
    if request.headers.get('Content-Type') == 'application/json':
        comentario_json = getattr(request, 'cleaned_json', {})
        usuario = comentario_json.get('usuario')
        descripcion = comentario_json.get('descripcion')
        
        if usuario and descripcion:
            if isinstance(usuario, str) and isinstance(descripcion, str) and len(usuario) < 50 and len(descripcion) < 500:
                respuesta, code = controlador_comentarios.insertar_comentario(usuario, descripcion)
            else:
                respuesta, code = {"status": "Bad parameters"}, 400
        else:
            respuesta, code = {"status": "Bad request", "mensaje": "Faltan campos obligatorios"}, 400
    else:
        respuesta, code = {"status": "Bad request"}, 400
        
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers['Content-Type'] = 'application/json'
    return response

@bp.route("/", methods=['GET'])
def consulta_comentarios():
    respuesta, code = controlador_comentarios.obtener_comentarios()
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers['Content-Type'] = 'application/json'
    return response
