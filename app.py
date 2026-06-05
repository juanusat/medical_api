from flask import Flask
from routes.auth import ws_usuario
from routes.paciente import ws_paciente
from routes.medico import ws_medico
from routes.especialidad import ws_especialidad
from routes.administrativo import ws_administrativo
from routes.medico_especialidad import ws_medico_especialidad
from routes.horarios import ws_horarios
from routes.citas import ws_cita
from get_env import _get_required_env

app = Flask(__name__)
app.register_blueprint(ws_usuario, url_prefix='/api')
app.register_blueprint(ws_paciente, url_prefix='/api')
app.register_blueprint(ws_medico, url_prefix='/api')
app.register_blueprint(ws_especialidad, url_prefix='/api')
app.register_blueprint(ws_administrativo, url_prefix='/api')
app.register_blueprint(ws_medico_especialidad, url_prefix='/api')
app.register_blueprint(ws_horarios, url_prefix='/api')
app.register_blueprint(ws_cita, url_prefix='/api')

@app.route('/')
def home():
    return 'MedicalApp - Running API Restful'

if __name__ == '__main__':
    app.run(port=_get_required_env('API_PORT', int), debug=True, host='0.0.0.0')