import tkinter as tk
from tkinter import messagebox, ttk
from products_controller import ver_productos, agregar_producto, actualizar_producto, eliminar_producto

class ProductosApp:
    def __init__(self, username, dashboard_root):
        self.username = username 
        self.dashboard_root = dashboard_root 
        
        self.root = tk.Toplevel(self.dashboard_root)
        self.root.title(f"Gestión de Productos - Bienvenido {username}")
        self.root.geometry("900x600")
        
        # 🟠 COLORES
        bg_color = "#F5F5DC" # Beige
        self.root.configure(bg=bg_color) 
        
        self.crear_elementos(bg_color) 
        self.ver_productos()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.root.mainloop() ELIMINADA (Para estabilidad)

    def on_closing(self):
        """Cierra la ventana actual y muestra el Dashboard."""
        self.root.destroy()
        self.dashboard_root.deiconify() 

    def crear_elementos(self, bg_color):
        
        btn_bg = "#FF8C00" # Naranja oscuro

        tk.Label(self.root, text=f"Hola, {self.username}", font=("Arial", 22, "bold"), bg=bg_color).pack(pady=10)

        frame = tk.Frame(self.root, bg=bg_color)
        frame.pack(pady=10)
        
        # Las llamadas a los métodos ahora serán reconocidas por self
        tk.Button(frame, text="Agregar producto", command=self.agregar_producto, bg=btn_bg, fg="white").pack(pady=25)
        tk.Button(frame, text="Actualizar producto", command=self.actualizar_producto, bg=btn_bg, fg="white").pack(pady=25)
        tk.Button(frame, text="Eliminar producto", command=self.eliminar_producto, bg=btn_bg, fg="white").pack(pady=25)
        
        tk.Button(frame, text="Regresar", command=self.on_closing, bg="#A9A9A9", fg="white").pack(pady=25) # Gris oscuro

        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Marca", "Precio", "Stock"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Stock", text="Stock")
        self.tree.pack(fill="both", expand=True)

    # ASEGÚRATE de que estos métodos están indentados correctamente DENTRO de la clase ProductosApp
    def ver_productos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in ver_productos():
            self.tree.insert("", tk.END, values=p)

    def agregar_producto(self):
        def guardar():
            n = entry_nombre.get().strip()
            m = entry_marca.get().strip()
            try:
                pr = float(entry_precio.get().strip())
                st = int(entry_stock.get().strip())
            except ValueError:
                messagebox.showwarning("Error", "Precio y stock deben ser números.")
                return
            if agregar_producto(n, m, pr, st):
                messagebox.showinfo("Éxito", f"Producto '{n}' agregado.")
                ventana.destroy()
                self.root.after(100, self.ver_productos)
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto.")

        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar producto")
        ventana.geometry("300x300")

        tk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack()

        tk.Label(ventana, text="Marca:").pack(pady=5)
        entry_marca = tk.Entry(ventana)
        entry_marca.pack()

        tk.Label(ventana, text="Precio:").pack(pady=5)
        entry_precio = tk.Entry(ventana)
        entry_precio.pack()

        tk.Label(ventana, text="Stock:").pack(pady=5)
        entry_stock = tk.Entry(ventana)
        entry_stock.pack()

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)

    def actualizar_producto(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un producto.")
            return

        id_producto, nom, marca, precio, stock = self.tree.item(sel, "values")

        def guardar():
            n = entry_nombre.get().strip() 
            m = entry_marca.get().strip()
            try:
                pr = float(entry_precio.get().strip())
                st = int(entry_stock.get().strip())
            except ValueError:
                messagebox.showwarning("Error", "Precio y stock deben ser números.")
                return
            if actualizar_producto(id_producto, n, m, pr, st):
                messagebox.showinfo("Éxito", "Producto actualizado.")
                ventana.destroy()
                self.root.after(100, self.ver_productos)
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto.")

        ventana = tk.Toplevel(self.root)
        ventana.title("Actualizar producto")
        ventana.geometry("300x300")

        tk.Label(ventana, text="Nombre:").pack(pady=5)
        entry_nombre = tk.Entry(ventana)
        entry_nombre.insert(0, nom)
        entry_nombre.pack()

        tk.Label(ventana, text="Marca:").pack(pady=5)
        entry_marca = tk.Entry(ventana)
        entry_marca.insert(0, marca)
        entry_marca.pack()

        tk.Label(ventana, text="Precio:").pack(pady=5)
        entry_precio = tk.Entry(ventana)
        entry_precio.insert(0, precio)
        entry_precio.pack()

        tk.Label(ventana, text="Stock:").pack(pady=5)
        entry_stock = tk.Entry(ventana)
        entry_stock.insert(0, stock)
        entry_stock.pack()

        tk.Button(ventana, text="Guardar cambios", command=guardar).pack(pady=10)

    def eliminar_producto(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un producto.")
            return
        id_producto = self.tree.item(sel, "values")[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar el producto?"):
            if eliminar_producto(id_producto):
                messagebox.showinfo("Éxito", "Producto eliminado.")
                self.root.after(100, self.ver_productos)
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto.")