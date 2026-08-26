
from config.database import conectar, conectar_row
from tkinter import messagebox, ttk
from tkinter import ttk
import customtkinter as ctk
ctk.set_appearance_mode("System")  # "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Puedes cambiar el tema

root = ctk.CTk()

# ==========================================================
# CONSULTA A LAS VISTAS
# ==========================================================

def obtener_ganancias(tipo):
    """
    tipo: 'dia', 'mes' o 'anio'
    Lee de la vista correspondiente (ganancias_diarias / _mensuales / _anuales)
    """
    vistas = {
        "dia":  ("ganancias_diarias", "fecha"),
        "mes":  ("ganancias_mensuales", "mes"),
        "anio": ("ganancias_anuales", "anio"),
    }
    vista, columna_periodo = vistas[tipo]

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(f"""
        SELECT {columna_periodo}, total_ventas, total_gastos, ganancia_neta
        FROM {vista}
        ORDER BY {columna_periodo} DESC
    """)
    filas = cursor.fetchall()
    conexion.close()
    return filas


# ==========================================================
# UI DE GANANCIAS
# ==========================================================

def ui_ganancias():
    ventana = ctk.CTkToplevel(root)
    ventana.title("Ganancias")
    ventana.after(100, lambda: ventana.state("zoomed"))

    tabview = ctk.CTkTabview(ventana, width=900, height=600)
    tabview.pack(fill="both", expand=True, padx=15, pady=15)

    tab_dia = tabview.add("Por día")
    tab_mes = tabview.add("Por mes")
    tab_anio = tabview.add("Por año")

    tablas = {}

    def crear_tabla(tab, encabezado_periodo):
        columnas = ("periodo", "ventas", "gastos", "neta")
        tabla = ttk.Treeview(tab, columns=columnas, show="headings", height=20)

        tabla.heading("periodo", text=encabezado_periodo)
        tabla.heading("ventas", text="Total Ventas")
        tabla.heading("gastos", text="Total Gastos")
        tabla.heading("neta", text="Ganancia Neta")

        for col in columnas:
            tabla.column(col, width=180, anchor="center")

        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # fila roja si la ganancia neta es negativa
        tabla.tag_configure("negativa", foreground="#e04b4b")
        tabla.tag_configure("positiva", foreground="#3bb273")

        return tabla

    tablas["dia"] = crear_tabla(tab_dia, "Fecha")
    tablas["mes"] = crear_tabla(tab_mes, "Mes")
    tablas["anio"] = crear_tabla(tab_anio, "Año")

    label_resumen = {}
    for tipo, tab in (("dia", tab_dia), ("mes", tab_mes), ("anio", tab_anio)):
        label_resumen[tipo] = ctk.CTkLabel(
            tab, text="", font=ctk.CTkFont(size=15, weight="bold")
        )
        label_resumen[tipo].pack(pady=(0, 10))

    def cargar_datos(tipo):
        tabla = tablas[tipo]
        tabla.delete(*tabla.get_children())

        filas = obtener_ganancias(tipo)
        total_neta_acumulada = 0

        for periodo, ventas, gastos, neta in filas:
            tag = "negativa" if neta < 0 else "positiva"
            tabla.insert(
                "", "end",
                values=(periodo, f"${ventas:,.2f}", f"${gastos:,.2f}", f"${neta:,.2f}"),
                tags=(tag,)
            )
            total_neta_acumulada += neta

        label_resumen[tipo].configure(
            text=f"Ganancia neta acumulada (todo el historial): ${total_neta_acumulada:,.2f}"
        )

    def refrescar_todo():
        for tipo in ("dia", "mes", "anio"):
            cargar_datos(tipo)

    refrescar_todo()

    ctk.CTkButton(ventana, text="Actualizar", command=refrescar_todo).pack(pady=10)

    ventana.mainloop()