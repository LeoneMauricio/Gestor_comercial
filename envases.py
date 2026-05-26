from database import conectar, conectar_row
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
# AGREGAR ENVASES
def agregar_envase(envase, stock, precio):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO envases(envase, stock, precio)
        VALUES(?, ?, ?)
        """, (envase, stock, precio))

        conexion.commit()
        return True
    finally:
        conexion.close()
# UI AGREGAR ENVASES
def ui_agregar_envase():
    ventana = ctk.CTkToplevel(root)
    ventana.title("Agregar Envase")
    ventana.geometry("600x500")

    envase = ctk.CTkEntry(ventana, placeholder_text="Nombre del envase")
    stock = ctk.CTkEntry(ventana, placeholder_text="Stock")
    precio = ctk.CTkEntry(ventana, placeholder_text="Precio")

    envase.pack(pady=5)
    stock.pack(pady=5)
    precio.pack(pady=5)

    def guardar():
        try:
            resultado = agregar_envase(envase.get(), int(stock.get()), float(precio.get()))
            msg = "Envase agregado correctamente" if resultado else "Error al agregar envase"
        except ValueError:
            msg = "Error: Stock y precio deben ser numéricos"
        ctk.CTkLabel(ventana, text=msg).pack(pady=10)

    ctk.CTkButton(ventana, text="Guardar", command=guardar).pack(pady=10)
    
    ventana.mainloop()
# MODIFICAR ENVASES
def modificar_envases(id_envase, campo, nuevo_valor):
    campos_validos = [
        "envase",
        "stock",
        "precio",
    ]
    
    if campo not in campos_validos:
        return False
    
    conexion = None

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = f"""
        UPDATE envases
        SET {campo} = ?
        WHERE id_envase = ?
        """
        cursor.execute(sql, (nuevo_valor, id_envase))
        conexion.commit()
        return True

    except Exception as e:
        print(e)
        return False
    finally:
        if conexion:
            conexion.close()
# UI MODIFICAR ENVASE
def ui_modificar_envase():
    ventana = ctk.CTk()
    ventana.title("Modificar Envase")
    ventana.geometry("600x500")
    #Entrada id cliente 
    lbl_id = ctk.CTkLabel(ventana, text="ID del envase:")
    lbl_id.pack(pady=5)
    entry_id = ctk.CTkEntry(ventana)
    entry_id.pack(pady=5)
    # Menu de campo
    lbl_opciones = ctk.CTkLabel(ventana, text="¿Qué desea modificar?")
    lbl_opciones.pack(pady=10)
    opciones = {
        "Envase": "envase",
        "Stock": "stock",
        "Precio": "precio",
    }

    campo_var = tk.StringVar(value="envase")
    menu_campos = ctk.CTkOptionMenu(ventana, variable=campo_var, values=list(opciones.keys()))
    menu_campos.pack(pady=5)

    lbl_valor = ctk.CTkLabel(ventana, text="Nuevo valor:")
    lbl_valor.pack(pady=5)
    entry_valor = ctk.CTkEntry(ventana)
    entry_valor.pack(pady=5)

    def actualizar():
        try:
            id_envase = int(entry_id.get())
            campo = opciones[menu_campos.get()]
            nuevo_valor = entry_valor.get()

            resultado = modificar_envases(id_envase, campo, nuevo_valor)

            if resultado:
                messagebox.showinfo("Éxito", "Envase actualizado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el envase")
        except ValueError:
            messagebox.showerror("Error", "El ID debe ser un número")

    btn_actualizar = ctk.CTkButton(ventana, text="Actualizar", command=actualizar)
    btn_actualizar.pack(pady=20)

    ventana.mainloop()
# MOSTRAR ENVASES
def obtener_envases():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM envases")
    datos = cursor.fetchall()
    conexion.close()
    return datos
# UI MOSTRAR ENVASES
def ui_mostrar_envases():
    ventana = ctk.CTk()
    ventana.title("Lista de Envases")
    ventana.geometry("600x400")

    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = ("ID", "Envase", "Stock", "Precio")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    envases = obtener_envases()
    if not envases:
        messagebox.showinfo("Aviso", "No hay envases registrados en la base de datos")
    else:
        for envase in envases:
            tabla.insert("", tk.END, values=envase)

    tabla.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    ventana.mainloop()

# AGREGAR PRÉSTAMO
def agregar_prestamo(id_cliente, id_envase, cantidad):
    conexion = None
    try:
        conexion = conectar_row()
        cursor = conexion.cursor()
        # VERIFICAR STOCK
        cursor.execute("""
        SELECT stock
        FROM envases
        WHERE id_envase = ?
        """, (id_envase,))
        resultado = cursor.fetchone()

        # REGISTRAR PRÉSTAMO
        cursor.execute("""
        INSERT INTO prestamos_envases(
            id_cliente,
            id_envase,
            cantidad
        )
        VALUES(?, ?, ?)
        """, (id_cliente, id_envase, cantidad))

        # DESCONTAR STOCK
        cursor.execute("""
        UPDATE envases
        SET stock = stock - ?
        WHERE id_envase = ?
        """, (cantidad, id_envase))

        conexion.commit()
        return True

    finally:
        if conexion:
            conexion.close()
# REGISTRAR PRESTAMOS DE ENVASE
def ui_agregar_prestamos():
    ventana = ctk.CTkToplevel(root)
    ventana.title("Agregar Prestamos de Envases")
    ventana.geometry("600x500")
    
    id_cliente = ctk.CTkEntry(ventana, placeholder_text="ID del cliente")
    id_envase = ctk.CTkEntry(ventana, placeholder_text="ID del envase")
    cantidad = ctk.CTkEntry(ventana, placeholder_text="Cantidad prestada")

    id_cliente.pack(pady=5)
    id_envase.pack(pady=5)
    cantidad.pack(pady=5)

    def guardar():
        try:
            resultado = agregar_prestamo(int(id_cliente.get()), int(id_envase.get()), int(cantidad.get()))
            msg = "Prestamo registrado correctamente" if resultado else "Error al agregar envase"
        except ValueError:
            msg = "Error: Los ID o la cantidad deben ser numéricos"
        ctk.CTkLabel(ventana, text=msg).pack(pady=10)

    ctk.CTkButton(ventana, text="Guardar", command=guardar).pack(pady=10)

    ventana.mainloop()
# MOSTRAR TABLA PRESTAMOS DE ENVASES
def obtener_envases_prestados():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
    SELECT p.id_prestamo,
        c.nombre AS cliente,
        c.apellido AS apellido,
        e.envase AS envase,
        p.cantidad,
        p.fecha_prestamo
    FROM prestamos_envases p
    INNER JOIN clientes c ON p.id_cliente = c.id_cliente
    INNER JOIN envases e ON p.id_envase = e.id_envase
    """)
    datos = cursor.fetchall()
    conexion.close()
    return datos
# UI MOSTRAR ENVASES PRESTADOS
def ui_mostrar_envases_prestados():
    ventana = ctk.CTk()
    ventana.title("Lista de Envases Prestados")
    ventana.geometry("600x400")

    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = ("ID", "Nombre", "Apellido", "Envase", "Cantidad", "Fecha de Prestamo")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    envases = obtener_envases_prestados()
    if not envases:
        messagebox.showinfo("Aviso", "No hay envases prestados registrados en la base de datos")
    else:
        for envase in envases:
            tabla.insert("", tk.END, values=envase)

    tabla.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    ventana.mainloop()
