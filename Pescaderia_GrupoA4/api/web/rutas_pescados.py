from flask import request, Blueprint, jsonify
import os
import controlador_pescados

bp = Blueprint('pescados', __name__)

# Configuración de IVA recuperada del entorno (por defecto 0.21)
IVA_RATE = float(os.getenv('IVA_RATE', 0.21))

def calculariva(importe):
    """Calcula el impuesto basado en el ratio configurado."""
    return importe * IVA_RATE

@bp.route("/", methods=["GET"])
def pescados():
    """Obtiene el listado completo y calcula el IVA dinámicamente."""
    respuesta, code = controlador_pescados.obtener_pescados()
    
    if code == 200:
        for pescado in respuesta:
            try:
                precio = float(pescado.get("precio", 0))
                pescado["iva"] = calculariva(precio)
            except (ValueError, TypeError):
                pescado["iva"] = 0 

    return jsonify(respuesta), code
    
@bp.route("/<id>", methods=["GET"])
def pescado_por_id(id):
    """Obtiene un producto específico por su ID."""
    respuesta, code = controlador_pescados.obtener_pescado_por_id(id)
    
    if code == 200 and respuesta:
        try:
            precio = float(respuesta.get("precio", 0))
            respuesta["iva"] = calculariva(precio)
        except (ValueError, TypeError):
            pass

    return jsonify(respuesta), code

@bp.route("/", methods=["POST"])
def guardar_pescado():
    """Inserta un nuevo registro validando que la entrada sea JSON."""
    if request.is_json:
        datos = request.get_json()
        
        # Extracción segura de datos
        nombre = datos.get("nombre")
        descripcion = datos.get("descripcion")
        precio = datos.get("precio")
        foto = datos.get("foto")
        origen = datos.get("origen") 
        
        respuesta, code = controlador_pescados.insertar_pescado(nombre, descripcion, precio, foto, origen)
    else:
        respuesta = {"status": "Bad request", "mensaje": "Se requiere JSON"}
        code = 400 # Error de sintaxis en la petición
        
    return jsonify(respuesta), code

@bp.route("/<id>", methods=["DELETE"])
def eliminar_pescado(id):
    """Elimina un producto del catálogo."""
    respuesta, code = controlador_pescados.eliminar_pescado(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_pescado():
    """Actualiza un producto existente."""
    if request.is_json:
        datos = request.get_json()
        
        id_pescado = datos.get("id")
        nombre = datos.get("nombre")
        descripcion = datos.get("descripcion")
        precio = datos.get("precio")
        foto = datos.get("foto")
        origen = datos.get("origen")
        
        respuesta, code = controlador_pescados.actualizar_pescado(id_pescado, nombre, descripcion, precio, foto, origen)
    else:
        respuesta = {"status": "Bad request", "mensaje": "Se requiere JSON"}
        code = 400
        
    return jsonify(respuesta), code
