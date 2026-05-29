from database import conectar, conectar_row
from tkinter import messagebox, ttk
import tkinter as tk
import customtkinter as ctk
import sqlite3

ctk.set_appearance_mode("System")  # "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Puedes cambiar el tema

root = ctk.CTk()
root.title("Sodería - Gestión")
root.geometry("600x500")

# Frame principal
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# AGREGAR CLIENETES
def agregar_cliente(nombre, apellido, direccion, celular):
    try:        
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO clientes(nombre, apellido, direccion, celular)
        VALUES(?, ?, ?, ?)
        """, (nombre, apellido, direccion, celular))
        
        conexion.commit()
        return True

    except Exception as e:
        return False
    finally:
        conexion.close()
# UI PARA AGREGAR CLIENTES
def ui_agregar_cliente():
    ventana = ctk.CTkToplevel(root)
    ventana.title("Agregar Cliente")
    ventana.geometry("500x400")
    # Campos
    nombre = ctk.CTkEntry(ventana, placeholder_text="Nombre")
    apellido = ctk.CTkEntry(ventana, placeholder_text="Apellido")
    direccion = ctk.CTkEntry(ventana, placeholder_text="Dirección")
    celular = ctk.CTkEntry(ventana, placeholder_text="Celular")

    nombre.pack(pady=5)
    apellido.pack(pady=5)
    direccion.pack(pady=5)
    celular.pack(pady=5)

    def guardar():
        resultado = agregar_cliente(
            nombre.get(),
            apellido.get(),
            direccion.get(),
            celular.get()
        )
        msg = "Cliente agregado correctamente" if resultado else "Error al agregar cliente"
        ctk.CTkLabel(ventana, text=msg).pack(pady=10)

    ctk.CTkButton(ventana, text="Guardar", command=guardar).pack(pady=10)

    ventana.mainloop()
# MOSTRAR CLIENTES
def obtener_clientes():
    conexion = conectar()
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT id_cliente, nombre, apellido, direccion, celular FROM clientes")
    datos = cursor.fetchall()
    conexion.close()
    return [tuple(fila) for fila in datos]
# UI PARA MOSTRAR CLIENTES / MODIFICAR EN TABLA
def ui_mostrar_clientes():
    ventana = ctk.CTk()
    ventana.title("Lista de Clientes")
    ventana.geometry("600x400")

    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = ("ID", "Nombre", "Apellido", "Dirección", "Celular")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    clientes = obtener_clientes()
    if not clientes:
        messagebox.showinfo("Aviso", "No hay clientes registrados en la base de datos")
    else:
        for cliente in clientes:
            tabla.insert("", tk.END, values=cliente)

    tabla.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def abrir_modificar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un cliente para modificar")
            return

        item = seleccion[0]
        datos = tabla.item(item, "values") 

        top = ctk.CTkToplevel(ventana)
        top.title("Modificar Cliente")

        labels = ["Nombre", "Apellido", "Dirección", "Celular"]
        entries = []

        for i, campo in enumerate(labels, start=1):
            ctk.CTkLabel(top, text=campo).pack()
            entry = ctk.CTkEntry(top)
            entry.insert(0, datos[i])
            entry.pack(pady=5)
            entries.append(entry)

        def guardar():
            nuevo_nombre = entries[0].get()
            nuevo_apellido = entries[1].get()
            nueva_direccion = entries[2].get()
            nuevo_celular = entries[3].get()
            id_cliente = datos[0]

            conexion = sqlite3.connect("soderia.db")
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE clientes
                SET nombre=?, apellido=?, direccion=?, celular=?
                WHERE id_cliente=?
            """, (nuevo_nombre, nuevo_apellido, nueva_direccion, nuevo_celular, id_cliente))
            conexion.commit()
            conexion.close()

            tabla.item(item, values=(id_cliente, nuevo_nombre, nuevo_apellido, nueva_direccion, nuevo_celular))
            top.destroy()
            messagebox.showinfo("Éxito", "Cliente actualizado correctamente")

        ctk.CTkButton(top, text="Guardar cambios", command=guardar).pack(pady=10)

    boton_modificar = ctk.CTkButton(ventana, text="Modificar Cliente", command=abrir_modificar)
    boton_modificar.pack(pady=10)

    ventana.mainloop()