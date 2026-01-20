from flask import request, Blueprint, jsonify


try:
    import api.web.controlador_usuarios as controlador_usuarios
except ImportError:
    try:
        import controlador_usuarios
    except ImportError:
        from . import controlador_usuarios

bp = Blueprint('usuarios', __name__)

@bp.route("/login", methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
        
        username = login_json.get('username')
        password = login_json.get('password')
        
        respuesta, code = controlador_usuarios.login_usuario(username, password)
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    return jsonify(respuesta), code

@bp.route("/registro", methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
        username = login_json.get('username')
        password = login_json.get('password')
        profile = login_json.get('profile', 'normal')
        
        respuesta, code = controlador_usuarios.alta_usuario(username, password, profile)
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    return jsonify(respuesta), code


@bp.route("/logout", methods=['GET'])
def logout():
    respuesta, code = controlador_usuarios.logout()
    return jsonify(respuesta), code