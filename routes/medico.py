from flask import Blueprint, jsonify, send_from_directory
from routes.common import respuesta, password_complejo, usuario
from models.medico import Medico
from tools.jwt_required import jwt_token_requerido

ws_medico = Blueprint('ws_medico', __name__)

medico = Medico()

@ws_medico.route('/medicos', methods=['POST'])
@jwt_token_requerido
def registrar_medico():
    try:
        data = __import__('flask').request.get_json() or {}
        obligatorios = ['email', 'password', 'nombres', 'apellidos', 'dni', 'cmp', 'estado_medico_id']
        if not all(data.get(k) for k in obligatorios):
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        if not password_complejo(data.get('password')):
            return respuesta(None, 'La contraseña no cumple complejidad', False, 400)

        creado = usuario.crear_medico(data)
        if not creado:
            return respuesta(None, 'No se pudo registrar médico (duplicado o dato inválido)', False, 400)

        return respuesta(creado, 'Médico registrado correctamente', True, 201)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_medico.route('/medicos', methods=['GET'])
@jwt_token_requerido
def listar_medicos():
    try:
        resultado = medico.listar_medicos()

        data = []
        for row in resultado:
            data.append({
                "medico_id": row["medico_id"],
                "usuario_id": row["usuario_id"],
                "email": row["email"],
                "nombres": row["nombres"],
                "apellidos": row["apellidos"],
                "cmp": row["cmp"],
                "consultorio": row["consultorio"],
                "imagen_url": f"/medicos/{row['medico_id']}/imagen"
            })
        
        return jsonify({
            'data': data,
            'message': 'Lista de medicos obtenida correctamente',
            'status': True
        }), 200
    except Exception as e:
        return jsonify({'data': None, 'message': str(e), 'status': False}), 500


@ws_medico.route('/medicos/<int:id_medico>', methods=['GET'])
@jwt_token_requerido
def obtener_medico(id_medico):
    try:
        resultado = usuario.obtener_medico(id_medico)
        if not resultado:
            return respuesta(None, 'Médico inexistente', False, 404)
        return respuesta(resultado, 'Médico obtenido correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_medico.route('/medicos/<int:id_medico>', methods=['PUT'])
@jwt_token_requerido
def actualizar_medico(id_medico):
    try:
        data = __import__('flask').request.get_json() or {}
        if not data.get('estado_medico_id'):
            return respuesta(None, 'Campos obligatorios vacíos', False, 400)

        ok = usuario.actualizar_medico(id_medico, data)
        if not ok:
            return respuesta(None, 'Médico inexistente', False, 404)
        return respuesta({'medico_id': id_medico}, 'Médico actualizado correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_medico.route('/medicos/<int:id_medico>', methods=['DELETE'])
@jwt_token_requerido
def eliminar_medico(id_medico):
    try:
        ok = usuario.eliminar_medico(id_medico)
        if not ok:
            return respuesta(None, 'Médico inexistente', False, 404)
        return respuesta({'medico_id': id_medico}, 'Médico eliminado correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_medico.route('/medicos/especialidad/<int:id_especialidad>', methods=['GET'])
@jwt_token_requerido
def listar_medicos_por_especialidad(id_especialidad):
    try:
        data = usuario.listar_medicos_por_especialidad(id_especialidad)
        return respuesta(data, 'Lista de médicos por especialidad obtenida correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)


@ws_medico.route('/medicos/<int:id_medico>/citas', methods=['GET'])
@jwt_token_requerido
def listar_citas_medico(id_medico):
    try:
        return respuesta(usuario.listar_citas_medico(id_medico), 'Listado de citas del médico obtenido correctamente', True, 200)
    except Exception as e:
        return respuesta(None, str(e), False, 500)

# E.6 Obtener la imagen de la especialidad
@ws_medico.route('/medicos/<int:id>/imagen', methods=['GET'])
@jwt_token_requerido
def obtener_imagen(id):
    print("alapez")
    #validar si se cuenta con el id para obtener la foto
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400

    try:
        resultado = medico.obtener_imagen(id)
        print("Resultado de obtener imagen del médico:")
        print(resultado)
        if resultado:
            return send_from_directory('uploads/fotos/medicos', resultado['imagen_url'])
        else:
            return send_from_directory('uploads/fotos/medicos', 'default.png')
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500