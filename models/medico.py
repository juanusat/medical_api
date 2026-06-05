from conexionBD import Conexion
import MySQLdb
from .auth import Auth

class Medico:
    def crear_medico(self, data):
        con = Conexion().open
        cursor = con.cursor()
        try:
            sql_usuario = """
                INSERT INTO usuario (email, password, rol_id, estado_usuario_id)
                VALUES (
                    %s,
                    %s,
                    (SELECT id FROM rol WHERE nombre = 'MEDICO' LIMIT 1),
                    (SELECT id FROM estado_usuario WHERE nombre = 'ACTIVO' LIMIT 1)
                )
            """
            hashed = Auth()._hash_password(data['password'])
            cursor.execute(sql_usuario, [data['email'], hashed])
            usuario_id = cursor.lastrowid

            sql_medico = """
                INSERT INTO medico (
                    usuario_id, nombres, apellidos, dni, cmp, telefono, consultorio, estado_medico_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_medico, [
                usuario_id,
                data['nombres'],
                data['apellidos'],
                data['dni'],
                data['cmp'],
                data.get('telefono'),
                data.get('consultorio'),
                data['estado_medico_id']
            ])
            medico_id = cursor.lastrowid
            con.commit()
            return {'usuario_id': usuario_id, 'medico_id': medico_id, 'email': data['email']}
        except MySQLdb.IntegrityError:
            con.rollback()
            return None
        except Exception:
            con.rollback()
            raise
        finally:
            cursor.close()
            con.close()

    def listar_medicos(self):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            SELECT
                m.id AS medico_id,
                u.id AS usuario_id,
                u.email,
                m.nombres,
                m.apellidos,
                m.cmp,
                m.consultorio
            FROM medico m
            INNER JOIN usuario u ON m.usuario_id = u.id
            ORDER BY m.id
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        con.close()
        return resultados

    def obtener_medico(self, medico_id):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            SELECT
                m.id AS medico_id,
                u.id AS usuario_id,
                u.email,
                m.nombres,
                m.apellidos,
                m.dni,
                m.cmp,
                m.telefono,
                m.consultorio,
                em.nombre AS estado_medico
            FROM medico m
            INNER JOIN usuario u ON m.usuario_id = u.id
            INNER JOIN estado_medico em ON m.estado_medico_id = em.id
            WHERE m.id = %s
            LIMIT 1
        """
        cursor.execute(sql, [medico_id])
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        return resultado

    def actualizar_medico(self, medico_id, data):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            UPDATE medico
            SET telefono = %s,
                consultorio = %s,
                estado_medico_id = %s
            WHERE id = %s
        """
        cursor.execute(sql, [
            data.get('telefono'),
            data.get('consultorio'),
            data['estado_medico_id'],
            medico_id
        ])
        con.commit()
        actualizado = cursor.rowcount > 0
        cursor.close()
        con.close()
        return actualizado

    def eliminar_medico(self, medico_id):
        con = Conexion().open
        cursor = con.cursor()
        try:
            cursor.execute("SELECT usuario_id FROM medico WHERE id = %s", [medico_id])
            fila = cursor.fetchone()
            if not fila:
                return False

            usuario_id = fila['usuario_id']
            cursor.execute("DELETE FROM cita WHERE horario_disponible_id IN (SELECT id FROM horario_disponible WHERE medico_id = %s)", [medico_id])
            cursor.execute("DELETE FROM horario_disponible WHERE medico_id = %s", [medico_id])
            cursor.execute("DELETE FROM medico_especialidad WHERE medico_id = %s", [medico_id])
            cursor.execute("DELETE FROM medico WHERE id = %s", [medico_id])
            cursor.execute("DELETE FROM usuario WHERE id = %s", [usuario_id])
            con.commit()
            return True
        except Exception:
            con.rollback()
            raise
        finally:
            cursor.close()
            con.close()

    def listar_medicos_por_especialidad(self, especialidad_id):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            SELECT
                m.id AS medico_id,
                CONCAT(m.nombres, ' ', m.apellidos) AS medico,
                m.cmp,
                m.consultorio,
                e.id AS especialidad_id,
                e.nombre AS especialidad
            FROM medico_especialidad me
            INNER JOIN medico m ON me.medico_id = m.id
            INNER JOIN especialidad e ON me.especialidad_id = e.id
            WHERE e.id = %s
            ORDER BY m.id
        """
        cursor.execute(sql, [especialidad_id])
        resultados = cursor.fetchall()
        cursor.close()
        con.close()
        return resultados

    def obtener_imagen(self, medico_id):
            #Abrir conexión
            con = Conexion().open
            
            #Crear un cursor para ejecutar una sentencia SQL
            cursor = con.cursor()
            
            #Definir la sentencia SQL
            sql = """
            select coalesce(imagen_url, 'x') as imagen_url from medico where id = %s
            """
            
            #Ejecutar la sentencia SQL
            cursor.execute(sql, [medico_id])
            
            #Recuperar los datos
            resultado = cursor.fetchone()
            
            #Cerrar el cursor y la conexión
            cursor.close()
            con.close()
            
            print(resultado)
            #Verificar si se encontró la imagen¬
            if resultado and resultado['imagen_url'] != 'x':
                return resultado
            else: #No se encontró la imagen
                return None
        