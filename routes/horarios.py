from flask import Blueprint
from routes.common import respuesta, usuario
from tools.jwt_required import jwt_token_requerido

ws_horarios = Blueprint('ws_horarios', __name__)


@ws_horarios.route('/horarios/disponibles', methods=['POST'])
@jwt_token_requerido
def horarios_disponibles():
    try:
        data = __import__('flask').request.get_json() or {}
        if not data.get('especialidad_id') or not data.get('fecha'):
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        resultados = usuario.horarios_disponibles(data['especialidad_id'], data['fecha'])
        return respuesta(resultados, 'Horarios disponibles obtenidos correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)
