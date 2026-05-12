from flask import Flask, jsonify
import os

def create_app():
    app = Flask(__name__)

    # Configuración de Debug desde el entorno (por defecto True en desarrollo)
    app.config.setdefault('DEBUG', os.getenv('DEBUG', 'True') == 'True')

    # Registro de Blueprints (Controladores)
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
        print(f'An exception occurred during a request. ERROR: {error}', flush=True)
        ret = {"status": "Internal Server Error"}
        return jsonify(ret), 500

    return app

if __name__ == '__main__':
    app = create_app()
    
    try:
        # Usamos los valores de tu .env (8080 y 0.0.0.0)
        port = int(os.getenv('PORT', 8080))
        host = os.getenv('HOST', '0.0.0.0')
        
        print(f"Iniciando servidor en {host}:{port}...", flush=True)
        app.run(host=host, port=port)
    except Exception as e:
        print(f"Error starting server: {e}", flush=True)
