import tkinter as tk
from tkinter import messagebox, ttk
from compra_controller import registrar_compra, ver_productos_todos 

class CompraApp:
    def __init__(self, username, dashboard_root):
        self.username = username
        self.dashboard_root = dashboard_root 
        
        self.root = tk.Toplevel(self.dashboard_root) 
        
        self.root.title(f"Módulo de Compra (Inventario) - {username}")
        self.root.geometry("1460x700") 
        # 🟠 CAMBIO DE COLOR PRINCIPAL
        self.root.configure(bg="#F5F5DC") # Beige
        
        self.lista_compra = [] 
        
        self.crear_elementos()
        self.cargar_productos_disponibles()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.root.mainloop() ELIMINADA (Para estabilidad)

    def on_closing(self):
        """Cierra la ventana actual y muestra el Dashboard."""
        self.root.destroy()
        self.dashboard_root.deiconify()

    def crear_elementos(self):
        bg_main = "#F5F5DC"    # Beige
        bg_accent = "#FFDAB9"  # Naranja Claro (PeachPuff)
        btn_primary = "#FF8C00" # Naranja oscuro
        btn_secondary = "#A9A9A9" # Gris

        tk.Label(self.root, text="Registrar Nueva Compra (Entrada de Inventario)", font=("Arial", 24, "bold"), bg=bg_main).pack(pady=10)

        main_frame = tk.Frame(self.root, bg=bg_main)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # --- Panel Izquierdo: Inventario de Productos ---
        left_frame = tk.LabelFrame(main_frame, text="Inventario de Productos", bg=bg_accent, padx=5, pady=5) # 🟠 Color de acento
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.tree_inventario = ttk.Treeview(left_frame, columns=("ID", "Nombre", "Precio Venta", "Stock Actual"), show="headings", height=15)
        self.tree_inventario.heading("ID", text="ID")
        self.tree_inventario.heading("Nombre", text="Nombre")
        self.tree_inventario.heading("Precio Venta", text="Precio Venta")
        self.tree_inventario.heading("Stock Actual", text="Stock Actual")
        self.tree_inventario.pack(fill="both", expand=True)

        # --- Entrada de Cantidad y Costo ---
        input_frame = tk.Frame(left_frame, bg=bg_accent) # 🟠 Color de acento
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Cantidad a Comprar:", bg=bg_accent).pack(side="left", padx=5) # 🟠 Color de acento
        self.qty_entry = tk.Entry(input_frame, width=5)
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side="left", padx=5)
        
        tk.Label(input_frame, text="Costo Unitario:", bg=bg_accent).pack(side="left", padx=5) # 🟠 Color de acento
        self.costo_entry = tk.Entry(input_frame, width=8)
        self.costo_entry.insert(0, "0.00")
        self.costo_entry.pack(side="left", padx=5)
        
        tk.Button(input_frame, text="Añadir a Compra", command=self.agregar_a_compra, bg=btn_primary, fg="white").pack(side="left", padx=10)

        # --- Panel Derecho: Detalle de Compra y Total ---
        right_frame = tk.LabelFrame(main_frame, text="Detalle de la Compra", bg=bg_accent, padx=5, pady=5) # 🟠 Color de acento
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tree_detalle = ttk.Treeview(right_frame, columns=("ID", "Nombre", "Cant", "Costo/U", "Subtotal"), show="headings", height=15)
        self.tree_detalle.heading("ID", text="ID")
        self.tree_detalle.heading("Nombre", text="Nombre")
        self.tree_detalle.heading("Cant", text="Cant.")
        self.tree_detalle.heading("Costo/U", text="Costo/U")
        self.tree_detalle.heading("Subtotal", text="Subtotal")
        self.tree_detalle.pack(fill="both", expand=True)

        # --- Área de Totales y Botones Finales ---
        totals_frame = tk.Frame(right_frame, bg=bg_accent) # 🟠 Color de acento
        totals_frame.pack(fill='x', pady=10)

        tk.Label(totals_frame, text="TOTAL:", font=("Arial", 16, "bold"), bg=bg_accent).pack(side="left") # 🟠 Color de acento
        self.total_label = tk.Label(totals_frame, text="$ 0.00", font=("Arial", 16, "bold"), fg="#D2691E", bg=bg_accent)
        self.total_label.pack(side="right")
        
        button_frame = tk.Frame(right_frame, bg=bg_accent) # 🟠 Color de acento
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Registrar Compra", command=self.procesar_compra, bg="#FF4500", fg="white").pack(side="left", padx=10)
        tk.Button(button_frame, text="Quitar de Compra", command=self.quitar_de_compra).pack(side="left", padx=10)
        
        tk.Button(button_frame, text="Regresar", command=self.on_closing, bg=btn_secondary, fg="white").pack(side="left", padx=10)

    # ... (El resto de métodos se mantienen iguales)
    def cargar_productos_disponibles(self):
        """Carga TODOS los productos para el módulo de compras."""
        for row in self.tree_inventario.get_children():
            self.tree_inventario.delete(row)
        
        # Asumo que la función ver_productos_todos() está en compra_controller
        productos = ver_productos_todos() 
        for p in productos:
            # p: (id, nombre, categoria, precio_venta, stock_actual)
            self.tree_inventario.insert("", tk.END, values=(p[0], p[1], f"${p[3]:.2f}", p[4]), tags=('producto',))

    def actualizar_detalle_y_total(self):
        """Refresca el Treeview del detalle de compra y recalcula el total."""
        for row in self.tree_detalle.get_children():
            self.tree_detalle.delete(row)
        
        total_acumulado = 0.0
        
        for item in self.lista_compra:
            # item: [id, nombre, cantidad, costo_unitario, subtotal, stock_actual]
            self.tree_detalle.insert("", tk.END, values=(item[0], item[1], item[2], f"${item[3]:.2f}", f"${item[4]:.2f}"))
            total_acumulado += item[4] 
            
        self.total_label.config(text=f"$ {total_acumulado:.2f}")

    def agregar_a_compra(self):
        """Añade un producto a la lista de compra con la cantidad y costo especificados."""
        sel = self.tree_inventario.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un producto del inventario.")
            return
            
        producto_data = self.tree_inventario.item(sel, "values")
        
        try:
            cantidad = int(self.qty_entry.get().strip())
            costo_unitario = float(self.costo_entry.get().strip())
            
            if cantidad <= 0 or costo_unitario < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese una Cantidad válida (>0) y un Costo Unitario válido (>=0).")
            return
            
        producto_id, nombre, _, stock_actual = producto_data
        producto_id = int(producto_id)
        
        subtotal = cantidad * costo_unitario
        
        # Verificar si el producto ya está en la lista (para consolidar)
        for item in self.lista_compra:
            if item[0] == producto_id:
                # Sumamos la cantidad nueva a la ya existente.
                item[2] = item[2] + cantidad
                # El costo unitario se actualiza al último valor ingresado 
                item[3] = costo_unitario 
                item[4] = item[2] * item[3]
                self.actualizar_detalle_y_total()
                return

        # Si no está en la lista, agregarlo como un nuevo item
        stock_actual_int = int(stock_actual) 
        self.lista_compra.append([producto_id, nombre, cantidad, costo_unitario, subtotal, stock_actual_int])
        self.actualizar_detalle_y_total()
        
    def quitar_de_compra(self):
        """Quita el producto seleccionado de la lista de compra."""
        sel = self.tree_detalle.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un artículo en el detalle de compra para quitar.")
            return

        item_values = self.tree_detalle.item(sel, "values")
        producto_id_a_quitar = int(item_values[0])
        self.lista_compra = [item for item in self.lista_compra if item[0] != producto_id_a_quitar]

        self.actualizar_detalle_y_total()


    def procesar_compra(self):
        """Ejecuta la transacción final de registro de compra (entrada de inventario)."""
        if not self.lista_compra:
            messagebox.showwarning("Compra Vacía", "La lista de compra está vacía. Agregue productos.")
            return

        if not messagebox.askyesno("Confirmar Compra", f"¿Desea registrar la compra por {self.total_label.cget('text')}? Esto aumentará el stock de sus productos."):
            return

        # Prepara los datos para el controlador: (producto_id, cantidad, costo_unitario, subtotal)
        productos_para_registro = [
            (item[0], item[2], item[3], item[4]) for item in self.lista_compra
        ]
        
        total_str = self.total_label.cget('text').replace('$', '').strip()
        costo_total = float(total_str)

        # Llama al controlador para registrar la compra
        if registrar_compra(productos_para_registro, costo_total):
            messagebox.showinfo("Éxito", "¡Compra (Entrada de Inventario) registrada correctamente!")
            
            # Limpia y reinicia la vista
            self.lista_compra = []
            self.actualizar_detalle_y_total()
            self.cargar_productos_disponibles() # Recarga para mostrar el nuevo stock
        else:
            messagebox.showerror("Error de Compra", "No se pudo registrar la compra. (Consulte la consola por errores de BD)")