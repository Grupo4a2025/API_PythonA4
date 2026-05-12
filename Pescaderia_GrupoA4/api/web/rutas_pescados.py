from flask import request, Blueprint, jsonify, make_response
import json
import os
import controlador_pescados
from funciones_auxiliares import calculariva, Encoder

bp = Blueprint('pescados', __name__)

@bp.route("/", methods=["GET"])
def pescados():
    respuesta, code = controlador_pescados.obtener_pescados()
    if code == 200:
        for pescado in respuesta:
            try:
                precio = float(pescado.get("precio", 0))
                pescado["iva"] = calculariva(precio)
            except (ValueError, TypeError):
                pescado["iva"] = 0 
    
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers['Content-Type'] = 'application/json'
    return response
    
@bp.route("/<id>", methods=["GET"])
def pescado_por_id(id):
    respuesta, code = controlador_pescados.obtener_pescado_por_id(id)
    if code == 200 and respuesta:
        try:
            precio = float(respuesta.get("precio", 0))
            respuesta["iva"] = calculariva(precio)
        except (ValueError, TypeError):
            pass

    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers['Content-Type'] = 'application/json'
    return response

@bp.route("/", methods=["POST"])
def guardar_pescado():
    if request.headers.get('Content-Type') == 'application/json':
        datos = getattr(request, 'cleaned_json', {})
        
        nombre = datos.get("nombre")
        descripcion = datos.get("descripcion")
        precio = datos.get("precio")
        foto = datos.get("foto")
        origen = datos.get("origen") 
        
        if (nombre and descripcion and precio is not None and foto and origen and
            isinstance(nombre, str) and isinstance(descripcion, str) and 
            (isinstance(precio, int) or isinstance(precio, float)) and 
            isinstance(foto, str) and isinstance(origen, str) and len(nombre) < 100):
            
            respuesta, code = controlador_pescados.insertar_pescado(nombre, descripcion, precio, foto, origen)
        else:
            respuesta, code = {"status": "Bad parameters"}, 400
    else:
        respuesta, code = {"status": "Bad request"}, 400
        
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers['Content-Type'] = 'application/json'
    return response

@bp.route("/<id>", methods=["DELETE"])
def eliminar_pescado(id):
    respuesta, code = controlador_pescados.eliminar_pescado(id)
    return jsonify(respuesta), code

@bp.route("/", methods=["PUT"])
def actualizar_pescado():
    if request.headers.get('Content-Type') == 'application/json':
        datos = getattr(request, 'cleaned_json', {})
        
        id_pescado = datos.get("id")
        nombre = datos.get("nombre")
        descripcion = datos.get("descripcion")
        precio = datos.get("precio")
        foto = datos.get("foto")
        origen = datos.get("origen")
        
        if (id_pescado and nombre and descripcion and precio is not None and foto and origen and
            isinstance(nombre, str) and isinstance(descripcion, str) and 
            (isinstance(precio, int) or isinstance(precio, float)) and 
            isinstance(foto, str) and isinstance(origen, str)):
            
            respuesta, code = controlador_pescados.actualizar_pescado(id_pescado, nombre, descripcion, float(precio), foto, origen)
        else:
            respuesta, code = {"status": "Bad parameters"}, 400
    else:
        respuesta, code = {"status": "Bad request"}, 400
        
    response = make_response(json.dumps(respuesta, cls=Encoder), code)
    response.headers['Content-Type'] = 'application/json'
    return response
