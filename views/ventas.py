from config.database import conectar, conectar_row
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
import os
import datetime
from pathlib import Path
import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("System")  # "Light", "Dark", "System"
ctk.set_default_color_theme("dark-blue")  # Puedes cambiar el tema

root = ctk.CTk()

# Frame principal
frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

# CONSULTAS A LA BASE DE DATOS

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


# GENERACIÓN E IMPRESIÓN DE RECIBO

def generar_recibo(carrito):
    """Genera un archivo .txt con el detalle de la venta y devuelve su ruta."""
    carpeta_recibos = Path(__file__).resolve().parent / "recibos"
    carpeta_recibos.mkdir(exist_ok=True)

    ahora = datetime.datetime.now()
    nombre_archivo = f"recibo_{ahora.strftime('%Y%m%d_%H%M%S')}.txt"
    ruta = carpeta_recibos / nombre_archivo

    total_general = sum(item["subtotal"] for item in carrito)
    nombre_cliente = carrito[0]["nombre_cliente"]

    lineas = []
    lineas.append("=" * 40)
    lineas.append("           SODERÍA - RECIBO")
    lineas.append("=" * 40)
    lineas.append(f"Fecha: {ahora.strftime('%d/%m/%Y %H:%M')}")
    lineas.append(f"Cliente: {nombre_cliente}")
    lineas.append("-" * 40)
    lineas.append(f"{'Envase':<15}{'Cant.':>6}{'P.Unit.':>9}{'Subt.':>10}")
    lineas.append("-" * 40)
    for item in carrito:
        lineas.append(
            f"{item['nombre_envase']:<15}"
            f"{item['cantidad']:>6}"
            f"{item['precio_unitario']:>9.2f}"
            f"{item['subtotal']:>10.2f}"
        )
    lineas.append("-" * 40)
    lineas.append(f"{'TOTAL:':<30}{total_general:>10.2f}")
    lineas.append("=" * 40)
    lineas.append("¡Gracias por su compra!")

    ruta.write_text("\n".join(lineas), encoding="utf-8")
    return ruta


def imprimir_recibo(ruta):
    """Envía el archivo de recibo a imprimir usando el sistema operativo."""
    try:
        if os.name == "nt":  # Windows
            os.startfile(str(ruta), "print")
        else:  # Linux / Mac (requiere 'lp' instalado)
            os.system(f"lp '{ruta}'")
    except Exception as e:
        messagebox.showwarning(
            "Aviso",
            f"El recibo se generó en:\n{ruta}\n\n"
            f"Pero no se pudo enviar a imprimir automáticamente.\nError: {e}"
        )


# UI NUEVA VENTA (CON CARRITO)

