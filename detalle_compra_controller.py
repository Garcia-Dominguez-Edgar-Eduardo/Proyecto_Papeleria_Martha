# detalle_compra_controller.py

from database import crear_conexion

# ---------------------------------------------------------------------

def ver_historial_compras():
    """Obtiene una lista de todas las compras realizadas para mostrar en el historial."""
    conexion = crear_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        # Consulta para ver el resumen de cada compra: ID, Fecha, Total
        consulta = "SELECT id_compra, fecha, total FROM compras ORDER BY fecha DESC"
        cursor.execute(consulta)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener historial de compras: {e}")
        return []
    finally:
        if conexion:
            conexion.close()

# ---------------------------------------------------------------------

def ver_detalle_compra(id_compra):
    """
    Obtiene el detalle de los productos incluidos en una compra específica (su contenido), 
    uniendo las tablas detalle_compra y productos.
    """
    conexion = crear_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        # Selecciona el nombre del producto, cantidad, costo unitario y subtotal
        consulta = """
        SELECT 
            p.nombre, 
            dc.cantidad, 
            dc.costo_unitario, 
            dc.subtotal
        FROM detalle_compra dc
        JOIN productos p ON dc.id_producto = p.id_producto
        WHERE dc.id_compra = %s
        """
        cursor.execute(consulta, (id_compra,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener detalle de compra {id_compra}: {e}")
        return []
    finally:
        if conexion:
            conexion.close()