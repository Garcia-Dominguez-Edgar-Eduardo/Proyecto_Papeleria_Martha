from database import crear_conexion

#ver productos
def ver_productos():
    conexion = crear_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_producto, nombre, categoria, precio, stock FROM productos")
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []
    finally:
        conexion.close()


#agregar productos
def agregar_producto(nombre, categoria, precio, stock):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        # 🟢 CORRECCIÓN: Se usan las variables 'nombre' y 'categoria' que son los argumentos de la función.
        cursor.execute("INSERT INTO productos (nombre, categoria, precio, stock) VALUES (%s, %s, %s, %s)", (nombre, categoria, precio, stock))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al agregar producto: {e}")
        return False
    finally:
        conexion.close()


#actualizar productos
def actualizar_producto(id_producto, nombre, categoria, precio, stock):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE productos SET nombre=%s, categoria=%s, precio=%s, stock=%s WHERE id_producto=%s", (nombre, categoria, precio, stock, id_producto))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar producto: {e}")
        return False
    finally:
        conexion.close()


#eliminar productos
def eliminar_producto(id_producto):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id_producto,))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        return False
    finally:
        conexion.close()