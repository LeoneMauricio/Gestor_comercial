from database import conectar, conectar_row
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
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

# OBTENER CLIENTES Y ENVASES PARA LOS DESPLEGABLES
def obtener_clientes_dict():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_cliente, nombre, apellido FROM clientes")
    filas = cursor.fetchall()
    conexion.close()
    return {fila[0]: f"{fila[1]} {fila[2]}" for fila in filas}

def obtener_envases_dict():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_envase, envase, precio FROM envases")
    filas = cursor.fetchall()
    conexion.close()
    return {fila[0]: {"nombre": fila[1], "precio": fila[2]} for fila in filas}
# REGISTRAR VENTA
def nueva_venta(id_cliente, id_envase, cantidad, precio_unitario, subtotal):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO ventas(id_cliente, id_envase, cantidad, precio_unitario, subtotal)
            VALUES(?, ?, ?, ?, ?)
        """, (id_cliente, id_envase, cantidad, precio_unitario, subtotal))
        conexion.commit()
        return True
    finally:
        conexion.close()
# UI NUEVA VENTA
def ui_nueva_venta():
    ventana = ctk.CTkToplevel(root)
    ventana.title("Nueva Venta")
    ventana.geometry("400x450")

    clientes_dict = obtener_clientes_dict()   
    envases_dict  = obtener_envases_dict()    

    clientes_inv = {v: k for k, v in clientes_dict.items()}
    envases_inv  = {v["nombre"]: k for k, v in envases_dict.items()}

    ctk.CTkLabel(ventana, text="Cliente").pack(pady=(15, 0))
    opciones_clientes = list(clientes_dict.values())
    combo_cliente = ctk.CTkComboBox(ventana, values=opciones_clientes, state="readonly", width=300)
    combo_cliente.set("Seleccionar cliente")
    combo_cliente.pack(pady=5)

    ctk.CTkLabel(ventana, text="Envase").pack(pady=(10, 0))
    opciones_envases = [v["nombre"] for v in envases_dict.values()]
    combo_envase = ctk.CTkComboBox(ventana, values=opciones_envases, state="readonly", width=300)
    combo_envase.set("Seleccionar envase")
    combo_envase.pack(pady=5)

    ctk.CTkLabel(ventana, text="Precio unitario").pack(pady=(10, 0))
    entry_precio = ctk.CTkEntry(ventana, placeholder_text="Precio unitario", width=300)
    entry_precio.configure(state="disabled")
    entry_precio.pack(pady=5)

    def al_seleccionar_envase(nombre_envase):
        id_envase = envases_inv.get(nombre_envase)
        if id_envase:
            precio = envases_dict[id_envase]["precio"]
            entry_precio.configure(state="normal")
            entry_precio.delete(0, "end")
            entry_precio.insert(0, f"{precio:.2f}")
            entry_precio.configure(state="disabled")
            calcular_subtotal()

    combo_envase.configure(command=al_seleccionar_envase)

    ctk.CTkLabel(ventana, text="Cantidad").pack(pady=(10, 0))
    entry_cantidad = ctk.CTkEntry(ventana, placeholder_text="Cantidad de envases", width=300)
    entry_cantidad.pack(pady=5)

    ctk.CTkLabel(ventana, text="Subtotal").pack(pady=(10, 0))
    entry_subtotal = ctk.CTkEntry(ventana, placeholder_text="Subtotal", width=300)
    entry_subtotal.configure(state="disabled")
    entry_subtotal.pack(pady=5)

    def calcular_subtotal(*args):
        try:
            cant   = float(entry_cantidad.get())
            precio = float(entry_precio.get())
            total  = cant * precio
            entry_subtotal.configure(state="normal")
            entry_subtotal.delete(0, "end")
            entry_subtotal.insert(0, f"{total:.2f}")
            entry_subtotal.configure(state="disabled")
        except ValueError:
            pass

    entry_cantidad.bind("<KeyRelease>", calcular_subtotal)

    ctk.CTkButton(ventana, text="Calcular Subtotal", command=calcular_subtotal).pack(pady=10)


    def registrar_venta():
        nombre_cliente = combo_cliente.get()
        nombre_envase  = combo_envase.get()

        if nombre_cliente == "Seleccionar cliente" or nombre_envase == "Seleccionar envase":
            messagebox.showwarning("Atención", "Seleccione un cliente y un envase.")
            return
        if not entry_subtotal.get():
            messagebox.showwarning("Atención", "Primero calcule el subtotal.")
            return

        try:
            id_cliente     = clientes_inv[nombre_cliente]
            id_envase      = envases_inv[nombre_envase]
            cantidad       = int(entry_cantidad.get())
            precio_unitario = float(entry_precio.get())
            subtotal       = float(entry_subtotal.get())

            nueva_venta(id_cliente, id_envase, cantidad, precio_unitario, subtotal)
            messagebox.showinfo("Éxito", f"Venta registrada. Total: ${subtotal:.2f}")
            ventana.destroy()
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")

    ctk.CTkButton(ventana, text="Registrar Venta", command=registrar_venta).pack(pady=10)
    ventana.mainloop()
# MOSTRAR TABLA VENTAS
def mostrar_ventas():
    conexion = conectar_row()
    cursor = conexion.cursor()
    cursor.execute("""
    SELECT p.id_venta,
        c.nombre AS cliente,
        c.apellido AS apellido,
        e.envase AS envase,
        p.cantidad,
        p.precio_unitario,
        p.subtotal,
        p.fecha_venta
    FROM ventas p
    INNER JOIN clientes c ON p.id_cliente = c.id_cliente
    INNER JOIN envases e ON p.id_envase = e.id_envase
    """)
    datos = cursor.fetchall()
    conexion.close()
    return [tuple(fila) for fila in datos]
# UI MOSTRAR TABLA VENTAS
def ui_mostrar_ventas():
    ventana = ctk.CTk()
    ventana.title("Registro de ventas")
    ventana.geometry("600x400")

    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = ("ID", "Nombre", "Apellido", "Envase", "Cantidad", "Precio por unidad", "Total", "Fecha de venta")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    ventas = mostrar_ventas()
    if not ventas:
        messagebox.showinfo("Aviso", "No hay ventas registrados en la base de datos")
    else:
        for venta in ventas:
            tabla.insert("", tk.END, values=venta)

    tabla.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def abrir_modificar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una venta para modificar")
            return

        item = seleccion[0]
        datos = tabla.item(item, "values")

        top = ctk.CTkToplevel(ventana)
        top.title("Modificar Venta")

        columnas_a_modificar = [("Cantidad", 4), ("Total", 6)]
        entries = []

        for cant, tot in columnas_a_modificar:
            ctk.CTkLabel(top, text=cant).pack()
            entry = ctk.CTkEntry(top)
            entry.insert(0, datos[tot])
            entry.pack(pady=5)
            entries.append(entry)
            
        def guardar():
            nueva_cantidad = entries[0].get()
            nuevo_total = entries[1].get()
            id_venta = datos[0] 

            conexion = conectar()
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE ventas
                SET cantidad=?, subtotal=?
                WHERE id_venta=?
            """, (nueva_cantidad, nuevo_total, id_venta))
            conexion.commit()
            conexion.close()
            
            valores_actualizados = list(datos)
            valores_actualizados[4] = nueva_cantidad
            valores_actualizados[6] = nuevo_total
            tabla.item(item, values=valores_actualizados)
            messagebox.showinfo("Éxito", "Ventas  actualizada correctamente")

        ctk.CTkButton(top, text="Guardar cambios", command=guardar).pack(pady=10)

    boton_modificar = ctk.CTkButton(ventana, text="Modificar Venta", command=abrir_modificar)
    boton_modificar.pack(pady=10)
    
    ventana.mainloop()
