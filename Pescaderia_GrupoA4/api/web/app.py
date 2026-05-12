from flask import Flask, jsonify
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)

    # 1. Configuración de Seguridad y CORS
    # Permite que el WAF en Apache o un frontend externo se comuniquen con la API
    CORS(app)
    
    # Asegura que caracteres como la 'ñ' o tildes se vean correctamente en JSON
    app.config['JSON_AS_ASCII'] = False

    # 2. Configuración de Debug desde el entorno
    # Se recupera del .env inyectado por Docker; por defecto False por seguridad
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'

    # 3. Registro de Blueprints (Rutas)
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

    # 4. Manejador de errores global
    @app.errorhandler(500)
    def server_error(error):
        # El error detallado solo se imprime en los logs del contenedor para triaje técnico
        print(f'Critical error in request: {error}', flush=True)
        return jsonify({"status": "Internal Server Error", "msg": "Consulte los logs del sistema"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    
    try:
        # Recuperamos la configuración del servidor desde el entorno (.env)
        # Se utilizan los valores de tu infraestructura: 0.0.0.0 y puerto 8080
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 8080))
        
        print(f"Servidor API iniciado en http://{host}:{port}", flush=True)
        app.run(host=host, port=port)
    except Exception as e:
        print(f"No se pudo iniciar el servidor: {e}", flush=True)
