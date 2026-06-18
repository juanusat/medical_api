from conexionBD import Conexion

class Horario:
    def horarios_disponibles(self, especialidad_id, fecha_inicio=None, fecha_fin=None):
        con = Conexion().open
        cursor = con.cursor()

        # 1. Condiciones fijas que SIEMPRE se van a cumplir
        condiciones = [
            "hd.especialidad_id = %s",
            "ehd.nombre = 'DISPONIBLE'",
            "em.nombre = 'ACTIVO'",
            "CAST(CONCAT(hd.fecha, ' ', hd.hora_inicio) AS DATETIME) > NOW()"
        ]
        
        # El primer parámetro siempre será el ID de la especialidad
        parametros = [especialidad_id]

        # 2. Condiciones DINÁMICAS (Solo si el cliente envía fechas)
        if fecha_inicio and fecha_fin:
            condiciones.append("hd.fecha BETWEEN %s AND %s")
            parametros.append(fecha_inicio)
            parametros.append(fecha_fin)
        elif fecha_inicio: # Por si solo mandan una fecha fija
            condiciones.append("hd.fecha = %s")
            parametros.append(fecha_inicio)

        # 3. Armamos el SQL con la solución a prueba de balas para los tipos de dato (CAST)
        sql = f"""
            SELECT
                hd.id AS horario_disponible_id,
                CAST(hd.fecha AS CHAR) AS fecha,
                SUBSTRING(CAST(hd.hora_inicio AS CHAR), 1, 5) AS hora_inicio,
                SUBSTRING(CAST(hd.hora_fin AS CHAR), 1, 5) AS hora_fin,

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
        
        print('SQL EJECUTADO:', sql)
        print('PARAMETROS:', parametros)
        
        cursor.execute(sql, parametros)
        resultados = cursor.fetchall()
        cursor.close()
        con.close()
        return resultados