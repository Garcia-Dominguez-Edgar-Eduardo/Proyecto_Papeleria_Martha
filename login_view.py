import tkinter as tk
from tkinter import messagebox
from auth_controller import validar_credenciales
from dashboard import DashboardApp

class LoginApp: 
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de inicio de sesión")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        tk.Label(root, text="Bienvenido al Login", font=("Arial",16,"bold")).pack(pady=15)

        tk.Label(root, text="Nombre de usuario:").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Contraseña").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Iniciar sesión", command=self.Login).pack(pady=20)
        tk.Button(root, text="Salir", command=self.root.quit).pack()

    def Login(self):
        usuario = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not usuario or not password: 
            messagebox.showwarning("Faltan datos", "Por favor ingresa usuario y contraseña.")
            return

        if validar_credenciales(usuario, password):
            messagebox.showinfo("Acceso concedido", f"Bienvenido {usuario}")
            self.root.destroy()
            DashboardApp(usuario)
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos")
