from flask import request, Blueprint, jsonify
try:
    import api.web.controlador_pescados as controlador_pescados
except ImportError:
    import controlador_pescados

bp = Blueprint('pescados', __name__)

def calculariva(importe):
    return importe * 0.21

@bp.route("/", methods=["GET"])
def pescados():
    respuesta, code = controlador_pescados.obtener_pescados()
    
    if code == 200:
        for pescado in respuesta:
            try:
                precio = float(pescado["precio"])
                pescado["iva"] = calculariva(precio)
            except:
                pescado["iva"] = 0 

    return jsonify(respuesta), code
    
@bp.route("/<id>", methods=["GET"])
def pescado_por_id(id):
    respuesta, code = controlador_pescados.obtener_pescado_por_id(id)
    
    if code == 200:
        try:
            precio = float(respuesta["precio"])
            respuesta["iva"] = calculariva(precio)
        except:
            pass

    return jsonify(respuesta), code

@bp.route("/", methods=["POST"])
def guardar_pescado():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        pescado_json = request.json
        
        nombre = pescado_json["nombre"]
        descripcion = pescado_json["descripcion"]
        precio = pescado_json["precio"]
        foto = pescado_json["foto"]
        origen = pescado_json["origen"] 
        
        respuesta, code = controlador_pescados.insertar_pescado(nombre, descripcion, precio, foto, origen)
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    return jsonify(respuesta), code

@bp.route("/<id>", methods=["DELETE"])
def eliminar_pescado(id):
    respuesta, code = controlador_pescados.eliminar_pescado(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_pescado():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        pescado_json = request.json
        
        id = pescado_json["id"]
        nombre = pescado_json["nombre"]
        descripcion = pescado_json["descripcion"]
        precio = float(pescado_json["precio"])
        foto = pescado_json["foto"]
        origen = pescado_json["origen"]
        
        respuesta, code = controlador_pescados.actualizar_pescado(id, nombre, descripcion, precio, foto, origen)
    else:
        respuesta = {"status": "Bad request"}
        code = 401
    return jsonify(respuesta), code