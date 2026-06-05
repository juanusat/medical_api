from conexionBD import Conexion
import MySQLdb

class Especialidad:
    def consultarEspecialidades(self):
        #Abrir una conexion
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        #Definir la sentencia SQL
        sql = "SELECT id, nombre, descripcion FROM especialidad;"
        
        cursor.execute(sql)
        
        #Recuperar datos del usuario
        resultado = cursor.fetchall()
        
        cursor.close()
        con.close()
        
        return resultado

    def crear_especialidad(self, data):
        con = Conexion().open
        cursor = con.cursor()
        try:
            sql = "INSERT INTO especialidad (nombre, descripcion) VALUES (%s, %s)"
            cursor.execute(sql, [data['nombre'], data.get('descripcion')])
            especialidad_id = cursor.lastrowid
            con.commit()
            return {'especialidad_id': especialidad_id}
        except MySQLdb.IntegrityError:
            con.rollback()
            return None
        finally:
            cursor.close()
            con.close()

    def listar_especialidades(self):
        con = Conexion().open
        cursor = con.cursor()
        sql = "SELECT id, nombre, descripcion FROM especialidad ORDER BY id"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        con.close()
        return resultados

    def obtener_especialidad(self, especialidad_id):
        con = Conexion().open
        cursor = con.cursor()
        sql = "SELECT id, nombre, descripcion FROM especialidad WHERE id = %s LIMIT 1"
        cursor.execute(sql, [especialidad_id])
        resultado = cursor.fetchone()
        cursor.close()
        con.close()
        return resultado

    def actualizar_especialidad(self, especialidad_id, data):
        con = Conexion().open
        cursor = con.cursor()
        sql = "UPDATE especialidad SET nombre = %s, descripcion = %s WHERE id = %s"
        cursor.execute(sql, [data['nombre'], data.get('descripcion'), especialidad_id])
        con.commit()
        actualizado = cursor.rowcount > 0
        cursor.close()
        con.close()
        return actualizado

    def eliminar_especialidad(self, especialidad_id):
        con = Conexion().open
        cursor = con.cursor()
        sql = "DELETE FROM especialidad WHERE id = %s"
        cursor.execute(sql, [especialidad_id])
        con.commit()
        eliminado = cursor.rowcount > 0
        cursor.close()
        con.close()
        return eliminado
    
    def obtener_imagen(self, especialidad_id):
        #Abrir conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        #Definir la sentencia SQL
        sql = """
           select coalesce(imagen_url, 'x') as imagen_url from especialidad where id = %s
        """
        
        #Ejecutar la sentencia SQL
        cursor.execute(sql, [especialidad_id])
        
        #Recuperar los datos
        resultado = cursor.fetchone()
        
        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()
        
        #Verificar si se encontró la imagen
        if resultado and resultado['imagen_url'] != 'x':
            return resultado
        else: #No se encontró la imagen
            return None
    