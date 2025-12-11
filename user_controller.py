from database import crear_conexion

def obtener_id_por_nombre(username):
    """Obtiene el ID del usuario de la BD dado su nombre de usuario."""
    conexion = crear_conexion()
    if not conexion:
        return None
    try:
        cursor = conexion.cursor()
        consulta = "SELECT id FROM usuarios WHERE usuario = %s"
        cursor.execute(consulta, (username,))
        resultado = cursor.fetchone()
        
        if resultado:
            return resultado[0] 
        return None
    except Exception as e:
        print(f"Error al obtener ID de usuario: {e}")
        return None
    finally:
        conexion.close()

def ver_usuarios():
    conexion = crear_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        # DEBE USAR 'id' y 'usuario' (minúsculas) y 'usuarios' (tabla)
        cursor.execute("SELECT id, usuario FROM usuarios") 
        return cursor.fetchall()
    except Exception as e:
        # Revisa la consola por si aparece algún error nuevo aquí
        print("Error al ver usuarios:", e) 
        return []
    finally:
        conexion.close()

def agregar_usuarios(username, password):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (Usuario, Password) VALUES (%s, %s)",
            (username, password)
        )
        conexion.commit()
        return True
    except Exception as e:
        print("Error al agregar usuario:", e)
        return False
    finally:
        conexion.close()


def actualizar_usuarios(id_usuario, new_usuario, new_password):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        sql = "UPDATE usuarios SET Usuario = %s, Password = %s WHERE Id = %s"
        cursor.execute(sql, (new_usuario, new_password, id_usuario))
        conexion.commit()
        return True
    except Exception as e:
        print("Error al actualizar usuario:", e)
        return False
    finally:
        conexion.close()


def eliminar_usuarios(id_usuario):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        # Se corrige el nombre de la tabla a 'usuarios' y la columna a 'id' (minúsculas)
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return False
    finally:
        conexion.close()