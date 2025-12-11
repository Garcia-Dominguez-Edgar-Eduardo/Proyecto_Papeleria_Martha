# dashboard.py

import tkinter as tk
from tkinter import messagebox
# --- Importaciones de Vistas ---
# Módulos de Operación y Reporte
from products_view import ProductosApp 
from venta_view import VentaApp
from compra_view import CompraApp 
from historial_ventas_view import HistorialVentasApp 
from detalle_compra_view import DetalleCompraApp 

# Archivo 'user_view' y Clase 'UserApp'
from user_view import UserApp 


class DashboardApp:
    def __init__(self, username):
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"Dashboard Principal - {username}")
        self.root.geometry("800x800")
        
        self.crear_elementos()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def crear_elementos(self):
        """Crea la interfaz principal del dashboard con los botones de módulos."""
        tk.Label(self.root, text=f"Bienvenido, {self.username}", font=("Arial", 24, "bold")).pack(pady=30)

        # --- Frame para organizar los botones ---
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # --- MÓDULOS DE OPERACIÓN DIARIA ---
        tk.Button(button_frame, text="Realizar Venta 🛒", command=self.abrir_ventas, 
                  width=25, height=2, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10, padx=10)

        tk.Button(button_frame, text="Registrar Compra / Inventario 📦", command=self.abrir_compras, 
                  width=25, height=2, font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=10, padx=10)
        
        # --- Separador ---
        tk.Frame(self.root, height=1, bg="gray").pack(fill='x', padx=50, pady=10)
        
        # --- MÓDULOS DE GESTIÓN Y REPORTES ---
        
        tk.Button(button_frame, text="Gestión de Usuarios 👤", command=self.abrir_usuarios, 
                  width=25, height=2, font=("Arial", 12)).pack(pady=10, padx=10)
            
        tk.Button(button_frame, text="Gestión de Productos 📋", command=self.abrir_productos, 
                  width=25, height=2, font=("Arial", 12)).pack(pady=10, padx=10)
        
        tk.Button(button_frame, text="Historial de Ventas 📜", command=self.abrir_historial_ventas, 
                  width=25, height=2, font=("Arial", 12)).pack(pady=10, padx=10)
            
        tk.Button(button_frame, text="Historial de Compras 📈", command=self.abrir_historial_compras, 
                  width=25, height=2, font=("Arial", 12)).pack(pady=10, padx=10)
        
        # --- Botón de Cerrar Sesión ---
        tk.Button(self.root, text="Cerrar Sesión", command=self.root.destroy, 
                  width=15, height=1, bg="#F44336", fg="white", font=("Arial", 12, "bold")).pack(pady=40)
        
    # --- MÉTODOS CORREGIDOS PARA ABRIR LAS VISTAS ---
    
    def abrir_usuarios(self):
        """Oculta el dashboard y abre el módulo de gestión de usuarios."""
        self.root.withdraw()
        # Se pasa self.root (la referencia al dashboard)
        UserApp(self.username, self.root) 
        # Ya no se llama a self.root.deiconify() aquí
        
    def abrir_productos(self):
        self.root.withdraw()
        # Se pasa self.root
        ProductosApp(self.username, self.root)
        
    def abrir_ventas(self):
        self.root.withdraw()
        # ¡CORRECCIÓN! Se pasa self.root
        VentaApp(self.username, self.root)
        
    def abrir_compras(self):
        self.root.withdraw()
        # Se pasa self.root
        CompraApp(self.username, self.root)
        
    def abrir_historial_ventas(self):
        self.root.withdraw()
        # Se pasa self.root
        HistorialVentasApp(self.username, self.root)
        
    def abrir_historial_compras(self):
        self.root.withdraw()
        # Se pasa self.root
        DetalleCompraApp(self.username, self.root) 
        
    def on_closing(self):
        if messagebox.askokcancel("Cerrar Aplicación", "¿Desea cerrar la aplicación?"):
            self.root.destroy()