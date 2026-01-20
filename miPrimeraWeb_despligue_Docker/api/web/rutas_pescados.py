from flask import request, Blueprint, jsonify
try:
    import api.web.controlador_pescados as controlador_pescados
except ImportError:
    import controlador_pescados

bp = Blueprint('pescados', __name__)

# --- 1. FUNCIÓN OBLIGATORIA DEL EXAMEN ---
def calculariva(importe):
    return importe * 0.21

@bp.route("/", methods=["GET"])
def pescados():
    # 1. Obtenemos los datos crudos de la BBDD (vía controlador)
    respuesta, code = controlador_pescados.obtener_pescados()
    
    # 2. Si todo ha ido bien (code 200), añadimos el IVA al vuelo
    if code == 200:
        # Recorremos la lista de pescados que nos ha dado el controlador
        for pescado in respuesta:
            try:
                # Aseguramos que sea float para calcular
                precio = float(pescado["precio"])
                # Calculamos y añadimos el campo nuevo 'iva'
                pescado["iva"] = calculariva(precio)
            except:
                pescado["iva"] = 0 # Por si falla algún precio

    # 3. Devolvemos la respuesta modificada
    return jsonify(respuesta), code
    
@bp.route("/<id>", methods=["GET"])
def pescado_por_id(id):
    respuesta, code = controlador_pescados.obtener_pescado_por_id(id)
    
    # Opcional: También calculamos IVA si piden uno solo
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