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

# REGISTRAR VENTA
def nueva_venta(id_cliente, id_envase,cantidad,precio_unitario, subtotal):
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
    ventana.geometry("600x500")

    # Entradas
    id_cliente = ctk.CTkEntry(ventana, placeholder_text="ID del cliente")
    id_cliente.pack(pady=5)

    id_envase = ctk.CTkEntry(ventana, placeholder_text="ID del envase")
    id_envase.pack(pady=5)

    cantidad = ctk.CTkEntry(ventana, placeholder_text="Cantidad de envases")
    cantidad.pack(pady=5)

    precio_unitario = ctk.CTkEntry(ventana, placeholder_text="Precio por unidad")
    precio_unitario.pack(pady=5)

    # Subtotal (solo lectura)
    subtotal = ctk.CTkEntry(ventana, placeholder_text="Subtotal")
    subtotal.configure(state="readonly")  # lo dejamos solo lectura
    subtotal.pack(pady=5)

    # Función para calcular subtotal
    def calcular_subtotal(*args):
        try:
            cant = float(cantidad.get())
            precio = float(precio_unitario.get())
            total = cant * precio
            subtotal.configure(state="normal")   # habilitamos para escribir
            subtotal.delete(0, "end")
            subtotal.insert(0, f"{total:.2f}")
            subtotal.configure(state="readonly") # volvemos a solo lectura
        except ValueError:
            # Si no hay valores numéricos aún, no hacemos nada
            pass

    # Botón para calcular
    btn_calcular = ctk.CTkButton(ventana, text="Calcular Subtotal", command=calcular_subtotal)
    btn_calcular.pack(pady=10)


    def registrar_venta():
        try:
            nueva_venta(int(id_cliente.get()), int(id_envase.get()), int(cantidad.get()),
            float(precio_unitario.get()), float(subtotal.get()))
            if not subtotal.get():
                messagebox.showwarning("Atención", "Primero calcule el subtotal.")
                return
            messagebox.showinfo("Venta registrada", f"Total: {subtotal.get()}")
        except ValueError:
            msg = "Error: Los valores deben ser numéricos"
        ctk.CTkLabel(ventana, text=msg).pack(pady=10)

    ctk.CTkButton(ventana, text="Registrar Venta", command=registrar_venta).pack(pady=10)

    ventana.mainloop()

# MOSTRAR TABLA VENTAS
def mostrar_ventas():
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
    """)
    datos = cursor.fetchall()
    conexion.close()
    return datos

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

    ventana.mainloop()