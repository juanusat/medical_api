import os
from flask import Blueprint, request, g, send_from_directory
from werkzeug.utils import secure_filename
from routes.common import respuesta, password_complejo, extension_permitida, usuario
from tools.jwt_utils import generar_token
from tools.jwt_required import jwt_token_requerido
import firebase.fcm as fcm
import datetime
ws_usuario = Blueprint('ws_usuario', __name__)


@ws_usuario.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    clave = data.get('clave') or data.get('password')

    if not all([email, clave]):
        return respuesta(None, 'Faltan datos obligatorios', False, 400)

    try:
        resultado = usuario.login(email, clave)
        if resultado: 
            if resultado.get('estado_usuario') != 'ACTIVO':
                return respuesta(None, 'Usuario inactivo', False, 403)

            resultado.pop('clave', None)
            token = generar_token({'usuario_id': resultado['usuario_id']}, 600)
            resultado['token'] = token
            ahora = datetime.datetime.now()
            fecha_hora_formato = ahora.strftime("%Y-%m-%d %H:%M:%S")
            fcm.enviar_notificacion(resultado['usuario_id'], 'Medical App', f'Inicio de sesión satisfactorio el {fecha_hora_formato}')
            return respuesta(resultado, 'Inicio de sesión satisfactorio', True, 200)
        else:
            return respuesta(None, 'Credenciales incorrectas', False, 401)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_usuario.route('/perfil', methods=['GET'])
@jwt_token_requerido
def perfil():
    try:
        payload = g.jwt_payload
        resultado = usuario.obtener_perfil(payload['usuario_id'])
        if not resultado:
            return respuesta(None, 'Usuario inexistente', False, 404)
        return respuesta(resultado, 'Perfil obtenido correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_usuario.route('/usuarios/foto/<id>', methods=['GET'])
@jwt_token_requerido
def obtener_foto(id):
    if not all([id]):
        return respuesta(None, 'Faltan datos obligatorios', False, 400)

    try:
        resultado = usuario.obtener_foto(id)
        if resultado:
            return send_from_directory('uploads/fotos/usuarios', resultado['foto'])
        else:
            return send_from_directory('uploads/fotos/usuarios', 'default.jpg')
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_usuario.route('/usuarios/foto/<id_usuario>', methods=['GET'])
@jwt_token_requerido
def obtener_foto_api(id_usuario):
    return obtener_foto(id_usuario)


@ws_usuario.route('/usuarios/actualizar/foto', methods=['PUT'])
@jwt_token_requerido
def actualizar_foto():
    try:
        usuario_id = request.form.get('id')
        foto = request.files.get('foto')

        if not all([usuario_id, foto]):
            return respuesta(None, 'Faltan datos obligatorios', False, 400)

        if foto.filename == '' or not extension_permitida(foto.filename):
            return respuesta(None, 'Archivo de foto inválido', False, 400)

        extension = foto.filename.rsplit('.', 1)[1].lower()
        nombre_archivo = secure_filename(f'{usuario_id}.{extension}')

        carpeta_destino = os.path.join('uploads', 'fotos', 'usuarios')
        os.makedirs(carpeta_destino, exist_ok=True)
        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)
        foto.save(ruta_archivo)

        actualizado = usuario.actualizar_foto(usuario_id, nombre_archivo)
        if not actualizado:
            return respuesta(None, 'Usuario inexistente', False, 404)

        return respuesta({'usuario_id': int(usuario_id), 'foto': nombre_archivo}, 'Foto actualizada correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_usuario.route('/usuarios/password/<int:id_usuario>', methods=['PUT'])
@jwt_token_requerido
def cambiar_password(id_usuario):
    try:
        data = request.get_json() or {}
        password_actual = data.get('password_actual')
        password_nueva = data.get('password_nueva')

        if not all([password_actual, password_nueva]):
            return respuesta(None, 'Faltan datos obligatorios', False, 400)

        if not password_complejo(password_nueva):
            return respuesta(None, 'La contraseña nueva no cumple complejidad', False, 400)

        resultado = usuario.cambiar_password(id_usuario, password_actual, password_nueva)
        if resultado == 'NO_EXISTE':
            return respuesta(None, 'Usuario inexistente', False, 404)
        if resultado == 'PASSWORD_ACTUAL_INVALIDA':
            return respuesta(None, 'Credenciales inválidas', False, 401)

        return respuesta({'usuario_id': id_usuario}, 'Contraseña actualizada correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_usuario.route('/usuarios/registrar/token', methods=['PUT'])
@jwt_token_requerido
def registrar_token():
    data = request.get_json()
    usuario_id = data.get('id')
    token = data.get('token')
    dispositivo = data.get('dispositivo')

    if not all([usuario_id, token, dispositivo]):
        return respuesta(None, 'Faltan datos obligatorios', False, 400)

    try:
        estado, mensaje = usuario.registrar_token_dispositivo(usuario_id, dispositivo, token)
        if estado:
            return respuesta(None, 'Token registrado correctamente', True, 200)
        else:
            return respuesta(None, mensaje, False, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)
