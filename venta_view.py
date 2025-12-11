import tkinter as tk
from tkinter import messagebox, ttk
from venta_controller import registrar_venta, ver_productos_disponibles, obtener_precio_producto

class VentaApp:
    def __init__(self, username, dashboard_root):
        self.username = username
        self.dashboard_root = dashboard_root
        
        self.root = tk.Toplevel(self.dashboard_root)
        self.root.title(f"Módulo de Venta - {username}")
        self.root.geometry("1460x700") 
        # 🟠 CAMBIO DE COLOR PRINCIPAL
        self.root.configure(bg="#F5F5DC") # Beige (Fondo)
        
        self.lista_venta = [] 
        
        self.crear_elementos()
        self.cargar_productos_disponibles()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.root.mainloop() ELIMINADA (Para estabilidad)
        
    def on_closing(self):
        self.root.destroy()
        self.dashboard_root.deiconify() 
        
    def crear_elementos(self):
        
        bg_main = "#F5F5DC"    # Beige
        bg_accent = "#FFDAB9"  # Naranja Claro (PeachPuff)

        tk.Label(self.root, text="Registrar Nueva Venta", font=("Arial", 24, "bold"), bg=bg_main).pack(pady=10)

        main_frame = tk.Frame(self.root, bg=bg_main)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # --- Panel Izquierdo: Inventario de Productos ---
        left_frame = tk.LabelFrame(main_frame, text="Inventario Disponible", bg=bg_accent, padx=5, pady=5) # 🟠 Color de acento
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.tree_inventario = ttk.Treeview(left_frame, columns=("ID", "Nombre", "Marca", "Precio", "Stock Actual"), show="headings", height=15)
        self.tree_inventario.heading("ID", text="ID")
        self.tree_inventario.heading("Nombre", text="Nombre")
        self.tree_inventario.heading("Marca", text="Marca")
        self.tree_inventario.heading("Precio", text="Precio Venta")
        self.tree_inventario.heading("Stock Actual", text="Stock Actual")
        self.tree_inventario.pack(fill="both", expand=True)

        # --- Entrada de Cantidad ---
        input_frame = tk.Frame(left_frame, bg=bg_accent) # 🟠 Color de acento
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Cantidad a Vender:", bg=bg_accent).pack(side="left", padx=5) # 🟠 Color de acento
        self.qty_entry = tk.Entry(input_frame, width=5)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side="left", padx=5)
        
        tk.Button(input_frame, text="Añadir a Venta", command=self.agregar_a_venta, bg="#FF8C00", fg="white").pack(side="left", padx=10) # Naranja Oscuro

        # --- Panel Derecho: Detalle de Venta y Total ---
        right_frame = tk.LabelFrame(main_frame, text="Detalle de la Venta", bg=bg_accent, padx=5, pady=5) # 🟠 Color de acento
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tree_detalle = ttk.Treeview(right_frame, columns=("ID", "Nombre", "Cant", "Precio/U", "Subtotal"), show="headings", height=15)
        self.tree_detalle.heading("ID", text="ID")
        self.tree_detalle.heading("Nombre", text="Nombre")
        self.tree_detalle.heading("Cant", text="Cant.")
        self.tree_detalle.heading("Precio/U", text="Precio/U")
        self.tree_detalle.heading("Subtotal", text="Subtotal")
        self.tree_detalle.pack(fill="both", expand=True)

        # --- Área de Totales y Botones Finales ---
        totals_frame = tk.Frame(right_frame, bg=bg_accent) # 🟠 Color de acento
        totals_frame.pack(fill='x', pady=10)

        tk.Label(totals_frame, text="TOTAL:", font=("Arial", 16, "bold"), bg=bg_accent).pack(side="left") # 🟠 Color de acento
        self.total_label = tk.Label(totals_frame, text="$ 0.00", font=("Arial", 16, "bold"), fg="#D2691E", bg=bg_accent) # 🟠 Color de acento
        self.total_label.pack(side="right")
        
        button_frame = tk.Frame(right_frame, bg=bg_accent) # 🟠 Color de acento
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Procesar Venta", command=self.procesar_venta, bg="#FF4500", fg="white").pack(side="left", padx=10) # Naranja Rojizo
        tk.Button(button_frame, text="Quitar Producto", command=self.quitar_de_venta).pack(side="left", padx=10)
        
        tk.Button(button_frame, text="Regresar", command=self.on_closing, bg="#A9A9A9", fg="white").pack(side="left", padx=10) # Gris oscuro
    
    # ... (El resto de métodos se mantienen iguales)
    def cargar_productos_disponibles(self):
        """Carga los productos disponibles para la venta."""
        for row in self.tree_inventario.get_children():
            self.tree_inventario.delete(row)
        
        productos = ver_productos_disponibles()
        for p in productos:
            # p: (id, nombre, marca, precio_venta, stock_actual)
            self.tree_inventario.insert("", tk.END, values=(p[0], p[1], p[2], f"${p[3]:.2f}", p[4]), tags=('producto',))

    def actualizar_detalle_y_total(self):
        """Refresca el Treeview del detalle de venta y recalcula el total."""
        for row in self.tree_detalle.get_children():
            self.tree_detalle.delete(row)
        
        total_acumulado = 0.0
        
        for item in self.lista_venta:
            # item: [id, nombre, cantidad, precio_unitario, subtotal, stock_actual]
            self.tree_detalle.insert("", tk.END, values=(item[0], item[1], item[2], f"${item[3]:.2f}", f"${item[4]:.2f}"))
            total_acumulado += item[4] 
            
        self.total_label.config(text=f"$ {total_acumulado:.2f}")

    def agregar_a_venta(self):
        """Añade un producto a la lista de venta con la cantidad especificada."""
        sel = self.tree_inventario.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un producto del inventario.")
            return
            
        producto_data = self.tree_inventario.item(sel, "values")
        
        try:
            cantidad = int(self.qty_entry.get().strip())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese una Cantidad válida (>0).")
            return
        
        producto_id = int(producto_data[0])
        nombre = producto_data[1]
        precio_unitario = float(producto_data[3].replace('$', ''))
        stock_actual = int(producto_data[4])
        
        if cantidad > stock_actual:
            messagebox.showerror("Stock Insuficiente", f"Solo quedan {stock_actual} unidades de {nombre}.")
            return
            
        subtotal = cantidad * precio_unitario
        
        encontrado = False
        for item in self.lista_venta:
            if item[0] == producto_id:
                nueva_cantidad = item[2] + cantidad
                
                if nueva_cantidad > stock_actual:
                    messagebox.showerror("Stock Insuficiente", f"La cantidad total ({nueva_cantidad}) excede el stock disponible ({stock_actual}).")
                    return
                
                item[2] = nueva_cantidad
                item[4] = item[2] * item[3]
                encontrado = True
                break
        
        if not encontrado:
            self.lista_venta.append([producto_id, nombre, cantidad, precio_unitario, subtotal, stock_actual])
            
        self.actualizar_detalle_y_total()
        
    def quitar_de_venta(self):
        """Quita el producto seleccionado de la lista de venta."""
        sel = self.tree_detalle.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un artículo en el detalle de venta para quitar.")
            return

        item_values = self.tree_detalle.item(sel, "values")
        producto_id_a_quitar = int(item_values[0])
        
        self.lista_venta = [item for item in self.lista_venta if item[0] != producto_id_a_quitar]

        self.actualizar_detalle_y_total()

    def procesar_venta(self):
        """Ejecuta la transacción final de registro de venta."""
        if not self.lista_venta:
            messagebox.showwarning("Venta Vacía", "La lista de venta está vacía. Agregue productos.")
            return

        total_str = self.total_label.cget('text').replace('$', '').strip()
        total_venta = float(total_str)
        
        if not messagebox.askyesno("Confirmar Venta", f"¿Desea registrar la venta por {self.total_label.cget('text')}? Esto disminuirá el stock de sus productos."):
            return

        productos_para_registro = [
            (item[0], item[2], item[3], item[4]) for item in self.lista_venta
        ]
        
        if registrar_venta(productos_para_registro, total_venta):
            messagebox.showinfo("Éxito", "¡Venta registrada correctamente!")
            
            self.lista_venta = []
            self.actualizar_detalle_y_total()
            self.cargar_productos_disponibles() 
        else:
            messagebox.showerror("Error de Venta", "No se pudo registrar la venta. (Consulte la consola por errores de BD)")