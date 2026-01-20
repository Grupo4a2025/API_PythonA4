from flask import request, Blueprint, jsonify

# INTENTO DE IMPORTACIÓN ROBUSTA
# Esto permite que funcione tanto si lanzas la app desde /api como desde la raíz
try:
    import api.web.controlador_usuarios as controlador_usuarios
except ImportError:
    try:
        import controlador_usuarios
    except ImportError:
        # Último intento: import relativo (si estuvieran en el mismo paquete)
        from . import controlador_usuarios

bp = Blueprint('usuarios', __name__)

@bp.route("/login", methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
        
        # Usamos .get() para evitar que el servidor explote si falta el campo
        username = login_json.get('username')
        password = login_json.get('password')
        
        # Llamamos al controlador que arreglamos antes (con seguridad SQL)
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
        # Si no envían profile, ponemos 'normal' por defecto
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