import tkinter as tk
from tkinter import ttk
import sqlite3

class Producto:
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("Gestión de productos")  # Título de la cabecera
        self.ventana.resizable(1, 1)  # Redimensionable
        self.ventana.wm_iconbitmap('recursos/icon.ico')

        # Creando el título
        self.titulo = tk.Label(text="Gestión de productos", font=("Calibri", 20))
        self.titulo.grid(row=0, column=0, padx=50)

        # Creando el texto de la cabecera
        self.texto = tk.Label(text="Introduzca el producto", font=("Calibri", 14))
        self.texto.grid(row=1, column=0)

        # Creando las casillas de nombre y precio
        self.titulo_nombre = tk.Label(text="Nombre:", font=("Calibri", 12))
        self.titulo_nombre.grid(row=2, column=0)
        self.titulo_precio = tk.Label(text="Precio:", font=("Calibri", 12))
        self.titulo_precio.grid(row=3, column=0)
        self.texto_nombre = tk.Entry()
        self.texto_nombre.grid(row=2, column=1)
        self.texto_precio = tk.Entry()
        self.texto_precio.grid(row=3, column=1)
        self.texto_nombre.focus_set()

        # Conectándonos a la base de datos
        self.conn = sqlite3.connect("database/producto.db")
        self.cursor = self.conn.cursor()
        query = "CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL)"
        self.cursor.execute(query)
        self.conn.commit()

        # Creando el botón de guardar
        self.boton_guardar = tk.Button(text="Guardar", command=self.crear_producto)
        self.boton_guardar.grid(row=4, column=0, columnspan=2)
        self.mensaje = tk.Label(text="",fg="red")
        self.mensaje.grid(row=5, column=0, columnspan=2)

        # Mostrando los productos en pantalla
        self.tabla = ttk.Treeview(self.ventana, columns=("nombre", "precio"), show="headings")
        self.tabla.grid(row=6, column=0, columnspan=2)
        self.tabla.heading("nombre", text="Nombre", anchor=tk.CENTER)
        self.tabla.heading("precio", text="Precio", anchor=tk.CENTER)
        self.mostrar_datos()

        self.boton_editar = tk.Button(text="Editar", command=self.editar_producto)
        self.boton_editar.grid(row=7, column=0)
        self.boton_eliminar = tk.Button(text="Eliminar", command=self.eliminar_producto)
        self.boton_eliminar.grid(row=7, column=1)

    def crear_producto(self):
        nombre = self.texto_nombre.get().capitalize()
        precio = self.texto_precio.get()
        if nombre and precio:
            try:
                precio = float(precio)
                self.mensaje["text"] = "Producto creado con éxito"
                query = "INSERT INTO productos (nombre, precio) VALUES (?, ?)"
                self.cursor.execute(query, (nombre, precio))
                self.conn.commit()
                self.mostrar_datos()  # Actualizar la tabla después de insertar
                self.texto_nombre.delete(0, tk.END)
                self.texto_precio.delete(0, tk.END)
                self.texto_nombre.focus_set()
            except ValueError:
                self.mensaje["text"] = "El precio debe ser un número."
        elif nombre and not precio:
            self.mensaje["text"] = "Se debe añadir un precio."
        elif precio and not nombre:
            self.mensaje["text"] = "Se debe añadir un nombre."
        else:
            self.mensaje["text"] = "Se debe añadir un nombre y un precio."

    def editar_producto(self):
        ventana_editar = tk.Toplevel(self.ventana)

        # Título
        ventana_editar.title("Editar producto")
        ventana_editar_titulo = tk.Label(ventana_editar, text="Editar producto", font=("Calibri", 20))
        ventana_editar_titulo.grid(row=0, column=0, padx=50, columnspan=2)
        ventana_editar_texto = tk.Label(ventana_editar, text="Introduzca el producto que desea editar", font=("Calibri", 14))
        ventana_editar_texto.grid(row=1, column=0, columnspan=2)
        ventana_editar.wm_iconbitmap('recursos/icon.ico')


        # Nombre actual
        viejo_nombre = tk.Label(ventana_editar, text="Nombre actual:", font=("Calibri", 12))
        viejo_nombre.grid(row=2, column=0)
        texto_viejo_nombre = tk.Entry(ventana_editar)
        texto_viejo_nombre.grid(row=2, column=1)

        # Nombre nuevo
        nuevo_nombre = tk.Label(ventana_editar, text="Nombre nuevo:", font=("Calibri", 12))
        nuevo_nombre.grid(row=3, column=0)
        texto_nuevo_nombre = tk.Entry(ventana_editar)
        texto_nuevo_nombre.grid(row=3, column=1)

        # Precio nuevo
        nuevo_precio = tk.Label(ventana_editar, text="Precio nuevo:", font=("Calibri", 12))
        nuevo_precio.grid(row=4, column=0)
        texto_nuevo_precio = tk.Entry(ventana_editar)
        texto_nuevo_precio.grid(row=4, column=1)

        mensaje = tk.Label(ventana_editar, text="",fg="red")
        mensaje.grid(row=5, column=0, columnspan=2)

        def guardar_cambios():
            get_viejo_nombre = texto_viejo_nombre.get().capitalize()
            get_nuevo_nombre = texto_nuevo_nombre.get().capitalize()
            get_nuevo_precio = texto_nuevo_precio.get()

            if get_viejo_nombre and get_nuevo_nombre and get_nuevo_precio:
                try:
                    get_nuevo_precio = float(get_nuevo_precio)
                    query = "UPDATE productos SET nombre = ?, precio = ? WHERE nombre = ?"
                    self.cursor.execute(query, (get_nuevo_nombre, get_nuevo_precio, get_viejo_nombre))
                    self.conn.commit()
                    self.mostrar_datos()
                    ventana_editar.destroy()
                except ValueError:
                    mensaje["text"]="El precio debe ser un número."
                except Exception:
                    mensaje["text"]=f"El producto no coincide."
            elif get_viejo_nombre and get_nuevo_nombre and not get_nuevo_precio:
                mensaje["text"]="Debe añadir un precio nuevo o escribir el actual."
            elif get_viejo_nombre and get_nuevo_precio and not get_nuevo_nombre:
                mensaje["text"]="Debe añadir un nombre nuevo o escribir el actual."
            elif not get_viejo_nombre and get_nuevo_precio and not get_nuevo_nombre:
                mensaje.config(text="El nombre no coincide con ningún producto.")
            else:
                mensaje["text"]="Todos los campos deben estar rellenados."

        # Botón de guardar
        boton_guardar = tk.Button(ventana_editar, text="Guardar", command=guardar_cambios)
        boton_guardar.grid(row=6, column=0, columnspan=2)

    def eliminar_producto(self):
        ventana_eliminar = tk.Toplevel(self.ventana)

        # Título
        ventana_eliminar.title("Eliminar producto")
        ventana_eliminar_titulo = tk.Label(ventana_eliminar, text="Eliminar producto", font=("Calibri", 20))
        ventana_eliminar_titulo.grid(row=0, column=0, padx=50, columnspan=2)
        ventana_eliminar_texto = tk.Label(ventana_eliminar, text="Introduzca el producto que desea eliminar",
                                        font=("Calibri", 14))
        ventana_eliminar_texto.grid(row=1, column=0, columnspan=2)
        ventana_eliminar.wm_iconbitmap('recursos/icon.ico')


        # Nombre
        nombre = tk.Label(ventana_eliminar, text="Nombre:", font=("Calibri", 12))
        nombre.grid(row=2, column=0)
        texto_nombre = tk.Entry(ventana_eliminar)
        texto_nombre.grid(row=2, column=1)

        #Mensaje
        mensaje = tk.Label(ventana_eliminar, text="",fg="red")
        mensaje.grid(row=3, column=0, columnspan=2)

        def confirmar():
            get_nombre = texto_nombre.get().capitalize()
            if get_nombre:
                try:
                    query = "DELETE FROM productos WHERE nombre = ?"
                    self.cursor.execute(query, (get_nombre,))
                    self.conn.commit()
                    self.mostrar_datos()
                    ventana_eliminar.destroy()
                except Exception:
                    mensaje["text"]="El nombre no coincide."
            else:
                mensaje["text"]="El campo nombre debe estar relleno."

        # Botón de guardar
        boton_guardar = tk.Button(ventana_eliminar, text="Confirmar",command=confirmar)
        boton_guardar.grid(row=4, column=0, columnspan=2)

    def mostrar_datos(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        query = "SELECT nombre, precio FROM productos"
        filas = self.cursor.execute(query)
        for fila in filas:
            self.tabla.insert("", tk.END, values=fila)

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

# Configuraciones iniciales
if __name__ == "__main__":
    root = tk.Tk()
    app = Producto(root)
    root.mainloop()
