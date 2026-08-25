import customtkinter as ctk

from PIL import Image

from views.envases import (
    ui_agregar_envase,
    ui_mostrar_envases,
    ui_agregar_prestamos,
    ui_mostrar_envases_prestados
)

from views.clientes import (
    ui_agregar_cliente,
    ui_mostrar_clientes
)

from views.ventas import (
    ui_nueva_venta,
    ui_mostrar_ventas,
    ui_mostrar_ventas_por_fecha
)

from views.gastos import (
    ui_agregar_gastos,
    ui_mostrar_gastos,
    ui_mostrar_gastos_por_fecha
)

# CONFIGURACIÓN DE CUSTOMTKINTER

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

# VENTANA PRINCIPAL

principal = ctk.CTk()
principal.title("Sodería - Gestión")

# Maximizar la ventana después de crearla
principal.after(100, lambda: principal.state("zoomed"))

# CONTENEDOR PRINCIPAL

contenedor = ctk.CTkFrame(
    principal,
    corner_radius=0
)

contenedor.pack(
    fill="both",
    expand=True
)

# MENÚ LATERAL

menu = ctk.CTkFrame(
    contenedor,
    width=230,
    corner_radius=0
)

menu.pack(
    side="left",
    fill="y"
)

# Evita que el Frame cambie de tamaño por sus widgets
menu.pack_propagate(False)

# ÁREA DE CONTENIDO

contenido = ctk.CTkFrame(
    contenedor,
    corner_radius=0
)

contenido.pack(
    side="right",
    fill="both",
    expand=True,
    padx=15,
    pady=15
)


# TÍTULO DEL MENÚ

titulo = ctk.CTkLabel(
    menu,
    text="SODERÍA",
    font=("Arial", 26, "bold")
)

titulo.pack(
    pady=(40, 30)
)


subtitulo = ctk.CTkLabel(
    menu,
    text="Gestión Comercial",
    font=("Arial", 13)
)

subtitulo.pack(
    pady=(0, 30)
)

# FRAMES DE LAS SECCIONES

frame_clientes = ctk.CTkFrame(
    contenido,
    fg_color="transparent"
)

frame_envases = ctk.CTkFrame(
    contenido,
    fg_color="transparent"
)

frame_ventas = ctk.CTkFrame(
    contenido,
    fg_color="transparent"
)

frame_gastos = ctk.CTkFrame(
    contenido,
    fg_color="transparent"
)

frame_ganancias = ctk.CTkFrame(
    contenido,
    fg_color="transparent"
)

# COLOCAR LOS FRAMES

for frame in (
    frame_clientes,
    frame_envases,
    frame_ventas,
    frame_gastos,
    frame_ganancias
):
    frame.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )

# FUNCIÓN PARA CAMBIAR DE SECCIÓN

def mostrar_frame(frame):
    frame.tkraise()

# TÍTULOS DE LAS SECCIONES

ctk.CTkLabel(
    frame_clientes,
    text="Clientes",
    font=("Arial", 28, "bold")
).pack(
    pady=(30, 30)
)

ctk.CTkLabel(
    frame_envases,
    text="Envases",
    font=("Arial", 28, "bold")
).pack(
    pady=(30, 30)
)

ctk.CTkLabel(
    frame_ventas,
    text="Ventas",
    font=("Arial", 28, "bold")
).pack(
    pady=(30, 30)
)

ctk.CTkLabel(
    frame_gastos,
    text="Gastos",
    font=("Arial", 28, "bold")
).pack(
    pady=(30, 30)
)

ctk.CTkLabel(
    frame_ganancias,
    text="Ganancias",
    font=("Arial", 28, "bold")
).pack(
    pady=(30, 30)
)

# CLIENTES

ctk.CTkButton(
    frame_clientes,
    text="Agregar cliente",
    command=ui_agregar_cliente,
    width=300,
    height=45
).pack(
    pady=8
)

ctk.CTkButton(
    frame_clientes,
    text="Mostrar clientes",
    command=ui_mostrar_clientes,
    width=300,
    height=45
).pack(
    pady=8
)

# ENVASES

ctk.CTkButton(
    frame_envases,
    text="Agregar envase",
    command=ui_agregar_envase,
    width=300,
    height=45
).pack(
    pady=8
)

ctk.CTkButton(
    frame_envases,
    text="Mostrar envases",
    command=ui_mostrar_envases,
    width=300,
    height=45
).pack(
    pady=8
)

ctk.CTkButton(
    frame_envases,
    text="Registrar préstamo",
    command=ui_agregar_prestamos,
    width=300,
    height=45
).pack(
    pady=8
)

ctk.CTkButton(
    frame_envases,
    text="Mostrar envases prestados",
    command=ui_mostrar_envases_prestados,
    width=300,
    height=45
).pack(
    pady=8
)

# VENTAS

ctk.CTkButton(
    frame_ventas,
    text="Nueva venta",
    command=ui_nueva_venta,
    width=300,
    height=45
).pack(
    pady=8
)

ctk.CTkButton(
    frame_ventas,
    text="Registro de ventas",
    command=ui_mostrar_ventas,
    width=300,
    height=45
).pack(
    pady=8
)

ctk.CTkButton(
    frame_ventas,
    text="Buscar ventas por fecha",
    command=ui_mostrar_ventas_por_fecha,
    width=300,
    height=45
).pack(
    pady=8
)

# GASTOS

ctk.CTkButton(
    frame_gastos,
    text="Registrar gasto",
    command=ui_agregar_gastos,
    width=300,
    height=45
).pack(
    pady=8
)

ctk.CTkButton(
    frame_gastos,
    text="Registro de gastos",
    command=ui_mostrar_gastos,
    width=300,
    height=45
).pack(
    pady=8
)

ctk.CTkButton(
    frame_gastos,
    text="Buscar gastos por fecha",
    command=ui_mostrar_gastos_por_fecha,
    width=300,
    height=45
).pack(
    pady=8
)

# GANANCIAS

ctk.CTkLabel(
    frame_ganancias,
    text="Módulo de ganancias",
    font=("Arial", 18)
).pack(
    pady=20
)

# BOTONES DEL MENÚ LATERAL

ctk.CTkButton(
    menu,
    text="Clientes",
    width=190,
    height=45,
    command=lambda: mostrar_frame(frame_clientes)
).pack(
    pady=7
)

ctk.CTkButton(
    menu,
    text="Envases",
    width=190,
    height=45,
    command=lambda: mostrar_frame(frame_envases)
).pack(
    pady=7
)

ctk.CTkButton(
    menu,
    text="Ventas",
    width=190,
    height=45,
    command=lambda: mostrar_frame(frame_ventas)
).pack(
    pady=7
)

ctk.CTkButton(
    menu,
    text="Gastos",
    width=190,
    height=45,
    command=lambda: mostrar_frame(frame_gastos)
).pack(
    pady=7
)

ctk.CTkButton(
    menu,
    text="Ganancias",
    width=190,
    height=45,
    command=lambda: mostrar_frame(frame_ganancias)
).pack(
    pady=7
)

# SEPARADOR VISUAL

ctk.CTkLabel(
    menu,
    text=""
).pack(
    expand=True
)

# BOTÓN SALIR

ctk.CTkButton(
    menu,
    text="Cerrar aplicación",
    width=190,
    height=45,
    fg_color="#C62828",
    hover_color="#8E0000",
    command=principal.destroy
).pack(
    pady=(10, 30)
)

# MOSTRAR CLIENTES AL INICIAR

mostrar_frame(frame_clientes)

# EJECUTAR

principal.mainloop()