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

# UI MOSTRAR GANANCIAS POR FECHA
def ui_mostrar_ganancias_fecha():
    ventana = ctk.CTk()
    ventana.title("Ganancias por Fecha")
    ventana.geometry("700x500")

    frame_filtro = ctk.CTkFrame(ventana)
    frame_filtro.pack(pady=10)

    tk.Label(frame_filtro, text="Seleccione una fecha:").pack(side="left", padx=5)
    calendario = DateEntry(frame_filtro, width=12, background="darkblue",
                        foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
    calendario.pack(side="left", padx=5)

    frame_tabla = ctk.CTkFrame(ventana)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
# VER DESDE ACÁ PARA ESTABLECER RELACIÓN
    columnas = ("Gastos", "Ventas", "Ganancia")
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
    
    frame_total = ctk.CTkFrame(ventana)
    frame_total.pack(fill="x", padx=10, pady=10)

    def calcular_total():
        total_dia = 0.0
        # Recorremos todas las filas que están actualmente en la tabla
        for row in tabla.get_children():
            valores = tabla.item(row)["values"]
            # El índice 6 corresponde a la columna "Total"
            try:
                total_dia += float(valores[6])
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