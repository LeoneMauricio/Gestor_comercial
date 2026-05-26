from database import conectar
from tkinter import messagebox, ttk
import tkinter as tk
import customtkinter as ctk

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
        print(e)
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

# MODIFICAR CLIENTES
def modificar_cliente(id_cliente, campo, nuevo_valor):
    campos_validos = [
        "nombre",
        "apellido",
        "direccion",
        "celular",
    ]
    if campo not in campos_validos:
        return False
    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        sql = f"""
        UPDATE clientes
        SET {campo} = ?
        WHERE id_cliente = ?
        """
        cursor.execute(sql, (nuevo_valor, id_cliente))
        conexion.commit()
        return True
    except Exception as e:

        print(e)
        return False
    finally:
        if conexion:
            conexion.close()
# UI PARA MODIFICAR CLIENTES
def ui_modificar_cliente():
    ventana = ctk.CTk()
    ventana.title("Modificar Cliente")
    ventana.geometry("600x500")
    
#Entrada id cliente 
    lbl_id = ctk.CTkLabel(ventana, text="ID del cliente:")
    lbl_id.pack(pady=5)
    entry_id = ctk.CTkEntry(ventana)
    entry_id.pack(pady=5)
# Menu de campo
    lbl_opciones = ctk.CTkLabel(ventana, text="¿Qué desea modificar?")
    lbl_opciones.pack(pady=10)
    opciones = {
        "Nombre": "nombre",
        "Apellido": "apellido",
        "Dirección": "direccion",
        "Celular": "celular"
    }

    campo_var = tk.StringVar(value="nombre")
    menu_campos = ctk.CTkOptionMenu(ventana, variable=campo_var, values=list(opciones.keys()))
    menu_campos.pack(pady=5)
    # Entrada nuevo valor
    lbl_valor = ctk.CTkLabel(ventana, text="Nuevo valor:")
    lbl_valor.pack(pady=5)
    entry_valor = ctk.CTkEntry(ventana)
    entry_valor.pack(pady=5)
# Botón actualizar
    def actualizar():
        try:
            id_cliente = int(entry_id.get())
            campo = opciones[menu_campos.get()]
            nuevo_valor = entry_valor.get()

            resultado = modificar_cliente(id_cliente, campo, nuevo_valor)

            if resultado:
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el cliente")
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número")

    btn_actualizar = ctk.CTkButton(ventana, text="Actualizar", command=actualizar)
    btn_actualizar.pack(pady=20)

    ventana.mainloop()

# MOSTRAR CLIENTES
def obtener_clientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_cliente, nombre, apellido, direccion, celular FROM clientes")
    datos = cursor.fetchall()
    conexion.close()
    return datos
# UI PARA MOSTRAR CLIENTES
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

    ventana.mainloop()