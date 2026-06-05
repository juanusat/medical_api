from functools import wraps
from flask import request, jsonify, g
from tools.jwt_utils import verificar_token

def jwt_token_requerido(f):
    @wraps(f)
    def envoltura(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({'status': False, 'data': None, 'message': 'Cabecera no válida'}), 401

        token = auth_header.replace("Bearer ", "", 1).strip()
        if not token:
            return jsonify({'status': False, 'data': None, 'message': 'Token requerido'}), 401

        payload = verificar_token(token)
        if not payload:
            return jsonify({'status': False, 'data': None, 'message': 'Token inválido o expirado'}), 401

        g.jwt_payload = payload
        #Almacenar el usuario_id en el objeto request
        request.usuario_id = payload.get('usuario_id')

        return f(*args, **kwargs)
    return envoltura
