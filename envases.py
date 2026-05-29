import sqlite3
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
# MOSTRAR ENVASES
def obtener_envases():
    conexion = conectar_row()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM envases")
    datos = cursor.fetchall()
    conexion.close()
    return [tuple(fila) for fila in datos]
# UI MOSTRAR ENVASES / MODIFICAR
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

    def abrir_modificar(): # MODIFICAR TABLA ENVASES
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un envase para modificar")
            return

        item = seleccion[0]
        datos = tabla.item(item, "values")  # valores de la fila seleccionada

        top = ctk.CTkToplevel(ventana)
        top.title("Modificar Envase")

        # Campos editables
        labels = ["Envase", "Stock", "Precio"]
        entries = []

        for i, campo in enumerate(labels, start=1):
            ctk.CTkLabel(top, text=campo).pack()
            entry = ctk.CTkEntry(top)
            entry.insert(0, datos[i])  # valores desde la fila seleccionada
            entry.pack(pady=5)
            entries.append(entry)

        def guardar():
            nuevo_envase = entries[0].get()
            nuevo_stock = int(entries[1].get())
            nueva_precio = float(entries[2].get())
            id_envase = datos[0]  # ID siempre viene de la primera columna

            conexion = sqlite3.connect("soderia.db")
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE envases
                SET envase=?, stock=?, precio=?
                WHERE id_envase=?
            """, (nuevo_envase, nuevo_stock, nueva_precio, id_envase))
            conexion.commit()
            conexion.close()

            # refrescar tabla
            tabla.item(item, values=(id_envase, nuevo_envase, nuevo_stock, nueva_precio))
            top.destroy()
            messagebox.showinfo("Éxito", "Envase actualizado correctamente")

        ctk.CTkButton(top, text="Guardar cambios", command=guardar).pack(pady=10)

    boton_modificar = ctk.CTkButton(ventana, text="Modificar Envase", command=abrir_modificar)
    boton_modificar.pack(pady=10)

    ventana.mainloop()
# AGREGAR PRÉSTAMO ENVASES
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

        if resultado is None:
            return False, "El envase no existe"

        stock_actual = resultado["stock"]
        # VALIDAR STOCK
        if cantidad > stock_actual:
            return False, f"Stock insuficiente. Disponible: {stock_actual}"
        # REGISTRAR O ACUMULAR PRÉSTAMO
        try:
            cursor.execute("""
            INSERT INTO prestamos_envases(id_cliente, id_envase, cantidad)
            VALUES(?, ?, ?)
            """, (id_cliente, id_envase, cantidad))
        except sqlite3.IntegrityError:
            # Ya existe el registro, acumular cantidad
            cursor.execute("""
            UPDATE prestamos_envases
            SET cantidad = cantidad + ?
            WHERE id_cliente = ? AND id_envase = ?
            """, (cantidad, id_cliente, id_envase))
        # DESCONTAR STOCK
        cursor.execute("""
        UPDATE envases
        SET stock = stock - ?
        WHERE id_envase = ?
        """, (cantidad, id_envase))

        conexion.commit()
        return True, "Préstamo registrado correctamente"
    except Exception as e:
        return False, f"Error: {e}"
    finally:
        if conexion:
            conexion.close()
# REGISTRAR PRESTAMOS DE ENVASE
def ui_agregar_prestamos():
    ventana = ctk.CTkToplevel(root)
    ventana.title("Agregar Préstamos de Envases")
    ventana.geometry("600x500")
    
    id_cliente = ctk.CTkEntry(ventana, placeholder_text="ID del cliente")
    id_envase = ctk.CTkEntry(ventana, placeholder_text="ID del envase")
    cantidad = ctk.CTkEntry(ventana, placeholder_text="Cantidad prestada")

    id_cliente.pack(pady=5)
    id_envase.pack(pady=5)
    cantidad.pack(pady=5)

    def guardar():
        try:
            resultado, msg = agregar_prestamo(
                int(id_cliente.get()), 
                int(id_envase.get()), 
                int(cantidad.get())
            )
        except ValueError:
            resultado, msg = False, "Error: Los ID o la cantidad deben ser numéricos"

        ctk.CTkLabel(ventana, text=msg).pack(pady=10)

    ctk.CTkButton(ventana, text="Guardar", command=guardar).pack(pady=10)

    ventana.mainloop()
# TABLA PRESTAMOS DE ENVASES
def obtener_envases_prestados():
    conexion = conectar_row()
    cursor = conexion.cursor()
    cursor.execute("""
    SELECT p.id_prestamo,
        p.id_cliente,
        c.nombre AS cliente,
        c.apellido AS apellido,
        p.id_envase,
        e.envase AS envase,
        p.cantidad,
        p.fecha_prestamo
    FROM prestamos_envases p
    INNER JOIN clientes c ON p.id_cliente = c.id_cliente
    INNER JOIN envases e ON p.id_envase = e.id_envase
    """)
    datos = cursor.fetchall()
    conexion.close()
    return [tuple(fila) for fila in datos]
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

    datos_completos = {}

    def cargar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)
        datos_completos.clear()

        envases = obtener_envases_prestados()
        if not envases:
            messagebox.showinfo("Aviso", "No hay envases prestados registrados en la base de datos")
        else:
            for envase in envases:
                # envase = (id_prestamo, id_cliente, nombre, apellido, id_envase, envase, cantidad, fecha)
                item_id = tabla.insert("", tk.END, values=(
                    envase[0],  # id_prestamo
                    envase[2],  # nombre
                    envase[3],  # apellido
                    envase[5],  # envase
                    envase[6],  # cantidad
                    envase[7]   # fecha
                ))
                datos_completos[item_id] = envase

    cargar_tabla()

    tabla.pack(fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def abrir_modificar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un prestamo para modificar")
            return

        item = seleccion[0]
        envase = datos_completos[item]

        top = ctk.CTkToplevel(ventana)
        top.title("Modificar Prestamo de envases")

        labels = ["Id del cliente", "Id del envase", "Cantidad prestada"]
        valores_iniciales = [envase[1], envase[4], envase[6]]
        entries = []

        for campo, valor in zip(labels, valores_iniciales):
            ctk.CTkLabel(top, text=campo).pack()
            entry = ctk.CTkEntry(top)
            entry.insert(0, str(valor))
            entry.pack(pady=5)
            entries.append(entry)

        def guardar():
            try:
                nuevo_id_cliente = int(entries[0].get())
                nuevo_id_envase = int(entries[1].get())
                nueva_cantidad = int(entries[2].get())
            except ValueError:
                messagebox.showerror("Error", "Los campos deben ser numéricos")
                return

            id_prestamo = envase[0]
            cantidad_anterior = envase[6]
            id_envase_anterior = envase[4]

            conexion = conectar_row() 
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE prestamos_envases
                SET id_cliente=?, id_envase=?, cantidad=?
                WHERE id_prestamo=?
            """, (nuevo_id_cliente, nuevo_id_envase, nueva_cantidad, id_prestamo))

            if id_envase_anterior != nuevo_id_envase:
                cursor.execute("UPDATE envases SET stock = stock + ? WHERE id_envase=?",
                            (cantidad_anterior, id_envase_anterior))
                cursor.execute("UPDATE envases SET stock = stock - ? WHERE id_envase=?",
                            (nueva_cantidad, nuevo_id_envase))
            else:
                diferencia = nueva_cantidad - cantidad_anterior
                cursor.execute("UPDATE envases SET stock = stock - ? WHERE id_envase=?",
                            (diferencia, nuevo_id_envase))

            conexion.commit()
            conexion.close()

            top.destroy()
            cargar_tabla()
            messagebox.showinfo("Éxito", "Préstamo y stock actualizados correctamente")

        ctk.CTkButton(top, text="Guardar cambios", command=guardar).pack(pady=10)

    boton_modificar = ctk.CTkButton(ventana, text="Modificar Prestamos", command=abrir_modificar)
    boton_modificar.pack(pady=10)

    ventana.mainloop()