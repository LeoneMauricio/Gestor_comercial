from database import conectar

# MODIFICAR CLIENTE
def modificar_cliente(id_cliente, campo, nuevo_valor):

    campos_validos = [
        "nombre",
        "apellido",
        "direccion",
        "celular",
    ]

    if campo not in campos_validos:
        return False

    conexion = None

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        sql = f"""
        UPDATE clientes
        SET {campo} = ?
        WHERE id_cliente = ?
        """

        cursor.execute(sql, (nuevo_valor, id_cliente))
        conexion.commit()

        return True

    except Exception as e:
        print(e)
        return False

    finally:
        if conexion:
            conexion.close()

def modificar_envases(id_envase, campo, nuevo_valor):
    
    campos_validos = [
        "envase",
        "stock",
        "precio",
    ]
    
    if campo not in campos_validos:
        return False
    
    conexion = None
    
    try:

        conexion = conectar()
        cursor = conexion.cursor()

        sql = f"""
        UPDATE envases
        SET {campo} = ?
        WHERE id_envase = ?
        """

        cursor.execute(sql, (nuevo_valor, id_envase))
        conexion.commit()

        return True

    except Exception as e:

        print(e)

        return False

    finally:

        if conexion:
            conexion.close()