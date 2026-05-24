from agregar import agregar_cliente, agregar_envase
from modificar import modificar_cliente, modificar_envases
from prestamos import agregar_prestamo
from mostrar import mostrar_clientes,mostrar_ventas,mostrar_envases_prestados,mostrar_detalle_ventas,mostrar_envases

def mostrar_menu():
    print("\n--- SODERIA ---")
    print("1. Agregar cliente.")
    print("2. Agregar envase.")
    print("3. Modificar cliente.")
    print("4. Modificar envase.")
    print("5. Registrar prestamo.")
    print("6. Mostrar clientes.")
    print("7. Mostrar registo de ventas.")
    print("8. Mostrar detalles de ventas.")
    print("9. Mostrar envases.")
    print("10. Mostrar envases prestados.")
    print("0. Salir")

while True:
    mostrar_menu()
    op = input("Seleccione una opción: ")
# AGREGAR CLIENTE
    if op == "1":
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        direccion = input("Dirección: ")
        celular = input("Celular: ")

        resultado = agregar_cliente(
            nombre,
            apellido,
            direccion,
            celular
        )
        if resultado:
            print("\nCliente agregado correctamente\n")
        else:
            print("\nError al agregar cliente\n")
        
        input("Presione ENTER para continuar...")
# AGREGAR ENVASE
    elif op == "2":
        envase = input("Nombre del envase: ")
        stock = int(input("Stock: "))
        precio = float(input("Precio: "))

        resultado = agregar_envase(
            envase,
            stock,
            precio
        )
        if resultado:
            print("\nEnvase agregado correctamente\n")
        else:
            print("\nError al agregar envase\n")

        input("\nPresione ENTER para volver al menú...")
# MODIFICAR CLIENTE
    elif op == "3":
        id_cliente = int(input("ID del cliente: "))
        
        print("""
¿Qué desea modificar?

1. Nombre
2. Apellido
3. Dirección
4. Celular
""")
        op_campo = input("Seleccione una opción: ")
        
        campos = {
            "1":"nombre",
            "2":"apellido",
            "3":"direccion",
            "4":"celular"
        }
        
        if op_campo not in campos:
            print("\nOpción inválida")
        else:
            campo = campos[op_campo]
            
            nuevo_valor = input(f"Nuevo {campo}: ")
            
            resultado = modificar_cliente(
                id_cliente,
                campo,
                nuevo_valor
            )

            if resultado:
                print("\nCliente actualizado correctamente")
            else:
                print("\nError al actualizar cliente")

        input("\nPresione ENTER para volver al menú...")

# MODIFICAR ENVASES
    elif op == "4":
        id_envase = int(input("ID del envase: "))
        
        print("""
¿Qué desea modificar?

1. Envase
2. Stock
3. Precio
""")
        op_campo = input("Seleccione una opción: ")
        
        campos = {
            "1":"envase",
            "2":"stock",
            "3":"precio"
        }
        
        if op_campo not in campos:
            print("\nOpción inválida")
        else:
            campo = campos[op_campo]
            
            nuevo_valor = input(f"Nuevo {campo}: ")
            
            resultado = modificar_envases(
                id_envase,
                campo,
                nuevo_valor
            )

            if resultado:
                print("\nEnvase actualizado correctamente")
            else:
                print("\nError al actualizar envase")

        input("\nPresione ENTER para volver al menú...")
# PRESTAMOS DE ENVASES
    elif op == "5":
        id_cliente = int(input("ID cliente: "))
        id_envase = int(input("ID envase: "))
        cantidad = int(input("Cantidad: "))

        resultado = agregar_prestamo(
            id_cliente,
            id_envase,
            cantidad
        )

        if resultado:
            print("\nPréstamo registrado correctamente")
        else:
            print("\nError al registrar préstamo")

        input("\nPresione ENTER para volver al menú...")
# MOSTRAR CLIENTES
    elif op == "6":
        mostrar_clientes()
        input("Presione ENTER para continuar...")
# MOSTRAR REGISTROS VENTAS
    elif op =="7":
        mostrar_ventas()
        input("Presione ENTER para continuar...")
# MOSTRAR DETALLES DE VENTAS
    elif op == "8":
        mostrar_detalle_ventas()
        input("Presione ENTER para continuar...")
# MOSTRAR ENVASES
    elif op == "9":
        mostrar_envases()
        input("Presione ENTER para continuar...")
# MOSTRAR ENVASES PRESTADOS
    elif op == "10":
        mostrar_envases_prestados()
        input("Presione ENTER para continuar...")
# SALIR
    elif op == "0":
        print("\n Saliendo...")
        break
# OPCIÓN INVALIDA
    else:
        print("\nOpción invalida, intente nuevamente.\n")
        input("Presione ENTER para continuar...")