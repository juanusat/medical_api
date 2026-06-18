import json

from flask import Blueprint, request
from routes.common import respuesta, usuario
from tools.jwt_required import jwt_token_requerido

ws_horarios = Blueprint('ws_horarios', __name__)


@ws_horarios.route('/horarios/disponibles', methods=['POST'])
@jwt_token_requerido
def horarios_disponibles():
    try:
        data = request.get_json() or {}
        if not data:
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)
        else:
            especialidad_id = data.get('especialidad_id')
            fecha_inicio = data.get('fecha_inicio') or data.get('fecha')
            fecha_fin = data.get('fecha_fin') or data.get('fecha')

        if not especialidad_id:
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            return respuesta(None, 'La fecha inicio no puede ser mayor que la fecha fin', False, 400)

        resultados = usuario.horarios_disponibles(especialidad_id, fecha_inicio, fecha_fin)
        return respuesta(resultados, 'Horarios disponibles obtenidos correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)
