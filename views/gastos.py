import sqlite3
from config.database import conectar, conectar_row
from tkinter import messagebox, ttk
import tkinter as tk
import customtkinter as ctk
from tkcalendar import DateEntry

ctk.set_appearance_mode("System")  # "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Puedes cambiar el tema

root = ctk.CTk()
root.title("Sodería - Gestión")
root.geometry("600x500")
# Frame principal
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# AGREGAR GASTOS
def agregar_gastos(motivo, monto):
    try:        
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO gastos(motivo, monto)
        VALUES(?, ?)
        """, (motivo, monto))

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
    motivo = ctk.CTkEntry(ventana, placeholder_text="Detalle el motivo del gasto.")
    monto = ctk.CTkEntry(ventana, placeholder_text="Ingrese el monto del gasto detallado anteriormente.")

    motivo.pack(pady=5)
    motivo.configure(width=250, height=50)
    monto.pack(pady=5)

    def guardar():
        resultado = agregar_gastos(
            motivo.get(),
            monto.get()
        )
        msg = "Gasto agregado correctamente" if resultado else "Error al agregar gasto"
        ctk.CTkLabel(ventana, text=msg).pack(pady=10)

    ctk.CTkButton(ventana, text="Guardar", command=guardar).pack(pady=10)

    ventana.mainloop()

# MOSTRAR GASTOS
def obtener_gastos():
    conexion = conectar()
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    cursor.execute("SELECT id_gasto, motivo, monto, fecha_del_gasto FROM gastos")
    datos = cursor.fetchall()
    conexion.close()
    return [tuple(fila) for fila in datos]
# UI PARA MOSTRAR GASTOS / MODIFICAR EN TABLA
def ui_mostrar_gastos():
    ventana = ctk.CTk()
    ventana.title("Lista de GASTOS")
    ventana.geometry("600x400")

    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = ("ID", "Motivo del Gasto", "Monto", "Fecha del Gasto")
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
        top.title("Modificar Gasto")

        labels = ["Motivo del Gasto", "Monto"]
        entries = []

        for i, campo in enumerate(labels, start=1):
            ctk.CTkLabel(top, text=campo).pack()
            entry = ctk.CTkEntry(top)
            entry.insert(0, datos[i])
            entry.pack(pady=5)
            entries.append(entry)

        def guardar():
            nuevo_motivo = entries[0].get()
            nuevo_monto = entries[1].get()
            id_gasto = datos[0]

            conexion = sqlite3.connect("soderia.db")
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE gastos
                SET motivo=?, monto=?
                WHERE id_gasto=?
            """, (nuevo_motivo, nuevo_monto, id_gasto))
            conexion.commit()
            conexion.close()

            tabla.item(item, values=(id_gasto, nuevo_motivo, nuevo_monto))
            top.destroy()
            messagebox.showinfo("Éxito", "Gasto actualizado correctamente")

        ctk.CTkButton(top, text="Guardar cambios", command=guardar).pack(pady=10)

    boton_modificar = ctk.CTkButton(ventana, text="Modificar Gasto", command=abrir_modificar)
    boton_modificar.pack(pady=10)

    ventana.mainloop()

# MOSTRAR GASTOS DÍAS/MES
def ui_mostrar_gastos_por_fecha():
    ventana = ctk.CTk()
    ventana.title("Gastos por Fecha")
    ventana.geometry("700x500")

    frame_filtro = ctk.CTkFrame(ventana)
    frame_filtro.pack(pady=10)

    tk.Label(frame_filtro, text="Seleccione una fecha:").pack(side="left", padx=5)
    calendario = DateEntry(frame_filtro, width=12, background="darkblue",
                        foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
    calendario.pack(side="left", padx=5)

    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    columnas = ("ID", "Motivo del Gasto", "Monto", "Fecha del gasto")
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
                SELECT id_gasto,
                    motivo,
                    monto,
                    fecha_del_gasto
                FROM gastos 
                WHERE DATE(fecha_del_gasto) = ?
            """, (fecha,))

            gastos = cursor.fetchall()

            for row in tabla.get_children():
                tabla.delete(row)

            if not gastos:
                messagebox.showinfo("Gatos", f"No hay gastos registradas en {fecha}.")
                return

            for gasto in gastos:
                tabla.insert("", tk.END, values=gasto)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        finally:
            if conexion:
                conexion.close()

    btn_buscar = ctk.CTkButton(frame_filtro, text="Buscar", command=buscar)
    btn_buscar.pack(side="left", padx=5)
    
    frame_total = ctk.CTkFrame(ventana)
    frame_total.pack(fill="x", padx=10, pady=10)

    def calcular_total():
        total_dia = 0.0
        # Recorremos todas las filas que están actualmente en la tabla
        for row in tabla.get_children():
            valores = tabla.item(row)["values"]
            # El índice 6 corresponde a la columna "Total"
            try:
                total_dia += float(valores[2])
            except (ValueError, TypeError):
                pass # Ignoramos si por algún motivo el valor no se puede convertir a número
        
        # Actualizamos la etiqueta con el total formateado a 2 decimales
        lbl_total.configure(text=f"Total del día: ${total_dia:.2f}")

    btn_calcular = ctk.CTkButton(frame_total, text="Calcular Total", command=calcular_total)
    btn_calcular.pack(side="left", padx=10)

    # Etiqueta que mostrará el monto
    lbl_total = ctk.CTkLabel(frame_total, text="Total del día: $0.00", font=("Arial", 16, "bold"))
    lbl_total.pack(side="right", padx=10)

    ventana.mainloop()