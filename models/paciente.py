from conexionBD import Conexion
import MySQLdb
from .auth import Auth

class Paciente:
    def crear_paciente(self, data):
        con = Conexion().open
        cursor = con.cursor()
        try:
            sql_usuario = """
                INSERT INTO usuario (email, password, rol_id, estado_usuario_id)
                VALUES (
                    %s,
                    %s,
                    (SELECT id FROM rol WHERE nombre = 'PACIENTE' LIMIT 1),
                    (SELECT id FROM estado_usuario WHERE nombre = 'ACTIVO' LIMIT 1)
                )
            """
            hashed = Auth()._hash_password(data['password'])
            cursor.execute(sql_usuario, [data['email'], hashed])
            usuario_id = cursor.lastrowid

            sql_paciente = """
                INSERT INTO paciente (usuario_id, nombres, apellidos, dni, celular, fecha_nacimiento, genero)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_paciente, [
                usuario_id,
                data['nombres'],
                data['apellidos'],
                data['dni'],
                data.get('celular'),
                data.get('fecha_nacimiento'),
                data.get('genero', 'Otro')
            ])
            paciente_id = cursor.lastrowid

            con.commit()
            return {'usuario_id': usuario_id, 'paciente_id': paciente_id, 'email': data['email']}
        except MySQLdb.IntegrityError:
            con.rollback()
            return None
        except Exception:
            con.rollback()
            raise
        finally:
            cursor.close()
            con.close()

    def listar_pacientes(self):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            SELECT
                p.id AS paciente_id,
                u.id AS usuario_id,
                u.email,
                p.nombres,
                p.apellidos,
                p.dni,
                p.celular
            FROM paciente p
            INNER JOIN usuario u ON p.usuario_id = u.id
            ORDER BY p.id
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        con.close()
        return resultados

    def obtener_paciente(self, paciente_id):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            SELECT
                p.id AS paciente_id,
                u.id AS usuario_id,
                u.email,
                p.nombres,
                p.apellidos,
                p.dni,
                p.celular,
                p.fecha_nacimiento,
                p.genero
            FROM paciente p
            INNER JOIN usuario u ON p.usuario_id = u.id
            WHERE p.id = %s
            LIMIT 1
        """
        cursor.execute(sql, [paciente_id])
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        return resultado

    def actualizar_paciente(self, paciente_id, data):
        con = Conexion().open
        cursor = con.cursor()

        sql = """
            UPDATE paciente
            SET nombres = %s,
                apellidos = %s,
                celular = %s,
                fecha_nacimiento = %s,
                genero = %s
            WHERE id = %s
        """
        cursor.execute(sql, [
            data['nombres'],
            data['apellidos'],
            data.get('celular'),
            data.get('fecha_nacimiento'),
            data.get('genero', 'Otro'),
            paciente_id
        ])
        con.commit()
        actualizado = cursor.rowcount > 0

        cursor.close()
        con.close()
        return actualizado

    def eliminar_paciente(self, paciente_id):
        con = Conexion().open
        cursor = con.cursor()
        try:
            cursor.execute("SELECT usuario_id FROM paciente WHERE id = %s", [paciente_id])
            fila = cursor.fetchone()
            if not fila:
                return False

            usuario_id = fila['usuario_id']
            cursor.execute("DELETE FROM cita WHERE paciente_id = %s", [paciente_id])
            cursor.execute("DELETE FROM paciente WHERE id = %s", [paciente_id])
            cursor.execute("DELETE FROM usuario WHERE id = %s", [usuario_id])
            con.commit()
            return True
        except Exception:
            con.rollback()
            raise
        finally:
            cursor.close()
            con.close()
