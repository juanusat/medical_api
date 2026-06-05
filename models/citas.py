from conexionBD import Conexion

class Cita:
    #PUNTO H.1(REVISAR EXAMEN)
    def registrar(self, paciente_id, paciente_oncologico, creado_por_usuario_id, citas):
        #Abrir conexión
        con = Conexion().open
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()

        try:
            #===============================
            #1. Validar la existencia del paciente
            #===============================
            sql_validar_paciente = """
                SELECT id FROM paciente WHERE id = %s
            """
            cursor.execute(sql_validar_paciente, [paciente_id])
            paciente = cursor.fetchone()
            if not paciente:
                return False, "El paciente no existe"
            #===============================
            #2. Validar que los horarios seleccionados
            #Aún sigan disponibles
            #===============================
            sql_validar_horarios = """
                Select id, estado_horario_disponible_id from horario_disponible where id = %s 
            """
            for cita in citas:
                horario_disponible_id = cita.get("horario_disponible_id")
                cursor.execute(sql_validar_horarios, [horario_disponible_id])
                horario = cursor.fetchone()
                if horario['estado_horario_disponible_id'] != 1:
                    return False, f"El horario con ID {horario_disponible_id} ya no está disponible"
            #===============================
            #3. Registrar las citas y 
            # actualizar el estado de los horarios
            #===============================
            sql_insertar_cita = """
                INSERT INTO cita (
                paciente_id, 
                horario_disponible_id, 
                motivo, 
                paciente_oncologico, 
                estado_cita_id, 
                creado_por_usuario_id
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            sql_actualizar_horario = """
                UPDATE horario_disponible SET estado_horario_disponible_id = 2 WHERE id = %s
            """

            #Almacenar en una variable Array las citas registradas
            citas_registradas = []
            for cita in citas:
                horario_disponible_id = cita.get("horario_disponible_id")
                motivo = cita.get("motivo", "")
                #Insertar en la tabla de citas
                cursor.execute(sql_insertar_cita, [paciente_id, horario_disponible_id, motivo, paciente_oncologico, 1, creado_por_usuario_id])
                
                #Obtener el ID de la cita recién insertada
                cita_id = cursor.lastrowid

                #Actualizar el estado del horario
                cursor.execute(sql_actualizar_horario, [horario_disponible_id])
                #Almacenar la cita registrada en el array
                citas_registradas.append(
                    {
                        "cita_id": cita_id,
                        "horario_disponible_id": horario_disponible_id,
                        "estado_cita_id": "PENDIENTE",
                        "motivo": motivo
                    }
                )
            #Si TODAS las operaciones anteriores se ejecutaron correctamente, entonces confirmamos la transacción
            con.commit()
            return True, citas_registradas








        except Exception as e:
            con.rollback()
            return False, str(e)
        finally:
            con.close()