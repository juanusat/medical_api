from flask import Blueprint
from routes.common import respuesta, password_complejo, usuario
from tools.jwt_required import jwt_token_requerido

ws_administrativo = Blueprint('ws_administrativo', __name__)


@ws_administrativo.route('/administrativos', methods=['POST'])
@jwt_token_requerido
def registrar_administrativo():
    try:
        data = __import__('flask').request.get_json() or {}
        obligatorios = ['email', 'password', 'nombres', 'apellidos', 'dni', 'cargo']
        if not all(data.get(k) for k in obligatorios):
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        if not password_complejo(data.get('password')):
            return respuesta(None, 'La contraseña no cumple complejidad', False, 400)

        creado = usuario.crear_administrativo(data)
        if not creado:
            return respuesta(None, 'No se pudo registrar administrativo (duplicado o dato inválido)', False, 400)

        return respuesta(creado, 'Administrativo registrado correctamente', True, 201)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_administrativo.route('/administrativos', methods=['GET'])
@jwt_token_requerido
def listar_administrativos():
    try:
        return respuesta(usuario.listar_administrativos(), 'Lista de administrativos obtenida correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_administrativo.route('/administrativos/<int:id_administrativo>', methods=['GET'])
@jwt_token_requerido
def obtener_administrativo(id_administrativo):
    try:
        resultado = usuario.obtener_administrativo(id_administrativo)
        if not resultado:
            return respuesta(None, 'Administrativo inexistente', False, 404)
        return respuesta(resultado, 'Administrativo obtenido correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_administrativo.route('/administrativos/<int:id_administrativo>', methods=['PUT'])
@jwt_token_requerido
def actualizar_administrativo(id_administrativo):
    try:
        data = __import__('flask').request.get_json() or {}
        if not data.get('cargo'):
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        ok = usuario.actualizar_administrativo(id_administrativo, data)
        if not ok:
            return respuesta(None, 'Administrativo inexistente', False, 404)
        return respuesta({'administrativo_id': id_administrativo}, 'Administrativo actualizado correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_administrativo.route('/administrativos/<int:id_administrativo>', methods=['DELETE'])
@jwt_token_requerido
def eliminar_administrativo(id_administrativo):
    try:
        ok = usuario.eliminar_administrativo(id_administrativo)
        if not ok:
            return respuesta(None, 'Administrativo inexistente', False, 404)
        return respuesta({'administrativo_id': id_administrativo}, 'Administrativo eliminado correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)
