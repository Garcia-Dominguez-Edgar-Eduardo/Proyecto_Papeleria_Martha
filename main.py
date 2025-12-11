#Cuando un proyecto de python se ejecuta, el archivo main.py es el archivo principal o punto de entrada,
#aqui se inicializa la app

from tkinter import Tk
from login_view import LoginApp

def main():
    try:
        root = Tk()
        app = LoginApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")

if __name__ == "__main__":
    main()
