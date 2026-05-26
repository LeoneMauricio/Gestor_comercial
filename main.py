import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from envases import (ui_agregar_envase, ui_modificar_envase, ui_mostrar_envases,
ui_agregar_prestamos, ui_mostrar_envases_prestados)
from clientes import (ui_modificar_cliente, ui_agregar_cliente, 
ui_mostrar_clientes)
from ventas import ui_nueva_venta, ui_mostrar_ventas

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("System")  # "Light", "Dark", "System"
ctk.set_default_color_theme("blue")

# Ventana principal
root = ctk.CTk()
root.title("Sodería - Gestión")
root.geometry("700x500")
# PESTAÑAS
tabview = ctk.CTkTabview(root)
tabview.pack(fill="both", expand=True, padx=20, pady=20)

tabview.add("Clientes")
tabview.add("Envases")
tabview.add("Ventas")
tabview.add("Salir")


frame_clientes = tabview.tab("Clientes")
ctk.CTkButton(frame_clientes, text="Agregar cliente", command=ui_agregar_cliente).pack(pady=5, fill="x")
ctk.CTkButton(frame_clientes, text="Modificar cliente", command=ui_modificar_cliente).pack(pady=5, fill="x")
ctk.CTkButton(frame_clientes, text="Mostrar clientes", command=ui_mostrar_clientes).pack(pady=5, fill="x")


frame_envases = tabview.tab("Envases")
ctk.CTkButton(frame_envases, text="Agregar envase", command=ui_agregar_envase).pack(pady=5, fill="x")
ctk.CTkButton(frame_envases, text="Modificar envase", command=ui_modificar_envase).pack(pady=5, fill="x")
ctk.CTkButton(frame_envases, text="Mostrar envases", command=ui_mostrar_envases).pack(pady=5, fill="x")
ctk.CTkButton(frame_envases, text="Registrar préstamo", command=ui_agregar_prestamos).pack(pady=5, fill="x")
ctk.CTkButton(frame_envases, text="Mostrar envases prestados", command=ui_mostrar_envases_prestados).pack(pady=5, fill="x")


frame_ventas = tabview.tab("Ventas")
ctk.CTkButton(frame_ventas, text="Nueva venta", command=ui_nueva_venta).pack(pady=5, fill="x")
ctk.CTkButton(frame_ventas, text="Registro de ventas", command=ui_mostrar_ventas).pack(pady=5, fill="x")
frame_salir = tabview.tab("Salir")
ctk.CTkButton(frame_salir, text="Cerrar aplicación", command=root.destroy).pack(pady=20, fill="x")

root.mainloop()