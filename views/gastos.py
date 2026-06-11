import sqlite3
from config.database import conectar, conectar_row
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

# AGREGAR GASTOS
def agregar_gastos(insumos, pagos_empleado, servicios, otros, monto):
    try:        
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO gastos(insumos, pagos_empleados, servicios, otros, monto)
        VALUES(?, ?, ?, ?, ?)
        """, (insumos, pagos_empleado, servicios, otros, monto))

        conexion.commit()
        return True

    except Exception:
        return False
    finally:
        conexion.close()
# UI AGREGAR GASTOS
def ui_agregar_gastos():
    ventana = ctk.CTkToplevel(root)
    ventana.title("Agregar Gastos")
    ventana.geometry("500x400")
    # Campos insumos, pagos_empleado, servicios, otros, monto
    insumos = ctk.CTkEntry(ventana, placeholder_text="Insumos, ej: gas, pintura, combustible, etc...")
    pagos_empleado = ctk.CTkEntry(ventana, placeholder_text="Escriba el nombre del o los empleados")
    servicios = ctk.CTkEntry(ventana, placeholder_text="Escriba si es: Luz, gas, agua, impuestos, etc..")
    otros = ctk.CTkEntry(ventana, placeholder_text="Especifique el gasto ej: comprar golosinas, medicamentos, etc... ")
    monto = ctk.CTkEntry(ventana, placeholder_text="Ingrese el monto del gasto detallado anteriormente.")

    insumos.pack(pady=5)
    pagos_empleado.pack(pady=5)
    servicios.pack(pady=5)
    otros.pack(pady=5)
    monto.pack(pady=5)

    def guardar():
        resultado = agregar_gastos(
            insumos.get(),
            pagos_empleado.get(),
            servicios.get(),
            otros.get(),
            monto.get()
        )
        msg = "Gasto agregado correctamente" if resultado else "Error al agregar monto"
        ctk.CTkLabel(ventana, text=msg).pack(pady=10)

    ctk.CTkButton(ventana, text="Guardar", command=guardar).pack(pady=10)

    ventana.mainloop()

# MOSTRAR GASTOS
def obtener_gastos():
    conexion = conectar()
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT id_gasto, insumos, pagos_empleados, servicios, otros, monto FROM gastos")
    datos = cursor.fetchall()
    conexion.close()
    return [tuple(fila) for fila in datos]
# UI PARA MOSTRAR GASTOS / MODIFICAR EN TABLA
def ui_mostrar_gastos():
    ventana = ctk.CTk()
    ventana.title("Lista de GASOS")
    ventana.geometry("600x400")

    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = ("ID", "Insumos", "Pago a Empleados", "Servicios", "Otros gastos", "Monto")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)

    gastos = obtener_gastos()
    if not gastos:
        messagebox.showinfo("Aviso", "No hay gastos registrados en la base de datos")
    else:
        for gasto in gastos:
            tabla.insert("", tk.END, values=gasto)

    tabla.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def abrir_modificar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un gasto para modificar")
            return

        item = seleccion[0]
        datos = tabla.item(item, "values") 

        top = ctk.CTkToplevel(ventana)
        top.title("Modificar Gato")

        labels = ["Insumos", "Pago a Empleados", "Servicios", "Otros gastos", "Monto"]
        entries = []

        for i, campo in enumerate(labels, start=1):
            ctk.CTkLabel(top, text=campo).pack()
            entry = ctk.CTkEntry(top)
            entry.insert(0, datos[i])
            entry.pack(pady=5)
            entries.append(entry)

        def guardar():
            nuevo_insumo = entries[0].get()
            nuevo_pago_empleado = entries[1].get()
            nuevo_servicio = entries[2].get()
            nuevo_otro = entries[3].get()
            nuevo_monto = entries[4].get()
            id_gasto = datos[0]

            conexion = sqlite3.connect("soderia.db")
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE gastos
                SET insumos=?, pagos_empleados=?, servicio=?, otros=?, monto=?
                WHERE id_gasto=?
            """, (nuevo_insumo, nuevo_pago_empleado, nuevo_servicio, nuevo_otro, nuevo_monto, id_gasto))
            conexion.commit()
            conexion.close()

            tabla.item(item, values=(id_gasto, nuevo_insumo, nuevo_pago_empleado, nuevo_servicio, nuevo_otro, nuevo_monto))
            top.destroy()
            messagebox.showinfo("Éxito", "Gasto actualizado correctamente")

        ctk.CTkButton(top, text="Guardar cambios", command=guardar).pack(pady=10)

    boton_modificar = ctk.CTkButton(ventana, text="Modificar Gasto", command=abrir_modificar)
    boton_modificar.pack(pady=10)

    ventana.mainloop()