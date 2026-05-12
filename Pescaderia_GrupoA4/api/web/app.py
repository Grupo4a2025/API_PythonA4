from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from funciones_auxiliares import sanitize_field

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['JSON_AS_ASCII'] = False
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'

    # --- PREVENCIÓN XSS: Interceptor Global ---
    @app.before_request
    def clean_request():
        if request.is_json:
            # Crea un nuevo objeto request.cleaned_json con los datos seguros
            request.cleaned_json = sanitize_field(request.get_json())

    # Registro de Blueprints
    from rutas_usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

    from rutas_pescados import bp as pescados_bp
    app.register_blueprint(pescados_bp, url_prefix='/api/pescados')

    from rutas_ficheros import bp as ficheros_bp
    app.register_blueprint(ficheros_bp, url_prefix='/api/ficheros')

    from rutas_comentarios import bp as comentarios_bp
    app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')

    @app.errorhandler(500)
    def server_error(error):
        print(f'Critical error in request: {error}', flush=True)
        return jsonify({"status": "Internal Server Error", "msg": "Consulte los logs"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    try:
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 8080))
        app.run(host=host, port=port)
    except Exception as e:
        print(f"No se pudo iniciar el servidor: {e}", flush=True)
