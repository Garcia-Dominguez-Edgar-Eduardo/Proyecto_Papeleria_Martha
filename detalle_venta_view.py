import tkinter as tk
from tkinter import messagebox, ttk
from detalle_venta_controller import ver_detalle_por_venta 

class DetalleVentaApp:
    def __init__(self, id_venta, dashboard_root):
        self.id_venta = id_venta
        self.dashboard_root = dashboard_root 
        
        self.root = tk.Toplevel(self.dashboard_root)
        self.root.title(f"Detalle de Venta #{id_venta}")
        self.root.geometry("600x450")
        
        # 🟠 COLORES: Beige
        self.root.configure(bg="#F5F5DC")
        
        self.crear_elementos()
        self.cargar_detalle()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.root.mainloop() ELIMINADA (Para estabilidad)
        
    def on_closing(self):
        """Cierra la ventana actual y muestra el Dashboard."""
        self.root.destroy()
        self.dashboard_root.deiconify() 

    def crear_elementos(self):
        bg_main = "#F5F5DC"    # Beige
        btn_bg = "#A9A9A9"     # Gris oscuro (para regresar)

        tk.Label(self.root, text=f"Detalle de Venta ID: {self.id_venta}", font=("Arial", 18, "bold"), bg=bg_main).pack(pady=10)

        # --- Treeview ---
        self.tree = ttk.Treeview(self.root, columns=("Producto", "Cantidad", "Precio/U", "Subtotal"), show="headings", height=12)
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio/U", text="Precio Unitario")
        self.tree.heading("Subtotal", text="Subtotal")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        # --- Botón de Regresar ---
        tk.Button(self.root, text="Regresar", command=self.on_closing, width=15, bg=btn_bg, fg="white").pack(pady=20)

    def cargar_detalle(self):
        # 🟢 Llama a la función del controlador
        detalle = ver_detalle_por_venta(self.id_venta)
        
        total_venta = 0.0
        
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        for d in detalle:
            # d: (nombre_producto, cantidad, precio_unitario, subtotal_decimal)
            nombre, cantidad, precio, subtotal_decimal = d
            
            # 🟢 CORRECCIÓN: Conversión de decimal.Decimal a float para la suma
            subtotal = float(subtotal_decimal) 
            
            self.tree.insert("", tk.END, values=(nombre, cantidad, f"${precio:.2f}", f"${subtotal:.2f}"))
            
            # Suma de floats
            total_venta += subtotal
            
        # Mostrar el total al final
        tk.Label(self.root, text=f"Total de la Venta: ${total_venta:.2f}", font=("Arial", 14, "bold"), bg="#F5F5DC").pack(pady=5)