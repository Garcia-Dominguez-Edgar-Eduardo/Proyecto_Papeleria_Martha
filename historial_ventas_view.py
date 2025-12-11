import tkinter as tk
from tkinter import messagebox, ttk
from detalle_venta_view import DetalleVentaApp
from venta_controller import ver_ventas_historial # Asumo que esta función existe

class HistorialVentasApp:
    def __init__(self, username, dashboard_root):
        self.username = username
        self.dashboard_root = dashboard_root
        
        # Usar Toplevel para la ventana secundaria
        self.root = tk.Toplevel(self.dashboard_root) 
        self.root.title(f"Historial de Ventas - {username}")
        self.root.geometry("800x600")
        
        # 🟠 CAMBIO DE COLOR PRINCIPAL
        self.root.configure(bg="#F5F5DC") # Beige
        
        self.crear_elementos()
        self.cargar_historial_ventas()
        
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

        tk.Label(self.root, text="Historial de Ventas", font=("Arial", 20, "bold"), bg=bg_main).pack(pady=20)

        # --- Treeview ---
        self.tree = ttk.Treeview(self.root, columns=("ID", "Fecha", "Total"), show="headings", height=15)
        self.tree.heading("ID", text="ID Venta")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Total", text="Total")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Asignar doble clic para ver detalle
        self.tree.bind("<Double-1>", self.abrir_detalle)

        # --- Botones ---
        button_frame = tk.Frame(self.root, bg=bg_main) # 🟠 Beige
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Ver Detalle", command=self.abrir_detalle, width=15, bg=btn_bg, fg="white").pack(side="left", padx=10)
        tk.Button(button_frame, text="Regresar", command=self.on_closing, width=15, bg="#A9A9A9", fg="white").pack(side="left", padx=10)

    def cargar_historial_ventas(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        ventas = ver_ventas_historial()
        for v in ventas:
            self.tree.insert("", tk.END, values=(v[0], v[1], f"${v[2]:.2f}"))

    def abrir_detalle(self, event=None):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una venta para ver el detalle.")
            return

        id_venta = self.tree.item(sel, "values")[0]
        
        self.root.withdraw()
        
        # Abrir DetalleVentaApp (que ya tiene las correcciones de estabilidad y color)
        DetalleVentaApp(id_venta, self.dashboard_root)