from flask import Blueprint, request
from routes.common import respuesta, password_complejo, usuario
from tools.jwt_required import jwt_token_requerido

ws_paciente = Blueprint('ws_paciente', __name__)


@ws_paciente.route('/pacientes', methods=['POST'])
@jwt_token_requerido
def registrar_paciente():
    try:
        data = request.get_json() or {}
        obligatorios = ['email', 'password', 'nombres', 'apellidos', 'dni']
        if not all(data.get(k) for k in obligatorios):
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        if not password_complejo(data.get('password')):
            return respuesta(None, 'La contraseña no cumple complejidad', False, 400)

        creado = usuario.crear_paciente(data)
        if not creado:
            return respuesta(None, 'No se pudo registrar paciente (duplicado o dato inválido)', False, 400)

        return respuesta(creado, 'Paciente registrado correctamente', True, 201)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_paciente.route('/pacientes', methods=['GET'])
@jwt_token_requerido
def listar_pacientes():
    try:
        return respuesta(usuario.listar_pacientes(), 'Lista de pacientes obtenida correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_paciente.route('/pacientes/<int:id_paciente>', methods=['GET'])
@jwt_token_requerido
def obtener_paciente(id_paciente):
    try:
        resultado = usuario.obtener_paciente(id_paciente)
        if not resultado:
            return respuesta(None, 'Paciente inexistente', False, 404)
        return respuesta(resultado, 'Paciente obtenido correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_paciente.route('/pacientes/<int:id_paciente>', methods=['PUT'])
@jwt_token_requerido
def actualizar_paciente(id_paciente):
    try:
        data = request.get_json() or {}
        obligatorios = ['nombres', 'apellidos']
        if not all(data.get(k) for k in obligatorios):
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        ok = usuario.actualizar_paciente(id_paciente, data)
        if not ok:
            return respuesta(None, 'Paciente inexistente', False, 404)
        return respuesta({'paciente_id': id_paciente}, 'Paciente actualizado correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_paciente.route('/pacientes/<int:id_paciente>', methods=['DELETE'])
@jwt_token_requerido
def eliminar_paciente(id_paciente):
    try:
        ok = usuario.eliminar_paciente(id_paciente)
        if not ok:
            return respuesta(None, 'Paciente inexistente', False, 404)
        return respuesta({'paciente_id': id_paciente}, 'Paciente eliminado correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_paciente.route('/pacientes/<int:id_paciente>/citas', methods=['GET'])
@jwt_token_requerido
def listar_citas_paciente(id_paciente):
    try:
        return respuesta(usuario.listar_citas_paciente(id_paciente), 'Listado de citas obtenido correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)
