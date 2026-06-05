from conexionBD import Conexion

class Horario:
    def horarios_disponibles(self, especialidad_id, fecha):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            SELECT
                hd.id AS horario_disponible_id,
                m.id AS medico_id,
                CONCAT(m.nombres, ' ', m.apellidos) AS medico,
                e.nombre AS especialidad,
                hd.fecha,
                hd.hora_inicio,
                hd.hora_fin,
                ehd.nombre AS estado
            FROM horario_disponible hd
            INNER JOIN medico m ON hd.medico_id = m.id
            INNER JOIN especialidad e ON hd.especialidad_id = e.id
            INNER JOIN estado_horario_disponible ehd ON hd.estado_horario_disponible_id = ehd.id
            WHERE hd.especialidad_id = %s
              AND hd.fecha = %s
              AND ehd.nombre = 'DISPONIBLE'
            ORDER BY hd.hora_inicio
        """
        cursor.execute(sql, [especialidad_id, fecha])
        resultados = cursor.fetchall()
        cursor.close()
        con.close()
        return resultados
