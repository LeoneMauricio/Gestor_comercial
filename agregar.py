from database import conectar

# AGREGAR CLIENTES
def agregar_cliente(nombre, apellido, direccion, celular):
    try:        
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO clientes(nombre, apellido, direccion, celular)
        VALUES(?, ?, ?, ?)
        """, (nombre, apellido, direccion, celular))
        
        conexion.commit()
            
        return True
        
    except Exception as e:
        
        print(e)

        return False

    finally:

        conexion.close()


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

    except Exception as e:
        print(e)

        return False
    finally:

        conexion.close()
