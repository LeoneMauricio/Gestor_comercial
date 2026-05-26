from database import conectar

# MOSTRAR TABLA VENTAS
def mostrar_ventas():
    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        
        cursor.execute("""SELECT
            ventas.id_venta,
            clientes.nombre,
            clientes.apellido,
            ventas.total,
            ventas.fecha_venta

        FROM ventas

        INNER JOIN clientes
        ON ventas.id_cliente = clientes.id_cliente
        """)
        
        ventas = cursor.fetchall()
        
        if not ventas:
            print("\nNo hay ventas registradas.")
            return
        
        print("\n========== VENTAS ==========\n")
        for venta in ventas:
            print(f"""
ID: {venta["id_venta"]}
Cliente: {venta["nombre"]} {venta["apellido"]}
Total: ${venta["total"]}
Fecha: {venta["fecha_venta"]}
-----------------------------
""")

    except Exception as e:
        print(f"\nError:{e}")

    finally:
        if conexion:
            conexion.close()    

# MOSTRAR TABLA DETALLE_VENTAS
def mostrar_detalle_ventas():
    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT*FROM detalle_ventas")
        
        detalle_ventas = cursor.fetchall()
        
        if not detalle_ventas:
            print("\n No Hay registro de venta.")
        
        print("\n========== VENTAS DETALLES ==========\n")
        for venta in detalle_ventas:
            print(f"""
ID: {venta["id_detalle"]}
Venta: {venta["id_venta"]}
Envase: {venta["id_envase"]}
Cantidad: {venta["cantidad"]}
Precio unitario: {venta["precio_unitario"]}
Subtotal: {venta["subtotal"]}
-----------------------------
""")
    except Exception as e:
        print(f"Error:{e}")

    finally: 
        if conexion:
            conexion.close()
