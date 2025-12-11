import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",        # <- usa luismgt si ese es el usuario que quieres usar
            password="",
            database="papeleria_martha"
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
