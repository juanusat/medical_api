from conexionBD import Conexion
import MySQLdb
from .auth import Auth

class Administrativo:
    def crear_administrativo(self, data):
        con = Conexion().open
        cursor = con.cursor()
        try:
            sql_usuario = """
                INSERT INTO usuario (email, password, rol_id, estado_usuario_id)
                VALUES (
                    %s,
                    %s,
                    (SELECT id FROM rol WHERE nombre = 'ADMINISTRATIVO' LIMIT 1),
                    (SELECT id FROM estado_usuario WHERE nombre = 'ACTIVO' LIMIT 1)
                )
            """
            hashed = Auth()._hash_password(data['password'])
            cursor.execute(sql_usuario, [data['email'], hashed])
            usuario_id = cursor.lastrowid

            sql_admin = """
                INSERT INTO administrativo (
                    usuario_id, nombres, apellidos, dni, celular, cargo, area
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_admin, [
                usuario_id,
                data['nombres'],
                data['apellidos'],
                data['dni'],
                data.get('celular'),
                data['cargo'],
                data.get('area')
            ])
            administrativo_id = cursor.lastrowid
            con.commit()
            return {'usuario_id': usuario_id, 'administrativo_id': administrativo_id}
        except MySQLdb.IntegrityError:
            con.rollback()
            return None
        except Exception:
            con.rollback()
            raise
        finally:
            cursor.close()
            con.close()

    def listar_administrativos(self):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            SELECT
                a.id AS administrativo_id,
                u.id AS usuario_id,
                u.email,
                a.nombres,
                a.apellidos,
                a.cargo,
                a.area
            FROM administrativo a
            INNER JOIN usuario u ON a.usuario_id = u.id
            ORDER BY a.id
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        con.close()
        return resultados

    def obtener_administrativo(self, administrativo_id):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            SELECT
                a.id AS administrativo_id,
                u.id AS usuario_id,
                u.email,
                a.nombres,
                a.apellidos,
                a.dni,
                a.celular,
                a.cargo,
                a.area
            FROM administrativo a
            INNER JOIN usuario u ON a.usuario_id = u.id
            WHERE a.id = %s
            LIMIT 1
        """
        cursor.execute(sql, [administrativo_id])
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        return resultado

    def actualizar_administrativo(self, administrativo_id, data):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            UPDATE administrativo
            SET celular = %s,
                cargo = %s,
                area = %s
            WHERE id = %s
        """
        cursor.execute(sql, [
            data.get('celular'),
            data.get('cargo'),
            data.get('area'),
            administrativo_id
        ])
        con.commit()
        actualizado = cursor.rowcount > 0
        cursor.close()
        con.close()
        return actualizado

    def eliminar_administrativo(self, administrativo_id):
        con = Conexion().open
        cursor = con.cursor()
        try:
            cursor.execute("SELECT usuario_id FROM administrativo WHERE id = %s", [administrativo_id])
            fila = cursor.fetchone()
            if not fila:
                return False

            usuario_id = fila['usuario_id']
            cursor.execute("DELETE FROM administrativo WHERE id = %s", [administrativo_id])
            cursor.execute("DELETE FROM usuario WHERE id = %s", [usuario_id])
            con.commit()
            return True
        except Exception:
            con.rollback()
            raise
        finally:
            cursor.close()
            con.close()
