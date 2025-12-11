# venta_controller.py

from database import crear_conexion

# ---------------------------------------------------------------------

def registrar_venta(productos_vendidos, total):
    """
    Registra una nueva venta, sin registrar el ID del usuario.
    Requiere que la tabla 'detalle_venta' tenga la columna 'subtotal'.
    """
    conexion = crear_conexion()
    if not conexion:
        return False
        
    try:
        cursor = conexion.cursor()
        
        # 1. INSERTAR en la tabla VENTAS (Solo insertamos 'total')
        consulta_venta = "INSERT INTO ventas (total) VALUES (%s)"
        cursor.execute(consulta_venta, (total,))
        
        venta_id = cursor.lastrowid 

        # 2. INSERTAR en la tabla DETALLE_VENTA y ACTUALIZAR STOCK
        consulta_detalle = "INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)"
        # ⚠️ CORRECCIÓN AQUÍ: Usamos 'stock' según tu esquema (image_910de3.png)
        consulta_stock = "UPDATE productos SET stock = stock - %s WHERE id_producto = %s"
        
        detalles = []
        for producto_id, cantidad, precio_unitario, subtotal in productos_vendidos:
            detalles.append((venta_id, producto_id, cantidad, precio_unitario, subtotal))
            
            cursor.execute(consulta_stock, (cantidad, producto_id))
            
        cursor.executemany(consulta_detalle, detalles)
        
        # 3. CONFIRMAR LA TRANSACCIÓN
        conexion.commit()
        return True
        
    except Exception as e:
        print(f"Error al registrar la venta (ROLLBACK): {e}")
        conexion.rollback()
        return False
        
    finally:
        if conexion:
            conexion.close()

# ---------------------------------------------------------------------

def ver_ventas_historial():
    """Ver todas las ventas (para historial)."""
    conexion = crear_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        consulta = "SELECT id_venta, fecha, total FROM ventas ORDER BY fecha DESC"
        cursor.execute(consulta)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener ventas: {e}")
        return []
    finally:
        if conexion:
            conexion.close()
            
# ---------------------------------------------------------------------

def ver_productos_disponibles():
    """Obtiene los productos con stock > 0 para la vista de ventas, usando ALIAS para coincidir con la vista de Python."""
    conexion = crear_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        # 🟢 FUNCIÓN CORREGIDA 🟢
        consulta = """
            SELECT 
                id_producto, 
                nombre, 
                categoria AS marca, 
                precio AS precio_venta, 
                stock AS stock_actual
            FROM 
                productos 
            WHERE 
                stock > 0 
            ORDER BY 
                nombre
        """
        cursor.execute(consulta)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener productos disponibles para venta: {e}")
        return []
    finally:
        if conexion:
            conexion.close()
            
# ---------------------------------------------------------------------

def obtener_precio_producto(producto_id):
    """Obtiene el precio de venta de un producto por su ID."""
    conexion = crear_conexion()
    if not conexion:
        return None
    try:
        cursor = conexion.cursor()
        # ⚠️ CORRECCIÓN AQUÍ: Usamos 'precio' según tu esquema
        consulta = "SELECT precio FROM productos WHERE id_producto = %s"
        cursor.execute(consulta, (producto_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"Error al obtener precio: {e}")
        return None
    finally:
        if conexion:
            conexion.close()