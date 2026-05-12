from flask import request, Blueprint, jsonify
# Simplificamos el import ya que controlador_usuarios.py está en la misma carpeta
import controlador_usuarios

bp = Blueprint('usuarios', __name__)

@bp.route("/login", methods=['POST'])
def login():
    """Endpoint para la autenticación de usuarios."""
    if request.is_json:
        login_json = request.get_json()
        
        username = login_json.get('username')
        password = login_json.get('password')
        
        # El controlador ya está securizado contra Inyección SQL
        respuesta, code = controlador_usuarios.login_usuario(username, password)
    else:
        respuesta = {"status": "Bad request", "mensaje": "Se requiere JSON"}
        code = 400 # Cambiado a 400 (Bad Request) que es más preciso que 401 aquí
        
    return jsonify(respuesta), code

@bp.route("/registro", methods=['POST'])
def registro():
    """Endpoint para dar de alta nuevos usuarios."""
    if request.is_json:
        login_json = request.get_json()
        username = login_json.get('username')
        password = login_json.get('password')
        profile = login_json.get('profile', 'normal')
        
        respuesta, code = controlador_usuarios.alta_usuario(username, password, profile)
    else:
        respuesta = {"status": "Bad request", "mensaje": "Se requiere JSON"}
        code = 400
        
    return jsonify(respuesta), code

@bp.route("/logout", methods=['GET'])
def logout():
    """Endpoint para el cierre de sesión."""
    respuesta, code = controlador_usuarios.logout()
    return jsonify(respuesta), code
