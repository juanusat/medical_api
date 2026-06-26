from flask import Blueprint, request, jsonify
from models.citas import Cita 
from tools.jwt_required import jwt_token_requerido
from routes.common import respuesta, usuario

#Crear un módulo (servicio WEB) para la gestión de citas
ws_cita = Blueprint('ws_cita', __name__)

#PUNTO H.1(REVISAR EXAMEN)
@ws_cita.route('/citas', methods=['POST'])
@jwt_token_requerido
def registrar_cita():
    data = request.get_json() or {}
    paciente_id = data.get("paciente_id")
    paciente_oncologico = data.get("paciente_oncologico", False)
    citas = data.get("citas", [])
    creado_por_usuario_id = request.usuario_id

    if not citas:
        return respuesta(None, 'Faltan datos obligatorios', False, 400)

    perfil = usuario.obtener_perfil(creado_por_usuario_id)
    if not perfil:
        return respuesta(None, 'Usuario inexistente', False, 404)

    if perfil.get('rol') == 'PACIENTE':
        paciente = usuario.obtener_paciente_por_usuario_id(creado_por_usuario_id)
        if not paciente:
            return respuesta(None, 'El usuario no tiene un paciente asociado', False, 400)
        paciente_id = paciente['paciente_id']
    else:
        if not paciente_id:
            return respuesta(None, 'Debe seleccionar un paciente para registrar la cita', False, 400)

    try:
        estado, resultado= Cita().registrar(paciente_id, paciente_oncologico, creado_por_usuario_id, citas)
        if estado:
            return respuesta({
                'paciente_id': paciente_id,
                'total_citas_registradas': len(resultado),
                'citas': resultado
            }, 'Citas registradas correctamente', True, 200)

        return respuesta(None, resultado, False, 500)
    except Exception as e:
        return respuesta(None, str(e), False, 500)