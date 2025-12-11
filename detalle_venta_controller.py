from database import crear_conexion

def ver_detalle_por_venta(venta_id):
    """
    Obtiene los productos específicos y calcula el subtotal al vuelo.
    :param venta_id: ID de la venta principal.
    :return: Lista de tuplas con (nombre, cantidad, precio_unitario, subtotal_calculado).
    """
    conexion = crear_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        
        # CONSULTA MODIFICADA: Cálculo del subtotal: (dv.cantidad * dv.precio_unitario) AS subtotal
        consulta = """
            SELECT 
                p.nombre AS nombre_producto, 
                dv.cantidad, 
                dv.precio_unitario, 
                (dv.cantidad * dv.precio_unitario) AS subtotal
            FROM detalle_venta dv
            JOIN productos p ON dv.id_producto = p.id_producto
            WHERE dv.id_venta = %s
        """
        cursor.execute(consulta, (venta_id,))
        return cursor.fetchall()
        
    except Exception as e:
        print(f"Error al obtener detalle de venta {venta_id}: {e}")
        return []
        
    finally:
        conexion.close()