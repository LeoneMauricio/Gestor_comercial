from database import conectar

# MOSTRAR TABLA CLIENTES
def mostrar_clientes():
    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT*FROM clientes")
        
        clientes = cursor.fetchall()
        
        if not clientes:
            print("\nNo hay clientes registrados.")
            return
        
        print("\n========== CLIENTES ==========\n")
        
        for cliente in clientes:
            print(f"""
ID: {cliente["id_cliente"]}
Nombre: {cliente["nombre"]}
Apellido: {cliente["apellido"]}
Dirección: {cliente["direccion"]}
Celular: {cliente["celular"]}
-----------------------------
""")
    
    except Exception as e:
        print(f"\n Error: {e}")
    
    finally:
        if conexion:
            conexion.close()

# MOSTRAR TABLA ENVASES
def mostrar_envases():
    conexion = None
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT*FROM envases")
        
        envases = cursor.fetchall()
        
        if not envases:
            print("\nNo hay envases registrados.")
            return
        
        print("\n========== ENVASES ==========\n")
        
        for envase in envases:
            print(f"""
ID: {envase["id_envase"]}
Envase: {envase["envase"]}
Stock: {envase["stock"]}
Precio: {envase["precio"]}
-----------------------------
""")
    except Exception as e:
        print(f"\n Error: {e}")
    finally:
        if conexion:
            conexion.close()

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

# MOSTRAR ENVASES PRESTADOS
def mostrar_envases_prestados():
    conexion = None

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT*FROM prestamos_envases")
        
        envases_prestados = cursor.fetchall()
        
        if not envases_prestados:
            print("\n No Hay registro de envases prestados.")
        
        print("\n========== ENVASES PRESTADOS ==========\n")
        
        for envase in envases_prestados:
            print(f"""
ID: {envase["id_prestamo"]}
cliente: {envase["id_cliente"]}
Envase: {envase["id_envase"]}
Cantidad: {envase["cantidad"]}
fecha de prestamo: {envase["fecha_prestamo"]}
-----------------------------
""")
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        if conexion:
            conexion.close()