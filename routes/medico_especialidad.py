from flask import Blueprint
from routes.common import respuesta, usuario
from tools.jwt_required import jwt_token_requerido

ws_medico_especialidad = Blueprint('ws_medico_especialidad', __name__)


@ws_medico_especialidad.route('/medico-especialidades', methods=['POST'])
@jwt_token_requerido
def registrar_medico_especialidad():
    try:
        data = __import__('flask').request.get_json() or {}
        if not data.get('medico_id') or not data.get('especialidad_id'):
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        creado = usuario.crear_medico_especialidad(data)
        if not creado:
            return respuesta(None, 'Relación médico-especialidad duplicada o inválida', False, 400)

        return respuesta(creado, 'Relación médico-especialidad registrada correctamente', True, 201)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_medico_especialidad.route('/medico-especialidades', methods=['GET'])
@jwt_token_requerido
def listar_medico_especialidades():
    try:
        return respuesta(usuario.listar_medico_especialidades(), 'Lista de relaciones obtenida correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_medico_especialidad.route('/medico-especialidades/<int:id_relacion>', methods=['GET'])
@jwt_token_requerido
def obtener_medico_especialidad(id_relacion):
    try:
        resultado = usuario.obtener_medico_especialidad(id_relacion)
        if not resultado:
            return respuesta(None, 'Relación inexistente', False, 404)
        return respuesta(resultado, 'Relación obtenida correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_medico_especialidad.route('/medico-especialidades/<int:id_relacion>', methods=['PUT'])
@jwt_token_requerido
def actualizar_medico_especialidad(id_relacion):
    try:
        data = __import__('flask').request.get_json() or {}
        if not data.get('medico_id') or not data.get('especialidad_id'):
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        actualizado = usuario.actualizar_medico_especialidad(id_relacion, data)
        if actualizado is None:
            return respuesta(None, 'Relación médico-especialidad duplicada', False, 400)
        if actualizado is False:
            return respuesta(None, 'Relación inexistente', False, 404)

        return respuesta({'id': id_relacion}, 'Relación actualizada correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_medico_especialidad.route('/medico-especialidades/<int:id_relacion>', methods=['DELETE'])
@jwt_token_requerido
def eliminar_medico_especialidad(id_relacion):
    try:
        ok = usuario.eliminar_medico_especialidad(id_relacion)
        if not ok:
            return respuesta(None, 'Relación inexistente', False, 404)
        return respuesta({'id': id_relacion}, 'Relación eliminada correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)
