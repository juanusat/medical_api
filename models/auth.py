from conexionBD import Conexion
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class Auth:
    def __init__(self):
        self.ph = PasswordHasher()

    def _verificar_password(self, hash_o_clave, clave_plana):
        try:
            return self.ph.verify(hash_o_clave, clave_plana)
        except VerifyMismatchError:
            return False
        except Exception:
            return hash_o_clave == clave_plana

    def _hash_password(self, clave_plana):
        return self.ph.hash(clave_plana)

    def login(self, email, clave):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
           SELECT 
                u.id AS usuario_id,
                u.email,
                r.nombre AS rol,
                eu.nombre AS estado_usuario,
                CONCAT( COALESCE(p.nombres, m.nombres, a.nombres), ' ', COALESCE(p.apellidos, m.apellidos, a.apellidos) ) AS nombre,
                u.password AS clave
            FROM usuario u
            INNER JOIN rol r 
                ON u.rol_id = r.id
            INNER JOIN estado_usuario eu 
                ON u.estado_usuario_id = eu.id
            LEFT JOIN paciente p 
                ON u.id = p.usuario_id
            LEFT JOIN medico m 
                ON u.id = m.usuario_id
            LEFT JOIN administrativo a 
                ON u.id = a.usuario_id
            WHERE u.email = %s
        """
        cursor.execute(sql, [email])
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        if resultado:
            if self._verificar_password(resultado['clave'], clave):
                return resultado
            else:
                return None
        else:
            return None

    def obtener_foto(self, usuario_id):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
           select coalesce(foto, 'x') as foto from usuario where id = %s
        """
        cursor.execute(sql, [usuario_id])
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        if resultado and resultado['foto'] != 'x':
            return resultado
        else:
            return None

    def obtener_perfil(self, usuario_id):
        con = Conexion().open
        cursor = con.cursor()
        sql = """
            SELECT
                u.id AS usuario_id,
                u.email,
                r.nombre AS rol,
                COALESCE(p.nombres, m.nombres, a.nombres) AS nombres,
                COALESCE(p.apellidos, m.apellidos, a.apellidos) AS apellidos
            FROM usuario u
            INNER JOIN rol r ON u.rol_id = r.id
            LEFT JOIN paciente p ON p.usuario_id = u.id
            LEFT JOIN medico m ON m.usuario_id = u.id
            LEFT JOIN administrativo a ON a.usuario_id = u.id
            WHERE u.id = %s
            LIMIT 1
        """
        cursor.execute(sql, [usuario_id])
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        return resultado

    def actualizar_foto(self, usuario_id, foto):
        con = Conexion().open
        cursor = con.cursor()
        sql = "UPDATE usuario SET foto = %s , fecha_hora_actualizacion =now() WHERE id = %s"
        cursor.execute(sql, [foto, usuario_id])
        con.commit()
        actualizado = cursor.rowcount > 0
        cursor.close()
        con.close()
        return actualizado

    def cambiar_password(self, usuario_id, password_actual, password_nueva):
        con = Conexion().open
        cursor = con.cursor()
        cursor.execute("SELECT password FROM usuario WHERE id = %s", [usuario_id])
        fila = cursor.fetchone()
        if not fila:
            cursor.close()
            con.close()
            return 'NO_EXISTE'

        if not self._verificar_password(fila['password'], password_actual):
            cursor.close()
            con.close()
            return 'PASSWORD_ACTUAL_INVALIDA'

        nueva_hash = self._hash_password(password_nueva)
        cursor.execute("UPDATE usuario SET password = %s WHERE id = %s", [nueva_hash, usuario_id])
        con.commit()
        cursor.close()
        con.close()
        return 'OK'

    def registrar_token_dispositivo(self, usuario_id, dispositivo, token):
        con = Conexion().open
        cursor = con.cursor()

        try:
            sql_verificar = """
                SELECT COUNT(*) as cantidad FROM usuario_fcm
                WHERE usuario_id = %s AND dispositivo = %s AND token = %s
            """
            cursor.execute(sql_verificar, [usuario_id, dispositivo, token])
            existe = cursor.fetchone()['cantidad']

            if existe == 0:
                sql_inhabilitar_token_antiguos = """
                    UPDATE usuario_fcm SET estado_id = 2
                    WHERE usuario_id = %s AND dispositivo = %s AND estado_id = 1
                """
                cursor.execute(sql_inhabilitar_token_antiguos, [usuario_id, dispositivo])

                sql_nuevo_token = """
                    INSERT INTO usuario_fcm (usuario_id, dispositivo, token, estado_id)
                    VALUES (%s, %s, %s, 1)
                """
                cursor.execute(sql_nuevo_token, [usuario_id, dispositivo, token])

                con.commit()
                return True, 'ok'
            else:
                return False, 'El token ya esta registrado para el dispositivo'

        except Exception as e:
            con.rollback()
            return False, str(e)
        finally:
            cursor.close()
            con.close()