def ui_nueva_venta():
    venta_fr = ctk.CTkToplevel(root)
    venta_fr.title("Nueva Venta")
    venta_fr.after(100, lambda: venta_fr.state("zoomed"))

    carrito = []  # lista de productos de esta venta, se reinicia cada vez que se abre la ventana

    clientes_dict = obtener_clientes_dict()
    envases_dict = obtener_envases_dict()

    clientes_inv = {v: k for k, v in clientes_dict.items()}
    envases_inv = {v["nombre"]: k for k, v in envases_dict.items()}

    # ---------------- FRAME IZQUIERDO: FORMULARIO ----------------
    frame_form = ctk.CTkFrame(venta_fr)
    frame_form.pack(side="left", fill="y", padx=15, pady=15)

    ctk.CTkLabel(frame_form, text="Cliente").pack(pady=(15, 0))
    opciones_clientes = list(clientes_dict.values())
    combo_cliente = ctk.CTkComboBox(frame_form, values=opciones_clientes, state="readonly", width=300)
    combo_cliente.set("Seleccionar cliente")
    combo_cliente.pack(pady=5)

    ctk.CTkLabel(frame_form, text="Envase").pack(pady=(10, 0))
    opciones_envases = [v["nombre"] for v in envases_dict.values()]
    combo_envase = ctk.CTkComboBox(frame_form, values=opciones_envases, state="readonly", width=300)
    combo_envase.set("Seleccionar envase")
    combo_envase.pack(pady=5)

    ctk.CTkLabel(frame_form, text="Precio unitario").pack(pady=(10, 0))
    entry_precio = ctk.CTkEntry(frame_form, placeholder_text="Precio unitario", width=300)
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

    ctk.CTkLabel(frame_form, text="Cantidad").pack(pady=(10, 0))
    entry_cantidad = ctk.CTkEntry(frame_form, placeholder_text="Cantidad de envases", width=300)
    entry_cantidad.pack(pady=5)

    ctk.CTkLabel(frame_form, text="Subtotal").pack(pady=(10, 0))
    entry_subtotal = ctk.CTkEntry(frame_form, placeholder_text="Subtotal", width=300)
    entry_subtotal.configure(state="disabled")
    entry_subtotal.pack(pady=5)

    def calcular_subtotal(*args):
        try:
            cant = float(entry_cantidad.get())
            precio = float(entry_precio.get())
            total = cant * precio
            entry_subtotal.configure(state="normal")
            entry_subtotal.delete(0, "end")
            entry_subtotal.insert(0, f"{total:.2f}")
            entry_subtotal.configure(state="disabled")
        except ValueError:
            pass

    entry_cantidad.bind("<KeyRelease>", calcular_subtotal)

    # ---------------- FRAME DERECHO: CARRITO ----------------
    frame_carrito = ctk.CTkFrame(venta_fr)
    frame_carrito.pack(side="right", fill="both", expand=True, padx=15, pady=15)

    ctk.CTkLabel(
        frame_carrito, text="Carrito de venta",
        font=ctk.CTkFont(size=16, weight="bold")
    ).pack(pady=(10, 5))

    columnas = ("cliente", "envase", "cantidad", "precio", "subtotal")
    tabla_carrito = ttk.Treeview(frame_carrito, columns=columnas, show="headings", height=15)
    for col, texto, ancho in [
        ("cliente", "Cliente", 150),
        ("envase", "Envase", 120),
        ("cantidad", "Cant.", 60),
        ("precio", "Precio U.", 80),
        ("subtotal", "Subtotal", 80),
    ]:
        tabla_carrito.heading(col, text=texto)
        tabla_carrito.column(col, width=ancho, anchor="center")
    tabla_carrito.pack(fill="both", expand=True, padx=10, pady=5)

    label_total = ctk.CTkLabel(
        frame_carrito, text="TOTAL: $0.00",
        font=ctk.CTkFont(size=18, weight="bold")
    )
    label_total.pack(pady=10)

    def refrescar_tabla():
        tabla_carrito.delete(*tabla_carrito.get_children())
        total_general = 0
        for item in carrito:
            tabla_carrito.insert("", "end", values=(
                item["nombre_cliente"],
                item["nombre_envase"],
                item["cantidad"],
                f"{item['precio_unitario']:.2f}",
                f"{item['subtotal']:.2f}",
            ))
            total_general += item["subtotal"]
        label_total.configure(text=f"TOTAL: ${total_general:.2f}")

    def agregar_al_carrito():
        nombre_cliente = combo_cliente.get()
        nombre_envase = combo_envase.get()

        if nombre_cliente == "Seleccionar cliente":
            messagebox.showwarning("Atención", "Seleccione un cliente.")
            return
        if nombre_envase == "Seleccionar envase":
            messagebox.showwarning("Atención", "Seleccione un envase.")
            return
        if not entry_cantidad.get() or not entry_subtotal.get():
            messagebox.showwarning("Atención", "Complete la cantidad.")
            return

        try:
            id_cliente = clientes_inv[nombre_cliente]
            id_envase = envases_inv[nombre_envase]
            cantidad = int(entry_cantidad.get())
            precio_unitario = float(entry_precio.get())
            subtotal = float(entry_subtotal.get())
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        if cantidad <= 0:
            messagebox.showwarning("Atención", "La cantidad debe ser mayor a 0.")
            return

        carrito.append({
            "id_cliente": id_cliente,
            "nombre_cliente": nombre_cliente,
            "id_envase": id_envase,
            "nombre_envase": nombre_envase,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal,
        })

        refrescar_tabla()

        # limpiar campos de envase/cantidad para cargar el siguiente producto
        combo_envase.set("Seleccionar envase")
        entry_precio.configure(state="normal")
        entry_precio.delete(0, "end")
        entry_precio.configure(state="disabled")
        entry_cantidad.delete(0, "end")
        entry_subtotal.configure(state="normal")
        entry_subtotal.delete(0, "end")
        entry_subtotal.configure(state="disabled")

    def quitar_seleccionado():
        seleccion = tabla_carrito.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto del carrito para quitar.")
            return
        indice = tabla_carrito.index(seleccion[0])
        carrito.pop(indice)
        refrescar_tabla()

    ctk.CTkButton(frame_form, text="Agregar al carrito", command=agregar_al_carrito).pack(pady=15)

    frame_botones_carrito = ctk.CTkFrame(frame_carrito, fg_color="transparent")
    frame_botones_carrito.pack(pady=5)

    ctk.CTkButton(
        frame_botones_carrito, text="Quitar seleccionado",
        fg_color="#a33", hover_color="#822", command=quitar_seleccionado
    ).pack(side="left", padx=5)

    # ---------------- FINALIZAR VENTA ----------------
    def finalizar_venta():
        if not carrito:
            messagebox.showwarning("Atención", "El carrito está vacío.")
            return

        try:
            for item in carrito:
                nueva_venta(
                    item["id_cliente"],
                    item["id_envase"],
                    item["cantidad"],
                    item["precio_unitario"],
                    item["subtotal"],
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta: {e}")
            return

        ruta_recibo = generar_recibo(carrito)
        imprimir_recibo(ruta_recibo)

        messagebox.showinfo("Éxito", "Venta registrada y recibo generado.")
        venta_fr.destroy()

    ctk.CTkButton(
        frame_botones_carrito, text="Finalizar venta e imprimir recibo",
        fg_color="#2a7", hover_color="#196", command=finalizar_venta
    ).pack(side="left", padx=5)

    venta_fr.mainloop()
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
    most_venta_fr = ctk.CTk()
    most_venta_fr("Registro de ventas")
    most_venta_fr.after(100, lambda: most_venta_fr.state("zoomed"))

    frame_tabla = ctk.CTkFrame(most_venta_fr)
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

        top = ctk.CTkToplevel(most_venta_fr)
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

    boton_modificar = ctk.CTkButton(most_venta_fr, text="Modificar Venta", command=abrir_modificar)
    boton_modificar.pack(pady=10)
    
    most_venta_fr.mainloop()
# MOSTRAR VENTAS POR FECHA
def ui_mostrar_ventas_por_fecha():
    venta_fecha_fr = ctk.CTk()
    venta_fecha_fr.title("Ventas por Fecha")
    venta_fecha_fr.after(100, lambda: venta_fecha_fr.state("zoomed"))

    frame_filtro = ctk.CTkFrame(venta_fecha_fr)
    frame_filtro.pack(pady=10)

    tk.Label(frame_filtro, text="Seleccione una fecha:").pack(side="left", padx=5)
    calendario = DateEntry(frame_filtro, width=12, background="darkblue",
                        foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
    calendario.pack(side="left", padx=5)

    frame_tabla = ctk.CTkFrame(venta_fecha_fr)
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
    
    frame_total = ctk.CTkFrame(venta_fecha_fr)
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

    venta_fecha_fr.mainloop()