from flask import Flask, jsonify
import os
from variables import cargarvariables

def create_app():
    app = Flask(__name__)

    app.config.setdefault('DEBUG', True)

    
    # 1. USUARIOS
    from rutas_usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

    # 2. PESCADOS 
    from rutas_pescados import bp as pescados_bp
    app.register_blueprint(pescados_bp, url_prefix='/api/pescados')

    # 3. FICHEROS
    from rutas_ficheros import bp as ficheros_bp
    app.register_blueprint(ficheros_bp, url_prefix='/api/ficheros')

    # 4. COMENTARIOS
    from rutas_comentarios import bp as comentarios_bp
    app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')

    @app.errorhandler(500)
    def server_error(error):
        # Convertimos error a str() por seguridad
        print('An exception occurred during a request. ERROR:' + str(error), flush=True)
        ret={"status": "Internal Server Error"}
        return jsonify(ret), 500

    return app

if __name__ == '__main__':
    app = create_app()
    # cargarvariables() # Descomentar si no usas Docker o necesitas variables locales
    try:
        # Añadidos valores por defecto (5000 y 0.0.0.0) por si fallan las variables de entorno
        port = int(os.environ.get('PORT', 5000))
        host = os.environ.get('HOST', '0.0.0.0')
        app.run(host=host, port=port)
    except Exception as e:
        print(f"Error starting server: {e}", flush=True)