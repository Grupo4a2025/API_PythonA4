from flask import request, Blueprint, jsonify, make_response
import json
import controlador_usuarios
from funciones_auxiliares import Encoder

bp = Blueprint('usuarios', __name__)

@bp.route("/login", methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        # Uso de los datos pre-sanitizados por app.py
        login_json = getattr(request, 'cleaned_json', {})
        
        username = login_json.get("username")
        password = login_json.get("password")
        
        if username and password:
            # VALIDACIÓN ESTRICTA: Tipos y longitud máxima
            if isinstance(username, str) and isinstance(password, str) and len(username) < 50 and len(password) < 50:
                respuesta, code = controlador_usuarios.login_usuario(username, password)
            else:
                respuesta = {"status": "Bad parameters"}
                code = 400
        else:
            respuesta = {"status": "Bad request"}
            code = 400
    else:
        respuesta = {"status": "Bad request"}
        code = 400
        
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers['Content-Type'] = 'application/json'
    return response

@bp.route("/registro", methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        login_json = getattr(request, 'cleaned_json', {})
        username = login_json.get('username')
        password = login_json.get('password')
        profile = login_json.get('profile', 'normal')
        
        # VALIDACIÓN ESTRICTA
        if (username and password and profile and 
            isinstance(username, str) and isinstance(password, str) and isinstance(profile, str) and 
            len(username) < 50 and len(password) < 50 and profile in ['normal', 'admin']):
            
            respuesta, code = controlador_usuarios.alta_usuario(username, password, profile)
        else:
            respuesta = {"status": "Bad parameters"}
            code = 400
    else:
        respuesta = {"status": "Bad request"}
        code = 400
        
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers['Content-Type'] = 'application/json'
    return response

@bp.route("/logout", methods=['GET'])
def logout():
    respuesta, code = controlador_usuarios.logout()
    return jsonify(respuesta), code
