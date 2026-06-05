import os
import re
from flask import request, jsonify, send_from_directory, g
from werkzeug.utils import secure_filename
from models.usuario import Usuario
from tools.jwt_utils import generar_token
from tools.jwt_required import jwt_token_requerido

# Instancia compartida del modelo
usuario = Usuario()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def respuesta(data, message, status=True, code=200):
    return jsonify({'status': status, 'data': data, 'message': message}), code


def password_complejo(password):
    if not password:
        return False
    patron = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$'
    return re.match(patron, password) is not None


def extension_permitida(filename):
    if '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
