import tkinter as tk
from tkinter import ttk, messagebox

def verificar_login():
    usuario = entrada_usuario.get()
    contrasena = entrada_contrasena.get()

    # Usuario y contraseña válidos
    if usuario == "admin" and contrasena == "1234":
        messagebox.showinfo("Acceso permitido", "¡Bienvenido!")
        login.destroy()
        abrir_tabla()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")


def abrir_tabla():
    # Crear ventana nueva para la tabla
    ventana = tk.Tk()
    ventana.title("Tabla de Artículos")
    ventana.geometry("600x350")
    ventana.configure(bg="#f2f2f2")

    # Título
    titulo = tk.Label(ventana, text="Lista de Artículos", font=("Arial", 18, "bold"), bg="#f2f2f2")
    titulo.pack(pady=10)

    # Crear tabla (Treeview)
    columnas = ("Artículo", "Precio", "Cantidad")
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings", height=8)

    # Encabezados
    tabla.heading("Artículo", text="Artículo")
    tabla.heading("Precio", text="Precio")
    tabla.heading("Cantidad", text="Cantidad")

    # Ancho de columnas
    tabla.column("Artículo", width=250)
    tabla.column("Precio", width=100, anchor='center')
    tabla.column("Cantidad", width=100, anchor='center')

    # Datos
    datos = [
        ("Libretas", "$20", 0),
        ("Lápices", "$5", 0),
        ("Barra de silicón", "$2", 0),
        ("Ramo de limpiapipas (Girasoles)", "$165", 0),
        ("Ramo de listón (Rosas)", "$200", 0),
        ("Peluches Stitch", "$140", 0),
        ("Peluche Kuromi", "$180", 0)
    ]

    # Insertar datos
    for articulo in datos:
        tabla.insert("", tk.END, values=articulo)

    tabla.pack(pady=10)

    ventana.mainloop()

# Login

login = tk.Tk()
login.title("Login")
login.geometry("350x250")
login.configure(bg="#e8e8e8")

titulo_login = tk.Label(login, text="Iniciar Sesión", font=("Arial", 16, "bold"), bg="#e8e8e8")
titulo_login.pack(pady=15)

# Usuario
tk.Label(login, text="Usuario:", font=("Arial", 12), bg="#e8e8e8").pack()
entrada_usuario = tk.Entry(login, font=("Arial", 12))
entrada_usuario.pack(pady=5)

# Contraseña
tk.Label(login, text="Contraseña:", font=("Arial", 12), bg="#e8e8e8").pack()
entrada_contrasena = tk.Entry(login, font=("Arial", 12), show="*")
entrada_contrasena.pack(pady=5)

# Botón iniciar sesión
boton_login = tk.Button(login, text="Acceder", font=("Arial", 12), bg="#4a90e2", fg="white", command=verificar_login)
boton_login.pack(pady=15)

login.mainloop()
