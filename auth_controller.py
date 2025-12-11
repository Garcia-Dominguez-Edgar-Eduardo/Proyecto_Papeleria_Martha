#Controlador responsable de la logica de autenticacion
#Separa la logica del login para mantener limpio el codigo de la interfaz

from database import crear_conexion

def validar_credenciales(usuario, password):
    conexion = crear_conexion()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        consulta = "SELECT * FROM usuarios WHERE usuario = %s AND password = %s"
        cursor.execute(consulta, (usuario, password))
        result = cursor.fetchone()
        return bool(result)
    except Exception as e:
        print(f"Error en la autenticación: {e}")
        return False
    finally:
        conexion.close()
