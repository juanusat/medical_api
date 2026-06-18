from conexionBD import Conexion

class Horario:
    def horarios_disponibles(self, especialidad_id, fecha_inicio=None, fecha_fin=None):
        con = Conexion().open
        cursor = con.cursor()

        condiciones = [
            "hd.especialidad_id = %s",
            "hd.fecha BETWEEN %s AND %s",
            "ehd.nombre = 'DISPONIBLE'",
            "em.nombre = 'ACTIVO'",
            "CAST(CONCAT(hd.fecha, ' ', hd.hora_inicio) AS DATETIME) > NOW()",
        ]
        parametros = [especialidad_id, fecha_inicio, fecha_fin]

        sql = f"""
            SELECT
                hd.id AS horario_disponible_id,
                DATE_FORMAT(hd.fecha, '%%Y-%%m-%%d') AS fecha,
                TIME_FORMAT(hd.hora_inicio, '%%H:%%i') AS hora_inicio,
                TIME_FORMAT(hd.hora_fin, '%%H:%%i') AS hora_fin,

                m.id AS medico_id,
                CONCAT(m.nombres, ' ', m.apellidos) AS medico,
                m.cmp,
                m.consultorio,

                e.id AS especialidad_id,
                e.nombre AS especialidad,

                ehd.nombre AS estado_horario
            FROM horario_disponible hd
            INNER JOIN medico m
                ON hd.medico_id = m.id
            INNER JOIN especialidad e
                ON hd.especialidad_id = e.id
            INNER JOIN estado_horario_disponible ehd
                ON hd.estado_horario_disponible_id = ehd.id
            INNER JOIN estado_medico em
                ON m.estado_medico_id = em.id
            WHERE {' AND '.join(condiciones)}
            ORDER BY
                hd.fecha,
                hd.hora_inicio,
                medico
        """
        print('SQL HORARIOS DISPONIBLES:', sql)
        print('PARAMETROS HORARIOS DISPONIBLES:', parametros)
        cursor.execute(sql, parametros)
        resultados = cursor.fetchall()
        cursor.close()
        con.close()
        return resultados
