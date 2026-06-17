from .auth import Auth
from .paciente import Paciente
from .medico import Medico
from .administrativo import Administrativo
from .especialidad import Especialidad
from .medico_especialidad import MedicoEspecialidad
from .horario import Horario
from .citas import Cita

class Usuario:
    """Fachada que delega operaciones a modelos especializados."""
    def __init__(self):
        # instancias de cada modelo
        self.auth = Auth()
        self.paciente = Paciente()
        self.medico = Medico()
        self.administrativo = Administrativo()
        self.especialidad = Especialidad()
        self.medico_especialidad = MedicoEspecialidad()
        self.horario = Horario()
        self.cita = Cita()

    # Auth / Usuario
    def login(self, email, clave):
        return self.auth.login(email, clave)

    def obtener_foto(self, usuario_id):
        return self.auth.obtener_foto(usuario_id)

    def obtener_perfil(self, usuario_id):
        return self.auth.obtener_perfil(usuario_id)

    def actualizar_foto(self, usuario_id, foto):
        return self.auth.actualizar_foto(usuario_id, foto)

    def cambiar_password(self, usuario_id, password_actual, password_nueva):
        return self.auth.cambiar_password(usuario_id, password_actual, password_nueva)

    # Paciente
    def crear_paciente(self, data):
        return self.paciente.crear_paciente(data)

    def listar_pacientes(self):
        return self.paciente.listar_pacientes()

    def obtener_paciente(self, paciente_id):
        return self.paciente.obtener_paciente(paciente_id)

    def actualizar_paciente(self, paciente_id, data):
        return self.paciente.actualizar_paciente(paciente_id, data)

    def eliminar_paciente(self, paciente_id):
        return self.paciente.eliminar_paciente(paciente_id)

    # Medico
    def crear_medico(self, data):
        return self.medico.crear_medico(data)

    def listar_medicos(self):
        return self.medico.listar_medicos()

    def obtener_medico(self, medico_id):
        return self.medico.obtener_medico(medico_id)

    def actualizar_medico(self, medico_id, data):
        return self.medico.actualizar_medico(medico_id, data)

    def eliminar_medico(self, medico_id):
        return self.medico.eliminar_medico(medico_id)

    def listar_medicos_por_especialidad(self, especialidad_id):
        return self.medico.listar_medicos_por_especialidad(especialidad_id)

    # Administrativo
    def crear_administrativo(self, data):
        return self.administrativo.crear_administrativo(data)

    def listar_administrativos(self):
        return self.administrativo.listar_administrativos()

    def obtener_administrativo(self, administrativo_id):
        return self.administrativo.obtener_administrativo(administrativo_id)

    def actualizar_administrativo(self, administrativo_id, data):
        return self.administrativo.actualizar_administrativo(administrativo_id, data)

    def eliminar_administrativo(self, administrativo_id):
        return self.administrativo.eliminar_administrativo(administrativo_id)

    # Especialidad
    def crear_especialidad(self, data):
        return self.especialidad.crear_especialidad(data)

    def listar_especialidades(self):
        return self.especialidad.listar_especialidades()

    def obtener_especialidad(self, especialidad_id):
        return self.especialidad.obtener_especialidad(especialidad_id)

    def actualizar_especialidad(self, especialidad_id, data):
        return self.especialidad.actualizar_especialidad(especialidad_id, data)

    def eliminar_especialidad(self, especialidad_id):
        return self.especialidad.eliminar_especialidad(especialidad_id)

    # Medico-Especialidad
    def crear_medico_especialidad(self, data):
        return self.medico_especialidad.crear_medico_especialidad(data)

    def listar_medico_especialidades(self):
        return self.medico_especialidad.listar_medico_especialidades()

    def obtener_medico_especialidad(self, relacion_id):
        return self.medico_especialidad.obtener_medico_especialidad(relacion_id)

    def actualizar_medico_especialidad(self, relacion_id, data):
        return self.medico_especialidad.actualizar_medico_especialidad(relacion_id, data)

    def eliminar_medico_especialidad(self, relacion_id):
        return self.medico_especialidad.eliminar_medico_especialidad(relacion_id)

    # Horarios
    def horarios_disponibles(self, especialidad_id, fecha_inicio=None, fecha_fin=None):
        return self.horario.horarios_disponibles(especialidad_id, fecha_inicio, fecha_fin)

    # Citas
    def registrar_cita(self, data, creado_por_usuario_id):
        return self.cita.registrar_cita(data, creado_por_usuario_id)

    def listar_citas_paciente(self, paciente_id):
        return self.cita.listar_citas_paciente(paciente_id)

    def cancelar_cita(self, cita_id, motivo_cancelacion):
        return self.cita.cancelar_cita(cita_id, motivo_cancelacion)

    def listar_citas_medico(self, medico_id):
        return self.cita.listar_citas_medico(medico_id)
