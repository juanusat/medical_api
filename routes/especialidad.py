from flask import Blueprint, request, jsonify, send_from_directory
from routes.common import respuesta, usuario
from models.especialidad import Especialidad
from tools.jwt_required import jwt_token_requerido

ws_especialidad = Blueprint('ws_especialidad', __name__)

especialidad = Especialidad()

@ws_especialidad.route('/especialidades', methods=['POST'])
@jwt_token_requerido
def registrar_especialidad():
    try:
        data = __import__('flask').request.get_json() or {}
        if not data.get('nombre'):
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        creado = usuario.crear_especialidad(data)
        if not creado:
            return respuesta(None, 'Especialidad duplicada o inválida', False, 400)

        return respuesta(creado, 'Especialidad registrada correctamente', True, 201)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_especialidad.route('/especialidades', methods=['GET'])
@jwt_token_requerido
def listar_especialidades():
    try:
        resultado = especialidad.consultarEspecialidades()

        data = []
        for row in resultado:
            data.append({
                "id": row["id"],
                "nombre": row["nombre"],
                "descripcion": row["descripcion"],
                "imagen_url": f"/especialidades/{row['id']}/imagen"
            })
        
        return jsonify({
            'data': data,
            'message': 'Lista de especialidades obtenida correctamente',
            'status': True
        }), 200
    except Exception as e:
        return jsonify({'data': None, 'message': str(e), 'status': False}), 500


@ws_especialidad.route('/especialidades/<int:id_especialidad>', methods=['GET'])
@jwt_token_requerido
def obtener_especialidad(id_especialidad):
    try:
        resultado = usuario.obtener_especialidad(id_especialidad)
        if not resultado:
            return respuesta(None, 'Especialidad inexistente', False, 404)
        return respuesta(resultado, 'Especialidad obtenida correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_especialidad.route('/especialidades/<int:id_especialidad>', methods=['PUT'])
@jwt_token_requerido
def actualizar_especialidad(id_especialidad):
    try:
        data = __import__('flask').request.get_json() or {}
        if not data.get('nombre'):
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        ok = usuario.actualizar_especialidad(id_especialidad, data)
        if not ok:
            return respuesta(None, 'Especialidad inexistente', False, 404)
        return respuesta({'especialidad_id': id_especialidad}, 'Especialidad actualizada correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_especialidad.route('/especialidades/<int:id_especialidad>', methods=['DELETE'])
@jwt_token_requerido
def eliminar_especialidad(id_especialidad):
    try:
        ok = usuario.eliminar_especialidad(id_especialidad)
        if not ok:
            return respuesta(None, 'Especialidad inexistente', False, 404)
        return respuesta({'especialidad_id': id_especialidad}, 'Especialidad eliminada correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)
    
# E.6 Obtener la imagen de la especialidad
@ws_especialidad.route('/especialidades/<int:id>/imagen', methods=['GET'])
@jwt_token_requerido
def obtener_imagen(id):
    #validar si se cuenta con el id para obtener la foto
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400

    try:
        resultado = especialidad.obtener_imagen(id)
        if resultado:
            return send_from_directory('uploads/fotos/especialidades', resultado['imagen_url'])
        else:
            return send_from_directory('uploads/fotos/especialidades', 'default.png')
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
