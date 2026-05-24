from database import conectar


# AGREGAR PRÉSTAMO

def agregar_prestamo(id_cliente, id_envase, cantidad):

    conexion = None

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # VERIFICAR STOCK
        cursor.execute("""
        SELECT stock
        FROM envases
        WHERE id_envase = ?
        """, (id_envase,))

        resultado = cursor.fetchone()

        if resultado is None:
            print("El envase no existe")
            return False

        stock_actual = resultado["stock"]

        if cantidad > stock_actual:
            print("Stock insuficiente")
            return False

        # REGISTRAR PRÉSTAMO
        cursor.execute("""
        INSERT INTO prestamos_envases(
            id_cliente,
            id_envase,
            cantidad
        )
        VALUES(?, ?, ?)
        """, (id_cliente, id_envase, cantidad))

        # DESCONTAR STOCK
        cursor.execute("""
        UPDATE envases
        SET stock = stock - ?
        WHERE id_envase = ?
        """, (cantidad, id_envase))

        conexion.commit()

        return True

    except Exception as e:

        print(e)

        return False

    finally:

        if conexion:
            conexion.close()