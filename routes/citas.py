from flask import Blueprint, request, jsonify
from models.citas import Cita 
from tools.jwt_required import jwt_token_requerido

#Crear un módulo (servicio WEB) para la gestión de citas
ws_cita = Blueprint('ws_cita', __name__)

#PUNTO H.1(REVISAR EXAMEN)
@ws_cita.route('/citas', methods=['POST'])
@jwt_token_requerido
def registrar_cita():
    #Obtener los datos del request body    
    data= request.get_json()
    #Alamacenar los datos en variables
    paciente_id = data.get("paciente_id")
    paciente_oncologico = data.get("paciente_oncologico", False)
    citas = data.get("citas", [])
    creado_por_usuario_id = request.usuario_id

    #Validar si contamos con los datos requeridos
    if not all([paciente_id, citas]):
        return jsonify({"status": False, "data": None, "message": "Faltan datos obligatorios"}), 400

    try:
        estado, resultado= Cita().registrar(paciente_id, paciente_oncologico, creado_por_usuario_id, citas)
        if estado: #Si es true se registraron las citas correctamente
            return jsonify({
                "status": True, 
                "data": {
                    "paciente_id": paciente_id,
                    "total_citas_registradas": len(resultado),
                    "citas": resultado
                }, 
                "message": "Citas registradas correctamente"
                }), 200
        else: #Si es false, significaria que ocurrió un error al registrar la transacción
            return jsonify({
                "status": False, 
                "data": None, 
                "message": resultado}), 500
    except Exception as e:
        return jsonify({"status": False, "data": None, "message": str(e)}), 500