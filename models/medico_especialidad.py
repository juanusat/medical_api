from conexionBD import Conexion
import MySQLdb

class MedicoEspecialidad:
    def crear_medico_especialidad(self, data):
        con = Conexion().open
        cursor = con.cursor()
        try:
            sql = "INSERT INTO medico_especialidad (medico_id, especialidad_id) VALUES (%s, %s)"
            cursor.execute(sql, [data['medico_id'], data['especialidad_id']])
            relacion_id = cursor.lastrowid
            con.commit()
            return {'medico_especialidad_id': relacion_id}
        except MySQLdb.IntegrityError:
            con.rollback()
            return None
        finally:
            cursor.close()
            con.close()

    def listar_medico_especialidades(self):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            SELECT
                me.id,
                m.id AS medico_id,
                CONCAT(m.nombres, ' ', m.apellidos) AS medico,
                e.id AS especialidad_id,
                e.nombre AS especialidad
            FROM medico_especialidad me
            INNER JOIN medico m ON me.medico_id = m.id
            INNER JOIN especialidad e ON me.especialidad_id = e.id
            ORDER BY me.id
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        con.close()
        return resultados

    def obtener_medico_especialidad(self, relacion_id):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            SELECT
                me.id,
                m.id AS medico_id,
                CONCAT(m.nombres, ' ', m.apellidos) AS medico,
                e.id AS especialidad_id,
                e.nombre AS especialidad
            FROM medico_especialidad me
            INNER JOIN medico m ON me.medico_id = m.id
            INNER JOIN especialidad e ON me.especialidad_id = e.id
            WHERE me.id = %s
            LIMIT 1
        """
        cursor.execute(sql, [relacion_id])
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        return resultado

    def actualizar_medico_especialidad(self, relacion_id, data):
        con = Conexion().open
        cursor = con.cursor()
        try:
            sql = """
                UPDATE medico_especialidad
                SET medico_id = %s,
                    especialidad_id = %s
                WHERE id = %s
            """
            cursor.execute(sql, [data['medico_id'], data['especialidad_id'], relacion_id])
            con.commit()
            return cursor.rowcount > 0
        except MySQLdb.IntegrityError:
            con.rollback()
            return None
        finally:
            cursor.close()
            con.close()

    def eliminar_medico_especialidad(self, relacion_id):
        con = Conexion().open
        cursor = con.cursor()
        sql = "DELETE FROM medico_especialidad WHERE id = %s"
        cursor.execute(sql, [relacion_id])
        con.commit()
        eliminado = cursor.rowcount > 0
        cursor.close()
        con.close()
        return eliminado
