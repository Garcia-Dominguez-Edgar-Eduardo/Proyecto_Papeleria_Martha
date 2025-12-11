# compra_controller.py

from database import crear_conexion

# ---------------------------------------------------------------------

def registrar_compra(productos_comprados, total_compra):
    """
    Registra una nueva compra (entrada de inventario) en la tabla 'compras',
    el detalle en 'detalle_compra', y SUMA la cantidad comprada al stock en 'productos'.
    
    :param productos_comprados: Lista de tuplas: [(producto_id, cantidad, costo_unitario, subtotal), ...]
    :param total_compra: El costo total de la transacción de compra.
    :return: True si la transacción es exitosa, False en caso contrario.
    """
    conexion = crear_conexion()
    if not conexion:
        return False
        
    try:
        cursor = conexion.cursor()
        
        # 1. INSERTAR en la tabla COMPRAS
        consulta_compra = "INSERT INTO compras (total) VALUES (%s)"
        cursor.execute(consulta_compra, (total_compra,))
        
        compra_id = cursor.lastrowid 

        # 2. INSERTAR en la tabla DETALLE_COMPRA y ACTUALIZAR STOCK
        # IMPORTANTE: Asegúrate de que detalle_compra tenga las columnas: id_compra, id_producto, cantidad, costo_unitario, subtotal.
        consulta_detalle = "INSERT INTO detalle_compra (id_compra, id_producto, cantidad, costo_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)"
        
        # SUMAMOS al stock
        consulta_stock = "UPDATE productos SET stock = stock + %s WHERE id_producto = %s"
        
        detalles = []
        for producto_id, cantidad, costo_unitario, subtotal in productos_comprados:
            detalles.append((compra_id, producto_id, cantidad, costo_unitario, subtotal))
            
            # Ejecuta la actualización de stock (SUMA)
            cursor.execute(consulta_stock, (cantidad, producto_id))
            
        cursor.executemany(consulta_detalle, detalles)
        
        # 3. CONFIRMAR LA TRANSACCIÓN
        conexion.commit()
        return True
        
    except Exception as e:
        print(f"Error al registrar la compra (ROLLBACK): {e}")
        conexion.rollback()
        return False
        
    finally:
        if conexion:
            conexion.close()
            
# ---------------------------------------------------------------------

def ver_productos_todos():
    """Obtiene TODOS los productos, incluyendo stock 0, para el módulo de compras."""
    conexion = crear_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        # Se listan TODOS para que el usuario pueda comprar stock para cualquier producto.
        consulta = "SELECT id_producto, nombre, categoria, precio, stock FROM productos ORDER BY nombre"
        cursor.execute(consulta)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener productos para compra: {e}")
        return []
    finally:
        if conexion:
            conexion.close()