# MOSTRAR VENTAS POR FECHA
def ui_mostrar_ventas_por_fecha():
    ventana = ctk.CTk()
    ventana.title("Ventas por Fecha")
    ventana.geometry("700x500")

    frame_filtro = ctk.CTkFrame(ventana)
    frame_filtro.pack(pady=10)

    tk.Label(frame_filtro, text="Seleccione una fecha:").pack(side="left", padx=5)
    calendario = DateEntry(frame_filtro, width=12, background="darkblue",
                        foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
    calendario.pack(side="left", padx=5)

    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = ("ID", "Nombre", "Apellido", "Envase", "Cantidad", "Precio por unidad", "Total", "Fecha de venta")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)

    tabla.pack(fill="both", expand=True, side="left")

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def buscar():
        fecha = calendario.get_date().strftime("%Y-%m-%d")
        conexion = None

        try:
            conexion = conectar() 
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT p.id_venta,
                    c.nombre AS cliente,
                    c.apellido AS apellido,
                    e.envase AS envase,
                    p.cantidad,
                    p.precio_unitario,
                    p.subtotal,
                    p.fecha_venta
                FROM ventas p
                INNER JOIN clientes c ON p.id_cliente = c.id_cliente
                INNER JOIN envases e ON p.id_envase = e.id_envase
                WHERE DATE(p.fecha_venta) = ?
            """, (fecha,))

            ventas = cursor.fetchall()

            for row in tabla.get_children():
                tabla.delete(row)

            if not ventas:
                messagebox.showinfo("Ventas", f"No hay ventas registradas en {fecha}.")
                return

            for venta in ventas:
                tabla.insert("", tk.END, values=venta)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            if conexion:
                conexion.close()

    btn_buscar = ctk.CTkButton(frame_filtro, text="Buscar", command=buscar)
    btn_buscar.pack(side="left", padx=5)

    ventana.mainloop()