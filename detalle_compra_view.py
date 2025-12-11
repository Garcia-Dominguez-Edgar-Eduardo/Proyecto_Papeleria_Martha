import tkinter as tk
from tkinter import messagebox, ttk
from detalle_compra_controller import ver_historial_compras, ver_detalle_compra

class DetalleCompraApp:
    def __init__(self, username, dashboard_root):
        self.username = username
        self.dashboard_root = dashboard_root 
        
        self.root = tk.Toplevel(self.dashboard_root) 
        self.root.title(f"Historial de Compras - {username}")
        self.root.geometry("800x600")
        
        # 🟠 CAMBIO DE COLOR PRINCIPAL
        self.root.configure(bg="#F5F5DC") # Beige
        
        self.crear_elementos()
        self.cargar_historial_compras()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.root.mainloop() ELIMINADA (Para estabilidad)

    def on_closing(self):
        """Cierra la ventana actual y muestra el Dashboard."""
        self.root.destroy()
        self.dashboard_root.deiconify()

    def crear_elementos(self):
        bg_main = "#F5F5DC"    # Beige
        bg_accent = "#FFDAB9"  # Naranja Claro (PeachPuff)
        btn_bg = "#FF8C00"     # Naranja Oscuro

        tk.Label(self.root, text="Historial de Compras (Entrada de Inventario)", font=("Arial", 20, "bold"), bg=bg_main).pack(pady=20)

        # --- Treeview de Historial ---
        self.tree_historial = ttk.Treeview(self.root, columns=("ID", "Fecha", "Total"), show="headings", height=10)
        self.tree_historial.heading("ID", text="ID Compra")
        self.tree_historial.heading("Fecha", text="Fecha")
        self.tree_historial.heading("Total", text="Costo Total")
        self.tree_historial.pack(fill="x", padx=20, pady=10)
        self.tree_historial.bind("<<TreeviewSelect>>", self.mostrar_detalle)
        
        # --- Treeview de Detalle ---
        tk.Label(self.root, text="Detalle de Productos Comprados:", font=("Arial", 14), bg=bg_main).pack(pady=10) # 🟠 Beige
        self.tree_detalle = ttk.Treeview(self.root, columns=("Producto", "Cantidad", "Costo/U", "Subtotal"), show="headings", height=8)
        self.tree_detalle.heading("Producto", text="Producto")
        self.tree_detalle.heading("Cantidad", text="Cantidad")
        self.tree_detalle.heading("Costo/U", text="Costo Unitario")
        self.tree_detalle.heading("Subtotal", text="Subtotal")
        self.tree_detalle.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Botón de Regresar ---
        tk.Button(self.root, text="Regresar", command=self.on_closing, width=15, bg="#A9A9A9", fg="white").pack(pady=20)

    # ... (El resto de métodos se mantienen iguales)
    def cargar_historial_compras(self):
        for row in self.tree_historial.get_children():
            self.tree_historial.delete(row)
        
        compras = ver_historial_compras()
        for c in compras:
            # c: (id_compra, fecha, total)
            self.tree_historial.insert("", tk.END, values=(c[0], c[1], f"${c[2]:.2f}"))

    def mostrar_detalle(self, event):
        sel = self.tree_historial.focus()
        if not sel:
            return

        id_compra = self.tree_historial.item(sel, "values")[0]
        
        # Limpiar detalle anterior
        for row in self.tree_detalle.get_children():
            self.tree_detalle.delete(row)
            
        detalle = ver_detalle_compra(id_compra)
        
        for d in detalle:
            # d: (nombre, cantidad, costo_unitario, subtotal)
            nombre, cantidad, costo, subtotal = d
            self.tree_detalle.insert("", tk.END, values=(nombre, cantidad, f"${costo:.2f}", f"${subtotal:.2f}"))